export PYTHONPATH=$PYTHONPATH:..:.

echo "Run tests of libtodomanager"
./libtodomanager/libtodomanagertest.py

echo "Run tests of todomanagercli"
./todomanagercli/todomanagerclitest.py

