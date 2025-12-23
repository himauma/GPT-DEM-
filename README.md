# GPT-DEM-

GPTでDEMシミュレーションしてみる (DEM Simulation with GPT)

## 概要 (Overview)

このプロジェクトは、DEM (Discrete Element Method: 離散要素法) シミュレーションのPython実装です。
粒子の動力学をシミュレートし、衝突、重力、境界条件を考慮します。

This project is a Python implementation of DEM (Discrete Element Method) simulation.
It simulates particle dynamics with collisions, gravity, and boundary conditions.

## 機能 (Features)

- 粒子間の衝突検出と力の計算
- 重力の適用
- 境界条件の処理
- リアルタイムアニメーション可視化
- 2つのシミュレーションモード：
  - 落下する粒子
  - 粒子の山の形成

## 必要要件 (Requirements)

- Python 3.7以上
- NumPy
- Matplotlib

## インストール (Installation)

```bash
pip install -r requirements.txt
```

## 使い方 (Usage)

シミュレーションを実行：

```bash
python main.py
```

実行すると、シミュレーションタイプを選択できます：
1. 落下する粒子
2. 粒子の山の形成

## ファイル構成 (File Structure)

- `particle.py` - 粒子クラスの定義
- `dem_simulation.py` - DEMシミュレーションエンジン
- `main.py` - メインスクリプト（シミュレーション実行）
- `requirements.txt` - 必要なPythonパッケージ

## 物理パラメータ (Physics Parameters)

- 法線方向剛性: 1000 N/m
- 接線方向剛性: 800 N/m
- 減衰係数: 0.3
- 摩擦係数: 0.5
- 反発係数: 0.8
- 重力: -9.81 m/s²

## ライセンス (License)

MIT License