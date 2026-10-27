# Lab 4: VibeCoding (Snake, repo `SETAPESU26/45_snake`)

## Contents

| Path | Deliverable |
|------|-------------|
| `videos/before.mp4` | (a) 10 s of gameplay on the original code. Pressing the opposite direction key kills the snake instantly, and the game then freezes with no game-over screen (it only prints to the console). |
| `videos/after.mp4` | (a) 10 s of gameplay after the changes. A reverse key press is ignored, a quick double tap makes a safe U-turn, the Game Over screen shows the final score and difficulty menu, and a replay starts on Hard. The eat and game-over sounds are in the audio. |
| `code/` | (b) The updated game code |
| `PES1UG24AM170_Lab4_Chat_History.pdf` | (c) The exported chat history with the AI assistant |

The videos were captured frame by frame from the running game (`main.py`). The caption bar under the game explains each moment and shows the key that was pressed.

## Run the game

```bash
cd code
pip install -r requirements.txt
python main.py
```

## Commits (one per task)

```
114601f  Initial Snake  starter
ceb9fc9  Task 1: Refine collision detection
3a63280  Fix food spawning on top of the snake
bfb15f5  Task 2: Implement Game Over screen
af8034d  Task 3: Add replay option with difficulty selection
42fe755  Task 4: Add sound feedback
227c452  Darken the game-over overlay so the menu stays readable
6dace4c  Document the changes and controls; stop tracking __pycache__
```

`code/README.md` has a table of what changed for each task and a list of the controls.
