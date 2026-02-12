#!/bin/bash

ps -eo pid,comm,%mem --sort=%mem | head -n 6
