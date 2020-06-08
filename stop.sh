#! /bin/bash

ROOT=$(cd "$(dirname "$0")";pwd)
PYTHON="${ROOT}/venv/bin/python"
CRAWL="${ROOT}/bin/crawl.py"
CHECK="${ROOT}/bin/check.py"
SLEEP=5

echo '[DETECT] - crawler proxy'
ps -ef|grep ${PYTHON}|grep -v grep
if [ $? -eq 0 ]
then
    echo '[KILL] - old crawler proxy'
    ps -ef|grep ${PYTHON}|grep -v grep|cut -c 9-15|xargs kill -9
    sleep ${SLEEP}
else
    echo '[KILL] - old crawler proxy'
fi
