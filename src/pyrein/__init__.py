import pygame
from typing import Callable, Generator, NoReturn
import copy


def run[S, M](
    simulate: Callable[[S, M], S],
    decide: Callable[[], Generator[None, None, M]],
    render: Callable[[S, S], Generator[None, None, NoReturn]],
    initial_state: S,
) -> None:
    pygame.init()  # Pygameの初期化
    try:  # 必ずpygame.quit()が呼ばれるようにtryで囲む

        ##########################
        ## グローバル変数の宣言 ##
        ##########################

        global screen, elapsed, fps

        ################
        ## 初期化処理 ##
        ################

        # 画面サイズ設定
        WIDTH, HEIGHT = 800, 600
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pygame サンプル")

        # フレームレート設定
        clock = pygame.time.Clock()
        fps = 60

        # 色の定義
        BLACK = (0, 0, 0)

        ############################
        ## シミュレーションループ ##
        ############################

        prev = initial_state
        curr = initial_state

        while True:
            # 規定の時間が経過するまで描画ループ
            simstart = pygame.time.get_ticks()
            draw = render(prev, curr)
            act = decide()
            elapsed = 0.0  # 最後に状態が更新されてからの経過時間（秒）
            while True:
                # 経過時間の計算
                now = pygame.time.get_ticks()
                elapsed = (now - simstart) / 1000

                # イベント処理
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return

                # 描画
                screen.fill(BLACK)
                next(draw)
                pygame.display.flip()

                # キー入力受け付け
                try:
                    next(act)
                except StopIteration as e:
                    msg = e.value
                    break

                # フレームレート維持
                clock.tick(fps)

            # 時間が来たらゲーム世界を進める
            next_state = simulate(copy.copy(curr), msg)
            prev = curr
            curr = next_state
    finally:
        # Pygameの終了
        pygame.quit()


def lerp(start: float, end: float, easing: Callable[[float], float]) -> float:
    global elapsed
    ratio = easing(elapsed)
    return start * (1 - ratio) + end * ratio
