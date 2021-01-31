link = input('Enter link : ')

email1 = 'EXAMPLE@email.com'  # Mail Sender's Email


passwrd = 'EXAMPLE_PASSWORD'   # Mail sender's Password


receiver = input('\nEnter Mail Receiver\'s Email id: ')

time_period_in_hours = 12


# PATH TO SAVE FILES -------------------------------------------------------------

path_product_files = 'E:/Winter of Code/Product Details'
path_image_files = 'E:/Winter of Code/Product Images'

#------------------------------------------------------------------------------------

tp = time_period_in_hours
tp_sec = tp*60*60
print('\nPrice will be updated every %0.0f hours ' %tp, end = '')
print('%0.0f minutes' %(int(tp_sec/60)%60))

# CHOOSE ONE OPTION, (1) or (2) for "when to send" email
# 1 : Send only when price decreases
# 2 : At every checkpoint
when_to_send = 2

if(when_to_send == 1):
    print('\n> Mail will be sent only when price decreases')
elif(when_to_send == 2):
    print('\n> Mail will be sent after every %0.0f hours ' %tp, end = '')
    print('%0.0f minutes regardless of change' %(int(tp_sec/60)%60))

# ---------------------------------------------------------------------------------

#Selenium imports here
from logging import currentframe, fatal
from time import sleep, time
import urllib
from explicit.waiter import find_element
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
import itertools
#from explicit import waiter, XPATH
#from explicit.waiter import waiter


#Other imports here
import os
import sys # to exit code
import time
import datetime
import array
import csv

# Email imports
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from base64 import encodebytes




#-------------------------------------------------------------------------------    

def amazon(link):
    
    driver.get(link)

    title_element = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="productTitle"]')))
    #print('Product : ' + title_element.text)
    price_table = WebDriverWait(driver,10).until(EC.visibility_of_any_elements_located((By.XPATH, '//*[@id="price"]/table/tbody/tr')))
    
    deal = 0
    price_element_index = 0
    for i in range(len(price_table)):
        
        #print(price_table[i].get_attribute("id"))
        if(price_table[i].get_attribute('id') == 'priceblock_dealprice_row'):
            deal = 1
            price_element_index = i
        if(deal == 0 and price_table[i].get_attribute('id') == 'priceblock_ourprice_row'):
            price_element_index = i

    # if deal == 1:
    #     print('Deal Going on')

    price_path = '//*[@id="price"]/table/tbody/tr[' + str(price_element_index + 1) + ']/td/span'

    price_elem = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, price_path)))

    price_str = ''
    for i in range(len(price_elem.text)-2):
        if(price_elem.text[i+2] != ','):
            price_str = price_str + price_elem.text[i+2]

    #print('Price : %s' %price_str)
    price_int = float(price_str)

    img_element = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="landingImage"]')))    
    src_product = img_element.get_attribute('src')
    

    return price_int,title_element.text,src_product,deal

# -------------------------------------------------------------------------------------

def flipkart(link):
    
    driver.get(link)

    title_element = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[1]/h1/span')))
    #print('Product : ' + title_element.text)

    # try:
    #     price_elem = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[4]/div[1]/div/div[1]')))

    price_elem = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div//div[1]/div/div[1]')))
    price_str = ''
    for i in range(len(price_elem.text)-1):
        if(price_elem.text[i+1] != ','):
            price_str = price_str + price_elem.text[i+1]

    #print(price_str)
    price_int = float(price_str)
    
    img_element = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="container"]/div/div[3]/div[1]/div[1]/div[1]/div/div[1]/div[2]/div[1]/div[2]/img')))    
    src_product = img_element.get_attribute('src')
    
    return price_int,title_element.text,src_product

# --------------------------------------------------------------------------------------

def snapdeal(link):
    
    driver.get(link)

    title_element = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="productOverview"]/div[2]/div/div[1]/div[1]/div[1]/h1')))
    #print('Product : ' + title_element.text)
    
    price_elem = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="buyPriceBox"]/div[2]/div[1]/div[1]/div[1]/span[1]/span')))
    price_str = ''
    for i in range(len(price_elem.text)):
        if(price_elem.text[i] != ','):
            price_str = price_str + price_elem.text[i]

    #print(price_str)
    price_int = float(price_str)

    img_element = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="bx-slider-left-image-panel"]/li[1]/img')))    
    src_product = img_element.get_attribute('src')

    return price_int,title_element.text,src_product
    
# ---------------------------------------------------------------------------------------

def scrap_price(link):

    price = 0
    site = 'Not Found'
    product_name = 'None Found'
    src_link = ''
    if 'amazon' in link[0:25]:
        price,product_name,src_link,deal = amazon(link)
        site = 'Amazon Product'
    elif 'flipkart' in link[0:25]:
        price,product_name,src_link = flipkart(link)
        site = 'Flipkart Product'
    elif 'snapdeal' in link[0:25]:
        price,product_name,src_link = snapdeal(link)
        site = 'Snapdeal Product'
    return price,product_name,site,src_link

# ---------------------------------------------------------------------------------------

def next_time(tp_sec):
    dt = datetime.datetime.now()
    new_time = dt + datetime.timedelta(seconds=tp_sec)
    return new_time

# ------------------------------------------------------------------------------------------

def send_mail_to(email1,passwrd,receiver,price,product_name,site,diff,link,img_src):
    
    msg = MIMEMultipart()

    msg['Subject '] = 'Price Update :' + product_name[0:30] + '...'
    msg['From'] = email1
    msg['To'] = receiver

    msg1 = ''
    if diff>0:
        msg1 = 'Product price has decreased by : ' + str(diff)
    if diff==0:
        msg1 = 'No Change in Price'
    if diff<0:
        msg1 = 'Product price has increased by : ' + str(-diff) 
    
    body = '''
        <p style="text-align: center;"><em>'''+ site +'''</em></p>
        <p style="text-align: left;">Product name :</p>
        <p style="text-align: left;"><a title="Link" href="'''+ link +'''" target="_blank" rel="noopener">'''+ product_name +'''</a></p>
        <p style="text-align: center;"><img src="'''+ img_src +'''" alt="product image" width="" height="250" /></p>
        <p style="text-align: left;">''' + msg1 +'''</p>
        <p style="text-align: left;">'''+ 'Current Price : ₹ ' + str(int(price)) +'''</p>
    '''
    msg.attach(MIMEText(body,'html'))

    seson = smtplib.SMTP('smtp.gmail.com', 587)
    seson.starttls()
    seson.login(email1,passwrd)
    final_msg = msg.as_string()
    seson.sendmail(email1,receiver,final_msg)
    seson.quit()
    print('> Mail sent to : %s' %receiver)

 
# ----------------------------------------------------------------------------------------

def first_mail(email1,passwrd,receiver,price,product_name,site,link,src_link,tp):
    
    msg = MIMEMultipart()

    msg['Subject'] = 'Subscribed for Price Update for ' + product_name[0:30] + '...'
    msg['From'] = email1
    msg['To'] = receiver

    body = '''
        <p style="text-align: center;"><em>'''+ site +'''</em></p>
        <p style="text-align: left;">Product name :</p>
        <p style="text-align: left;"><a title="Link" href="'''+ link +'''" target="_blank" rel="noopener">'''+ product_name +'''</a></p>
        <p style="text-align: center;"><img src="'''+ src_link +'''" alt="product image" width="" height="250" /></p>
        <p style="text-align: left;">'''+ 'Current Price : ₹ ' + str(int(price)) +'''</p>
        <p style="text-align: left;"><em>You will be updated about changes in the price every ''' + str(tp) + ''' hours</em></p>
    '''

    msg.attach(MIMEText(body,'html'))

    seson = smtplib.SMTP('smtp.gmail.com', 587)
    seson.starttls()
    seson.login(email1,passwrd)
    final_msg = msg.as_string()
    seson.sendmail(email1,receiver,final_msg)
    seson.quit()
    print('> Mail sent to : %s' %receiver)
    

# ----------------------------------------------------------------------------------------

def check_fall(file_name):
    file = open(file_name, 'r')
    list = file.readlines()
    l = len(list)
    l1 = l - 3
    l2 = l - 8
    str1 = list[l1]
    str2 = list[l2]
    diff = - float(str1[0:len(list[l1]) - 1]) + float(str2[0:len(list[l2]) - 1])
    return diff


# -----------------------------------------------------------------------------------------
driver = webdriver.Chrome('E:/Chrome driver/chromedriver_win32/chromedriver.exe')
price,product_name,site,src_link = scrap_price(link)
driver.quit()


print('\n\nWebsite : %s' %site)
print('Product : %s' %product_name)
print('Price(INR) : %0.2f' %price)

# Variables-------------------------------------------------------------

dt = datetime.datetime.now()

count = 0

price_file_name = path_product_files+ '/' + product_name[0:50] + '.txt'
image_file_name = path_image_files + '/' + product_name[0:50] + '.jpg'


# ---------------------------------------------------------------------------------------

# Checking if file already exists ---------------------------------------------------------

file_check = open(price_file_name, 'a+')
file_check.close()

save_in_file = False

file_check = open(price_file_name, 'r+')
content_list = file_check.readlines()
file_check.close()
if(len(content_list) > 4):
    already_exists = 1
    count = int(len(content_list)/5)
    print('\n> File already exists')
    print('> Total Cycles completed : %d' %count)
    next_check = content_list[len(content_list)-1]
    
    time_check = datetime.datetime(int(next_check[0:4]), int(next_check[5:7]) , int(next_check[8:10]) , int(next_check[11:13]) , int(next_check[14:16]) , int(next_check[17:19]) )
    print('> Next check supposed to be at : ' + str(time_check)[0:19] )
    
    if(time_check <= dt):
        save_in_file = True
        print('> Time already passed, Updating Now.')
        file = open(price_file_name, 'a+')
        file.write(site + '\n' + product_name + '\n' + str(price) + '\n')
        file.write(str(dt)[0:19] + '\n')
        file.write(str(next_time(tp_sec))[0:19] + '\n')
        file.close()

        diff = check_fall(price_file_name)

        if(when_to_send == 2):
            send_mail_to(email1,passwrd,receiver,price,product_name,site,diff,link,src_link)
        elif(when_to_send == 1 and diff>0):
            send_mail_to(email1,passwrd,receiver,price,product_name,site,diff,link,src_link)
        
        count = count + 1
        print('> Total Cycles completed : %d' %count)
            

    else:
        some_time_datetime = time_check - dt
        some_time = some_time_datetime.total_seconds()
        print("> Time Left : {} hours {} minutes" .format(int(divmod(some_time, 3600)[0]) ,int(divmod(some_time,60)[0]%60)) )
        
        print('...')
        time.sleep(some_time)
        
        driver = webdriver.Chrome('E:/Chrome driver/chromedriver_win32/chromedriver.exe')
        price,product_name,site,src_link  = scrap_price(link)
        driver.quit()
        
        
        print('\n\nWebsite : %s' %site)
        print('Product : %s' %product_name)
        print('Price(INR) : %0.2f' %price)
        
        file = open(price_file_name, 'a+')
        file.write(site + '\n' + product_name + '\n' + str(price) + '\n')
        file.write(str(dt)[0:19] + '\n')
        file.write(str(next_time(tp_sec))[0:19] + '\n')
        file.close()
        
        diff = check_fall(price_file_name)
        
        if(when_to_send == 2):
            send_mail_to(email1,passwrd,receiver,price,product_name,site,diff,link,src_link)
        elif(when_to_send == 1 and diff>0):
            send_mail_to(email1,passwrd,receiver,price,product_name,site,diff,link,src_link)

        count = count + 1
        print('> Total Cycles completed : %d' %count)

else:
    already_exists = 0
    print('> New File Created.')
    file = open(price_file_name, 'a+')
    file.write(site + '\n' + product_name + '\n' + str(price) + '\n')
    file.write(str(dt)[0:19] + '\n')
    file.write(str(next_time(tp_sec))[0:19] + '\n')
    file.close()
    urllib.request.urlretrieve(src_link ,image_file_name)
    print('> Image Saved')

    first_mail(email1,passwrd,receiver,price,product_name,site,link,src_link,tp)
    
    count = 1
    print('> Total Cycles completed : %d' %count)




# ----------------------------------------------------------------------------------------

# Looping infinitely ----------------------------------------------------------------------

while(True):
    
    print('\n> Now Going to wait for %0.0f hours ' %tp, end = '')
    print('%0.0f minutes' %(int(tp_sec/60)%60))

    print('...')
    time.sleep(tp_sec)

    driver = webdriver.Chrome('E:/Chrome driver/chromedriver_win32/chromedriver.exe')
    price,product_name,site,src_link  = scrap_price(link)
    driver.quit()
    
    
    print('\n\nWebsite : %s' %site)
    print('Product : %s' %product_name)
    print('Price(INR) : %0.2f' %price)
    
    file = open(price_file_name, 'a+')
    file.write(site + '\n' + product_name + '\n' + str(price) + '\n')
    file.write(str(dt)[0:19] + '\n')
    file.write(str(next_time(tp_sec))[0:19] + '\n')
    file.close()
    
    diff = check_fall(price_file_name)
    
    if(when_to_send == 2):
        send_mail_to(email1,passwrd,receiver,price,product_name,site,diff,link,src_link)
    elif(when_to_send == 1 and diff>0):
        send_mail_to(email1,passwrd,receiver,price,product_name,site,diff,link,src_link)

    count = count + 1
    print('> Total Cycles completed : %d' %count)
        





        


# -------------------------------------------------------------------------------------






