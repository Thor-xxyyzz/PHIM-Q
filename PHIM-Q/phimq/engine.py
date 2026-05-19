# phimq/engine.py
import math
import torch

class OverdampedLangevinEngine:
    def __init__(self, system_particles: torch.Tensor, config):
        self.particles = system_particles
        self.config = config
        self.global_step = 0
        self.temp_eff = config.initial_temp
        
    def step(self):
        self.global_step += 1
        
        # 三段式物理退火計畫
        if self.global_step < self.config.phase1_steps:
            self.temp_eff = self.config.initial_temp
        elif self.global_step < (self.config.phase1_steps + self.config.phase2_steps):
            frac = (self.global_step - self.config.phase1_steps) / self.config.phase2_steps
            self.temp_eff = self.config.initial_temp * (1 - frac) + self.config.min_temp * frac
        else:
            self.temp_eff = self.config.min_temp
            
        # 計算當前回合的時間步長 (dt)
        current_lr = self.config.lr
        if self.global_step > (self.config.phase1_steps + self.config.phase2_steps):
            current_lr *= 0.1   # 低溫弛豫精細步長
        elif self.global_step > self.config.phase1_steps:
            current_lr *= 0.5
            
        if self.particles.grad is None:
            return
            
        v_drift = -self.particles.grad.data
        
        # 嚴格滿足漲落耗散定理的熱噪聲: sqrt(2 * T * dt)
        std_dev = math.sqrt(2 * self.temp_eff * current_lr)
        noise = torch.randn_like(self.particles.data, device=self.particles.device) * std_dev
        
        # 核心位置更新
        self.particles.data.add_(v_drift * current_lr + noise)