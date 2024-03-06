# PythonMiniGames

授業用 Python CLI/curses/tkinter ミニゲームサンプル集 ＆ チュートリアル

# チュートリアル

> フォルダ：[docs](docs)

Pythonのインストール方法や実行のしかたなどの紹介

- [Pythonのインストール（Windows）](docs/how-to-install-python/doc.md)
- [コンソール上でのPythonスクリプトの実行（Windows）](docs/how-to-run-python-cli/doc.md)
- [PyCharmのインストール（Windows）](docs/how-to-install-pycharm/doc.md)
- [Visual Studio Code の紹介](docs/intro-vscode/doc.md)

# ミニゲームサンプル集

> [samples](samples)フォルダ

## コンソール上で動くミニゲーム

> フォルダ：[samples/cli](samples/cli)

- [シンプル samples/cli/simple](samples/cli/simple)

|                                  ファイル名                                  |   内容   |       レベル       |
|:-----------------------------------------------------------------------:|:------:|:---------------:|
|               [kazuate.py](samples/cli/simple/kazuate.py)               | 数あてゲーム |     基本的な文法      |
|   [answer_func_kazuate.py](samples/cli/simple/answer_func_kazuate.py)   | 数あてゲーム |       関数        |
| [practice_func_kazuate.py](samples/cli/simple/practice_func_kazuate.py) | 数あてゲーム | （数あてゲーム関数版の穴埋め） |
|                [keisan.py](samples/cli/simple/keisan.py)                | 計算クイズ  |       関数        |
|      [machigai_sagashi.py](samples/cli/simple/machigai_sagashi.py)      | 間違い探し  |       関数        |

- [複雑 samples/cli/hard](samples/cli/hard)

|                             ファイル名                             |  内容   |           レベル           |
|:-------------------------------------------------------------:|:-----:|:-----------------------:|
| [minimax_marubatsu.py](samples/cli/hard/minimax_marubatsu.py) | 〇×ゲーム |    オブジェクト指向・ミニマックス法     |
|    [minimax_sevens.py](samples/cli/hard/minimax_sevens.py)    |  七並べ  | 少しだけオブジェクト指向・関数・ミニマックス法 |

## cursesによるコンソール上で動くグラフィクスゲーム

> フォルダ：[samples/curses](samples/curses)

[cursesライブラリ](https://docs.python.org/ja/3.12/howto/curses.html)は、
文字が上から下にしか流れなかったコンソールに、任意の位置に文字を表示する革命を起こすライブラリ。

|                  ファイル名                  |       内容       |   レベル    |
|:---------------------------------------:|:--------------:|:--------:|
| [invader.py](samples/curses/invader.py) | インベーダーゲーム（調整中） | オブジェクト指向 |
