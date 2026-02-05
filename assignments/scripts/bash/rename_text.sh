#!/bin/bash

for file in *.txt; do
	if [ -f "$file" ];then
		mv "$file" "OLD_$file"
	fi
done

echo "Renaming Complete"
