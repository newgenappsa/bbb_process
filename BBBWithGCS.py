import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import urllib3
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,WebDriverException,TimeoutException
from selenium.webdriver.common.by import By


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
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
            print('hey')
            driver = webdriver.Chrome(executable_path="/Users/macbook/Desktop/BBB/chromedriver",   chrome_options=chrome_options)
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
        links,information,chunks= [],{},[]
        information["company"] = account
        try:
            dict_det,name,details,email_id, title= {},[],[],[],''
            replace_list = ['.inc','.ltd',' corporation',' corp','.com','.co','industry','pty','pt.',' private','&',"'",'.llc','.au','.org','.net','.inc','.in']
            links,phone,name,branch= [],[],[],[]
            #array_words = word_tokenize(account)
            print(account)
            for replace in replace_list:
                account = account.lower().replace(replace,'')
            input_,link = account.replace(" ","+")+"+BBB",[]
            #driver = webdriver.Chrome(executable_path = '/Users/macbook/Downloads/chromedriver')
            #https://www.google.co.in/search?q=WorldStrides%2C+Inc.+BBB&oq=WorldStrides%2C+Inc.+BBB&aqs=chrome..69i57.3557j0j4&sourceid=chrome&ie=UTF-8
            url = "https://www.google.co.in/search?q="+input_+"&oq="+input_+"+&aqs=chrome.0.69i59j69i60j69i57j0l3.6896j0j4&sourceid=chrome&ie=UTF-8"
            #driver.get(url)
            req  = urllib3.PoolManager()
            res = req.request('GET',url)
        except UnicodeEncodeError:
            return details,list(set(name)),list(set(email_id))
        soup = BeautifulSoup(res.data, 'html.parser')
        div_container = soup.find_all("div",class_ = "g")
        for div in div_container:
            #print(div)
            a_tag = str(div.find('a'))
            #print(a_tag)
            start = a_tag.find("https")
            end = a_tag.find(";")
            link_a = a_tag[start:end]
            if link_a.find("www.bbb.org")> -1 and link_a.lower().replace("-","").find(account)>-1 :
                print("link",link_a)
                links.append(link_a.replace("&amp",""))
        for link in set(links):
            title,data = loop_through_links(link)
            if title!= '':
                information[title] = data
        print(information,"___",len(information))
        return information




#get_details_from_bbb("WorldStrides")
