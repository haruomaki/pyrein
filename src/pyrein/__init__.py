import pygame
from typing import TypeVar, Callable, Iterator
from datetime import datetime, timedelta

S = TypeVar("S")  # State
M = TypeVar("M")  # Message / Input

Simulator = Callable[[S, M], S]
Renderer = Callable[[S, S], Iterator[None]]
InputProvider = Callable[[], M]

# 色の定義
BLACK = (0, 0, 0)
RED = (255, 0, 0)


class Env[S, M]:
    simulate: Simulator[S, M]
    render: Renderer[S]
    input_provider: InputProvider[M]

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
        self.dt = 1

    def run_game(
        self,
        initial_state: S,
    ) -> None:
        print("run_gameはじめ")
        prev = initial_state
        curr = initial_state
        rd = self.render(prev, curr)  # TODO: 冗長？

        t = datetime.now()
        running = True
        while running:
            # イベント処理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # 規定の時間が経過したときだけゲーム世界を進める
            if datetime.now() - t >= timedelta(seconds=self.dt):
                msg = self.input_provider()
                next_state = self.simulate(curr, msg)
                prev = curr
                curr = next_state
                t = datetime.now()  # TODO: 冗長？
                rd = self.render(prev, curr)
                continue

            # 描画は毎フレーム行う
            # 画面を黒でクリア
            self.screen.fill(BLACK)

            # 描画
            next(rd)

            # 描画更新
            pygame.display.flip()

            # フレームレート維持
            self.clock.tick(self.FPS)
