import pygame
from typing import Callable, Iterator, Any
from datetime import datetime


# 色の定義
BLACK = (0, 0, 0)

_prev: Any = None  # S
_curr: Any = None  # S

# Pygameの初期化
pygame.init()

# 画面サイズ設定
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame サンプル")

# フレームレート設定
clock = pygame.time.Clock()
FPS = 60

# シミュレーションの時間間隔
dt = 1.0
elapsed = 0.0


def run[S, M](
    simulate: Callable[[S, M], S],
    render: Callable[[S, S], Iterator[None]],
    input_provider: Callable[[], M],
    initial_state: S,
) -> None:
    global _prev, _curr, elapsed
    print("run_gameはじめ")
    _prev = initial_state
    _curr = initial_state

    # シミュレーションループ
    running = True
    while running:
        # 規定の時間が経過するまで描画ループ
        simstart = datetime.now()
        it = render(_prev, _curr)
        elapsed = 0.0  # 最後に状態が更新されてからの経過時間（秒）
        while running and elapsed < dt:
            # 経過時間の計算
            now = datetime.now()
            elapsed = (now - simstart).total_seconds()

            # イベント処理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # 画面を黒でクリア
            screen.fill(BLACK)

            # 描画
            next(it)

            # 描画更新
            pygame.display.flip()

            # フレームレート維持
            clock.tick(FPS)

        # 時間が来たらゲーム世界を進める
        msg = input_provider()
        next_state = simulate(_curr, msg)
        _prev = _curr
        _curr = next_state

    # Pygameの終了
    pygame.quit()
