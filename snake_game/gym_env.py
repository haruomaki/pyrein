"""
snake_game/gym_env.py
"""

import gymnasium as gym
import numpy as np
from gymnasium import spaces
from pygame import Vector2 as Vec2
import copy

import snake_game.game as game


class SnakeEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 10}

    def __init__(self, render_mode=None):
        super().__init__()
        self.render_mode = render_mode

        # 行動: 0=上, 1=下, 2=左, 3=右
        self.action_space = spaces.Discrete(4)

        # 観測: 3チャンネル (頭, 体, リンゴ) の HxW グリッド
        self.observation_space = spaces.Box(
            low=0,
            high=1,
            shape=(3, game.GRID_HEIGHT, game.GRID_WIDTH),
            dtype=np.float32,
        )

        self.state: game.State = game.initialize()
        self.done = False

    # ---------- 観測変換 ----------
    def _get_obs(self) -> np.ndarray:
        # obs[0]頭の位置頭があるマスだけ 1、それ以外 0
        # obs[1]体の位置体があるマスだけ 1、それ以外 0
        # obs[2]リンゴの位置リンゴがあるマスだけ 1、それ以外 0
        obs = np.zeros((3, game.GRID_HEIGHT, game.GRID_WIDTH), dtype=np.float32)

        # 体（obs[1]）
        for b in self.state.body:
            obs[1, int(b.y), int(b.x)] = 1

        # 頭（obs[0]）※体チャンネルからは頭の位置を消す
        head = self.state.body[0]
        obs[0, int(head.y), int(head.x)] = 1
        obs[1, int(head.y), int(head.x)] = 0

        # リンゴ（obs[2]）
        if self.state.apple is not None:
            obs[2, int(self.state.apple.y), int(self.state.apple.x)] = 1

        return obs

    def _get_info(self) -> dict:
        return {"length": len(self.state.body)}

    # ---------- Gym API ----------
    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        self.state = game.initialize()
        self.done = False
        return self._get_obs(), self._get_info()

    def step(self, action: int):
        assert self.state is not None
        prev = copy.copy(self.state)
        alive = game.simulate(self.state, int(action))

        # 報酬設計
        reward = 0.0
        terminated = False
        truncated = False

        if not alive:
            reward = -1.0  # 壁にぶつかった
            terminated = True
        elif len(self.state.body) > len(prev.body):
            reward = +1.0  # リンゴを食べた
        else:
            reward = -0.01  # 時間ペナルティ（任意）

        # FIXME: これどうなん
        assert prev.apple is not None
        assert self.state.apple is not None

        # リンゴとのマンハッタン距離を計算
        prev_dist = abs(prev.body[0].x - prev.apple.x) + abs(
            prev.body[0].x - prev.apple.x
        )
        curr_dist = abs(self.state.body[0].x - self.state.apple.x) + abs(
            self.state.body[0].y - self.state.apple.y
        )

        # 前状態と比べてリンゴに近づいたら微プラス
        if curr_dist < prev_dist:
            reward += 0.005

        # リンゴがなくなった = 全マス制覇
        if self.state.apple is None:
            terminated = True
            reward = +2.0

        obs = self._get_obs()
        info = self._get_info()
        return obs, reward, terminated, truncated, info

    def render(self):
        # 既存の render を流用したい場合は engine 側と連携が必要。
        # ここではシンプルに print で可視化。
        if self.render_mode == "human":
            grid = [
                ["." for _ in range(game.GRID_WIDTH)] for _ in range(game.GRID_HEIGHT)
            ]
            for i, b in enumerate(self.state.body):
                grid[int(b.y)][int(b.x)] = "O" if i == 0 else "o"
            if self.state.apple is not None:
                grid[int(self.state.apple.y)][int(self.state.apple.x)] = "A"
            print("\n".join("".join(row) for row in grid))
            print()
