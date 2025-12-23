# GPT-DEM: Discrete Element Method Simulation

GPT-DEMは、離散要素法（Discrete Element Method）を使用した粒子シミュレーションの実装です。
This project implements a Discrete Element Method (DEM) simulation for granular materials and particle systems.

## 概要 (Overview)

このプロジェクトは、粒子の運動、衝突、重力、摩擦などの物理現象をシミュレートするDEMエンジンを提供します。

Key features:
- 粒子間の衝突検出と応答 (Particle-to-particle collision detection and response)
- 壁との衝突処理 (Wall collision handling)
- 重力、法線力、摩擦力の計算 (Gravity, normal forces, and friction calculations)
- リアルタイム可視化機能 (Real-time visualization capabilities)
- エネルギー保存の追跡 (Energy conservation tracking)

## インストール (Installation)

### 必要条件 (Requirements)

- Python 3.7以上
- NumPy
- Matplotlib

### セットアップ (Setup)

```bash
# リポジトリのクローン
git clone https://github.com/himauma/GPT-DEM-.git
cd GPT-DEM-

# 依存パッケージのインストール
pip install -r requirements.txt
```

## 使用方法 (Usage)

### 基本的な実行 (Basic Execution)

```bash
python main.py
```

このコマンドで、デフォルトの粒子シミュレーションが実行され、結果が`dem_simulation_result.png`として保存されます。

### サンプル例の実行 (Running Examples)

```bash
python examples.py
```

様々なシミュレーションシナリオを実行できます：
- 単一粒子の落下
- 複数粒子の衝突
- 粒子の山形成
- 粒子のバウンド

### カスタムシミュレーション (Custom Simulation)

```python
from dem_simulation import DEMSimulation
from visualizer import DEMVisualizer
import numpy as np

# シミュレーションの作成
sim = DEMSimulation(width=10.0, height=10.0, gravity=9.81)

# 材料パラメータの設定
sim.restitution_coeff = 0.8  # 反発係数
sim.friction_coeff = 0.3      # 摩擦係数
sim.stiffness = 1e5           # 接触剛性
sim.damping = 0.3             # 減衰係数

# 粒子の追加
for i in range(10):
    x = 5.0
    y = 5.0 + i * 0.5
    sim.add_particle(x, y, radius=0.2, mass=1.0)

# シミュレーションの実行
for step in range(1000):
    sim.step(dt=0.001)

# 可視化
viz = DEMVisualizer(sim)
viz.show_static()
```

## 技術詳細 (Technical Details)

### DEM方程式 (DEM Equations)

粒子の運動は、ニュートンの運動方程式に基づいています：

```
F = ma
v(t+Δt) = v(t) + a·Δt
x(t+Δt) = x(t) + v·Δt
```

接触力モデル：
- **法線力 (Normal Force)**: スプリング-ダンパーモデル
  - F_n = k·δ - γ·v_n
  - k: 剛性係数
  - δ: 重なり量
  - γ: 減衰係数
  - v_n: 法線方向の相対速度

- **接線力 (Tangential Force)**: クーロン摩擦モデル
  - F_t = -μ·|F_n|·sign(v_t)
  - μ: 摩擦係数
  - v_t: 接線方向の相対速度

### クラス構造 (Class Structure)

#### Particle
粒子を表現するクラス
- 位置、速度、加速度
- 質量、半径
- 力の計算と更新

#### DEMSimulation
シミュレーションエンジン
- 粒子管理
- 衝突検出
- 力の計算
- 時間積分

#### DEMVisualizer
可視化機能
- 静的表示
- アニメーション生成
- ファイル保存

## パラメータ調整 (Parameter Tuning)

### 重要なパラメータ (Important Parameters)

1. **時間刻み (Time Step)**: `dt`
   - 推奨値: 0.0001 ~ 0.001秒
   - 小さいほど精度が高いが計算時間が増加

2. **反発係数 (Restitution Coefficient)**: `restitution_coeff`
   - 範囲: 0.0 (完全非弾性) ~ 1.0 (完全弾性)
   - 一般的な値: 0.5 ~ 0.9

3. **摩擦係数 (Friction Coefficient)**: `friction_coeff`
   - 範囲: 0.0 (摩擦なし) ~ 1.0以上
   - 一般的な値: 0.2 ~ 0.5

4. **剛性 (Stiffness)**: `stiffness`
   - 推奨値: 1e4 ~ 1e6 N/m
   - 大きいほど粒子が硬い

5. **減衰 (Damping)**: `damping`
   - 範囲: 0.0 ~ 1.0
   - 一般的な値: 0.1 ~ 0.5

## エネルギー保存 (Energy Conservation)

シミュレーションは、運動エネルギーと位置エネルギーの合計を追跡します：

- **運動エネルギー (Kinetic Energy)**: KE = (1/2)·m·v²
- **位置エネルギー (Potential Energy)**: PE = m·g·h
- **全エネルギー (Total Energy)**: TE = KE + PE

## 出力ファイル (Output Files)

- `dem_simulation_result.png`: 最終状態の可視化
- `particle_demo.gif`: アニメーション（例から生成）

## ライセンス (License)

このプロジェクトはオープンソースです。

## 参考文献 (References)

- Cundall, P. A., & Strack, O. D. (1979). A discrete numerical model for granular assemblies. Geotechnique, 29(1), 47-65.
- Zhu, H. P., et al. (2007). Discrete particle simulation of particulate systems: Theoretical developments. Chemical Engineering Science, 62(13), 3378-3396.

## 貢献 (Contributing)

改善提案やバグ報告は、Issueまたはプルリクエストでお願いします。

## 作者 (Author)

himauma