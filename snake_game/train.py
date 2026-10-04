"""
snake_game/train.py
"""

import os
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import SubprocVecEnv
from snake_game.gym_env import SnakeEnv

MODEL_PATH = "snake_ppo_model.zip"
TOTAL_TIMESTEPS = 200000  # 学習ステップ数

if __name__ == "__main__":
    # 16環境で並列化
    env = make_vec_env(SnakeEnv, n_envs=64)

    if os.path.exists(MODEL_PATH):
        print(f'"{MODEL_PATH}" が見つかりました。追加学習を開始します！')
        model = PPO.load(MODEL_PATH, env=env, device="cpu")
        # 続きから追加学習（ログのステップ数を維持）
        model.learn(total_timesteps=TOTAL_TIMESTEPS, reset_num_timesteps=False)
    else:
        print(f'"{MODEL_PATH}" が見つかりません。ゼロから新規学習を開始します！')
        # model = PPO(
        #     "MlpPolicy",
        #     env,
        #     device="cpu",
        #     verbose=1,
        #     learning_rate=0.0003,
        #     ent_coef=0.02,  # ★探索を促す（ぐるぐるハック防止）
        # )
        model = PPO(
            "MlpPolicy",
            env,
            device="cpu",
            verbose=1,
            learning_rate=0.0003,
            ent_coef=0.02,
            n_steps=2048,
            batch_size=512,
            n_epochs=10,
            policy_kwargs=dict(net_arch=[256, 256]),
        )
        model.learn(total_timesteps=TOTAL_TIMESTEPS)

    # 学習完了後に保存
    model.save("snake_ppo_model")
    print("モデルの保存が完了しました！")
