"""
数学の関数：xが決まるとyが決まる対応関係

 ↓ xとyはたくさんあってもいいし，xがない関数やyがない関数，xもyもどちらもない関数があってもいい

プログラミングの関数：作業をまとめたもの，入力を受け取って作業をするもの，作業して出力だけ返すもの・・・

----

ひとまとまりの作業をする「人」だと思えばいい

「引数」：関数が作業するための材料
「呼び出し」：はたらけ！と命令する→働き始める→作業が終わる
「戻り値」：関数が作業した結果を呼び出した側に返してくれる

副作用付き関数：関数への入力は引数とは限らない

----
関数の使い方

関数名()
関数名(引数1, 引数2, ...)

戻り値を受け取る変数 = 関数名()
戻り値を受け取る変数 = 関数名(引数1, 引数2, ...)

トリック：
print(関数名(引数1, 引数2, ...))

x = 関数名(引数1, 引数2, ...)
print(x)

range(10)
list(range(10))


関数の作り方
def 関数名():
    関数の外で書いていたようにふつうに処理を書く
    ...
    return 値　←値を返して処理を終了する

def 関数名(引数1, 引数2, ...):
    処理
    ...


"""

# no inputs, no outputs
# 作業をまとめたもの
# ランダムなメッセージを出力する

import random


def print_random_message():
    r = random.randint(0, 2)
    if r == 0:
        print('おはよ！')
    elif r == 1:
        print('こんにちは！')
    else:
        print('こんばんは！')


for _ in range(10):
    print_random_message()


# single input, single output
# 中学数学で習う関数
# 計算とか？

def f(x):
    return x ** 2


print(f'f(1)={f(1)}')
print(f'f(2)={f(2)}')
print(f'f(3)={f(3)}')


# single input, no outputs
# 作業だけする関数

def say_hello_to(name):
    print(f'ハロー！{name}さん')


your_name = input('あなたの名前は？ > ')
say_hello_to(your_name)

# x 数あてゲーム
#   じゃんけん
#   ゆびすま
#   間違い探し
#   タイピングゲーム
#   計算ゲーム
