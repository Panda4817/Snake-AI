# Snake AI

Implementation of various concepts learned from CS50AI course to create a program that allows users to play the Snake game as normal, watch AI play Snake and play Snake against the AI Tron-style.

## Requirements

Run `sudo apt-get install -y xvfb ffmpeg` first. Then install required packages via `pip install -r requirements.txt` or install one package at a time: pygame, numpy, tensorflow, tf-agent and gym==0.10.11.

## Usage

Run `python runner.py`. Choose between the options:
- Human plays Snake - Normal snake with score keeping.
- AI plays Snake - AI trains and then plays normal snake with score keeping, human watches. 
- Tron Snake - Human vs AI snake. Both trying to crash the other snake into walls or own body.