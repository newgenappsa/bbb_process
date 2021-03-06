from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,WebDriverException,TimeoutException
from selenium.webdriver.common.by import By
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
#from text_partition import isPhoneNo,isBranch,isName


def is_element_present(driver,by,what):
    try:
           driver.find_element(by = by,value = what)
    except NoSuchElementException:
        #print('nope',what)
            return False
    return True

def filter_raw_data(soup):
    details,keys,values,dict_det,names,title = [],[],[],{},[],''
    try:
        title = soup.find('h1',class_='jss387 jss391 dtm-business-name styles__BusinessNameTitle-s4vaaw-3 bvuWns').get_text().replace(".","")
    except AttributeError:
        pass
    uls = soup.find_all("ul",class_= "styles__UlUnstyled-sc-1fixvua-1 ehMHcp")
    for ul in uls:
        try :
            print("name => ",ul.find("li").get_text())
            name = ul.find("li").get_text()
            print("position =>",ul.find("p").get_text())
            position = ul.find("p").get_text()
            if position != '':
                details.append({position:name})
        except AttributeError:
            names.append(name)
            details.append(name)
            pass
        try:
            print("second try ",ul.find("a").get_text())
            link = ul.find("a").get_text()
            details.append({'link': link})
        except AttributeError:
            pass
    #first bar
    try:
        div_container = soup.find_all('div',class_ = 'jss386 styles__StyledCardContent-sc-1po1jpn-3 lkHyQZ')
        address = []
        for div in div_container:
            ps = div.find_all('p')
            for p in ps:
                address.append(p.get_text())
        if len(address)> 0:
            details.append({'Address': address})
    except AttributeError:
         pass
        #table
    try:
        div_container = soup.find('div',class_ = 'jss359 jss362 jss360 jss358')
        table = div_container.find('table')
        ths = table.find_all('th')
        for th in ths:
            keys.append(th.get_text().replace(".",""))
        tds = table.find_all('td')
        for td in tds:
            values.append(td.get_text())
    except AttributeError:
         pass
        #phome number
    try:
        phone_no,phoneNo = div_container.find_all('span',class_='dtm-phone'),[]
        for no in phone_no:
            print(no.get_text())
            phoneNo.append(no.get_text())
        if len(phoneNo)>0:
           details.append({'phone number': phoneNo})
    except AttributeError:
         pass
    for i in range(0,len(keys)-1):
        dict_det[keys[i]] = values[i]
    if len(dict_det)>0:
        details.append(dict_det)
    #print(details)
    return title,details


def loop_through_links(link):
        title = ''
        try:
            driver = webdriver.Chrome(executable_path = '/Users/macbook/Downloads/chromedriver')
            driver.set_window_size(799, 830)
            driver.get(link)
            if is_element_present(driver,By.CLASS_NAME,"dtm-country-selection-modal-country-link"):
                WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,"dtm-country-selection-modal-country-link")))
                driver.find_element_by_xpath("//button[@class='dtm-country-selection-modal-country-link']").click()
        except (NoSuchElementException) as e:
            driver.quit()
            loop_through_links(link)
        html = driver.page_source
        soup = BeautifulSoup(html,"lxml")
        title,data = filter_raw_data(soup)
        driver.quit()
        return title,data


def get_details_from_bbb(account):
    text = []
    title = account
    driver = webdriver.Chrome(executable_path = '/Users/macbook/Downloads/chromedriver')
    driver.set_window_size(799, 830)
    links,information,chunks= [],{},[]
    information["company"] = account
    driver.get('https://www.google.com/')
    try:
        driver.find_element_by_xpath("//input[@id='lst-ib']").send_keys(account+" bbb")
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.NAME,'btnK')))
        driver.find_element_by_xpath("//input[@value='Google Search']").click()
    except (NoSuchElementException,WebDriverException) as e :
        driver.quit()
        get_details_from_bbb(account)
    try :
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,'g')))
        div_container = driver.find_elements_by_xpath("//div[@class='g']")
    except NoSuchElementException:
        driver.quit()
        return information
    for div in div_container:
              link_a = div.find_element_by_css_selector('a')
              chunks = word_tokenize(account.lower().replace('.','').replace("'","").replace("&","").replace(",",""))
              if len(chunks)>= 2 :
                  chunk = chunks[0]+"-"+chunks[1]
              else:
                  chunk = chunks[0]
              if link_a.text.find("www.bbb.org")> -1 and link_a.text.find(chunk)>-1 :
                     links.append(link_a.get_attribute("href"))
    driver.quit()
    for link in links[0:5]:
        title,data = loop_through_links(link)
        if title!= '':
            information[title] = data
    print(information,"___",len(information))
    return information




get_details_from_bbb("APPLAUSE")
