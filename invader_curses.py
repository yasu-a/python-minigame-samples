import collections
import curses
import itertools
import random
import time
from dataclasses import dataclass

import _curses
import numpy as np


@dataclass(frozen=False)
class Entity:
    name: str
    char: str
    pos: np.array

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return self.name == other.name and np.all(self.pos == other.pos)


class Timer:
    def __init__(self):
        self.__t = time.perf_counter()
        self.__count = -1

    def reset(self):
        self.__t = time.perf_counter()
        self.__count += 1

    def check(self, t):
        now = time.perf_counter()
        return now - self.__t >= t

    def elapsed(self, t):
        if self.check(t):
            self.reset()
            return True
        else:
            return False

    @property
    def count(self):
        return self.__count


FIELD_WIDTH = 41
ENEMY_HEIGHT_OFFSET = 3
ENEMY_HEIGHT = 20
ENEMY_MOVEMENT_GAP = 5
DEFENCE_HEIGHT_OFFSET = 2
DEFENCE_HEIGHT = 3


def main(stdscr: _curses.window):
    stdscr.nodelay(True)

    entities = []
    for x in range(FIELD_WIDTH):
        for y in range(ENEMY_HEIGHT_OFFSET, ENEMY_HEIGHT_OFFSET + 5):
            if 1 <= x < FIELD_WIDTH - 1 - ENEMY_MOVEMENT_GAP and x % 2 == 0:
                entities.append(Entity(name='enemy', char='O', pos=np.array([x, y])))
    for y in range(40):
        entities.append(Entity(name='wall', char='|', pos=np.array([FIELD_WIDTH, y])))
    for x in range(FIELD_WIDTH):
        for y in range(ENEMY_HEIGHT_OFFSET + ENEMY_HEIGHT + DEFENCE_HEIGHT_OFFSET,
                       ENEMY_HEIGHT_OFFSET + ENEMY_HEIGHT + DEFENCE_HEIGHT_OFFSET + DEFENCE_HEIGHT):
            if x % 5 not in (0, 1):
                entities.append(Entity(name='defence', char='W', pos=np.array([x, y])))

    me = Entity(name='me', char='M', pos=np.array([
        3,
        ENEMY_HEIGHT_OFFSET + ENEMY_HEIGHT + DEFENCE_HEIGHT_OFFSET + DEFENCE_HEIGHT + 2
    ]))
    entities.append(me)

    def iter_entity(name):
        for entity in entities:
            if entity.name == name:
                yield entity

    timer_enemy_motion = Timer()
    timer_beam_motion = Timer()
    timer_x_beam_hold = Timer()
    time_x_beam = Timer()
    timer_next_beam = Timer()
    timer_enemy_beam = Timer()

    while True:
        # key hit
        key = -1
        while True:
            ch = stdscr.getch()
            if ch == -1:
                break
            if ch >= 0:
                key = ch

        if key != -1:
            if key == ord('a'):
                me.pos[0] = max(0, me.pos[0] - 1)
            if key == ord('d'):
                me.pos[0] = min(FIELD_WIDTH - 1, me.pos[0] + 1)
            if key == ord(' ') and timer_next_beam.elapsed(0.2):
                entities.append(Entity(name='my-beam', char='|', pos=me.pos - (0, 1)))
                timer_next_beam.reset()
            if key == ord('x'):
                timer_x_beam_hold.reset()

        # game process
        if time_x_beam.elapsed(0.1) and not timer_x_beam_hold.check(
                5) and timer_x_beam_hold.count >= 0:
            beams = [
                Entity(name='my-beam', char='.', pos=me.pos - (dx, 1))
                for dx in (-3, -2, -1, 0, 1, 2, 3)
            ]
            for beam in beams:
                if 0 <= beam.pos[0] <= FIELD_WIDTH - 1:
                    entities.append(beam)

        if timer_enemy_motion.elapsed(1):
            cnt = timer_enemy_motion.count
            for entity in iter_entity('enemy'):
                x = cnt % 10
                if x == 0:
                    vel = 0, 1
                elif x < 5:
                    vel = +1, 0
                elif x == 5:
                    vel = 0, 1
                else:
                    vel = -1, 0
                entity.pos += vel

        remove_after = set()

        if timer_beam_motion.elapsed(0.1):
            for entity in iter_entity('my-beam'):
                entity.pos -= (0, 1)
                if entity.pos[1] < 0:
                    remove_after.add(entity)
            for entity in iter_entity('enemy-beam'):
                entity.pos += (0, 1)
                if entity.pos[1] > me.pos[1]:
                    remove_after.add(entity)

        if timer_enemy_beam.elapsed(1):
            top = {}
            for entity in iter_entity('enemy'):
                col_top = top.get(entity.pos[0])
                if col_top is None or col_top.pos[1] < entity.pos[1]:
                    top[entity.pos[0]] = entity
            if top:
                entity = random.choice(list(top.values()))
                entities.append(Entity(name='enemy-beam', char='V', pos=entity.pos + (0, 1)))

        # collision detection
        collision_dict = collections.defaultdict(lambda: collections.defaultdict(set))
        for entity in entities:
            collision_dict[tuple(entity.pos)][entity.name].add(entity)

        def iter_collide(name_1, name_2):
            for group in collision_dict.values():
                group_1, group_2 = group.get(name_1, set()), group.get(name_2, set())
                for a in group_1:
                    for b in group_2:
                        yield a, b

        for beam, defence in itertools.chain(iter_collide('enemy-beam', 'defence'),
                                             iter_collide('my-beam', 'defence'),
                                             iter_collide('my-beam', 'enemy'),
                                             iter_collide('my-beam', 'enemy-beam')):
            remove_after.add(beam)
            remove_after.add(defence)

        for entity in remove_after:
            entities.remove(entity)

        # update screen
        stdscr.clear()
        for entity in entities:
            stdscr.addch(int(entity.pos[1]), int(entity.pos[0]), entity.char)
        stdscr.addch(0, 0, ' ')
        stdscr.refresh()


curses.wrapper(main)
