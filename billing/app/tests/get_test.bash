#!/bin/bash
FILE=rates.xlsx
ld=$(curl --silent -X GET http://18.194.15.175:8085/rates --output "$FILE")
status=$?
if [ $status -eq 0 ] &&  [ -f "$FILE" ]; then
	rm "$FILE" 
     exit 0
else
	rm "$FILE"  
    exit 1 
fi
