# phimq/system.py
import torch
import random
from .config import PHIMQConfig

class LangevinFluidSystem:
    def __init__(self, config: PHIMQConfig):
        self.config = config
        self.device = torch.device(config.device if torch.cuda.is_available() else "cpu")
        self.reset()
        
    def reset(self):
        """ 初始化或重置粒子，確保完美的宇稱對稱性 """
        torch.manual_seed(self.config.seed)
        random.seed(self.config.seed)
        
        half_N = self.config.num_particles // 2
        p_half = torch.randn(half_N, 2, device=self.device) * 0.05
        p_mirror = p_half.clone()
        p_mirror[:, 0] = -p_mirror[:, 0]
        
        self.particles = torch.cat([p_half, p_mirror], dim=0)
        self.particles.requires_grad = True
        self.cutoff_sq = self.config.cutoff_radius ** 2

    def update_gradient(self, current_temp: float) -> float:
        """ 計算自由能並執行 backward 傳遞梯度，回傳真實總梯度範數 """
        if self.particles.grad is not None:
            self.particles.grad.zero_()
            
        x = self.particles[:, 0]
        y = self.particles[:, 1]
        
        # 1. 外部勢能
        V_energy = torch.sum((x**2 - 1)**2 + self.config.y_weight * y**2)
        
        # 2. 核密度估計 (KDE)
        effective_sigma_sq = self.config.sigma_sq_base * max(0.5, current_temp / self.config.initial_temp)
        d_sq_full = torch.cdist(self.particles, self.particles) ** 2
        kernel = torch.exp(-d_sq_full / (2 * effective_sigma_sq))
        rho = ((kernel.sum(dim=1) - 1.0) / (self.config.num_particles - 1)).clamp(min=1e-8)
        
        # 3. 廣延熱力學熵 (-T * S)
        entropy_term = -self.config.entropy_coef * current_temp * torch.sum(torch.log(rho))
        
        # 4. 高斯互斥力
        repulsion_sum = torch.tensor(0.0, device=self.device)
        for i in range(0, self.config.num_particles, self.config.chunk_size):
            end_i = min(i + self.config.chunk_size, self.config.num_particles)
            d_sq = d_sq_full[i:end_i]
            mask = (d_sq < self.cutoff_sq) & (d_sq > 1e-12)
            
            if mask.any():
                d_sq_close = d_sq[mask]
                envelope = ((self.cutoff_sq - d_sq_close) / self.cutoff_sq) ** 2
                e_base = torch.exp(-d_sq_close / (2 * effective_sigma_sq))
                repulsion_sum += torch.sum(e_base * envelope)
                
        repulsion_raw = (self.config.repulsion_coef * repulsion_sum) / self.config.num_particles
        
        # 總自由能
        total_energy = V_energy + repulsion_raw + entropy_term
        total_energy.backward()
        
        # 解封物理限制，只做安全防爆
        torch.nn.utils.clip_grad_norm_([self.particles], max_norm=50.0)
        true_grad_norm = torch.sqrt(torch.sum(self.particles.grad ** 2)).item()
        
        return true_grad_norm

    def get_statistics(self):
        """ 計算當前系統的對稱度、重心與 IQR 厚度 """
        p_np = self.particles.data.cpu()
        left_mask = p_np[:, 0] < 0
        right_mask = p_np[:, 0] >= 0
        
        p_left_x = p_np[left_mask, 0]
        p_right_x = p_np[right_mask, 0]
        
        q75_l, q25_l = torch.quantile(p_left_x, torch.tensor([0.75, 0.25])) if p_left_x.numel() > 0 else (0, 0)
        q75_r, q25_r = torch.quantile(p_right_x, torch.tensor([0.75, 0.25])) if p_right_x.numel() > 0 else (0, 0)
        
        return {
            "ratio_left": left_mask.sum().item(),
            "ratio_right": right_mask.sum().item(),
            "center_left": p_left_x.mean().item() if p_left_x.numel() > 0 else 0.0,
            "center_right": p_right_x.mean().item() if p_right_x.numel() > 0 else 0.0,
            "iqr_left": (q75_l - q25_l).item(),
            "iqr_right": (q75_r - q25_r).item()
        }