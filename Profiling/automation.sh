#!/bin/sh
python3 url_fetch.py

sudo chmod 777 firefox_collect_samples.sh
touch key.log
sudo chmod 777 key.log
export SSLKEYLOGFILE=./key.log
python profile.py -whole 0 -webdir . -listfile url.txt

python3 Sequence.py
python3 commonsubseq.py Output