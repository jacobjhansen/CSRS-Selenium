import sys, time, os, glob
from zipfile import ZIP_DEFLATED, ZipFile
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pyvirtualdisplay import Display

print('Starting CSRS-Selenium...\n')

# Start Virtual Display for headless operation
display = Display(visible=0, size=(1920, 1080)).start()
time.sleep(1)

# Get most recent .obs file
pattern="*.obs" # This pattern may need updated to only search a specific directory
files = list(filter(os.path.isfile, glob.glob(pattern)))
files.sort(key=lambda x: os.path.getmtime(x))
lastfilename = files[-1]
lastfilepath = str(Path(lastfilename).resolve())

file_size = os.path.getsize(lastfilepath)
print("File Size is :", file_size, "bytes")

if file_size >= 300000000:
    print("File is too large to submit as .obs")
    zipname = os.path.splitext(lastfilename)[0]+'.zip'
    print('Zipping File into:',zipname)
    ZipFile(zipname, mode='w', compression=ZIP_DEFLATED).write(lastfilename)
    zip_size = os.path.getsize(zipname)
    zippath = str(Path(zipname).resolve())
    print('Zip Path:',zippath)
    print('Zip Size:',zip_size)
    print('File Zip Successful.')
    print('Replacing file with zip')
    file = zippath
else:
    file = lastfilepath

# Set configuration variables
myemail = 'YOUREMAILHERE'
mypassword = 'YOURPASSWORDHERE'

print("Your file is " + file)
print("Your email is " + myemail)

# Set Driver
driver = webdriver.Firefox("/usr/local/bin")
#driver._is_remote = False

# Get OPUS Webpage
driver.get("https://webapp.csrs-scrs.nrcan-rncan.gc.ca/geod/tools-outils/ppp.php")
assert "Precise Point Positioning" in driver.title

# Sign in to Web App
signin = driver.find_element(by=By.XPATH, value="/html/body/div/div/main/div[2]/p/a")
signin.click()
print('Signing in to web app')

# Set Email Address Value
email = driver.find_element(by=By.NAME, value="emaillogin")
time.sleep(1)
email.send_keys(myemail)
print('Email Entered')
time.sleep(1)

# Enter Password
password = driver.find_element(by=By.NAME, value="passlogin")
time.sleep(1)
password.send_keys(mypassword)
print('Password Entered')
time.sleep(1)

# Click Sign In
signin2 = driver.find_element(by=By.XPATH, value='//*[@id="loginform"]/button')
signin2.click()
print('Sign in completed')

time.sleep(10)

# Select ITRF Mode
itrf = driver.find_element(by=By.XPATH, value='//*[@id="itrftab-lnk"]')
itrf.click()
print('ITRF Mode Selected')
time.sleep(1)

# Upload File
upload = driver.find_element(by=By.NAME, value="rfile_upload")
upload.send_keys(file)
print('File Uploaded Successfully')
time.sleep(1)

# Submit to PPP
submit = driver.find_element(by=By.XPATH, value='//*[@id="submit_btn"]')
submit.click()
time.sleep(1)

driver.quit()
display.stop()
sys.exit()