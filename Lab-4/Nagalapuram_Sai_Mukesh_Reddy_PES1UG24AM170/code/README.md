# Snake Game

This project is a terminal-based Snake game using **Pygame**. It introduces students to interactive game design using object-oriented principles and real-time graphical rendering.

---

## What’s Provided

A partially working version of a snake game with:

- Grid-based snake movement controlled by the player
- Food spawning and snake growth
- Score display

You are expected to **analyze**, **interact with an AI assistant**, and **complete/fix** the game to make it fully functional.

### **Use an LLM (e.g. ChatGPT or Claude) as your debugging and pair-programming partner for this lab.**

---

## Getting Started

### Setup

1. Clone the repo or download the project folder.
2. Make sure you have Python 3.10+ installed.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the game:

```bash
python main.py
```

---


## Tasks to Complete

Each task must be completed using an iterative process involving LLM suggestions and your critical code review.

### Task 1: Refine Collision Detection

> The snake can die instantly and unfairly if you tap the opposite direction key while moving (e.g. pressing Left while already moving Right), because the new head moves straight into the segment behind it. Investigate and enhance collision accuracy so direction changes and self/wall collisions behave fairly.


### Task 2: Implement Game Over Condition

> Add a screen that displays the final score once the snake hits a wall or itself, then gracefully waits for input instead of just printing to the console.


### Task 3: Add Replay Option

> After Game Over, allow the user to play again by choosing a difficulty (Easy, Medium, or Hard speed), or exit.



### Task 4: Add Sound Feedback

> Add basic sound effects for eating food and for the game-over moment.


---

## Changes Made

| Task | What changed | Where |
|------|--------------|-------|
| 1. Collision detection | Reversing into the body is ignored. Turns are checked against the last *queued* turn, so two quick presses between moves (e.g. Up then Left while moving Right) can't sneak in a reversal; up to two turns are buffered so quick taps aren't lost. Wall/self collisions are checked on the cell the head is about to enter, so the snake stays on screen where it crashed, and the cell the tail is leaving counts as free (unless growing). | `game/snake.py`, `game/game_engine.py` |
| Bug fix | The first food could spawn on top of the snake. Food now picks from free cells only. | `game/food.py` |
| 2. Game Over | An in-game Game Over screen with the final score replaces the console `print`; the game waits for input. | `game/game_engine.py` |
| 3. Replay | The Game Over screen offers Easy / Medium / Hard (5 / 8 / 12 moves per second) or Exit. The current difficulty is shown top-right. | `game/game_engine.py` |
| 4. Sound | A blip when food is eaten and a descending tune at Game Over, synthesised in code (no audio files). The game stays silent instead of crashing if there is no audio device. | `game/sound.py` |

### Controls

| Key | Action |
|-----|--------|
| Arrow keys / `WASD` | Steer the snake |
| Up/Down (or `W`/`S`) + `Enter` | Pick an option on the Game Over screen |
| `1` / `2` / `3` | Replay on Easy / Medium / Hard |
| `Q` / `Esc` | Exit from the Game Over screen |

---

## Expected Behavior

- Smooth, grid-based snake movement using arrow keys or `WASD`
- Snake grows by one segment each time it eats food
- Food never spawns on top of the snake
- Score updates as food is eaten
- Game ends (and optionally restarts) when the snake hits a wall or itself

---

## Folder Structure

```
snake-main/
├── main.py
├── requirements.txt
├── game/
│   ├── game_engine.py
│   ├── snake.py
│   ├── food.py
│   └── sound.py
└── README.md
```

---

## Submission Checklist

Submission is only the following three things:

- [] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [] The Chat/LLM used page link, with the complete chat history
