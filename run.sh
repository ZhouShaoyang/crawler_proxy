#! /bin/bash

ROOT=$(cd "$(dirname "$0")";pwd)
PYTHON="${ROOT}/Venv/bin/python"
CRAWL="${ROOT}/bin/crawl.py"
CHECK="${ROOT}/bin/check.py"
API="${ROOT}/bin/api.py"

echo '[DETECT] - crawler proxy'
ps -ef|grep ${PYTHON}|grep -v grep
if [ $? -eq 0 ]
then
    echo '[KILL] - old crawler proxy'
    ps -ef|grep ${PYTHON}|grep -v grep|cut -c 9-15|xargs kill -9
    sleep 5
else
    echo '[KILL] - old crawler proxy'
fi

echo '[START] - crawler proxy crawl schedule'
nohup ${PYTHON} ${CRAWL} > /dev/null 2>&1 &
echo '[WAIT] - 60s...'
sleep 60
echo '[START] - crawler proxy check schedule'
nohup ${PYTHON} ${CHECK} > /dev/null 2>&1 &
echo '[START] - crawler proxy api schedule'
nohup ${PYTHON} ${API} > /dev/null 2>&1 &