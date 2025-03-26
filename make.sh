#!/bin/bash

sudo rm -rf /tmp/vulperon-work
sudo mkarchiso -v -w /tmp/vulperon-work -o ./build .
