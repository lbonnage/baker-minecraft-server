#!/bin/sh
echo "[SHUTDOWN] Beginning shutdown script"
# Check to see if there is a screen running (there should be)
if screen -list | grep -q "mcs"; then
        # This is the string we would receive if there were 0 players online
        PLAYERSEMPTY=" There are 0"
        PLAYERSEMPTYVANILLA=" There are 0 of a max 20 players online"
        # Send the '/list' command to the server twice and wait 5 seconds, in order to get some results in the log
        $(screen -S mcs -p 0 -X stuff "list^M")
        sleep 5
        $(screen -S mcs -p 0 -X stuff "list^M")
        sleep 5
        # Now, retrieve the current player count and put it into the PLAYERSLIST variable
        PLAYERSLIST=$(sudo perl -ne '$l=$_ if /There are/; END{print $l}' /home/minecraft/logs/latest.log | cut -f2 -d"/" | cut -f2 -d ":")
        echo "[SHUTDOWN] Initial check: ${PLAYERSLIST}"
        # Check to see if the player list is empty
        if [ "$PLAYERSLIST" = "$PLAYERSEMPTY" ] || [ "$PLAYERSLIST" = "$PLAYERSEMPTYVANILLA" ]
        then
                # Echo a status to the report file so a user can view it
                echo "[SHUTDOWN] Waiting for players to come back in 12m, otherwise shutdown"
                sleep 12m
                # Check the players list again
                $(screen -S mcs -p 0 -X stuff "list^M")
                sleep 5
                $(screen -S mcs -p 0 -X stuff "list^M")
                sleep 5
                PLAYERSLIST=$(sudo perl -ne '$l=$_ if /There are/; END{print $l}' /home/minecraft/logs/latest.log | cut -f2 -d"/" | cut -f2 -d ":")
                echo "[SHUTDOWN] Final check: ${PLAYERSLIST}"
                # Perform the final check
                if [ "$PLAYERSLIST" = "$PLAYERSEMPTY" ] || [ "$PLAYERSLIST" = "$PLAYERSEMPTYVANILLA" ]
                then
                        echo "[SHUTDOWN] Server has been empty for 15 minutes and shutdown will be initiated"
                        $(sudo shutdown)
                fi
        fi
else
        echo "[SHUTDOWN] Screen does not exist, briefly waiting before trying again"
        # Give the server a bit of time to start up, in case this script triggers before its ready for anything
        sleep 10m
        if ! screen -list | grep -q "mcs"; then
                echo "[SHUTDOWN] Screen does not exist, shutting down server"
                $(sudo shutdown)
        fi
fi