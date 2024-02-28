def create_random_number():
    """
    コンピュータが考えたランダムな数字を作って返す

    引数：（なし）
    戻り値：
     - ランダムな数字
    """
    raise NotImplementedError()


def get_player_input(count):
    """
    プレイヤーに入力を促すメッセージを表示して、プレイヤーの入力を受け取る。
    変な入力を受け取ったらもう一度入力させる

    引数：
     - count：現在のループカウント（メッセージの表示に使える）。ただし、ここで受け取るループカウントは0が1回目を表す。
    戻り値
     - プレイヤーが入力した正しい数字
    """
    raise NotImplementedError()


def check_answer_and_show_message(r, i, count):
    """
    コンピュータの考えた数字とプレイヤーの入力した数字を受け取って、その結果を処理し、
    その結果ゲームが終わるならTrue、続くならFalseを返す。
    例えば、プレイヤーの入力が間違いならヒントを表示してFalseを返す。あっていれば正解のメッセージを表示してTrueを返す。

    引数：
     - r：コンピュータが考えたランダムな数字
     - i：プレイヤーが考えて入力した数字
     - count: 現在のループカウント（メッセージの表示に使える）
    戻り値：
     - ゲーム（ループ）が終わるならTrue、ゲームが続くならFalse
    """
    raise NotImplementedError()


def main():
    # ランダムな数字を作る
    r = create_random_number()
    # カウントを初期化する
    count = 0
    # ゲームのメインループ
    while True:
        # プレイヤーに数字を入力してもらう
        i = get_player_input(count)
        # ループカウントを1足す
        count += 1
        # 入力を判定してゲーム終了かどうかを受け取る
        success = check_answer_and_show_message(r, i, count)
        # ゲーム終了ならゲームを終わる
        if success:
            break


if __name__ == '__main__':
    main()
