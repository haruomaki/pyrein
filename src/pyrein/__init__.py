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
        self.elapsed = 0.0  # 最後に状態が更新されてからの経過時間（秒）

    def _step(self) -> bool:
        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        # 時間の更新
        now = datetime.now()
        self.elapsed = (now - self.t).total_seconds()

        # 規定の時間が経過したときだけゲーム世界を進める
        if self.elapsed >= self.dt:
            msg = self.input_provider()
            next_state = self.simulate(self._curr, msg)
            self._prev = self._curr
            self._curr = next_state
            self.t = now
            self._rd = self.render(self._prev, self._curr)
            return True

        # 描画は毎フレーム行う
        # 画面を黒でクリア
        self.screen.fill(BLACK)

        # 描画
        next(self._rd)

        # 描画更新
        pygame.display.flip()

        # フレームレート維持
        self.clock.tick(self.FPS)

        return True

    def run(
        self,
        initial_state: S,
    ) -> None:
        print("run_gameはじめ")
        self._prev = initial_state
        self._curr = initial_state
        self._rd = self.render(self._prev, self._curr)  # TODO: 冗長？

        self.t = datetime.now()
        while self._step():
            pass

        # Pygameの終了
        pygame.quit()
