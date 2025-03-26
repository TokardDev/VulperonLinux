#!/bin/bash

run_archiso -i "$(ls -t *.iso | head -n 1)"
