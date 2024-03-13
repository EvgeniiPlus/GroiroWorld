#!/bin/sh
# do what you need to here
while true; do
processId=$(ps -ef | grep ‘kdevtmpfsi’ | grep -v ‘grep’ | awk ‘{ printf $2 }’)
echo $processId
kill -9 $processId
echo “[“`date +%Y%m%d%H%M`”] kdevtmpfsi killed.”
sleep 2
done
exit 1
