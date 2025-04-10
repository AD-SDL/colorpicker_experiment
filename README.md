# colorpicker_experiment

The Colorpicker demonstration autonomous experiment used in the RPL's SDL.

This experiment uses [the MADSci Toolkit](https://github.com/ad-sdl/MADSci) to demonstrate a closed-loop autonomous discovery experiment.

The application generates a random target color, and attempts to mix that target color using provided inks as inputs. The experiment will autonomously evaluate it's outputs, generate new candidates, and test those candidates using a Bayesian Solver.

## Equipment

- Opentrons OT-2 Liquidhandler
- Precise Automation PF400 Robotic Sample Handler
- Hudson Robotics Sciclops Platecrane
- A 1080p Webcam
- Barty the Bartending Robot
