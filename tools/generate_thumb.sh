#!/bin/bash

CONCAT_FILE=concat.mp4
ffmpeg -i concat:"$(fdfind . | sed 's/$/|/g' | tr -d '\n')" -c:v copy -map 0:v:0 -f mp4 "$CONCAT_FILE"
ffmpeg -i "$CONCAT_FILE" -vf "fps=30,select='not(mod(n\,30))',scale=160:90,tile=250x1" -frames:v 1 preview.jpg
