# main_experiment.py
from phimq.config import PHIMQConfig
from phimq.system import LangevinFluidSystem
from phimq.engine import OverdampedLangevinEngine
from tqdm import tqdm

# 1. 自由宣告任意粒子數與設定
config = PHIMQConfig(num_particles=5000, seed=42, device="cuda")

# 2. 實例化物理系統與求解引擎
system = LangevinFluidSystem(config)
engine = OverdampedLangevinEngine(system.particles, config)

# 3. 優雅清晰的實驗 Loop
for step in tqdm(range(config.total_steps), desc="Running PHIM-Q"):
    # 步驟 A: 物理場更新梯度
    grad_norm = system.update_gradient(engine.temp_eff)
    
    # 步驟 B: 引擎推進時間步長 (執行朗之萬運動)
    engine.step()

# 4. 一鍵印出最終頂尖物理矩陣
stats = system.get_statistics()
print(f"\n🪐 實驗完成！最終物理矩陣：")
print(f"📊 粒子對稱比率 (L:R) = {stats['ratio_left']} : {stats['ratio_right']}")
print(f"📍 實際物理重心 (L/R) = {stats['center_left']:.4f} / {stats['center_right']:.4f}")
print(f"🔮 核心流體寬度 (IQR L/R) = {stats['iqr_left']:.4f} / {stats['iqr_right']:.4f}")
print(f"🔥 最終真實梯度 = {grad_norm:.2f}")