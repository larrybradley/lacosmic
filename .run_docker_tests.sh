#!/bin/bash

docker info

cat << EOF | docker run -i \
                        -v ${PWD}:/lacosmic_src \
                        -a stdin -a stdout -a stderr \
                        astropy/affiliated-32bit-test-env:1.6 \
                        bash || exit $?

cd /lacosmic_src

echo "Output of uname -m:"
uname -m

echo "Output of sys.maxsize in Python:"
python -c 'import sys; print(sys.maxsize)'

python setup.py test -V -a "-s"

EOF
