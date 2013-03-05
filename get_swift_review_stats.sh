#!/bin/sh

for i in 1 7 14 30 60 90 180; do
    ./stats.py -p swift -d ${i} >swift-${i}days.json
done
