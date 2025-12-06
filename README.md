# Two-Finger Hand Gesture Volume Control

This project allows you to control your laptop's volume using hand gestures detected via webcam.

## Installation

1. Install Python 3.8+.
2. Install dependencies: `pip install -r requirements.txt`

## Usage

Run `python main.py`

Position your hand in front of the webcam. Use thumb and index finger to control volume:
- Bring fingers closer: decrease volume
- Spread fingers apart: increase volume
- Make a fist: mute/unmute

## Gestures

- **Volume Control**: Distance between thumb and index finger tips.
- **Mute/Unmute**: Close all fingers into a fist.

## Visual Feedback

The webcam feed displays:
- Current volume percentage
- UP/DOWN arrows indicating volume change direction

## Requirements

- Webcam
- OpenCV
- Mediapipe
- Platform-specific volume control libraries (PyCaw for Windows, amixer for Linux, osascript for macOS)

## Error Handling

- If no hand is detected, volume remains unchanged.
- Handles landmark detection failures gracefully.
