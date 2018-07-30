from time import sleep
def proxy_connect(proxy,port,driver):
    driver.get("chrome-extension://fhnlhdgbgbodgeeabjnafmaobfomfopf/options.html?host="+proxy+"&port="+port)
    driver.find_element_by_xpath("//input[@id='socks5']").click()
    sleep(2)
    driver.find_element_by_xpath("//input[@id='socks4']").click()
    sleep(2)
    driver.find_element_by_xpath("//input[@id='socks5']").click()
    sleep(2)
    driver.find_element_by_xpath("//input[@id='socks4']").click()
    sleep(2)
    driver.find_element_by_xpath("//input[@id='socks5']").click()
    sleep(3)
    driver.get("chrome-extension://fhnlhdgbgbodgeeabjnafmaobfomfopf/popup.html?host="+proxy+"&port="+port)
    sleep(3)
    try:
        driver.find_element_by_xpath("//span[@id='http']").click()
    except NoSuchElementException:
        print("X 1")
    sleep(3)


