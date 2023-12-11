import pandas as pd
import os.path
import numpy as np

def laplace_mech(v, sensitivity, epsilon):
    return v + np.random.laplace(loc=0, scale=sensitivity / epsilon)

#applying this generalizing function of the days leads to 0 matches being found
def slice_up_and_add_dp(x):
    x = str(x[:10])#make x only the date and not the time
    day = int(x[3:5])
    noisy_day = int(laplace_mech(day,1,1.0))
    return x[:3]+str(noisy_day)+x[5:]

def slice_up_and_add_more_dp(x):
    x = str(x[:10])#make x only the date and not the time
    day = int(x[3:5])
    noisy_day = int(laplace_mech(day,1,0.5))
    year = int(x[-4:])
    noisy_year = int(laplace_mech(year,1,0.5))
    return x[:3]+str(noisy_day)+x[5:]

#applying this generalizing function of the days leads to 0 matches being found
def slice_up_and_generalize_more(x):
    x = str(x[:10])#make x only the date and not the time
    day = int(int(x[3:5])/10)
    x = x[:3]+str(int(day*10))+x[5:]
    return x

#applying this generalizing function of years leads to 0 matches being found
def slice_up_and_generalize_less(x):
    x = str(x[:10])#make x only the date and not the time
    year = int(int(x[-4:])/10)
    x = x[:-4]+str(int(year*10))
    return x


framed_crime = pd.read_csv(os.path.dirname(__file__) + '/../Crime_Data_from_2010_to_2019.csv')#puts crime in a dataframe

framed_crime['Date Rptd'] = framed_crime['Date Rptd'].apply(slice_up_and_add_more_dp)
framed_crime['DATE OCC'] = framed_crime['DATE OCC'].apply(slice_up_and_add_more_dp)

print(framed_crime)

aux_file = open('inmates.txt','r')
aux_dates_occ = []
aux_names = []
aux_dates_rep = []
aux_dates_sent = []
num_criminals = 0
aux_file.readline()
for line in aux_file.readlines():
    split = line.split(',')
    aux_names.append(split[1]+' '+split[0])
    aux_rep_date = split[4]
    aux_dates_rep.append(aux_rep_date)
    aux_date_sent = split[5]
    aux_dates_sent.append(slice_up_and_add_more_dp(aux_date_sent))
    aux_occ_date = split[6]
    aux_dates_occ.append(slice_up_and_add_more_dp(aux_occ_date))
    num_criminals+=1

possible_matches = 0
for i in range(1,len(aux_dates_sent)):
    if(int(aux_dates_rep[i][-4:])>2009 and int(aux_dates_rep[i][-4:])<2020):
        possible_matches+=1
print("There are",possible_matches,"possible matches to find")

count = 0#keeps track of index of aux_dates_rep
perfect_matches = 0
half_chance_matches = 0
for date in aux_dates_rep:
    date = str(date[:10])
    if(date in framed_crime['Date Rptd'].values):
        #print('\n\n'+date)
        matches = [i for i in range(len(framed_crime['Date Rptd'])) if(framed_crime['Date Rptd'][i]==date and (framed_crime['DATE OCC'][i] == aux_dates_sent[count]))]
        #print(matches)
        if(len(matches)==1):#we know thier info
            print("We likely linked the name of this offender with thier crime")
            #print(matches[0],framed_crime['Date Rptd'][matches[0]],date,framed_crime['Date Rptd'][matches[0]])
            print(aux_names[count],framed_crime['DATE OCC'][matches[0]],aux_dates_sent[count],framed_crime['Crm Cd Desc'][matches[0]],framed_crime['Weapon Desc'][matches[0]])
            print('\n\n')
            perfect_matches+=1
        if(len(matches)==2):#we know thier info
            print("We less \nlikely linked the name of this offender with thier crime")
            #print(matches[0],framed_crime['Date Rptd'][matches[0]],date,framed_crime['Date Rptd'][matches[0]])
            print(aux_names[count],framed_crime['DATE OCC'][matches[0]],aux_dates_sent[count],framed_crime['Crm Cd Desc'][matches[0]],framed_crime['Weapon Desc'][matches[0]])
            print(aux_names[count],framed_crime['DATE OCC'][matches[1]],aux_dates_sent[count],framed_crime['Crm Cd Desc'][matches[1]],framed_crime['Weapon Desc'][matches[1]])
            print('\n\n')
            half_chance_matches+=1
        # else: #prints out all potential matches
        #     print("This offender likely committed at least one of these crimes, but we do not know which one")
        #     for i in range(len(framed_crime['Date Rptd'].values)):    
        #         if(framed_crime['Date Rptd'][i]==date and (framed_crime['DATE OCC'][i] == aux_dates_sent[count])):
        #             #print(i,framed_crime['Date Rptd'][i],date,framed_crime['Date Rptd'][i])
        #             print(aux_names[count],framed_crime['DATE OCC'][i],aux_dates_sent[count],framed_crime['Crm Cd Desc'][i])
    count+=1
print('we were able to find',perfect_matches,'matches linked through the two datasets out of',possible_matches,'possible crimes after 2009.',perfect_matches/possible_matches,'%')
print('we were able to find',half_chance_matches,'matches linked through the two datasets out of',possible_matches,'possible crimes after 2009.',(perfect_matches+half_chance_matches)/possible_matches,'%')
