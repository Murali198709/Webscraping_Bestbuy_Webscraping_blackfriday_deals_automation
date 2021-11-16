#!/usr/bin/env python
# coding: utf-8

# In[278]:


#import pyspark
import pandas as pd
#from pyspark.sql import SparkSession,functions
#from pyspark.sql.types import *
#from pyspark.sql import DataFrame
import re
#spark=SparkSession.builder.appName('learn').getOrCreate()
#from pyspark.sql import regexp_replace
#spark

#!/usr/bin/env python
# coding: utf-8

# In[81]:

from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time
import datetime
import calendar


# In[92]:


products=[] #List to store name of the product
prices=[] #List to store price of the product
ratings=[] #List to store rating of the product
from requests_html import HTMLSession
session = HTMLSession()

driver = webdriver.Chrome(r"/Users/muralitulluri/Documents/Dalplex_webscraping/chromedriver")
driver.get("https://www.bestbuy.ca/en-ca/collection/laptops-on-sale/46082?icmp=computing_20211112_laptops_category_feature_slideshow_shopby_save_on_laptops")
time.sleep(10)
for i in range(100):
    driver.find_element_by_class_name("loadMore_3AoXT").click()
    time.sleep(5)


# In[93]:


content = driver.page_source
soup = BeautifulSoup(content,"html.parser")
#soup=BeautifulSoup(response.content, 'html.parser')
#soup
name=[]
price=[]
name=[a.get_text() for a in soup.findAll("div", {"data-automation":"productItemName"})]
price=[a.get_text() for a in soup.findAll("span", {"class":"screenReaderOnly_3anTj large_3aP7Z"})]
save=[a.get_text() for a in soup.findAll("span", {"data-automation":"product-saving"})]

df = pd.DataFrame({'Product_Name':name,'Price':price,'Save':save}) 
df.to_csv('/Users/muralitulluri/Documents/Best_Buy_Laptops_Black_Friday_Deals.csv', index=False, encoding='utf-8')
                   

#df_spark=spark.read.option('header','true').csv("/Users/muralitulluri/Documents/Best_Buy_Laptops.csv",inferSchema=True)

laptops = pd.read_csv("/Users/muralitulluri/Documents/Best_Buy_Laptops_Black_Friday_Deals.csv")


# In[286]:


#laptops.Product_Name
laptops.Product_Name=laptops.Product_Name.str.replace('2-in-1', '2in1')
laptops.Price=laptops.Price.str.replace('\$', '')
laptops.Save=laptops.Save.str.replace('SAVE \$', '')
laptops.Save=laptops.Save.str.replace(',', '')
laptops['Price']=pd.to_numeric(laptops['Price'])
laptops['Save']=pd.to_numeric(laptops['Save'])
#print(laptop_list)
laptops1=laptops[laptops['Product_Name'].str.contains("Lenovo|HP|Dell")]

Certified_refurbished_laptops1=laptops1[(laptops1['Product_Name'].str.lower()).str.contains("certified refurbished")]
refurbished_laptops1=laptops1[(~(laptops1['Product_Name'].str.lower()).str.contains("certified refurbished")) & ((laptops1['Product_Name'].str.lower()).str.contains("refurbished"))]
OpenBox_laptops1=laptops1[(laptops1['Product_Name'].str.lower()).str.contains("open box")]
new_laptops1=laptops1[(~(laptops1['Product_Name'].str.lower()).str.contains("certified refurbished")) & (~(laptops1['Product_Name'].str.lower()).str.contains("refurbished")) & (~laptops1['Product_Name'].str.contains("Open Box"))]
new_laptops2=new_laptops1[(new_laptops1['Product_Name'].str.contains("8GB RAM|12GB RAM|16GB RAM")) & (new_laptops1['Product_Name'].str.contains("i5|i7")) & (new_laptops1['Product_Name'].str.contains("256GB SSD|512GB SSD"))]

new_openbox_laptops2=OpenBox_laptops1[(OpenBox_laptops1['Product_Name'].str.contains("8GB RAM|12GB RAM|16GB RAM")) & (OpenBox_laptops1['Product_Name'].str.contains("i5|i7")) & (OpenBox_laptops1['Product_Name'].str.contains("256GB SSD|512GB SSD"))]
#new_openbox_laptops2
final_openbox_laptop_list=new_openbox_laptops2[new_openbox_laptops2['Price']<=1100]
final_new_laptop_list=new_laptops2[new_laptops2['Price']<=1100]
x = str(datetime.datetime.now())
filename1='/Users/muralitulluri/Documents/New_Laptops_Best_Buy_'+x+'.xlsx'
final_new_laptop_list.to_excel(filename1,index = False)
filename2='/Users/muralitulluri/Documents/OpenBox_Laptops_Best_Buy_'+x+'.xlsx'
final_openbox_laptop_list.to_excel(filename2,index = False)


# In[245]:


import smtplib,ssl

# Import the email modules we'll need
from email.message import EmailMessage
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate


# In[289]:


smtp_server = 'smtp.gmail.com'
smtp_port = 587
#Replace with your own gmail account
gmail = 'tulluri.murali@gmail.com'
password = '$password'
message = MIMEMultipart('mixed')
message['From'] = 'Contact <{sender}>'.format(sender = gmail)
message['To'] = 'jayalex7001@gmail.com'
message['CC'] = 'tulluri.murali@gmail.com'
message['Subject'] = 'Bestbuy NewLaptops and Open Box laptops under $1100 as of '+x


# In[290]:



try:
	with open(filename1, "rb") as attachment:
		p = MIMEApplication(attachment.read(),_subtype="csv")	
		p.add_header('Content-Disposition', "attachment; filename= %s" % filename1.split("\\")[-1]) 
		message.attach(p)
except Exception as e:
	print(str(e))

try:
	with open(filename2, "rb") as attachment:
		p = MIMEApplication(attachment.read(),_subtype="csv")	
		p.add_header('Content-Disposition', "attachment; filename= %s" % filename2.split("\\")[-1]) 
		message.attach(p)
except Exception as e:
	print(str(e))

msg_full = message.as_string()
context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, smtp_port) as server:
	server.ehlo()  
	server.starttls(context=context)
	server.ehlo()
	server.login(gmail, password)
	server.sendmail(gmail, message['To'].split(";") + (message['CC'].split(";") if message['CC'] else []),msg_full)
	server.quit()

print("email sent out successfully")


# In[ ]:




