# 素数シューティングゲーム

import random
import time
import tkinter
from dataclasses import dataclass

import numpy as np

PRIMES = 2, 3, 5, 7


@dataclass
class Number:
    value: int
    factors: tuple[int, ...]

    @classmethod
    def from_factors(cls, factors: list[int] | tuple[int]):
        assert factors

        n = 1
        for f in factors:
            n *= f

        return Number(value=n, factors=tuple(factors))

    @classmethod
    def compose_random_number(cls):
        factors = []
        for _ in range(random.randint(4, 10 + 1)):
            factors.append(random.choice(PRIMES))
        return Number.from_factors(factors)

    def decompose(self):
        if len(self.factors) == 1:
            return None
        else:
            i = len(self.factors) // 2
            factor_1 = Number.from_factors(self.factors[:i])
            factor_2 = Number.from_factors(self.factors[i:])
            return factor_1, factor_2


root = tkinter.Tk()
root.resizable(width=False, height=False)
root.geometry("300x800")

cvs = tkinter.Canvas(root)
cvs.pack(fill="both", expand=True)


def get_mouse_pos():
    # https://stackoverflow.com/questions/22925599/mouse-position-python-tkinter
    abs_coord_x = root.winfo_pointerx() - root.winfo_rootx()
    abs_coord_y = root.winfo_pointery() - root.winfo_rooty()
    return np.array([abs_coord_x, abs_coord_y]).astype(float)


@dataclass
class Enemy:
    n: Number
    pos: np.ndarray


enemies: list[Enemy] = []

ENEMY_SIDE_MARGIN = 20
N_ENEMY_SPAWN_LIMIT = 80


def spawn_enemy(n=None, pos=None):
    if len(enemies) >= N_ENEMY_SPAWN_LIMIT:
        return

    if n is None:
        n = Number.compose_random_number()
    if pos is None:
        w = root.winfo_width()
        pos = np.array([random.randint(ENEMY_SIDE_MARGIN, w - ENEMY_SIDE_MARGIN), -30]).astype(
            float)
    e = Enemy(n=n, pos=pos)
    enemies.append(e)


beams_pos: list[np.ndarray] = []

FPS = 40
ENEMY_VELOCITY_BASE = 30 / FPS
BEAM_VELOCITY = 200 / FPS
COLLISION_RADIUS = 15
ENEMY_SCATTER_RADIUS = 10
BEAM_HOLD = 0.01
BEAM_MARGIN = 10
DIFFUSION_GRAVITY_FACTOR = 20000
DIFFUSE_PROCESS_RADIUS_LIMIT = 100

mb_flag = False
t_prev_beam_spawned = 0


def main():
    ts = time.time()

    w, h = root.winfo_width(), root.winfo_height()

    # Spawn beams
    global t_prev_beam_spawned
    if mb_flag and time.time() - t_prev_beam_spawned >= BEAM_HOLD:
        m_pos = get_mouse_pos()
        beams_pos.append(np.array([m_pos[0], h - BEAM_MARGIN]))
        t_prev_beam_spawned = time.time()

    # Spawn enemies
    if random.random() < 0.03:
        spawn_enemy()

    # Move enemies
    for e in enemies:
        v = ENEMY_VELOCITY_BASE
        e.pos[1] += v

    # Move beams
    for i in range(len(beams_pos)):
        beams_pos[i] = beams_pos[i] + [0, -BEAM_VELOCITY]

    # Process collisions
    col_beams = set()
    col_enemies = set()
    for bi, b_pos in enumerate(beams_pos):
        for ei, e in enumerate(enemies):
            e_pos = e.pos
            if np.linalg.norm(e_pos - b_pos) <= COLLISION_RADIUS:
                col_beams.add(bi)
                col_enemies.add(ei)

    # for ei, e in enumerate(enemies):
    #     if len(e.n.factors) >= 2 and random.random() * FPS < 0.3:
    #         col_enemies.add(ei)  # Enemy auto boom

    for ei, e in enumerate(enemies):
        if e.pos[1] > h + 50:
            col_enemies.add(ei)  # Delete entities

    for bi, b_pos in enumerate(beams_pos):
        if b_pos[1] < 0 - 50:
            col_beams.add(bi)  # Delete beams

    for bi, b_pos in reversed(list(enumerate(beams_pos))):
        if bi in col_beams:
            beams_pos.pop(bi)

    for ei, e in reversed(list(enumerate(enemies))):
        if ei in col_enemies:
            enemies.pop(ei)
            shot_result = e.n.decompose()
            if shot_result is not None:
                for n, dx in zip(shot_result, [-ENEMY_SCATTER_RADIUS, +ENEMY_SCATTER_RADIUS]):
                    e_pos = e.pos + [dx, 0]
                    spawn_enemy(n=n, pos=e_pos)

    # Diffuse Enemy
    for e in enemies:
        force = 0
        for ee in enemies:
            if e is ee:
                continue
            if np.all(e.pos - ee.pos > DIFFUSE_PROCESS_RADIUS_LIMIT):
                continue
            r = e.pos - ee.pos
            norm_r = np.linalg.norm(r) + 1e-6
            force += 1 / norm_r ** 3 * r
        v = force / FPS * DIFFUSION_GRAVITY_FACTOR
        v_norm = np.linalg.norm(v) + 1e-6
        v = min(v_norm, ENEMY_VELOCITY_BASE * 6) * v / v_norm
        e.pos += v

    # Wall Correction
    for e in enemies:
        e.pos[0] = np.clip(e.pos[0], ENEMY_SIDE_MARGIN, w - ENEMY_SIDE_MARGIN)

    cvs.delete("all")

    # Render enemies
    for e in enemies:
        cvs.create_text(*e.pos, text=str(e.n.value), font=("Consolas", 10), fill="Black")

    # Render beams
    for b_pos in beams_pos:
        cvs.create_text(*b_pos, text="|", font=("Consolas", 10), fill="Black")

    te = time.time()
    cvs.create_text(
        0, h,
        text=f"PPS:{1 / (te - ts + 1e-6):5.0f}, NB:{len(beams_pos):4}, NE:{len(enemies):4}",
        font=("Consolas", 10),
        fill="Black",
        anchor="sw"
    )
    root.after(max(1, int((1 / FPS - (te - ts)) * 1000)), main)


def mouse_pressed(evt: tkinter.Event):
    global mb_flag
    mb_flag = True


def mouse_released(evt: tkinter.Event):
    global mb_flag
    mb_flag = False


root.bind("<ButtonPress-1>", mouse_pressed)
root.bind("<ButtonRelease-1>", mouse_released)

root.after(100, main)
root.mainloop()
