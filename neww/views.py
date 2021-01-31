from django.http.response import HttpResponse
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from bs4 import *

import datetime
import time
import os


when_to_send = 2

main_path = 'F:/random/'

# Create your views here.

def page_html_content(link):
    print('inside html content function')
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html_page = session.get(f'{link}').text
    return html_page

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

def send_mail(price,product_name,site,src_link,email1,receiver,link,passwrd,time_period_in_hours):
    # Email imports
    import smtplib
    import email
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    from base64 import encodebytes

    msg = MIMEMultipart()
    
    print('product name inside of mail : ' + product_name[0:30])
    msg['Subject'] = 'Subscribed for Price Update for ' + product_name[0:30] + '...'
    msg['From'] = email1
    msg['To'] = receiver

    

    body = '''
        <p style="text-align: center;"><em>'''+ site +'''</em></p>
        <p style="text-align: left;">Product name :</p>
        <p style="text-align: left;"><a title="Link" href="'''+ link +'''" target="_blank" rel="noopener">'''+ product_name +'''</a></p>
        <p style="text-align: center;"><img src="'''+ src_link +'''" alt="product image" width="" height="250" /></p>
        <p style="text-align: left;">'''+ 'Current Price : ₹ ' + str(int(price)) +'''</p>
        <p style="text-align: left;"><em>You will be updated about changes in the price every ''' + str(time_period_in_hours) + ''' hour(s)</em></p>
    '''
    #

    msg.attach(MIMEText(body,'html'))

    seson = smtplib.SMTP('smtp.gmail.com', 587)
    seson.starttls()
    seson.login(email1,passwrd)
    final_msg = msg.as_string()
    seson.sendmail(email1,receiver,final_msg)
    seson.quit()
    print('> Mail sent to : %s' %receiver)

def file_save(msg):
    msg = str(msg)
    print('file msg : ' + msg)
    file = open('somenew thing.txt','w+')
    file.write(msg)
    file.close

def next_time(tp_sec):
    dt = datetime.datetime.now()
    new_time = dt + datetime.timedelta(seconds=tp_sec)
    return new_time

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

#def bg_waiter():

def start_email_timer(product_name,time_left,time_final,receiver):
    print('----------------------------------------')
    import os
    
    path = path_temp + '/temp_name.txt'
    file = open(path, 'w+')
    file.write(product_name[0:50])
    file.write('\n' + str(time_left) + '\n' + str(time_final) + '\n' + receiver )

    file.close()

    os.system('powershell "pythonw -u "f:\\vscodeprojects\djangofirstlearn\hi\\email_timer.py" "')
    print('----------------------------------------')

def file_handling(price,product_name,site,src_link,path_product_files,path_image_files,time_period_in_hours,email1,passwrd,receiver,link):

    #import for img download
    import urllib

    #setting some variables
    dt = datetime.datetime.now() #current datetime
    price_file_name = path_product_files + '/' + product_name[0:50] + '.txt'
    image_file_name = path_image_files + '/' + product_name[0:50] + '.jpg'
    # price_file_name = product_name[0:50] + '.txt'
    # image_file_name = product_name[0:50] + '.jpg'
    tp = time_period_in_hours
    tp_sec = tp*60*60
    print('-----------------------------')
    print('>>> Inside function : file_handling....')

    print('\nPrice will be updated every %0.0f hours ' %tp, end = '')
    print('%0.0f minutes' %(int(tp_sec/60)%60))


    # Makes new empty file if it doesn't exist already
    file_check = open(price_file_name, 'a+')
    file_check.close()

    #opening file to check how much content it has i.e if its empty or not
    file_check = open(price_file_name, 'r+')
    content_list = file_check.readlines()
    file_check.close()

    #if its NOT empty then...    
    # if(len(content_list) > 4):
    #     already_exists = 1
    #     count = int(len(content_list)/7)
    #     print('\n> File already exists')
    #     print('> Total Cycles completed : %d' %count)
    #     next_check = content_list[len(content_list)-1]
        
    #     time_check = datetime.datetime(int(next_check[0:4]), int(next_check[5:7]) , int(next_check[8:10]) , int(next_check[11:13]) , int(next_check[14:16]) , int(next_check[17:19]) )
    #     print('> Next check supposed to be at : ' + str(time_check)[0:19] )
        
    #     if(time_check <= dt):
    #         save_in_file = True
    #         print('> Time already passed, Updating Now.')
    #         file = open(price_file_name, 'a+')
    #         file.write(site + '\n' + product_name + '\n' + str(price) + '\n' + str(link) + '\n' + str(src_link) + '\n' )
    #         file.write(str(dt)[0:19] + '\n')
    #         file.write(str(next_time(tp_sec))[0:19] + '\n')
    #         file.close()

    #         diff = check_fall(price_file_name)

    #         if(when_to_send == 2):
    #             send_mail_to(email1,passwrd,receiver,price,product_name,site,diff,link,src_link)
    #         elif(when_to_send == 1 and diff>0):
    #             send_mail_to(email1,passwrd,receiver,price,product_name,site,diff,link,src_link)
            
    #         count = count + 1
    #         print('> Total Cycles completed : %d' %count)

    #     else:
    #         some_time_datetime = time_check - dt
    #         some_time = some_time_datetime.total_seconds()
    #         print("> Time Left : {} hours {} minutes" .format(int(divmod(some_time, 3600)[0]) ,int(divmod(some_time,60)[0]%60)) )
            
    #         print('...')
    #         time_left = some_time
    #         time_final = tp_sec
    #         start_email_timer(product_name,time_left,time_final)
            
    #         count = count + 1
    #         print('> Total Cycles completed : %d' %count)
    if(len(content_list) > 4):
        print('Email is already subscribed for this product')
        already_exists = 1
        count = int(len(content_list)/7)

        next_check = content_list[len(content_list)-1]
        time_check = datetime.datetime(int(next_check[0:4]), int(next_check[5:7]) , int(next_check[8:10]) , int(next_check[11:13]) , int(next_check[14:16]) , int(next_check[17:19]) )


    else:
        time_check = next_time(tp_sec)
        already_exists = 0
        print('> New File Created.')
        file = open(price_file_name, 'a+')
        file.write(site + '\n' + product_name + '\n' + str(price) + '\n' + str(link) + '\n' + str(src_link) + '\n')
        file.write(str(dt)[0:19] + '\n')
        file.write(str(next_time(tp_sec))[0:19] + '\n')
        file.close()
        urllib.request.urlretrieve(src_link ,image_file_name)
        print('> Image Saved')

        send_mail(price,product_name,site,src_link,email1,receiver,link,passwrd,time_period_in_hours)
        
        count = 1
        print('> Total Cycles completed : %d' %count)
        time_left = tp_sec
        time_final = tp_sec
        start_email_timer(product_name,time_left,time_final,receiver)
        #bg_prog()

    return already_exists,count,time_check







def index(request):
    data = dict()
    if 'link' in request.GET:
        link = request.GET.get('link')
        email1 = 'svevendile@gmail.com'
        passwrd = 'svevendile04@Four'
        receiver = request.GET.get('email')
        global time_period_in_hours
        time_period_in_hours = float(request.GET.get('time_final'))

        print('link = ' + link)
        html = page_html_content(link)
        soup = BeautifulSoup(html, 'html.parser')

        try:
            os.mkdir(main_path + receiver)
            os.mkdir(main_path + receiver + '/products')
            os.mkdir(main_path + receiver + '/images')
            
            
        except:
            print('email already exists')

        global path_product_files,path_image_files,path_temp
        path_product_files = main_path + receiver + '/products'
        path_image_files = main_path + receiver + '/images'
        path_temp = 'F:/random/temp'

        price,product_name,site,src_link = scrap_price(link,soup)
        product_name = product_name.strip()
        data['price'] = price
        data['product_name'] = product_name
        data['site'] = site
        data['img_link'] = src_link

        
        

        print('product name out of mail : ' + product_name)
        price = price[2:len(price)]
        price_str_ref = ''
        for i in range(len(price)):
            if(price[i] != ',' ):
                price_str_ref = price_str_ref + price[i]
        price = price_str_ref

        price = float(price)
        price = int(price)

        print('>>>>>>>>>>>>>>>>>>>>> new refined : ' + str(price))
        send_mail(price,product_name,site,src_link,email1,receiver,link,passwrd,time_period_in_hours)
        
        already_exists,count,time_check = file_handling(price,product_name,site,src_link,path_product_files,path_image_files,time_period_in_hours,email1,passwrd,receiver,link)
        print('\n\n\n\nAlready Exists = ' + str(already_exists))
        print('\n\n\n\nNext Check = ' + str(time_check))
        print('\n\n\n\nCount = ' + str(count))
        pass

    

    return render(request, 'home.html',{'data':data})
    # return HttpResponse("this is neww page")














def about(request):
    a = 2
    b = 2 * a
    context = {
        'i' : str(b)
    }
    return render(request, 'about.html',context)

def services(request):
    a = 2
    b = 2 * a
    context = {
        'i' : str(b)
    }
    return render(request, 'services.html',context)

def contacts(request):
    a = 2
    b = 2 * a
    context = {
        'i' : str(b)
    }
    return render(request, 'contacts.html',context)







# if request.method == 'POST' and 'run_script' in request.POST:

#     # import function to run
#     from path_to_script import function_to_run

#     # call function
#     function_to_run() 

#     # return user to required page
#     return HttpResponseRedirect(reverse(app_name:view_name)
