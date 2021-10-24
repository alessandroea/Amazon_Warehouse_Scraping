import csv
from bs4 import BeautifulSoup
from selenium import webdriver

def get_url(search_term):
    template = 'https://www.amazon.it/s?k={}&i=electronics&bbn=3581999031&dcref=nb_sb_noss_1'
    search_term = search_term.replace(' ','+')
    url = template.format(search_term)
    url += '&page{}'
    
    return url

def extract_record(item):
    atag = item.h2.a
    description = atag.text
    url = 'https://www.amazon.com' + atag.get('href')    

    try:
        price_parent = item.find('div', 'a-section a-spacing-none a-spacing-top-mini')
        price_parent2 = price_parent.find('div', 'a-row a-size-base a-color-secondary')
        price = str(price_parent2.find('span', 'a-color-base').text)
    except AttributeError:
        return
     
    try:
        rating = item.i.text
        review_count = item.find('span', {'class': 'a-size-base'}).text
    except AttributeError:
        rating = ''
        review_count = ''   
       
    result = (description, price, rating, review_count, url)
    
    return result

def main(search_term):
    driver = webdriver.Chrome()
    records = []
    url = get_url(search_term)
    for page in range(1,21):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')   
        results = soup.find_all('div', {'data-component-type': 's-search-result'})
        for item in results:
            record = extract_record(item)
            if record:
                records.append(record)        
    driver.close()
    with open('amazonscraping_ws.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Description', 'Price', 'Rating', 'ReviewCount', 'Url'])
        writer.writerows(records)

product_to_search = 'YOUR PRODUCT'
min_budget = MIN BUDGET
max_budget = MAX BUDGET

main(product_to_search)


import pandas as pd
interest = pd.read_csv('amazonscraping_ws.csv')
interest["Price"] = interest["Price"].str[:-5]
interest["Price"] = interest["Price"].str.replace('.','')
interest["Price"] = pd.to_numeric(interest["Price"])
interest['Description'] = interest['Description'].str.lower()
interest = interest[interest['Description'].str.contains(product_to_search)]
interest = interest.sort_values(by = ["Price"], axis=0, ascending=True, ignore_index=True)
filtered_data = interest[(interest["Price"] > min_budget) & (interest["Price"] < max_budget)]
filtered_data.reset_index(drop=True, inplace=True)
filtered_data_email = filtered_data.copy()
filtered_data_email['Description'] = filtered_data_email['Description'].str[:21]
Table_for_Email = filtered_data_email[['Description', 'Price', 'Url']].head(1)
link = (Table_for_Email['Url']) 
link = (link.to_string(index=False, header=False))

message = 'Hi Ale, I just found a new deal for you for iphone 12; Check it here:  ' + '\n' + link

check_df_empty = 2
if filtered_data.empty:
    check_df_empty = 0
else:
    check_df_empty = 1


def sending_alert():
    import smtplib
    from email.message import EmailMessage
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = 'Deal found on Amazon'
    msg['From'] = "SENDER@GMAIL.COM"
    msg['To'] = "RECEIVER"

    try:    
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login("SENDER@GMAIL.COM", "PASSWORD GMAIL")
        server.send_message(msg)
        server.quit()      
        print('Email sent!')
        
    except:
        print('Something went wrong...')    
        
if (check_df_empty==1):
    sending_alert()   
elif (check_df_empty==0):
    print("No result...")
else:
    print("Something went wrong!")
        
import os
os.remove('amazonscraping_ws.csv') 




