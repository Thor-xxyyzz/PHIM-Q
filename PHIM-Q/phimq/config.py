# phimq/config.py
import math
from dataclasses import dataclass

@dataclass
class PHIMQConfig:
    # 粒子與硬體配置
    num_particles: int = 2000
    chunk_size: int = 2048
    device: str = "cuda"  # "cuda" 或 "cpu"
    
    # 外部雙井勢能曲率 (V = (x²-1)² + y_weight * y²)
    y_weight: float = 2.0            
    
    # 相互作用場與熵壓力
    sigma_sq_base: float = 0.135     
    repulsion_coef: float = 0.045    
    entropy_coef: float = 0.020      
    
    # 朗之萬动力學與時間步長 (dt)
    lr: float = 9.0e-3               
    initial_temp: float = 0.4        
    min_temp: float = 0.011          
    
    # 三段式退火時間排程
    total_steps: int = 6000          
    phase1_steps: int = 1500         
    phase2_steps: int = 2000         
    
    seed: int = 42

    @property
    def cutoff_radius(self) -> float:
        return math.sqrt(9.0 * self.sigma_sq_base)