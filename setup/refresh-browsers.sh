#!/bin/bash
set -x

export DISPLAY=:0
windows=("Clocktower Visualizer" "Gameboard" "Human Visualizer" "Neural Network Visualizer")

for w in "${windows[@]}"
do
  echo "Refreshing $w"
  xdotool windowactivate --sync $(xdotool search --name "$w")
  xdotool key --window $(xdotool search --name "$w") F5 
done
