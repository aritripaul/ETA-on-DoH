#!/bin/bash
#clear browser history, cache and cookies
url=\'$1\'
if [ "$3" -lt 5 ]
then
	sudo rm ~/.mozilla/firefox/*.default/*.sqlite
	sudo rm -r ~/.cache/mozilla/firefox/*.default/*
fi

#start packet capture
file1="$2.raw"
touch $file1
chmod o=rw $file1


sudo tshark -i wlo1 -p -w $file1 &
sleep 5
#start loading webpage in browser
cmd='firefox -new-window '$url' &'

eval $cmd
sleep 45

#kill browser
wmctrl -ic "$(wmctrl -l | grep 'Mozilla Firefox' | tail -1 | awk '{ print $url }')"

#pkill firefox

#stop capture
sudo pkill tshark

sleep 25
