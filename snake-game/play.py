# play.py
import pygame
from game import Action, initial_state, step, view
from render import draw_scene

CELL = 40
FPS = 10
GRID = (15, 15)

KEYMAP = {
    pygame.K_UP: Action.UP,
    pygame.K_w: Action.UP,
    pygame.K_DOWN: Action.DOWN,
    pygame.K_s: Action.DOWN,
    pygame.K_LEFT: Action.LEFT,
    pygame.K_a: Action.LEFT,
    pygame.K_RIGHT: Action.RIGHT,
    pygame.K_d: Action.RIGHT,
}


def main():
    pygame.init()
    screen = pygame.display.set_mode((GRID[0] * CELL, GRID[1] * CELL))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)

    state = initial_state(GRID)
    pending_action: Action | None = None

    running = True
    while running:
        # 入力
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    running = False
                elif e.key == pygame.K_r and not state.alive:
                    state = initial_state(GRID)
                    pending_action = None
                elif e.key in KEYMAP:
                    pending_action = KEYMAP[e.key]

        # 更新（毎フレームではなく、FPSに従って1歩）
        if state.alive:
            action = pending_action if pending_action is not None else state.direction
            result = step(state, action)
            state = result.state
            pending_action = None

        # 描画
        draw_scene(screen, view(state), CELL, font)
        if not state.alive:
            _draw_gameover(screen, state, font)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


def _draw_gameover(screen, state, font):
    text = font.render(
        f"Game Over  Score={state.score}  [R] Restart",
        True,
        (255, 255, 255),
    )
    rect = text.get_rect(center=screen.get_rect().center)
    bg = pygame.Surface((rect.width + 20, rect.height + 16), pygame.SRCALPHA)
    bg.fill((0, 0, 0, 180))
    screen.blit(bg, (rect.x - 10, rect.y - 8))
    screen.blit(text, rect)


if __name__ == "__main__":
    main()
