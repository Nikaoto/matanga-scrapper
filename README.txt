pip3 install selenium
cp firefox_profile.py ~/.local/lib/python3.6/site-packages/selenium/webdriver/firefox/.
sudo cp geckodriver /usr/local/bin/.
sudo apt install xvfb firefox tor
sudo systemctl restart tor
NOW_MONTH="$(date +%m)" mkdir -p "$NOW_MONTH" && xvfb-run python3 scrape.py "$NOW_MONTH"