import pygame
from typing import Callable, Iterator
from datetime import datetime


# 色の定義
BLACK = (0, 0, 0)


class Env[S, M]:
    simulate: Callable[[S, M], S]
    render: Callable[[S, S], Iterator[None]]
    input_provider: Callable[[], M]

    def __init__(self) -> None:
        # Pygameの初期化
        pygame.init()

        # 画面サイズ設定
        WIDTH, HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pygame サンプル")

        # フレームレート設定
        self.clock = pygame.time.Clock()
        self.FPS = 60

        # シミュレーションの時間間隔
        self.dt = 1.0

    def _simulation_step(self) -> bool:
        # 規定の時間が経過するまで描画ループ
        simstart = datetime.now()
        render = self.render(self._prev, self._curr)
        self.elapsed = 0.0  # 最後に状態が更新されてからの経過時間（秒）
        while self.elapsed < self.dt:
            # 経過時間の計算
            now = datetime.now()
            self.elapsed = (now - simstart).total_seconds()

            # イベント処理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

            # 画面を黒でクリア
            self.screen.fill(BLACK)

            # 描画
            next(render)

            # 描画更新
            pygame.display.flip()

            # フレームレート維持
            self.clock.tick(self.FPS)

        # 時間が来たらゲーム世界を進める
        msg = self.input_provider()
        next_state = self.simulate(self._curr, msg)
        self._prev = self._curr
        self._curr = next_state

        return True

    def run(
        self,
        initial_state: S,
    ) -> None:
        print("run_gameはじめ")
        self._prev = initial_state
        self._curr = initial_state

        while self._simulation_step():
            pass

        # Pygameの終了
        pygame.quit()
