# Lab 4: Vibe Coding – Dig Dug Repair Lab

**Student:** Rishyendra M (PES1UG24AM154) – Section C, AIML
**Assigned repository:** [SETAPESU26/29_digDug](https://github.com/SETAPESU26/29_digDug)
**AI assistant used:** Claude (Anthropic) – chat history in `PES1UG24AM154_Lab4_Chat_History.pdf`

## Tasks and commits (one commit per task)

| Task | Change | Commit message prefix |
|------|--------|-----------------------|
| Original code | `code/game.py` copied unchanged from the assigned repo | `Lab 4: add original Dig Dug game.py` |
| **Task 1 – Bug fix** | `bfs_path` used `queue.pop()` (LIFO → depth-first search). Changed to `queue.popleft()` (FIFO) so it is a real breadth-first search and enemies take the shortest tunnel route. | `Lab 4 Task 1` |
| **Task 2 – `dirt_color(row)`** | Four distinct soil strata (sand, orange, red-brown, purple) instead of a smooth gradient; sky row keeps default. | `Lab 4 Task 2` |
| **Task 3 – `on_enemy_popped(enemy, score)`** | 28-particle burst with gravity at the popped enemy plus a floating "+points (total)" pop-up; effects are updated and drawn every frame. | `Lab 4 Task 3` |
| **Task 4 – `enemy_speed_multiplier(level)`** | Level 1 = default speed; from level 2 enemies are `1 + 0.1 × level` faster, capped at 2×. | `Lab 4 Task 4` |

## Videos (10 seconds each)

| File | Shows |
|------|-------|
| `videos/before.mp4` | Original code. The yellow debug overlay draws each enemy's current route: routes are long and winding (41, 67, 75 steps) because the search is depth-first. Default smooth dirt gradient, no pop effect. |
| `videos/after.mp4` | Fixed code. Routes are straight and shortest (5, 7, 11 steps); enemies are pumped and pop with a particle burst and score pop-up; banded dirt colours; reaching Level 2 shows enemy speed ×1.2. |

The videos were recorded with `videos/record_gameplay.py`, which runs the game and drives the player with a simple bot. For a clear 10-second demo it pre-digs an open tunnel area, sets lives to 99 so the clip doesn't end early, and draws the route overlay. None of these demo settings are part of `game.py`.

## Contents

| Path | Description |
|------|-------------|
| `code/game.py` | Updated game (bug fixed + 3 features) |
| `code/README.md` | Original task README from the assigned repo |
| `videos/before.mp4`, `videos/after.mp4` | Gameplay videos before and after the changes |
| `PES1UG24AM154_Lab4_Chat_History.pdf` | Exported chat history with the AI assistant |
| `screenshots/` | Still frames from the videos |

## Run

```
pip install pygame
python code/game.py
```
Controls: arrow keys to dig/move, Space to pump, R to reset.
