#!/bin/bash

./test_provider_post_put.sh
[ $(echo "$?") -eq 1 ] && exit 1


exit 0

./get_test.bash
[ $(echo "$?") -eq 1 ] && exit 1


exit 0
