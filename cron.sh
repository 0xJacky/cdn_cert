CRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")

cd "$SCRIPTPATH"

/usr/bin/python3 cdncert.py > cdncert.log 2>&1
