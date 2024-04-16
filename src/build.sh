#!/bin/bash

ce=docker #podman
# docker build -t dw_ai -f ./ai/Dockerfile .
# docker build -t dw_depthfeed -f ./depthfeed/Dockerfile .
# docker build -t dw_game -f ./game/Dockerfile .
# docker build -t dw_motion -f ./motion/Dockerfile .
# docker build -t dw_visualization -f ./visualization/Dockerfile .
# cd pong-react
# docker build -t dw_pong-react -f ./Dockerfile .
# cd ..
# cd visualization-react
# docker build -t dw_visualization-react -f ./Dockerfile .
# cd ..


$ce build -t dw_ai -f ./ai/Dockerfile .
$ce build -t dw_depthfeed -f ./depthfeed/Dockerfile .
$ce build -t dw_game -f ./game/Dockerfile .
$ce build -t dw_motion -f ./motion/Dockerfile .
$ce build -t dw_visualization -f ./visualization/Dockerfile .
cd pong-react
$ce build -t dw_pong-react -f ./Dockerfile .
cd ..
cd visualization-react
$ce build -t dw_visualization-react -f ./Dockerfile .
cd ..
