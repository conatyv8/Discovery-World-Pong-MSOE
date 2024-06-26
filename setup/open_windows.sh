#! /bin/sh
set -x

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

#! /bin/sh

# neural-net-visualizer (top-left)
firefox -P neural-net-visualizer --kiosk --new-instance --new-window "http://localhost:5002" --kiosk-monitor 0 > /dev/null 2>&1 & 
sleep 2

# clocktower-visualizer (top-middle)
firefox -P clocktower-visualizer --kiosk --new-instance --new-window "http://localhost:5003" --kiosk-monitor 2 > /dev/null 2>&1 & 
sleep 2

# human-visualizer (top-right)
firefox -P human-visualizer --kiosk --new-instance --new-window "http://localhost:5001" --kiosk-monitor 1 > /dev/null 2>&1 & 
sleep 2

# gameboard (bottom-Middle)
firefox -P gameboard --kiosk --new-instance --new-window "http://localhost:5000" --kiosk-monitor 3 > /dev/null 2>&1 & 
sleep 2

exit 0
