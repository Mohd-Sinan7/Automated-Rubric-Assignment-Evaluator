# Missile Command Repair Lab

A small **Missile Command-lite** game built with Python and Pygame. The player protects six cities by launching interceptors at incoming missiles. The project demonstrates click-to-target movement, distance-based collision detection, explosions, scoring, limited ammunition, and waves of enemies.

The four repair-lab tasks are implemented in `game.py`:

1. Battery selection skips destroyed batteries and batteries with no ammunition.
2. Explosions change colour during their lifetime.
3. The game prints a warning when only two cities remain and a critical warning when only one remains.
4. Destroyed cities can be repaired when the score reaches each 2,000-point threshold.

## Requirements

- Python 3.10 or newer
- Pygame
- Git (only needed if you clone the project from GitHub)

## Setup and Run on Windows

### Option A: Clone the repository

Open **Command Prompt** or the VS Code terminal and run each command separately:

```cmd
git clone https://github.com/SETAPESU26/33_missileCommand.git
cd 33_missileCommand
python -m pip install pygame
python game.py
```

If `git` is not recognized, install [Git for Windows](https://git-scm.com/download/win) first. If `python` is not recognized, install Python from [python.org](https://www.python.org/downloads/windows/) and enable **Add python.exe to PATH** in the installer.

### Option B: Run files you downloaded manually

Put `game.py` and `README.md` in the same folder. Open Command Prompt in that folder and run:

```cmd
python -m pip install pygame
python game.py
```

If the game file is named `game_fixed.py`, rename it to `game.py` or run `python game_fixed.py` instead.

## Controls

- **Left-click** above the ground to launch an interceptor toward that point.
- **R** resets the game.
- Close the game window to exit.

The game window shows the score, current wave, and battery ammunition. City-destruction warnings are printed in the terminal where the game was started.

## Implemented Tasks

### Task 1: Fix battery selection

`nearest_battery(target)` now considers only batteries that are alive and have ammunition, then chooses the closest available one. If no battery is available, the click does not launch an interceptor.

**How to test:** Use all ammunition from the closest battery, then click near it again. A different living battery with ammunition should fire instead.

### Task 2: Implement `explosion_color(progress)`

`explosion_color(progress)` clamps the progress value to the range `0.0` through `1.0` and returns an RGB colour. The explosion begins orange-red, becomes bright and white-hot around the middle of its lifetime, then fades toward dark red.

**How to test:** Launch interceptors and watch their explosions change colour as they grow and shrink.

### Task 3: Implement `on_city_destroyed(city)`

When a missile destroys a city, `on_city_destroyed(city)` updates the remaining-city count. It prints a warning in the terminal when two cities remain and a critical warning when only one remains. It is called only when a standing city is destroyed, not when an already-destroyed city or a battery is hit.

**How to test:** Let missiles destroy cities and watch the terminal output when the count falls to two and then one.

### Task 4: Implement `city_repair_threshold()`

`city_repair_threshold()` returns `2000`. When the score reaches a new 2,000-point threshold, the game rebuilds one destroyed city if any are available to repair. The repair count is tracked so the same threshold is not awarded repeatedly.

**How to test:** Continue playing until the score reaches 2,000 points or a later multiple of 2,000 while at least one city is destroyed. A destroyed city should be rebuilt.

## Expected Behaviour

- A click launches an interceptor from the nearest living battery that has ammunition.
- Interceptors travel toward the selected target and detonate on arrival.
- Explosions destroy incoming missiles whose positions enter the blast radius.
- Missiles that reach their targets destroy the target if it is still standing/alive.
- Terminal warnings appear as the number of surviving cities gets dangerously low.
- Destroyed cities can be repaired at score thresholds of 2,000 points.
- The game ends when no cities remain alive. Press **R** to reset.

## Folder Structure

```text
33_missileCommand/
├── game.py
└── README.md
```

## Submission Checklist

- [ ] Record a 10-second gameplay video **before** the fixes, showing the original battery-selection bug or other broken behaviour.
- [ ] Record a 10-second gameplay video **after** the fixes, showing the corrected battery selection and the new features.
- [ ] Include the ChatGPT/LLM conversation link with the complete chat history, as required by the lab.

## Note

This README describes the implemented version of the project. Review the code and test each task yourself before submitting your lab work.
