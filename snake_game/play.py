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
    if engine.step == 0:
        prev = copy.copy(state)
        curr = copy.copy(state)
    elif engine.step != current_step:
        current_step = engine.step
        # print("prevとcurrが更新")
        prev = curr
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
        x = engine.lerp(pr.x * game.GRID_SIZE, cr.x * game.GRID_SIZE, ease_out(dt, 1.5))
        y = engine.lerp(pr.y * game.GRID_SIZE, cr.y * game.GRID_SIZE, ease_out(dt, 1.5))
        color = SNAKE_HEAD if i == 0 else SNAKE_BODY
        engine.draw.circle(color, (x, y), game.GRID_SIZE / 2)


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
        action, _ = model.predict(obs, deterministic=True)
        return int(action)

    return decide_ai


# コマンドライン引数で「human」「random」「ai」を選べる。
if __name__ == "__main__":
    args = sys.argv
    MODE = args[1] if len(args) > 1 else "human"

    match MODE.lower():
        case "random":
            decider = decide_random
        case "ai":
            decider = make_decide_ai("snake_ppo_model.zip")
        case _:
            decider = decide

    engine.run(
        game.simulate,
        decider,
        render,
        game.initialize,
        window_title="イモムシゲーム",
    )
