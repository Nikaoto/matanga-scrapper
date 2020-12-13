Install instructions:

$ pip3 install selenium
$ cp firefox_profile.py ~/.local/lib/python3.6/site-packages/selenium/webdriver/firefox/.
$ sudo cp geckodriver /usr/local/bin/.
$ sudo apt install xvfb firefox tor
$ sudo systemctl restart tor
$ chmod +x ./run-matanga-scrapper.sh
$ cp run-matanga-scrapper.sh /etc/cron.hourly/.
$ crontab -e # add entry: 0 * * * /home/nika/matanga-scrapper/run-matanga-scrapper.sh
$ vi mail_login.py # define user, password, and receivers variables
