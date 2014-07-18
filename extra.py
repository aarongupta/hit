#!/bin/sh

#  extra.py
#  
#
#  Created by Aaron Gupta on 7/18/14.
#
# gets NCBI accession ID from NAR website/xls (if available)
def get_id(x,y,barcode):
    '''
        data = json.load(urllib2.urlopen('http://research.gene.com/nar/isomorphic/IDACall?isc_rpc=1&isc_v=9.0a&isc_xhr=1'))
        
        #print data
        '''
    url = 'http://research.gene.com/nar/isomorphic/IDACall?isc_rpc=1&isc_v=9.0a&isc_xhr=1'
    r = requests.get(url, auth=('guptaa22', 'Scissor1'))
    print r.status_code
    print r.headers['content-type']
    print r.encoding
    print r.text
    print r.json
    print r.content
    try:
        print r.json()
    except ValueError:
        print 'no json'
    '''
        
        url = 'http://research.gene.com/nar/isomorphic/IDACall?isc_rpc=1&isc_v=9.0a&isc_xhr=1'
        username = 'guptaa22'
        password = 'Scissor1'
        p = urllib2.HTTPPasswordMgrWithDefaultRealm()
        
        p.add_password(None, url, username, password)
        
        handler = urllib2.HTTPBasicAuthHandler(p)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)
        
        data = json.load(urllib2.urlopen(url))
        print data
        
        accession = ''
        r = requests.get('guptaa22:Scissor1@http://research.gene.com/nar',auth=HTTPBasicAuth('guptaa22','Scissor1')).text
        print r
        #find tag in html and return accession
        
        url = 'guptaa22:Scissor1@http://research.gene.com/nar/'
        #url = 'google.com'
        xpath = '//*[@id="isc_O"]/table/tbody/tr/td/table/tbody/tr/td[2]'
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
        browser = webdriver.Chrome(chrome_options=options)
        browser.get(url)
        #time.sleep(1)
        #button = browser.find_element_by_xpath(xpath)
        present = False
        try:
        try:
        button = WebDriverWait(browser, 10).until(lambda browser : browser.find_element_by_xpath(xpath))
        present = True
        except TimeoutException:
        print 'button does not exist'
        except NoSuchElementException:
        present = False
        #button = WebDriverWait(browser, 10).until(lambda browser : browser.find_element_by_xpath(xpath))
        if present == True:
        button.click()
        browser.close()
        return present
        '''
