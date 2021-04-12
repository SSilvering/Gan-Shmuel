#!/bin/bash

#adding a name to DB
#cath his id, the one thet added
#cath if he in the DB - t1
#change his name by id
#check if changed name exict -t2

ID=$(curl -s -i -X POST -H 'Content-Type: application/json' -d '{"name": "test_name"}' http://18.194.15.175:8081/provider | grep id | cut -b 9- | rev | cut -b 3- | rev)
[ -z "${ID}" ] && exit 1 #if ID == null then exit 1
curl -s -i -X POST -H 'Content-Type: application/json' -d '{"name": "test_name"}' http://18.194.15.175:8081/provider | grep "already Exists"
[ $(echo "$?") -eq 1 ] && exit 1
curl -s -i -X PUT -H 'Content-Type: application/json' -d '{"name": "changed_test_name"}' http://18.194.15.175:8081/provider/$ID
curl -s -i -X POST -H 'Content-Type: application/json' -d '{"name": "changed_test_name"}' http://18.194.15.175:8081/provider | grep "already Exists"
[ $(echo "$?") -eq 1 ] && exit 1
exit "0"
