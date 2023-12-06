import requests
from bs4 import BeautifulSoup
from pprint import pprint
from datetime import datetime
 
# datetime object containing current date and time
now = datetime.now()
 
print("now =", now)

# dd/mm/YY H:M:S
dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
print("date and time =", dt_string)

url = 'https://www.cdcr.ca.gov/capital-punishment/condemned-inmate-list-secure-request/'
data = requests.get(url)

inmate_list = []

html = BeautifulSoup(data.text, 'html.parser')
articles = html.select('tr')
#print(articles)
file = open('inmates.txt', 'w')
count = 0
file.write('Last Name,First Name,Age,Age at Offense,Received Date,Sentenced Date,Offense Date,Trial County\n')
print(len(articles))
for tr in articles:
    data = html.select('td')
    inmate = []
    for instance in data:
        print (instance.text, end=' ')
        inmate.append(instance.text)
        count+=1
        file.write(instance.text+',')
        if(count%8==0):
            print('\n')
            file.write('\n')
    inmate_list.append(inmate)
    #print(count)
    if(count>=765):
        print(inmate_list)
        exit()
    