#!/bin/bash
set -x

export DISPLAY=:0
windows=("Clocktower Visualizer" "Gameboard" "Human Visualizer" "Neural Network Visualizer")

for w in "${windows[@]}"
do
  # Get window id from window name
  windowid=$(xdotool search --name "$w")
  # Check return code, make sure the window is open
  rc=$?
  if [ $rc -eq 0 ]; then
    echo "Refreshing $w"
    xdotool windowactivate --sync $windowid 
    xdotool key --window $windowid F5 
  else
    # Warn if window is not available. Also print out wanrning in GitHub 
    # Actions warning syntax so that actions will pick it up
    echo "Warning! Window $w not found"
    echo ":warning file={setup/refresh-browsers.sh},line={10},title={Window Not Found for Refresh}::{Window $w was not found by xdotool. Is the window open?}"
  fi
done
