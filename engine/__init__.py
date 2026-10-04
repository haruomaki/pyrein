"""
engine/__init__.py
"""

import pygame
from typing import Callable, Generator

# engine.draw公開
from . import draw  # pyright: ignore[reportUnusedImport]


def run[S, M](
    simulate: Callable[[S, M], bool],
    decide: Callable[[S], Generator[None, None, M]],
    render: Callable[[S], None],
    initialize: Callable[[], S],
    window_title: str = "Pygame サンプル",
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
        pygame.display.set_caption(window_title)

        # フレームレート設定
        clock = pygame.time.Clock()
        fps = 60

        # 色の定義
        BLACK = (0, 0, 0)

        ############################
        ## シミュレーションループ ##
        ############################

        global step
        step = 0
        state = initialize()

        while True:
            # 規定の時間が経過するまで描画ループ
            simstart = pygame.time.get_ticks()
            act = decide(state)
            elapsed = 0.0  # 最後に状態が更新されてからの経過時間（秒）
            while True:
                # 経過時間の計算
                now = pygame.time.get_ticks()
                elapsed = (now - simstart) / 1000  # ミリ秒を秒に直す

                # イベント処理・終了判定
                if pygame.key.get_pressed()[pygame.K_q]:
                    return
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return

                # 描画
                screen.fill(BLACK)
                render(state)
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
            simulation_running = simulate(state, msg)
            step += 1
            if not simulation_running:
                state = initialize()

    finally:
        # Pygameの終了
        pygame.quit()


# ===================
# ユーティリティ
# ===================
def lerp(start: float, end: float, easing: Callable[[float], float]) -> float:
    """経過時間（秒）とイージング関数を用いて、2つの値の間を線形補間（Lerp）します。

    グローバル変数 `elapsed`（秒単位の経過時間）をそのままイージング関数に渡し、
    得られた補間割合（ratio）に基づいて開始値から終了値までの現在の値を計算します。

    Args:
        start (float): 補間の開始値。
        end (float): 補間の終了値。
        easing (Callable[[float], float]): 経過時間（float）を受け取り、補間割合（0.0〜1.0）を返す関数。

    Returns:
        float: 補間された現在の値。
    """
    global elapsed
    ratio = easing(elapsed)
    return start * (1 - ratio) + end * ratio
