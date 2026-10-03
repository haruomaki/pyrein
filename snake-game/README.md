# スネークゲーム

snake/
  game.py       # 純粋ロジック（State, step, view）＋ Scene型
  render.py     # Scene → pygame
  play.py       # 人間プレイ
  gym_env.py    # gymラッパー（後回しでもOK、まずはgame.py）
