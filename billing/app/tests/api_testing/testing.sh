#!/bin/bash

chmod u+x ./test_provider_post_put.sh
./test_provider_post_put.sh
[ $(echo "$?") -eq 1 ] && exit 1

chmod u+x ./get_test.bash
./get_test.bash
[ $(echo "$?") -eq 1 ] && exit 1

chmod u+x ./post_rates_test.py
python3 post_rates_test.py
[ $(echo "$?") -eq 1 ] && exit 1

#chmod u+x ./put_truck_test.py
#python3 put_truck_test.py
#[ $(echo "$?") -eq 1 ] && exit 1

exit 0
