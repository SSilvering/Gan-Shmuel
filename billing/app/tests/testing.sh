#!/bin/bash
pushd $PWD/app/tests/
echo "Testing provider"
chmod u+x ./test_provider_post_put.sh
#./test_provider_post_put.sh
#[ $(echo "$?") -eq 1 ] && exit 1
echo "testing get/rates"
chmod u+x ./get_test.bash
#./get_test.bash
#[ $(echo "$?") -eq 1 ] && exit 1


chmod u+x ./post_rates_test.py
chmod u+x ./put_truck_test.py
cd ../../

export PATH="$HOME/.local/bin:$PATH"

echo "testing post/rates"
python3 -m app.tests.post_rates_test
[ $(echo "$?") -eq 1 ] && exit 1

echo "testing put/truck"
python3 -m app.tests.put_truck_test
[ $(echo "$?") -eq 1 ] && exit 1

popd
exit 0

