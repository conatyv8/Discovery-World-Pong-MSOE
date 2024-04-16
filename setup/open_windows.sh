#! /bin/sh
set -x

browser=chromium # `google-chrome` `chromium`or `firefox`

# We have 4 screens in the following layout:
#
#                     ----------------------------------
#                     |          |   ____   |          |
#                     |          |  /o  o\  |          |
#                     |          |  | __ |  |          |
#                     |          |  \____/  |          |
#                     |          |          |          |
#                     | 1 DP11   | 2 DP-3   | 3 DP-5   |
#                     | Left Info| ClckTwr  | Right    |
#                     | Screen   |          | Info     |
#                     |          |          | Screen   |
#                     |          |          |          |
#                     |          |          |          |
#                     ----------------------------------
#
#
#   ----------------------------------------------------------------------
#   |                                                ___                 |
#   |                                                                    |
#   |                                                                    |
#   |                                                                    |
#   |                            Main Play Area                          |
#   |                             0 HDMI-0 (Primary)                     |
#   |                                            *                       |
#   |                                                                    |
#   |                                                                    |
#   |                            ___                                     |
#   ----------------------------------------------------------------------
#
# Likely monitor configuration:
#$ DISPLAY=:0 xrandr --listactivemonitors 
#Monitors: 4
# 0: +*HDMI-0 1920/478x1080/269+0+0  HDMI-0
# 1: +DP-1 1920/521x1080/293+1920+0  DP-1
# 2: +DP-3 1920/521x1080/293+3840+0  DP-3
# 3: +DP-5 1920/521x1080/293+5760+0  DP-5
# Get the screen height

# Fix for ssh/remote connections:
export DISPLAY=:0

echo "Current monitor configuration:"
xrandr --listactivemonitors

left_info_width=$(xrandr --current | awk '/DP-1 connected / {print $3}' | cut -d '+' -f 1 | cut -d 'x' -f 1)
left_info_height=$(xrandr --current | awk '/DP-1 connected / {print $3}' | cut -d '+' -f 1 | cut -d 'x' -f 2)
echo "Left Info Monitor Dimensions: $left_info_width $left_info_height"

clocktower_width=$(xrandr --current | awk '/DP-3 connected / {print $3}' | cut -d '+' -f 1 | cut -d 'x' -f 1)
clocktower_height=$(xrandr --current | awk '/DP-3 connected / {print $3}' | cut -d '+' -f 1 | cut -d 'x' -f 2)
echo "Clocktower Monitor Dimensions: $clocktower_width $clocktower_height"

right_info_width=$(xrandr --current | awk '/DP-5 connected / {print $3}' | cut -d '+' -f 1 | cut -d 'x' -f 1)
right_info_height=$(xrandr --current | awk '/DP-5 connected / {print $3}' | cut -d '+' -f 1 | cut -d 'x' -f 2)
echo "Right Info Monitor Dimensions: $right_info_width $right_info_height"

main_play_area_width=$(xrandr --current | awk '/HDMI-0 connected primary/ {print $4}' | cut -d '+' -f 1 | cut -d 'x' -f 1)
main_play_area_height=$(xrandr --current | awk '/HDMI-0 connected primary/ {print $4}' | cut -d '+' -f 1 | cut -d 'x' -f 2)
echo "Main Play Area Monitor $main_play_area_width $main_play_area_height"


open_window () {
  if [ "$browser" = "firefox" ]; then
  	#$browser --new-window --kiosk $2 > /dev/null 2>&1 & 
	$browser --new-window $2 > /dev/null 2>&1 &
  else
  	$browser --new-window --window-size="1,1" --app=$2 > /dev/null 2>&1 & 
  fi
  sleep 2

  # $ DISPLAY=:0 xdotool windowmove --help
  # Usage: windowmove [options] [window=%1] x y
  # --sync      - only exit once the window has moved
  # --relative  - make movements relative to the current window position
  # If you use literal 'x' or 'y' for the x coordinates, then the current
  # coordinate will be used. This is useful for moving the window along
  # only one axis.
  xdotool windowmove --sync $(xdotool search --name "$1") $5 $6
  xdotool windowsize --sync $(xdotool search --name "$1") $3 $4
  # xdotool windowactivate --sync $(xdotool search --name "$1")
  xdotool key --window $(xdotool search --name "$1") F5 
}

# Firefox lets us use kiosk mode, so full screen windows don't need xdotool
# That is, if kiosk-montor actually placed windows on monitors....
#firefox --new-window --kiosk-monitor 2 "http://localhost:5003" > /dev/null 2>&1 &
#firefox --new-window --kiosk-monitor 0 "http://localhost:5000" > /dev/null 2>&1 &
#firefox --new-window --kiosk-monitor 1 "http://localhost:5001" > /dev/null 2>&1 &

# open_window "Name of window once open" "URL to open in browser" size_x size_y pos_x pos_y
open_window "Depth Feed" "http://localhost:5001" $((main_play_area_width / 2)) $((main_play_area_height / 2)) $right_info_width 0 
open_window "Visualization" "http://localhost:5002" $((main_play_area_width / 2)) $((main_play_area_height / 2)) $right_info_width $((main_play_area_height / 2))
open_window "Visualization React" "http://localhost:5003" $((main_play_area_width / 2)) $((main_play_area_height / 2)) $((main_play_area_width / 2 + $right_info_width)) 0 
open_window "DW PONG" "http://localhost:5000" $main_play_area_width $main_play_area_height 0 0 

exit 0
