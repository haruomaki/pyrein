import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
import os

# モデルファイルのパス
MODEL_PATH = "cartpole_ppo.zip"


def train_model():
    """モデルを学習する（初回のみ実行）"""
    print("モデルを学習中...")

    # ベクトル化環境
    env = make_vec_env("CartPole-v1", n_envs=4)

    # PPOアルゴリズムで学習
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=1000)

    # モデルの保存
    model.save(MODEL_PATH)
    print(f"モデルを保存しました: {MODEL_PATH}")

    env.close()
    return model


def load_and_play(model_path=MODEL_PATH, episodes=10, render_mode="human"):
    """学習済みモデルをロードしてプレイを表示"""

    # モデルの存在確認
    if not os.path.exists(model_path):
        print(f"モデルファイルが見つかりません: {model_path}")
        print("新規に学習を開始します...")
        model = train_model()
    else:
        print(f"学習済みモデルをロード中: {model_path}")
        model = PPO.load(model_path)

    # 表示用の環境を作成（ベクトル化しない単一環境）
    env = gym.make("CartPole-v1", render_mode=render_mode)

    print("プレイを開始します...")
    print("ウィンドウが表示されるまでお待ちください...")

    total_rewards = []

    for episode in range(episodes):
        obs, _ = env.reset()
        done = False
        episode_reward = 0

        while not done:
            # モデルが予測した行動を実行
            action, _states = model.predict(obs, deterministic=True)

            # 環境を1ステップ進める
            obs, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
            episode_reward += reward

            # 現在の状態を表示
            env.render()

        total_rewards.append(episode_reward)
        print(f"エピソード {episode + 1}: 報酬 = {episode_reward:.1f}")

    env.close()

    # 統計情報の表示
    if total_rewards:
        print(f"\n=== 統計 ===")
        print(f"平均報酬: {sum(total_rewards)/len(total_rewards):.1f}")
        print(f"最大報酬: {max(total_rewards):.1f}")
        print(f"最小報酬: {min(total_rewards):.1f}")


# メイン実行部分
if __name__ == "__main__":
    # 方法1: 既存モデルがあればそれをロード、なければ新規学習
    load_and_play()

    # 方法2: 強制的に新規学習から始めたい場合
    # train_model()  # まず学習
    # load_and_play()  # その後プレイ
