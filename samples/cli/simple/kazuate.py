# 数あてゲーム

import random

r = random.randint(1, 100)
count = 0
while True:
    try:
        i = int(input(f"1から100までの数字を当ててください（{count + 1}回目） ?> "))
    except ValueError:
        print("数字を入力してね")
        continue
    else:
        if not (1 <= i <= 100):
            print("1から100までの数字だよ")
            continue
    count += 1
    if i > r:
        print("正解はもっと小さい！")
    elif i < r:
        print("正解はもっと大きい！")
    else:
        break
print(f"正解！{count}回で成功！")
