import engine
import snake_game.game as game
import pygame
from pygame import Vector2 as Vec2
from engine.easing import ease_out

# 色の定義
BACKGROUND = (15, 56, 15)
GRID_COLOR = (20, 80, 20)
SNAKE_HEAD = (23, 200, 100)  # ミントグリーン
SNAKE_BODY = (46, 139, 87)  # シーグリーン
FOOD_COLOR = (220, 20, 60)  # クリムゾン
TEXT_COLOR = (255, 255, 255)


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


def render(prev: game.State, curr: game.State):
    while True:
        draw_grid()

        # リンゴを描画
        if curr.apple:
            engine.draw.circle(
                FOOD_COLOR, curr.apple * game.GRID_SIZE, game.GRID_SIZE / 3
            )

        # 円を描画。頭を最前面に描画するために逆順に
        if len(prev.body) != len(curr.body):
            prev.body = [prev.body[0]] + prev.body
        for i in range(len(curr.body) - 1, -1, -1):
            pr = prev.body[i]
            cr = curr.body[i]
            x = engine.lerp(
                pr.x * game.GRID_SIZE, cr.x * game.GRID_SIZE, ease_out(dt, 1.5)
            )
            y = engine.lerp(
                pr.y * game.GRID_SIZE, cr.y * game.GRID_SIZE, ease_out(dt, 1.5)
            )
            color = SNAKE_HEAD if i == 0 else SNAKE_BODY
            engine.draw.circle(color, (x, y), game.GRID_SIZE / 2)

        yield


def decide():
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


engine.run(
    game.simulate,
    decide,
    render,
    game.initialize,
)
