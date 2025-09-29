from selenium import webdriver
import time
import sys, os

memoid = sys.argv[1]

driver = webdriver.PhantomJS(service_log_path='/dev/null')
driver.implicitly_wait(10)
driver.get("http://localhost/read.php?id=" + memoid)
driver.get("http://localhost/check.php?id=" + memoid)
