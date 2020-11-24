# Granblue Fantasy Poker Bot

This Python script automates Granblue Fantasy's poker minigame through the use of the PyAutoGUI module.

## Warning

Although it is unlikely that cheat detection will notice you using the bot as it only runs for 30 minutes and the mouse clicks occur in randomized parts of the screen, this bot is not recommended for use without at least some supervision.

## Getting Started

Use pip to install the [PyAutoGUI module](https://pyautogui.readthedocs.io/en/latest/) if you haven't done so already. You also must install the opencv module as well or the bot won't work.

```bash
pip install pyautogui
pip install opencv-contrib-python
```

## Usage

1. Before you start, make sure that Graphics is set to 'Lite' and that your Window Size in the game's Browser Settings tab is set to Large. Graphics must be set to 'Lite' otherwise the bot won't be able to detect the in-game buttons (as they glow/flash colors), but I'll make the bot work for more window sizes in the future.
2. Go to the in-game poker table and select 1000-chip bet and 2 CARDS higher-or-lower.
3. Ensure that the entire board is on screen at once before starting. You can get by with just the bottom portion of the scoreboard where it explains how much a hand with a Full House or Two Pairs is worth, but anything less than that and the bot won't be able to detect the gameboard. Furthermore, the DEAL button must on screen as well.
4. Run the bot:

```bash
python poker.py
```
5. On its own, the bot runs for 30 minutes, but you can end the bot prematurely by entering 'Ctrl+c' in the command line. Upon exiting, you'll be shown how many chips you've made this session.
