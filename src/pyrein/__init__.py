import pygame
from typing import Callable, Iterator


def run[S, M](
    simulate: Callable[[S, M], S],
    render: Callable[[S, S], Iterator[None]],
    input_provider: Callable[[], M],
    initial_state: S,
) -> None:
    ##########################
    ## グローバル変数の宣言 ##
    ##########################

    global screen, elapsed, fps

    ################
    ## 初期化処理 ##
    ################

    # Pygameの初期化
    pygame.init()

    # 画面サイズ設定
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pygame サンプル")

    # フレームレート設定
    clock = pygame.time.Clock()
    fps = 60

    # シミュレーションの時間間隔
    dt = 1.0

    # 色の定義
    BLACK = (0, 0, 0)

    ############################
    ## シミュレーションループ ##
    ############################

    prev = initial_state
    curr = initial_state
    running = True
    while running:
        # 規定の時間が経過するまで描画ループ
        simstart = pygame.time.get_ticks()
        it = render(prev, curr)
        elapsed = 0.0  # 最後に状態が更新されてからの経過時間（秒）
        while running and elapsed < dt:
            # 経過時間の計算
            now = pygame.time.get_ticks()
            elapsed = (now - simstart) / 1000

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
            clock.tick(fps)

        # 時間が来たらゲーム世界を進める
        msg = input_provider()
        next_state = simulate(curr, msg)
        prev = curr
        curr = next_state

    # Pygameの終了
    pygame.quit()


def lerp(start: float, end: float, easing: Callable[[float], float]) -> float:
    global elapsed
    ratio = easing(elapsed)
    return start * (1 - ratio) + end * ratio
