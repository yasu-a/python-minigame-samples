import copy
import random
import time

CHAR_SET = 'QO'  # random_char()で使う文字セット


def random_char(forbid=None):
    """
    CHAR_SETに含まれている文字をランダムに返す。ただし，forbidに含まれる文字は選ばない。
    なお，forbidがNoneのときはCHAR_SETの文字すべてがランダムに選ばれる。

    :param forbid: 選ばない禁止文字
    :return: CHAR_SETに含まれforbidには含まれないランダムに選ばれた文字
    """

    while True:
        ch = random.choice(CHAR_SET)
        if forbid is not None and ch in forbid:
            continue
        break
    return ch


def create_image(width, height):
    """
    間違い探しに使う画像データを作る。
    画像データのサイズが 横width x 縦height で，画像を構成する文字はrandom_char()で選ばれるが使われる。

    :param width: 画像の横サイズ
    :param height: 画像の縦サイズ
    :return: 生成した画像データ
    """

    rows = []
    for i in range(height):
        row = []
        for j in range(width):
            row.append(random_char())
        rows.append(row)
    return rows


def show_images(left, right):
    """
    与えられた2枚の画像 left, right を並べて表示する。ついでに left のマスの座標も表示する。

    :param left: 表示する2枚の画像のうち，左側の画像データ
    :param right: 表示する2枚の画像のうち，右側の画像データ
    """

    width, height = len(left[0]), len(left)
    print(' ', ' ' * width, ''.join(map(str, range(width))))
    for i in range(height):
        print(i, ''.join(left[i]), ''.join(right[i]))


def random_replace(image):
    """
    与えられた画像データ image のうち1マスを CHAR_SET の新しい文字に置き換え，
    置き換えをした画像データと置き換えた位置を返す

    :param image: 置き換えをする前のもとにする画像
    :return: 3つの値：置き換え後の画像，縦に見てどこを置き換えたか，横に見てどこを置き換えたか
    """

    image = copy.deepcopy(image)
    width, height = len(image[0]), len(image)
    i = random.randint(0, height - 1)
    j = random.randint(0, width - 1)
    image[i][j] = random_char(forbid=image[i][j])
    return image, i, j


# 正解画像を作る
img1 = create_image(7, 7)
# 間違い画像を作り，間違いの位置(i, j)も取得する
img2, i, j = random_replace(img1)
# 2枚の画像を表示する
show_images(img1, img2)

# 時間を計る；開始時刻を取得する
time_start = time.time()
# ゲームループ
while True:
    try:
        # 入力を促し，入力された数字を整数に変換
        ans_j, ans_i = map(int, input('yoko tate ?> '))
    except ValueError:
        # 数字以外が入力される or 入力が2つじゃない：ValueErrorが起きるのでエラーで止まらないように捕捉する
        continue  # ゲームループの最初に戻る

    if ans_i == i and ans_j == j:  # もし指摘された間違いの位置が正しかったら
        break  # ゲームループ終了
    else:  # 指摘された間違いの位置がちがかったら
        print('ちがうよ！')
# 時間を計る；終了時刻を取得する
time_end = time.time()

# お祝いのメッセージと計った時間を表示する
print('正解！ 記録', round(time_end - time_start, 2), '秒')
