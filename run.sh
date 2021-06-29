
#!/bin/bash

ps -aux | grep python3


killall -KILL python3
python3 RasaTelegram.py > /dev/null 2>&1 &
python3 ScraperWordpress.py > /dev/null 2>&1 &
python3 ScraperWorrdpressASC.py > /dev/null 2>&1 &
python3 NuevoScrapperWordpress.py > /dev/null 2>&1 &
python3 NuevoScrapperWordPressASC.py > /dev/null 2>&1 &

python3 EnviaTelegram.py 01 > /dev/null 2>&1 &
python3 EnviaTelegramArgentina.py 50 > /dev/null 2>&1 &
python3 EnviaTelegramArgentina.py 81 > /dev/null 2>&1 &
python3 EnviaTelegramArgentina.py 45 > /dev/null 2>&1 &
python3 EnviaTelegramArgentina.py 62 > /dev/null 2>&1 &
python3 EnviaTelegramArgentina.py 41 > /dev/null 2>&1 &
python3 EnviaTelegramArgentina.py 01 > /dev/null 2>&1 &
python3 EnviaTelegramArgentina.py 59 > /dev/null 2>&1 &
python3 EnviaTelegramArgentina.py 32 > /dev/null 2>&1 &
python3 EnviaTelegramArgentina.py 57 > /dev/null 2>&1 &
python3 EnviaTelegramArgentina.py 87 > /dev/null 2>&1 &
python3 EnviaTelegramArgentina.py 34 > /dev/null 2>&1 &

python3 NuevoScrapperRss.py 1 > /dev/null 2>&1 &
python3 NuevoScrapperRss.py 2 > /dev/null 2>&1 &
python3 NuevoScrapperRss.py 3 > /dev/null 2>&1 &
python3 NuevoScrapperRss.py 4 > /dev/null 2>&1 &
python3 NuevoScrapperRss.py 5 > /dev/null 2>&1 &
python3 NuevoScrapperRss.py 6 > /dev/null 2>&1 &
python3 NuevoScrapperRss.py 7 > /dev/null 2>&1 &
python3 NuevoScrapperRss.py 8 > /dev/null 2>&1 &
python3 NuevoScrapperRss.py 9 > /dev/null 2>&1 &
python3 NuevoScrapperRss.py 10 > /dev/null 2>&1 &
python3 NuevoScrapperRss.py 11 > /dev/null 2>&1 &
python3 NuevoScrapperRss.py 12 > /dev/null 2>&1 &
python3 NuevoScrapperRss.py 13 > /dev/null 2>&1 &
python3 NuevoScrapperRss.py 14 > /dev/null 2>&1 &
python3 NuevoScrapperRss.py 15 > /dev/null 2>&1 &
python3 NuevoScrapperRss.py 16 > /dev/null 2>&1 &
python3 NuevoScrapperRss.py 17 > /dev/null 2>&1 &
python3 NuevoScrapperRss.py 18 > /dev/null 2>&1 &
python3 NuevoScrapperRss.py 19 > /dev/null 2>&1 &
python3 NuevoScrapperRss.py 20 > /dev/null 2>&1 &
python3 NuevoScrapperRss.py 21 > /dev/null 2>&1 &
python3 NuevoScrapperRss.py 22 > /dev/null 2>&1 &
python3 NuevoScrapperRss.py 23 > /dev/null 2>&1 &
python3 NuevoScrapperRss.py 24 > /dev/null 2>&1 &

