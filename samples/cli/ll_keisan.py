import math
import random
import time


def get_random_operator():
    return random.choice("+-×÷")


def get_random_operands():
    return random.randint(1, 30), random.randint(1, 30)


def calc_answer(x, op, y):
    if op == '+':
        return x + y
    elif op == '-':
        return x - y
    elif op == '×':
        return x * y
    elif op == '÷':
        return x / y
    else:
        assert False, "定義されてない計算だよ！"


def create_quiz_and_answer():
    op = get_random_operator()
    while True:
        x, y = get_random_operands()
        try:
            ans = calc_answer(x, op, y)
        except ZeroDivisionError:
            continue
        else:
            if math.modf(ans)[0] != 0:
                continue
            ans = int(ans)
            if ans > 100:
                continue
            if ans < 0:
                continue
        return x, op, y, ans


def quiz_to_string(x, op, y):
    return f"{x}{op}{y}"


def get_input():
    while True:
        try:
            player_answer = int(input(' ?> '))
        except ValueError:
            print("数字を入力してね")
            return None
        return player_answer


def main():
    n_quiz = 10
    time_start = time.time()
    for i in range(n_quiz):
        x, op, y, ans = create_quiz_and_answer()
        quiz_string = quiz_to_string(x, op, y)
        print(f"[Q.{i + 1}/{n_quiz}] {quiz_string}")
        while True:
            player_answer = get_input()
            if ans == player_answer:
                print("正解！")
                break
            else:
                print("ちがうよ")
    time_end = time.time()
    time_elapsed = time_end - time_start
    print(f"終わり！記録：{time_elapsed:.2f}秒")


if __name__ == '__main__':
    main()
