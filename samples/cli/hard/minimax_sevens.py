# ミニマックス法を使った七並べ

import copy
import random
import time
import typing

from tqdm import tqdm

STR_SUIT = '♦♥♧♤'
STR_NUMBER = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']


class Card(typing.NamedTuple):
    suit: int
    number: int

    @classmethod
    def list_cards(cls):
        lst = []
        for suit in range(4):
            for number in range(13):
                lst.append(cls(suit, number))
        return lst

    def __repr__(self):
        return f'[{STR_SUIT[self.suit]}{STR_NUMBER[self.number]:>2}]'


def distribute_cards(player_hands):
    cards = Card.list_cards()
    random.shuffle(cards)

    while cards:
        for i in range(len(player_hands)):
            card = cards.pop(0)
            player_hands[i].append(card)


def pop_seven(player_hands):
    for i in range(len(player_hands)):
        new_player_hand = []
        for card in player_hands[i]:
            if not STR_NUMBER[card.number] == '7':
                new_player_hand.append(card)
        player_hands[i] = new_player_hand


def print_field(field):
    for suit in range(len(field)):
        for number in range(len(field[suit])):
            if field[suit][number]:
                print(Card(suit, number), end=' ')
            else:
                print('_____', end=' ')
        print()


def valid_action(field):
    valid_cards = []
    for suit in range(len(field)):
        row = field[suit]
        for number in range(len(row)):
            if row[(number + 1) % len(row)] or row[(number + len(row) - 1) % len(row)]:
                valid_cards.append(Card(suit, number))
    return valid_cards


def print_hand(player_hand, target_cards):
    line = [(0, 'PASS')]
    i = 1
    for card in player_hand:
        if card in target_cards:
            line.append((i, card))
            i += 1
        else:
            line.append((None, card))

    print(' |', ' '.join(f'{elm[1]!s:5}' for elm in line))
    print(' |', ' '.join(' ' * 5 if elm[0] is None else '^^^^^' for elm in line))
    print(' |', ' '.join(' ' * 5 if elm[0] is None else f'{elm[0]:^5}' for elm in line))


def prompt_action(target_cards):
    while True:
        try:
            k = int(input(' | Your action ?> '))
            if k == 0:
                return None
            card = target_cards[k - 1]
        except (IndexError, ValueError):
            print(' | Invalid input')
        else:
            break
    return card


def player_action(field, my_hand):
    my_hand.sort()
    target_cards = sorted(set(my_hand) & set(valid_action(field)))
    print_hand(my_hand, target_cards)
    card = prompt_action(target_cards)
    if card is None:
        return None
    my_hand.remove(card)
    field[card.suit][card.number] = True
    return card


FULL_CARD_SET = frozenset(Card.list_cards())


def get_hidden_cards(field):
    return frozenset(
        Card(suit, number)
        for suit in range(4)
        for number in range(13)
        if not field[suit][number]
    )


def evaluate(me, field, my_hand, depth) -> int:
    valid_cards = set(valid_action(field))
    invalid_cards = FULL_CARD_SET - valid_cards
    hidden_cards = get_hidden_cards(field)

    valid_cards_for_me = my_hand & valid_cards
    invalid_cards_for_others = (hidden_cards - my_hand) & invalid_cards

    if my_hand:
        score = len(valid_cards_for_me) + len(invalid_cards_for_others) * 3 - depth
        if not me:
            score = -score
        return score
    else:
        return 999 - depth


def choice(a, size):
    idx = list(range(len(a)))
    random.shuffle(idx)
    return [list(a)[i] for i in idx[:size]]


def best_action(who, my_player_id, n_players, field, my_hand: frozenset, depth=None) \
        -> tuple[Card | None, int]:
    depth = depth or 0

    if game_over(field) or depth == n_players * 2:
        return None, evaluate(who == my_player_id, field, my_hand, depth)
    else:
        best_card, best_score = None, -99999
        if who == my_player_id:
            it = set(valid_action(field)) & my_hand
            if depth == 0:
                it = tqdm(it)
            for card in it:
                new_field = copy.deepcopy(field)
                new_field[card.suit][card.number] = True
                _, score = best_action(
                    (who + 1) % n_players,
                    my_player_id,
                    n_players,
                    new_field,
                    my_hand - {card},
                    depth + 1
                )
                if best_score < score:
                    best_card, best_score = card, score
        else:
            for card in choice(get_hidden_cards(field) & set(valid_action(field)), size=3):
                new_field = copy.deepcopy(field)
                new_field[card.suit][card.number] = True
                _, score = best_action(
                    (who + 1) % n_players,
                    my_player_id,
                    n_players,
                    new_field,
                    my_hand,
                    depth + 1
                )
                if best_score < score:
                    best_card, best_score = card, score
        return best_card, best_score


def com_action(player_id, n_players, field, my_hand):
    card, _ = best_action(player_id, player_id, n_players, field, frozenset(my_hand))

    if card is None:
        return None
    else:
        my_hand.remove(card)
        field[card.suit][card.number] = True
        return card


def game_over(field):
    for suit in range(4):
        for number in range(13):
            if not field[suit][number]:
                return False
    return True


def print_hand_stat(player_hands, your_id):
    for player_id in range(len(player_hands)):
        print(
            f'P{player_id + 1}',
            '[]' * len(player_hands[player_id]),
            '<- YOU!' if player_id == your_id else ''
        )


def main():
    n_players = 4
    your_id = 0
    player_hands = [[] for _ in range(n_players)]
    distribute_cards(player_hands)

    pop_seven(player_hands)

    field = [[STR_NUMBER[j] == '7' for j in range(13)] for _ in range(4)]
    print_field(field)
    print_hand_stat(player_hands, your_id)

    wins = []

    while not game_over(field):
        for player_id in range(n_players):
            if player_hands[player_id]:
                print(' ***', 'Player', player_id + 1, '***')
                if player_id == your_id:
                    _ = player_action(field, player_hands[player_id])
                    print_field(field)
                    print_hand_stat(player_hands, your_id)
                else:
                    print(' | Thinking ... ', end='')
                    card = com_action(player_id, n_players, field, player_hands[player_id])
                    print(card or 'PASS')
                    print_field(field)
                    print_hand_stat(player_hands, your_id)
                    time.sleep(1)

                if not player_hands[player_id]:
                    wins.append(player_id)

                print()

    print(' ===== RESULT =====')
    for i, player_id in enumerate(wins):
        print(i + 1, f'P{player_id + 1}', '<- YOU!' if player_id == your_id else '')


if __name__ == '__main__':
    main()
