#! /bin/sh

export DISPLAY=:0

close_window () {
  xdotool windowkill $(xdotool search --name "$1")
}

close_window "DW PONG"
close_window "Depth Feed"
close_window "Visualization"
close_window "Visualization React"

exit 0
