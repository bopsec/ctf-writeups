#!/bin/sh
echo "$FLAG" > /flag.txt
unset FLAG
exec socat -d -d tcp-listen:1337,reuseaddr,fork exec:./challenge,stderr
