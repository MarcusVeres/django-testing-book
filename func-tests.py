from selenium import webdriver

browser = webdriver.Chrome()
browser.get( 'http://localhost:9090' )

assert 'Django' in browser.title

