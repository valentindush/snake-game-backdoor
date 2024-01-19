# SNAKE GAME BACKDOOR

### How it works

When the program is runned. the game is launched normaly and the backdoor is also runned in a different thread in the background.

### The backdoor

The backdoor uses `netcat` to connect to the specified host, so that we can access the victim's PC using reverse sheell

the backdoor will run in the background even when the victim quits the game.

it will also run on statup everytimee

### How to run

* On **Windows** run `snakeGame.exe`
* On **linux** and **Mac Os** run `main.py`
