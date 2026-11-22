"""Record a ~10 s gameplay video of the Dig Dug game headlessly.

Usage: python record_digdug.py path/to/game.py out.mp4 label
A simple bot plays: it waits in an open tunnel arena, turns toward enemies and
pumps them. A debug overlay draws each enemy's current BFS route so the
pathfinding behaviour is visible in the video.
"""
import importlib.util
import os
import collections
import random
import sys

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"
import imageio.v2 as imageio  # noqa: E402
import numpy as np  # noqa: E402
import pygame  # noqa: E402

game_path, out, label = sys.argv[1], sys.argv[2], sys.argv[3]
spec = importlib.util.spec_from_file_location("game", game_path)
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

random.seed(7)
pygame.init()
screen = pygame.display.set_mode((g.WIDTH, g.HEIGHT))
game = g.Game()
game.lives = 99  # keep the demo running for the full 10 s

# Open tunnel arena (as if the player had already dug it) so routes are visible.
for r in range(1, 11):
    for c in range(2, 18):
        game.grid[r][c] = False
game.player = (1, 10)
game.dig(game.player)
for e in game.enemies:
    e.ghost_timer = 30  # keep enemies in tunnel (BFS) mode for the demo

FPS, SECONDS = 30, 10
font = pygame.font.Font(None, 22)
frames = []
pump_cd = 0.0
for i in range(FPS * SECONDS):
    dt = 1 / FPS
    # --- bot: face an aligned enemy and pump it -------------------------
    pump_cd -= dt
    pr, pc = game.player
    for e in game.enemies:
        er, ec = e.cell
        if er == pr and abs(ec - pc) <= g.PUMP_RANGE and ec != pc:
            game.facing = (0, 1 if ec > pc else -1)
        elif ec == pc and abs(er - pr) <= g.PUMP_RANGE and er != pr:
            game.facing = (1 if er > pr else -1, 0)
    keys = collections.defaultdict(bool)
    if pump_cd <= 0 and game.find_pump_target() is not None:
        game.pump()
        pump_cd = 0.15
    elif game.enemies and all(not g.bfs_path(game.grid, e.cell, game.player)
                              for e in game.enemies if not e.locked):
        # nobody can reach us: dig toward the nearest enemy
        tr, tc = min((e.cell for e in game.enemies),
                     key=lambda c: abs(c[0] - pr) + abs(c[1] - pc))
        if abs(tc - pc) > 0 and not (tr == pr and abs(tc - pc) <= 2):
            keys[pygame.K_RIGHT if tc > pc else pygame.K_LEFT] = True
        elif abs(tr - pr) > 1:
            keys[pygame.K_DOWN if tr > pr else pygame.K_UP] = True
    game.update(dt, keys)
    game.draw(screen)
    # --- debug overlay: each enemy's current route ----------------------
    for e in game.enemies:
        if e.locked or e.ghost:
            continue
        path = g.bfs_path(game.grid, e.cell, game.player)
        pts = [(c * g.TILE + g.TILE // 2, r * g.TILE + g.TILE // 2) for r, c in [e.cell] + path]
        if len(pts) > 1:
            pygame.draw.lines(screen, (255, 210, 0), False, pts, 2)
        txt = font.render(str(len(path)), True, (255, 255, 0))
        screen.blit(txt, (pts[0][0] + 10, pts[0][1] - 18))
    mult = g.enemy_speed_multiplier(game.level) or 1
    banner = font.render(f"{label}   |   yellow = enemy route (steps)   |   enemy speed x{mult:.1f}",
                         True, (255, 255, 255), (0, 0, 0))
    screen.blit(banner, (6, 4))
    frames.append(np.transpose(pygame.surfarray.array3d(screen), (1, 0, 2)).copy())

imageio.mimsave(out, frames, fps=FPS, codec="libx264", quality=8, macro_block_size=8)
imageio.imwrite(out.replace(".mp4", "_frame.png"), frames[FPS * 4])
print("saved", out, len(frames), "frames; score", game.score, "level", game.level)
