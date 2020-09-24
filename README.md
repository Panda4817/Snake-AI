# Snake AI

A program that allows users to play the Snake game as normal, watch AI play Snake and play Snake against the AI. Before settling on the Hamiltonian Cycle for the AI snake, I tried Q-learning and A* search algorithms.

![Snake AI demo](https://i.imgur.com/3TCFWi4.gif)

## Requirements

Run `sudo apt-get install -y xvfb ffmpeg` first. Then install required packages via `pip install -r requirements.txt` or install one package at a time: pygame and numpy.

## Usage

Run `python runner.py`. Choose between the options:
- Human plays Snake - Normal snake with score keeping.
- AI plays Snake - AI plays normal snake with score keeping, human watches. 
- Tron Snake - Human vs AI snake. Both trying to get the most food and trying not to crash into each other or the wall.

