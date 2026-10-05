"""
snake_game/play.py
"""

import sys
import engine
import snake_game.game as game
import pygame
from pygame import Vector2 as Vec2
from engine.easing import ease_out
import copy
import random

# 色の定義
BACKGROUND = "#0F380F"  # 深い緑
GRID_COLOR = "#145014"  # グリッド
SNAKE_HEAD = "#17C864"  # ミントグリーン
SNAKE_BODY = "#2E8B57"  # シーグリーン
FOOD_COLOR = "#DC143C"  # クリムゾン
TEXT_COLOR = "#FFFFFF"  # 白

POWER = 1.5  # 描画用のパラメータ。マスの移動のメリハリ
dt = 0.3
engine.draw.camera.set_offset(
    (game.GRID_WIDTH - 1) / 2 * game.GRID_SIZE,
    (game.GRID_HEIGHT - 1) / 2 * game.GRID_SIZE,
)
DIRECTIONS = [Vec2(0, -1), Vec2(0, 1), Vec2(-1, 0), Vec2(1, 0)]


def draw_grid():
    """グリッド線を描画"""
    for w in range(game.GRID_WIDTH):
        engine.draw.line(
            GRID_COLOR,
            (w * game.GRID_SIZE, 0),
            (w * game.GRID_SIZE, (game.GRID_HEIGHT - 1) * game.GRID_SIZE),
        )
    for h in range(game.GRID_HEIGHT):
        engine.draw.line(
            GRID_COLOR,
            (0, h * game.GRID_SIZE),
            ((game.GRID_WIDTH - 1) * game.GRID_SIZE, h * game.GRID_SIZE),
        )


prev: game.State | None = None
curr: game.State | None = None
current_step: int = 0


def render(state: game.State):
    global prev, curr, current_step
    if prev is None:
        prev = copy.copy(state)
    elif engine.step != current_step:
        current_step = engine.step
        # print("prevとcurrが更新")
        prev = copy.copy(curr)
    curr = copy.copy(state)

    assert prev is not None
    assert curr is not None

    draw_grid()

    # リンゴを描画
    if curr.apple is not None:
        engine.draw.circle(FOOD_COLOR, curr.apple * game.GRID_SIZE, game.GRID_SIZE / 3)

    # 円を描画。頭を最前面に描画するために逆順に
    if len(prev.body) != len(curr.body):
        prev.body = [prev.body[0]] + prev.body
    for i in range(len(curr.body) - 1, -1, -1):
        pr = prev.body[i]
        cr = curr.body[i]
        pos = engine.lerp(pr * game.GRID_SIZE, cr * game.GRID_SIZE, ease_out(dt, POWER))
        color = SNAKE_HEAD if i == 0 else SNAKE_BODY
        engine.draw.circle(color, pos, game.GRID_SIZE / 2)

    # 蛇の長さを表示
    engine.draw.text(f"Length: {len(curr.body)}", TEXT_COLOR, (10, 10))


# キーボード操作によって行動を決定する関数
def decide(_: game.State):
    action: game.Action = None
    while engine.elapsed < dt:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            action = 0
        if keys[pygame.K_DOWN]:
            action = 1
        if keys[pygame.K_LEFT]:
            action = 2
        if keys[pygame.K_RIGHT]:
            action = 3
        yield

    return action


# ランダムに行動を決定する関数
def decide_random(_: game.State):
    while engine.elapsed < dt:
        yield

    return random.randint(0, 3)


# サンプリング用の関数。TODO: engineの一部にする？
import numpy as np
import torch


def sample_with_top_k(distribution, top_k: int = 2, temperature: float = 1.0) -> int:
    """Logits（未正規化の確率）からTop-kおよびTemperatureを適用して行動を選択する"""
    logits = distribution.distribution.logits.clone()

    # 1. Top-k 以外の選択肢をマスク（-inf に設定）
    if top_k > 0 and top_k < logits.size(-1):
        indices_to_remove = logits < torch.topk(logits, top_k)[0][..., -1:]
        logits[indices_to_remove] = float("-inf")

    # 2. Temperature の適用
    if temperature != 1.0:
        logits = logits / temperature

    # 3. Softmax で確率分布に変換
    probs = torch.softmax(logits, dim=-1).cpu().numpy().squeeze()

    # 4. 確率に従ってサンプリング
    return int(np.random.choice(len(probs), p=probs))


# ★ AI は「ファクトリ関数」に。呼ばれた時だけ重い import とロードが走る
def make_decide_ai(model_path: str):
    from stable_baselines3 import PPO
    from snake_game.gym_env import SnakeEnv

    model = PPO.load(model_path, device="cpu")
    env = SnakeEnv()

    def decide_ai(state: game.State):
        while engine.elapsed < dt:
            yield
        env.state = state
        obs = env._get_obs()

        obs_tensor, _ = model.policy.obs_to_tensor(obs)

        with torch.no_grad():
            dist = model.policy.get_distribution(obs_tensor)
            # 独立させたパーツを呼び出す（上位2手から、わずかにランダム性を持たせて選ぶ）
            action = sample_with_top_k(dist, top_k=2, temperature=0.2)

        return action

    return decide_ai


# コマンドライン引数で「human」「random」「ai」を選べる。
if __name__ == "__main__":
    args = sys.argv
    MODE = args[1] if len(args) > 1 else "human"

    match MODE.lower():
        case "random":
            decider = decide_random
        case "ai":
            dt = 0.1
            POWER = 1  # なめらかにアニメーション
            decider = make_decide_ai("snake_ppo_model.zip")
        case _:
            decider = decide

    engine.run(
        game.simulate,
        decider,
        render,
        game.initialize,
        window_title="イモムシゲーム",
        window_size=(560, 420),
    )
