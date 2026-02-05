#!/bin/bash

echo "=====System Health Snapshot====="
echo "Date & Time: $(date)"
echo "Hostname: $(hostname)"
echo "Current User: $(whoami)"
echo "Disk Usage:"
df -h /
