hr = 0.001
main_path = 'F:/random/'


#----------------- IMPORTS
print('----------------------------')
import tkinter as tk
import time

from datetime import datetime as ddt
from tkinter.constants import CENTER, LEFT
# ctt = datetime.datetime.now() 
# print(ctt)
# ts = time.time()
# print(ts) 
# tt = datetime.fromtimestamp(ts-60) 
# print(tt)

from bs4 import BeautifulSoup
from bs4 import *

# ------------------------------
def klose():
    r.destroy()

def amazon(soup):
    title_elem = soup.find("span",attrs = {'id':'productTitle'})
    name = title_elem.text
    
    try:
        testing_deal = 1
        price_str = soup.find('span',attrs = {'id' : 'priceblock_dealprice'}).text
    except:
        testing_deal = 0
        print('\nNO DEAL CURRENTLY\n')
        price_str = soup.find('span',attrs = {'id' : 'priceblock_ourprice'}).text
        
    if(testing_deal == 1):
        print('\nDEAL FOUND\n')

    print("price : " + price_str[2:len(price_str)])

    price_str_ref = ''
    for i in range(len(price_str)-2):
        if(price_str[i+2] != ','):
            price_str_ref = price_str_ref + price_str[i+2]
    print(price_str_ref)

    img_src = soup.find("img",{'id':'landingImage'})
    img_link = img_src['data-old-hires']
    print(img_link)

    return price_str,name,img_link

def next_time(tp_sec):
    import datetime
    dt = datetime.datetime.now()
    new_time = dt + datetime.timedelta(seconds=tp_sec)
    return new_time

def page_html_content(link):
    import requests
    print('inside html content function')
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html_page = session.get(f'{link}').text
    return html_page

def scrap_price(link,soup):
    
    price = 0
    site = 'Not Found'
    product_name = 'None Found'
    src_link = ''
    if 'amazon' in link[0:25]:
        price,product_name,src_link = amazon(soup)
        site = 'Amazon'
    elif 'flipkart' in link[0:25]:
        #price,product_name,src_link = flipkart(soup)
        site = 'Flipkart'
    elif 'snapdeal' in link[0:25]:
        #price,product_name,src_link = snapdeal(soup)
        site = 'Snapdeal'

    return price,product_name,site,src_link

def send_mail_to(email1,passwrd,receiver,price,product_name,site,diff,link,img_src):
    # Email imports
    import smtplib
    import email
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    from base64 import encodebytes
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

def check_fall(file_name):
    file = open(file_name, 'r')
    list = file.readlines()
    l = len(list)
    print(l)
    l1 = l - 5
    l2 = l - 12
    str1 = list[l1]
    str2 = list[l2]
    print('str1 : ' + str1 + '\n' + 'str2 : ' + str2)

    diff = - float(str1[0:len(list[l1]) - 1]) + float(str2[0:len(list[l2]) - 1])
    return diff

def check(link,path_new):
    import datetime
    dt = datetime.datetime.now() #current datetime

    html = page_html_content(link)
    soup = BeautifulSoup(html, 'html.parser')

    price,product_name,site,src_link = scrap_price(link,soup)
    product_name = product_name.strip()


    price = price[2:len(price)]
    price_str_ref = ''
    for i in range(len(price)):
        if(price[i] != ',' ):
            price_str_ref = price_str_ref + price[i]
    price = price_str_ref
    price = float(price)
    price = int(price)

    file = open(path_new, 'a+')
    file.write(site + '\n' + product_name + '\n' + str(price) + '\n' + str(link) + str(src_link) + '\n')
    file.write(str(dt)[0:19] + '\n')
    file.write(str(next_time(int(time_total)))[0:19] + '\n')
    file.close()

    diff = check_fall(path_new)

    return price,product_name,site,src_link,diff

def ok():
    print('nothing')

def new_func(labl):

    global counter,sec,path_new

    labl['text'] = 'Checking Price'
    r.update_idletasks()
    
    price,product_name,site,src_link,diff = check(link,path_new)
    
    labl['text'] = 'Sending Mail'
    r.update_idletasks()
    send_mail_to(email1,passwrd,receiver,price,product_name,site,diff,link,src_link)
    
    counter = 66600 + sec
    counter = int(counter)

    labl['text'] = 'Mail Sent, timer starting Again'
    r.update_idletasks()
    time.sleep(2)
    counter_label(labl)

def counter_label(labl):  
    def count():  

        
            
        
        global counter,email1,passwrd,receiver 

        # To manage the intial delay.  

        tt = ddt.fromtimestamp(counter) 
        string = tt.strftime("%H:%M:%S") 
        display=string  

        labl['text']=display   # Or label.config(text=display)  

        # label.after(arg1, arg2) delays by   
        # first argument given in milliseconds  
        # and then calls the function given as second argument.  
        # Generally like here we need to call the   
        # function in which it is present repeatedly.  
        # Delays by 1000ms=1 seconds and call count again.  
        print('counter : ' + str(counter))
        if(counter != 66599):
            labl.after(1000, count) 
            counter = counter - 1
        else:
            print('checking new price')
            
            new_func(labl)
            
            
            

    
    # Triggering the start of the counter.  
    count() 





r = tk.Tk()
title = 'email watch'
r.minsize(500, 500)

sec = hr * 60 * 60
counter = 66600 + sec
counter = int(counter)

labl = tk.Label(r, text="Welcome!", fg="black", font="Verdana 30 bold")  
labl.pack()

email1 = 'svevendile@gmail.com'
passwrd = 'svevendile04@Four'
receiver = 'sarthakpatel2002@gmail.com'

#files
path_temp = main_path + 'temp'

path = path_temp + '/temp_name.txt'
file = open(path,'r')
file_array = file.readlines()
product_temp_name = file_array[0]
time_left = file_array[1]
time_total = file_array[2]
time_left = float(time_left[0:len(time_left)-2])
time_total = float(time_total[0:len(time_total)-2])

receiver = file_array[3]
counter = 66600 + int(time_left)
counter = int(counter)


path_product_files = 'F:/random/'+ receiver +'/products'
path_image_files = 'F:/random/'+ receiver +'/images'

path_new = path_product_files + '/' + product_temp_name[0:len(product_temp_name) - 1] + '.txt'

file = open(path_new,'r')
file_array = file.readlines()
product_info = file_array

print(product_temp_name)
print(product_info)
site = product_info[0]
product_name = product_info[1]
price = product_info[2]

link = product_info[3]
img_src = product_info[4]

#------------------------------------------------------


counter_label(labl)

close = tk.Button(r, text='Close',width=6, command=lambda:klose())  
close.pack(side = 'bottom')

r.mainloop()
