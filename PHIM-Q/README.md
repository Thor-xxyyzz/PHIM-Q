### 📄 `README.md`

```markdown
# PHIM-Q: Langevin Fluid Simulator

PHIM-Q 是一個基於純粹朗之萬動力學 (Langevin Dynamics) 的熱力學流體模擬器。本專案致力於通過簡約的物理方程式，精確模擬勢能阱中的均場流體行為。

[English Description below]

## 專案介紹
PHIM-Q 旨在提供一個**極簡、物理嚴謹且高效**的流體模擬框架。它不依賴複雜的數值作弊（如動量濾波或硬性剪裁），而是透過嚴格的統計物理定律（漲落-耗散定理），讓流體在勢能阱中自發演化至熱力學平衡狀態。

### 主要特色
* **物理嚴謹性：** 嚴格遵循過阻尼朗之萬方程式。
* **極簡架構：** 捨棄冗餘的工程優化，代碼純粹易讀。
* **高收斂效率：** 採用兩段式退火排程，可在 6000 步內達到平衡。

## 安裝方式
1. 確保已安裝 Python 3.11 或更高版本。
2. 克隆本專案並安裝依賴：
   ```bash
   git clone [https://github.com/YOUR_USERNAME/PHIM-Q.git](https://github.com/YOUR_USERNAME/PHIM-Q.git)
   cd PHIM-Q
   pip install -r requirements.txt

```

## 執行實驗

```bash
python main_experiment.py

```

---

## Project Introduction

PHIM-Q is a high-fidelity, physics-based simulator for many-particle systems in double-well potentials, powered by strict Langevin dynamics.

### Key Features

* **Physics-First:** Implements the overdamped Langevin equation without heuristic gradient clipping or artificial damping.
* **Minimalist Design:** Optimized for readability and scientific reproducibility.
* **Efficient Equilibrium:** Reaches Boltzmann equilibrium within 6,000 steps using two-stage simulated annealing.

## Getting Started

1. Clone the repository and install requirements:
```bash
git clone [https://github.com/YOUR_USERNAME/PHIM-Q.git](https://github.com/YOUR_USERNAME/PHIM-Q.git)
cd PHIM-Q
pip install -r requirements.txt

```


2. Run the simulation:
```bash
python main_experiment.py

```
