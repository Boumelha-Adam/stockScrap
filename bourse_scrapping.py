from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# import classes to manage the waiting time after cliking
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

import time
import os

import pandas as pd


options = Options()
options.add_argument("start-maximized")
# path of the web driver whish is in the same directory of our project
path = os.getcwd() + "/chromedriver"

#path of the driver, use chmod 755 chromedriver command to allow permissions
driver = webdriver.Chrome(chrome_options=options,executable_path=path)

# get the full path of the website to scrap 
driver.get("http://www.casablanca-bourse.com/bourseweb/Negociation-Historique.aspx?Cat=24&IdLink=302")


#search in the html code for the search bar containing the names of the companies
# & seperate the string into a list of companies

stringCompanies = driver.find_element_by_xpath('//*[@id="HistoriqueNegociation1_HistValeur1_DDValeur"]')

#list containing all the companies in the page
listCompanies = stringCompanies.text.split("\n")[1:]

# select your desired companie and interval of the data to scrap your data: option[4] index 4 ==> index of the companie alliances 

driver.find_element_by_xpath('//*[@id="HistoriqueNegociation1_HistValeur1_DDValeur"]/option[4]').click()
driver.find_element_by_xpath('//*[@id="HistoriqueNegociation1_HistValeur1_DDuree"]/option[6]').click()
driver.find_element_by_xpath('//*[@id="HistoriqueNegociation1_HistValeur1_Image1"]').click()


#manage the wiating time until the data is on the page
WebDriverWait(driver, 4).until(
      expected_conditions.presence_of_all_elements_located(
    (By.XPATH, '//*[@id="HistoriqueNegociation1_HistValeur1_PnlResultat"]')
  )
)


                                    
table = driver.find_element_by_xpath('/html/body/form/table/tbody/tr[2]/td[2]/table[3]/tbody/tr/td[3]/div/table/tbody/tr[6]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td[2]/table/tbody/tr[1]/td/table/tbody/tr[5]/td/div/table/tbody')


rows = table.find_elements_by_xpath(".//tr")

listRows = []

for row in rows[:10]:
    singleRow = [td.text for td in row.find_elements_by_xpath(".//td")]
    singleRow = list(filter(None,singleRow))
    listRows.append(singleRow)
    
listRows = list(filter(None,listRows))

# transform your list of rows to a pandas dataframe
finalTable=pd.DataFrame(listRows[1:],columns=listRows[0])    

#convert the dataframe to a csv
finalTable.to_csv('myData.csv')

driver.quit()