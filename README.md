# DreamNAP

A python based emulator for the NAPBOY handheld gaming system.

## Features

- Menu system to run programs
- Sprite based font rendering
- Game state space saving
- Game asset 

## Game/Program API Calls

- `canvas.blit(asset_id,x,y)`
- `led.show([led_color])`
- `led.fill(color)`

- `game.step()`
-  At each game step call, the game will be given a array of button presses and gyro data

## OS API Calls

- `driver.set_audio()`
- `os.load_sprite_pallete`
- `driver.set_background_color`


## Driver API Calls

- `driver.set_pallete([Array of RGB Color object])`
- `driver.set_background_color`
- `[driver api for file writing]`

## Todos
- [x] Add graphics to menu
- [x] Add support for text rendering
- [x] return to home on home button
- [ ] Write aliens game
- [x] Support for high score state 
- [x] Led simulation
- [ ] use gyro data