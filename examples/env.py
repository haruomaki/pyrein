import gymnasium as gym
import numpy as np

# 環境の作成
env = gym.make("CartPole-v1", render_mode="human")  # 可視化する場合
# または render_mode="rgb_array" で画像として取得可能

observation, info = env.reset()

for _ in range(1000):
    action = env.action_space.sample()  # ランダム行動（学習時はここを変更）

    # 1ステップ進める
    observation, reward, terminated, truncated, info = env.step(action)

    if terminated or truncated:
        observation, info = env.reset()

env.close()
