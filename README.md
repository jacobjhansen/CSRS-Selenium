# CSRS-Selenium
Headless Selenium automation for submitting .obs files to CSRS for Precise Point Positioning (PPP)

# Background
This project is intended to automate the process of uploading .obs files to the CSRS Precise Point Positioning Service to allow easy management of multiple GNSS Base Stations. The intended workflow is essentially as follows:
1. Log 24 hours of RAW-RAWX and RXM-SFRBX messages using the RTKLIB console app str2str
`timeout 24h ./RTKLIB/app/consapp/str2str/gcc/str2str -in serial://[serialdevice]:[baud]:8:n:1:off -out ~/[filename].ubx`
2. Process the resulting .ubx file into a .obs file using the RTKLIB console app convbin
`./RTKLIB/app/consapp/convbin/gcc/convbin -od -os -oi -ot [filename].ubx`
3. Wait a pre-determined length of time (Probably something like 2 weeks)
4. Automatically upload .obs file to CSRS (THIS PROJECT)
`python3 opus.py`

Where all steps are automated and scheduled via crontab

# Setup
I set up this project specifically to run on a Raspberry Pi 4 running Ubuntu Server 22.04. For this project, the following dependencies are needed:
1. [selenium](https://www.geeksforgeeks.org/how-to-install-selenium-in-python/)
`pip3 install selenium`
2. [Mozilla Firefox Gecko Driver](https://www.geeksforgeeks.org/how-to-install-selenium-in-python/)
`wget https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz` (You may need a more up-to-date version)
`tar -xvzf geckodriver*`
`chmox +x geckodriver`
`sudo mv geckodriver /usr/local/bin`
3. [xvfb](https://withr.github.io/set-up-selenium-headless-on-ubuntu-16.04/)
`sudo apt install xvfb`
4. [PyVirtualDisplay](https://withr.github.io/set-up-selenium-headless-on-ubuntu-16.04/)
`pip3 install pyvirtualdisplay`