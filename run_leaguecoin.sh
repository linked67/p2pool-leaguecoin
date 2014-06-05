#!/bin/sh
SERVICE='python ./run_p2pool.py --net leaguecoin'

if ps ax | grep -v grep | grep "$SERVICE" > /dev/null
then
        echo "$SERVICE is already running!"
else
        screen -d -m -S screenlol python ./run_p2pool.py --net leaguecoin --give-author 0 --disable-upnp -f 1 -a LT4C99mv1mqLBj2LpkrkEtV7McVNrGdDoS

	wait
fi
