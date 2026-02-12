#!/bin/bash

FILE="$1"

if [ -z "$FILE" ]; then
	echo "Usage: $0 filename"
	exit 1
fi

if [ ! -f "$FILE" ];then
	echo "File does not exist"
	exit 1
fi

LIMIT=1048576 #1MB
SIZE=$(stat -c%s "$FILE")

if [ "$SIZE" -gt "$LIMIT" ]; then
	echo "Warning: File is too large"
else
	echo "File size is within limits"
fi
