from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import pandas as pd
import time
PATH = r"C:\Users\madal\Desktop\seleniumScrap\chromedriver.exe"
driver = webdriver.Chrome(PATH)

HOME = "https://www.leaflabcannabis.com/"
driver.get(HOME)
pagination = driver.find_elements(By.CLASS_NAME,"_2k7xj")
globalJSON = {'Type':{},'Brand':{},'Product':{},'imgURL':{},'THC':{},'CBD':{},'Effects':{},'Description':{},'ProductUrl':{}}
pageIndex = 0
for link in pagination:
   
    if(link.text != "Subscribe Now" and link.text != "Accessories" and link.text != "Shop All" and link.text != "Shop Now"):
        print(link.text)
        currentWindowLink = link.get_attribute('href')
        driver.execute_script(f'''window.open("{link.get_attribute('href')}","_blank");''')
        driver.switch_to.window(driver.window_handles[1])
        print(driver.title)
        try:
                element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "desktop-product-list-item__ProductInfoContainer-sc-8wto4u-4"))
                )
        finally: 
            # Code for when there is no pagination
            if(len(driver.find_elements(By.CLASS_NAME,"pagination-controls__PageButton-sc-1436mnk-0")) == 0):
                try:
                    element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "desktop-product-list-item__ProductInfoContainer-sc-8wto4u-4"))
                    )
                finally: 
                        listings = driver.find_elements(By.CLASS_NAME,"desktop-product-list-item__ProductInfoContainer-sc-8wto4u-4")
                        for listing in listings:
                            pageIndex += 1
                            # you should go to the detils page here
                        
                            productUrl = listing.get_attribute('href')     
                            driver.execute_script(f'''window.open("{listing.get_attribute('href')}","_blank");''')
                            driver.switch_to.window(driver.window_handles[2])
                            try:
                                element = WebDriverWait(driver, 20).until(
                                EC.presence_of_element_located((By.CLASS_NAME, "product-image__LazyLoad-sc-16rwjkk-0"))
                                )
                            finally:
                                description = ''
                                effects = ""
                                infoListLabels = ['type','THC','CBD']
                                product = {}
                                infoChips =  driver.find_elements(By.CLASS_NAME,'info-chip__InfoChipText-sc-11n9ujc-0')
                                product['brand'] = driver.find_element_by_class_name('typography__Brand-sc-1q7gvs8-2').text
                                product['productName'] =  driver.find_element_by_class_name('typography__Name-sc-1q7gvs8-3').text
                                product['imgUrl'] = imgUrl =  driver.find_element_by_class_name("product-image__LazyLoad-sc-16rwjkk-0").get_attribute('src')
                                descriptionContainer = driver.find_element_by_class_name("sanitized-html__Wrapper-fpulka-0").get_attribute('innerHTML')
                                soup = BeautifulSoup(descriptionContainer,"lxml")
                                for text in soup.find_all("p"):
                                    description += f'{text.text},'
                             
                                product["description"] = description   
                                for i,info in enumerate(infoChips):
                                    product[infoListLabels[i]] = info.text
                                for i,effect in enumerate(driver.find_elements(By.CLASS_NAME,"effect-tile__Text-sc-1as4rkm-1")):
                                    if(i == 0):
                                        effects += effect.text
                                    else:
                                        effects += f',{effect.text}'
                                product["effects"] = effects 
                              
                                # print(product)
                                # {'Brand':{},'Product':{},'imgURL':{},'THC':{},'CBD':{},'Effects':{},'Description':{}}
                                globalJSON['Type'][pageIndex] = product.get('type','E')    
                                globalJSON['Brand'][pageIndex] = product.get('brand','E')    
                                globalJSON['Product'][pageIndex] = product.get('productName','E')    
                                globalJSON['imgURL'][pageIndex] = product.get('imgUrl','E')    
                                globalJSON['THC'][pageIndex] = product.get('THC','E')    
                                globalJSON['CBD'][pageIndex] = product.get('CBD','E')    
                                globalJSON['Effects'][pageIndex] = product.get('effects','E')    
                                globalJSON['Description'][pageIndex] = product.get('description','E') 
                                globalJSON['ProductUrl'][pageIndex] = productUrl    
                                print(globalJSON)
                            driver.execute_script(f'''window.close();''')   
                            driver.switch_to.window(driver.window_handles[1]) 

        
            else:
                print("has pagination")
                lastpageindex = len(driver.find_elements(By.CLASS_NAME,"pagination-controls__PageButton-sc-1436mnk-0")) - 1
                for i,page in enumerate(driver.find_elements(By.CLASS_NAME,"pagination-controls__PageButton-sc-1436mnk-0")):
                    try:
                        element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "desktop-product-list-item__ProductInfoContainer-sc-8wto4u-4"))
                        )
                    finally: 
                        listings = driver.find_elements(By.CLASS_NAME,"desktop-product-list-item__ProductInfoContainer-sc-8wto4u-4")
                        for listing in listings:
                            pageIndex += 1
                            # print(link1.text)
                            # you should go to the detils page here
                            productUrl = listing.get_attribute('href')   
                            driver.execute_script(f'''window.open("{listing.get_attribute('href')}","_blank");''')
                            driver.switch_to.window(driver.window_handles[2])
                            try:
                                element = WebDriverWait(driver, 20).until(
                                EC.presence_of_element_located((By.CLASS_NAME, "product-image__LazyLoad-sc-16rwjkk-0"))
                                )
                            finally:
                                description = ''
                                effects = ""
                                infoListLabels = ['type','THC','CBD']
                                product = {}
                                infoChips =  driver.find_elements(By.CLASS_NAME,'info-chip__InfoChipText-sc-11n9ujc-0')
                                product['brand'] = driver.find_element_by_class_name('typography__Brand-sc-1q7gvs8-2').text
                                product['productName'] =  driver.find_element_by_class_name('typography__Name-sc-1q7gvs8-3').text
                                product['imgUrl'] = imgUrl =  driver.find_element_by_class_name("product-image__LazyLoad-sc-16rwjkk-0").get_attribute('src')
                                descriptionContainer = driver.find_element_by_class_name("sanitized-html__Wrapper-fpulka-0").get_attribute('innerHTML')
                                soup = BeautifulSoup(descriptionContainer,"lxml")
                                for text in soup.find_all("p"):
                                    description += f'{text.text},'
                             
                                product["description"] = description   
                                for i,info in enumerate(infoChips):
                                    product[infoListLabels[i]] = info.text
                                for i,effect in enumerate(driver.find_elements(By.CLASS_NAME,"effect-tile__Text-sc-1as4rkm-1")):
                                    if(i == 0):
                                        effects += effect.text
                                    else:
                                        effects += f',{effect.text}'
                                product["effects"] = effects 
                            
                                # print(product)
                                globalJSON['Type'][pageIndex] = product.get('type','E')    
                                globalJSON['Brand'][pageIndex] = product.get('brand','E')    
                                globalJSON['Product'][pageIndex] = product.get('productName','E')    
                                globalJSON['imgURL'][pageIndex] = product.get('imgUrl','E')    
                                globalJSON['THC'][pageIndex] = product.get('THC','E')    
                                globalJSON['CBD'][pageIndex] = product.get('CBD','E')    
                                globalJSON['Effects'][pageIndex] = product.get('effects','E')    
                                globalJSON['Description'][pageIndex] = product.get('description','E') 
                                globalJSON['ProductUrl'][pageIndex] = productUrl    
                                print(globalJSON)
                            driver.execute_script(f'''window.close();''')   
                            driver.switch_to.window(driver.window_handles[1]) 

                    if(i < lastpageindex): 

                        driver.get(f"{currentWindowLink}?page={i+2}")
                    
            
            
        driver.execute_script(f'''window.close();''')   
        driver.switch_to.window(driver.window_handles[0])
                       

# Dump csv files here
json_object = json.dumps(globalJSON, indent = 4) 
print(json_object)
with open("LeafLabData.json", "w") as outfile: 
            json.dump(globalJSON, outfile) 
        
df = pd.read_json (r'LeafLabData.json')
df.to_csv (r'LeafLabData.csv', index = None)
  
   
       
  
   

            
 


