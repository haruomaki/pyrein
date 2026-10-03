# gym_env.py
from __future__ import annotations
import random
import numpy as np
import gymnasium as gym
from gymnasium import spaces

from game import Action, initial_state, step as game_step, State


class SnakeEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 10}

    def __init__(self, grid=(10, 10), render_mode=None):
        super().__init__()
        self.grid = grid
        self.render_mode = render_mode
        self.action_space = spaces.Discrete(len(Action))
        self.observation_space = spaces.Box(
            low=0.0,
            high=1.0,
            shape=(grid[0], grid[1], 3),
            dtype=np.float32,
        )
        self._state: State | None = None
        self._surface = None
        self._font = None

    # --- obs 構築 ---
    def _obs(self) -> np.ndarray:
        g = np.zeros(self.observation_space.shape, dtype=np.float32)
        for x, y in self._state.snake[1:]:
            g[y, x, 0] = 1.0
        hx, hy = self._state.snake[0]
        g[hy, hx, 0] = 0.5  # 頭は別値
        fx, fy = self._state.food
        if fx >= 0:
            g[fy, fx, 1] = 1.0
        g[:, :, 2] = self._state.direction / 3.0
        return g

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        rng = random.Random(seed)
        self._state = initial_state(self.grid, rng)
        if self.render_mode == "human":
            self._ensure_pygame()
        return self._obs(), {}

    def step(self, action):
        result = game_step(self._state, Action(int(action)))
        self._state = result.state
        if self.render_mode == "human":
            self.render()
        return (
            self._obs(),
            result.reward,
            result.terminated,
            result.truncated,
            result.info,
        )

    # --- render ---
    def _ensure_pygame(self):
        import pygame
        from render import draw_scene  # noqa

        pygame.init()
        cell = 40
        self._cell = cell
        self._surface = pygame.display.set_mode(
            (self.grid[0] * cell, self.grid[1] * cell)
        )
        self._font = pygame.font.SysFont(None, 28)
        pygame.display.set_caption("Snake (RL)")

    def render(self):
        if self.render_mode is None:
            return
        import pygame
        from render import draw_scene
        from game import view

        if self._surface is None:
            self._ensure_pygame()
        draw_scene(self._surface, view(self._state), self._cell, self._font)
        pygame.display.flip()

    def close(self):
        if self._surface is not None:
            import pygame

            pygame.quit()
            self._surface = None
