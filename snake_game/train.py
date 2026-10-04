"""
snake_game/train.py
"""

from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from snake_game.gym_env import SnakeEnv

if __name__ == "__main__":
    # 8つのゲーム環境を並列で同時に動かす（CPUコア数に合わせて 4〜8 程度がおすすめ）
    env = make_vec_env(SnakeEnv, n_envs=8)

    model = PPO(
        "MlpPolicy",
        env,
        device="cpu",  # 小型モデルはCPUの方が圧倒的に高速
        verbose=1,
        learning_rate=0.0003,
    )

    print("爆速学習を開始します...")
    model.learn(total_timesteps=200000)

    model.save("snake_ppo_model")
    print("モデルを保存しました！")
