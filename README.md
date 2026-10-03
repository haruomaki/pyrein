# pyrein

pyreinは、ゲーム状態の離散的な更新とPygameによるリアルタイム描画を分けて記述する、小さなゲームループ用ライブラリです。中心となるAPIは、次の4つのコールバックです。

```python
pyrein.run(
    simulate,
    decide,
    render,
    initialize,
)
```

`simulate`がゲームルールに従って状態を更新し、`decide`が操作・アクションを取得します。`render`は前状態から現状態への遷移を描き、`initialize`は初期状態を作ります。ゲームの更新は離散的なまま、描画側で状態間の動きを滑らかにアニメーションできます。

## pyreinがすること・しないこと

pyreinは軽量なゲームループ・描画補助ライブラリであり、強化学習ライブラリではありません。エージェントや学習アルゴリズム、報酬、観測、アクション空間、Gymnasium `Env`アダプターは実装していません。

リポジトリにはpyreinで作ったSnakeゲームがありますが、現状はキーボードで遊ぶPygameゲームであり、Gymnasiumの学習環境ではありません。別の`examples/env.py`はGymnasium組み込みの`CartPole-v1`をStable-Baselines3のPPOで学習・実行する例で、pyreinもSnakeも使っていません。`gymnasium`はプロジェクト依存関係に含まれていますが、現在のコードにpyreinとGymnasiumを接続する実装はありません。

Snakeをエージェントに学習させるには、少なくとも`reset()`、`step()`、観測空間、アクション空間、報酬、終了・打ち切り処理を定義するGymnasium環境の実装が別途必要です。その層はこのリポジトリにはありません。

## インストールとサンプルの実行

ライブラリ本体はPython 3.12以降の構文を使い、Pygameに依存しています。

```bash
python -m pip install -e .
python examples/snake.py
```

矢印キーで移動し、`Q`キーまたはウィンドウを閉じて終了します。描画ループは最大60 FPSで、Snakeのゲーム状態は0.3秒ごとに更新されます。

`examples/env.py`は別枠のStable-Baselines3サンプルです。実行する場合は、プロジェクトの依存関係に加えてStable-Baselines3をインストールしてください。

```bash
python -m pip install stable-baselines3
python examples/env.py
```

## コールバックの仕様

`pyrein.run(simulate, decide, render, initialize)`は次のように動作します。

| コールバック | 役割 |
| --- | --- |
| `initialize() -> state` | 新しい初期状態を返します。ループ開始時に前状態・現状態を作るために呼ばれ、`simulate`が`None`を返した場合にも再度呼ばれます。 |
| `decide() -> Generator[None, None, message]` | 入力待ちの間`yield`し、アクションが決まったら`return message`で返します。描画フレームごとにジェネレーターが進みます。 |
| `simulate(state, message) -> state \| None` | ゲームを1ステップ進めます。次状態を返すか、`None`を返して`initialize()`による再初期化を要求します。 |
| `render(previous, current) -> Generator[None, None, NoReturn]` | 2つの状態間のアニメーションを描き、1フレームごとに`yield`します。状態遷移ごとにジェネレーターが作り直されます。 |

`render`の実行中、`pyrein.elapsed`は現在の状態遷移が始まってからの経過秒数です。`pyrein.lerp(start, end, easing)`は`easing(pyrein.elapsed)`を使って数値を補間するため、位置などのアニメーションに利用できます。`pyrein.screen`はPygameの表示サーフェスです。

`pyrein.draw`には共有カメラを通して線・円を描くヘルパーがあります。`pyrein.draw.camera`ではワールド座標のオフセット、ズーム、アンカー位置を設定できます。`ease_out`などのイージング関数は`pyrein.easing`から利用できます。

## リポジトリ構成

```text
src/pyrein/
  __init__.py   メインループ、補間ヘルパー、draw名前空間の公開
  draw.py       カメラとPygameの線・円描画ヘルパー
  easing.py     clampおよびease-outイージング関数

examples/
  snake.py      pyreinで作ったキーボード操作のSnakeゲーム
  simple.py     最小限の移動・アニメーション例
  pygame_demo.py
                pyreinを使わない単独のPygameサンプル
  env.py        Gymnasium CartPoleとStable-Baselines3を使うPPO例
  type_test.py  ジェネリック型の小さな実験

cartpole_ppo.zip
                examples/env.pyが利用するCartPole PPOの保存モデル
```

## 便利さと現在の限界

小さなPygameゲームで「ゲーム状態は離散的に進めるが、見た目の移動は滑らかにしたい」という用途には、`simulate`と`render`の分離に`elapsed`、`lerp`、イージングを組み合わせる設計は分かりやすく、便利です。入力処理もゲームルールとは別の場所に置けます。

一方、現状は汎用ゲームエンジンやRLフレームワークというより、小さなプロトタイプです。ウィンドウサイズ・タイトル・FPS・終了キーはループ内で固定され、時間管理と画面初期化もループが担当します。描画APIは線と円のみです。エージェント学習が目的なら、Gymnasium連携と画面なしでステップ実行できる経路が大きな不足点です。人間が遊ぶデモを綺麗に見せる用途ならイージングを軸とした設計は土台になりますが、規模が大きくなるにつれてループや描画APIの設定自由度を増やす必要がありそうです。
