"""
snake_game/train.py
"""

import os
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from snake_game.gym_env import SnakeEnv

MODEL_PATH = "snake_ppo_model.zip"
LOG_DIR = "./tensorboard_logs/"  # ログの保存先フォルダを指定
TOTAL_TIMESTEPS = 500000  # 学習ステップ数

if __name__ == "__main__":
    # CPUスレッド数の環境で並列化
    env = make_vec_env(SnakeEnv, n_envs=16)

    if os.path.exists(MODEL_PATH):
        print(f'"{MODEL_PATH}" が見つかりました。追加学習を開始します！')
        model = PPO.load(MODEL_PATH, env=env, device="cpu", tensorboard_log=LOG_DIR)
        # 続きから追加学習（ログのステップ数を維持）
        model.learn(total_timesteps=TOTAL_TIMESTEPS, reset_num_timesteps=False)
    else:
        print(f'"{MODEL_PATH}" が見つかりません。ゼロから新規学習を開始します！')
        model = PPO(
            "MlpPolicy",  # 全結合NNの方策
            env,  # 学習環境
            device="cpu",  # CPUで計算
            verbose=1,  # 進捗表示
            learning_rate=0.0003,  # 学習率
            ent_coef=0.04,  # 探索を促す
            gamma=0.995,  # 割引率
            n_steps=512,  # 更新前に集めるステップ数
            batch_size=64,  # ミニバッチサイズ
            n_epochs=4,  # データを繰り返す回数
            policy_kwargs=dict(net_arch=[256, 256, 128]),  # NNの形状
            tensorboard_log=LOG_DIR,
        )
        model.learn(total_timesteps=TOTAL_TIMESTEPS)

    # 学習完了後に保存
    model.save(MODEL_PATH)
    print("モデルの保存が完了しました！")
