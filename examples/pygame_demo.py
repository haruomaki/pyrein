import pygame
import sys


def game():
    # Pygameの初期化
    pygame.init()

    # 画面サイズ設定
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pygame サンプル")

    # 色の定義
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    # 円の初期位置と速度
    x, y = WIDTH // 2, HEIGHT // 2
    dx, dy = 5, 5
    radius = 30

    # フレームレート設定
    clock = pygame.time.Clock()
    FPS = 60

    # メインループ
    running = True
    while running:
        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 円の位置更新
        x += dx
        y += dy

        # 壁に衝突したら方向を反転
        if x - radius < 0 or x + radius > WIDTH:
            dx = -dx
        if y - radius < 0 or y + radius > HEIGHT:
            dy = -dy

        # 画面を黒でクリア
        screen.fill(BLACK)

        # 円を描画
        pygame.draw.circle(screen, RED, (x, y), radius)

        # 描画更新
        pygame.display.flip()

        # フレームレート維持
        clock.tick(FPS)

    # Pygameの終了
    pygame.quit()
    sys.exit()


game()
