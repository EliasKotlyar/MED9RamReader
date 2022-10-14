# Setup Can:
config-pin P1_28 can
config-pin P1_26 can
sudo ip link set can0 type can bitrate 500000
sudo ip link set up can0
