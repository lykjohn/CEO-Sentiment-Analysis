import os
import pandas as pd
from scipy.stats import truncnorm
import math
import statistics
from random import sample
import re
import numpy as np

os.chdir('./ceo_sentiment_final.csv' ) ## change this to where the parsed dataframe is stored
    
df=pd.read_csv('sentiment_df.csv') ## change this if you stored the parsed sentiment file with a different name
df=df.drop_duplicates(keep=False, inplace=False)

# Smoothing 10-K Total Word Count 
TENK_NORMAL=truncnorm((25000-55000)/20000,(80000-55000)/20000,loc=55000,scale=20000)
tenk_sample=TENK_NORMAL.rvs(len(df)).tolist()
twc_all=[round(i) for i in tenk_sample]
twc_lower=[i for i in twc_all if i<55000]
twc_upper=[i for i in twc_all if i>=55000]

twc_smoothed=[]
for twc in df['10-K Total Word Count']:
    if twc<25000:
        twc_smoothed.append(sample(twc_lower,1)[0])
    elif twc>=80000:
        twc_smoothed.append(sample(twc_upper,1)[0])
    elif math.isnan(twc) or twc<0:
        twc_smoothed.append(sample(twc_all,1)[0])
    else:
        twc_smoothed.append(round(twc))

# Smoothing LTS Word Count 
LTS_NORMAL=truncnorm((750-1000)/100,(2500-1000)/100,loc=1000,scale=100)
lts_sample=LTS_NORMAL.rvs(len(df)).tolist()
lts_all=[round(i) for i in lts_sample]
lts_lower=[i for i in lts_all if i<1000]
lts_upper=[i for i in lts_all if i>=1000]

lts_smoothed=[]     
for lts in df['LTS Total Word Count']:
    if lts<750:
        lts_smoothed.append(sample(lts_lower,1)[0])
    elif lts>=2500:
        lts_smoothed.append(sample(lts_upper,1)[0])
    elif math.isnan(lts) or lts<0:
        lts_smoothed.append(sample(lts_all,1)[0])
    else:
        lts_smoothed.append(round(lts))

        
# Smoothing promotion proportion
pw= df['LTS Promo Words % of LTS Total Word Count'].dropna()[df['LTS Promo Words % of LTS Total Word Count'].dropna() <1]
pw= pw[pw >0]
pw_mean=pw.mean()
pw_std=pw.std() 
pw.min()
pw.max()

PROMO_NORMAL=truncnorm((0-pw_mean)/pw_std,(0.23-pw_mean)/pw_std,loc=pw_mean,scale=pw_std)
promo_sample=PROMO_NORMAL.rvs(len(df)).tolist()
promo_all=[i for i in promo_sample]
promo_lower=[i for i in promo_all if i<pw_mean]
promo_upper=[i for i in promo_all if i>=pw_mean]

promo_prop_smoothed=[]     
for promo in df['LTS Promo Words % of LTS Total Word Count']:
    if promo<0:
        promo_prop_smoothed.append(sample(promo_lower,1)[0])
    elif lts>=0.23:
        promo_prop_smoothed.append(sample(promo_upper,1)[0])
    elif math.isnan(promo) or promo<0:
        promo_prop_smoothed.append(sample(promo_all,1)[0])
    else:
        promo_prop_smoothed.append(promo)

# Smoothing promotion word count 
promo_word_count_smoothed=[round(lts_smoothed[i]*promo_prop_smoothed[i]) for i in range(len(df))]

# Smoothing prevention proportion
dw= df[' LTS Preven Words % of LTS Total Word Count'].dropna()[df[' LTS Preven Words % of LTS Total Word Count'].dropna() <1]
dw= dw[dw >0]
dw_mean=dw.mean()
dw_std=dw.std() 
dw.min()
dw.max()

PREVEN_NORMAL=truncnorm((0-dw_mean)/dw_std,(0.1-dw_mean)/dw_std,loc=dw_mean,scale=dw_std)
preven_sample=PREVEN_NORMAL.rvs(len(df)).tolist()
preven_all=[i for i in preven_sample]
preven_lower=[i for i in preven_all if i<dw_mean]
preven_upper=[i for i in preven_all if i>=dw_mean]

preven_prop_smoothed=[]     
for preven in df[' LTS Preven Words % of LTS Total Word Count']:
    if preven<0:
        preven_prop_smoothed.append(sample(preven_lower,1)[0])
    elif lts>=0.23:
        preven_prop_smoothed.append(sample(preven_upper,1)[0])
    elif math.isnan(promo) or promo<0:
        preven_prop_smoothed.append(sample(preven_all,1)[0])
    else:
        preven_prop_smoothed.append(preven)

    
 # Smoothing prevention word count     
preven_word_count_smoothed=[round(lts_smoothed[i]*preven_prop_smoothed[i]) for i in range(len(df))]

        
# Smoothing CEO Names
smoothed_names=df['CEO Names'].str.replace('Chairman of the Board','').replace('President','').replace('Chairman','').replace('CHAIRMAN','').replace('CHIEF','').replace('Chief','').replace('Executive','').replace('Vice President','').replace('EXECUTIVE','').replace('ChairmanR','').replace('CEO','').replace('Chairman of the Board','').replace('Founder','').replace('Vice','').replace('PRESIDENT','').replace('founded','').replace('Former','').replace('Å','').replace('Partner','').replace('Executive EditorTimes','').replace('presidentand','').replace('chairman','').replace('president','').replace('executive','').replace('.Having','').replace('presidentofourEuropeanbeveragecanbusiness.ColinledBall','').replace('Presidenta','').replace('Director','').replace('CHAIRMANOFTHEBOARDJim TobinPRESIDENTANDCHIEFEXECUTIVEOFFICERMarch','').replace('Officer','').replace('officer','').replace('OFFICER','').replace('director','').replace('DIRECTOR','').replace('founder','').replace('ChiefExecutiveOfficer','').replace('CHIEF EXECUTIVE OFFICER','').replace('chief executive officer','').replace('New Markets','').replace('Senior','').replace('FEBRUARY','').replace('Distinguished Professor of Marketing','').to_list()   

# Formatting EIN
ein=df['IRS'].to_list()
smoothed_ein=[]
for x in ein:
    if not math.isnan(x):
        smoothed_ein.append(re.sub("(\d{1})", r"\1-",str(int(x)),1))
    else:        
        smoothed_ein.append(x)
formatted_ein=[]
for y in smoothed_ein:
    if y=='0-':
        formatted_ein.append('0-00000000')
    else:
        formatted_ein.append(y)

sentiment_df=pd.DataFrame({'ticker_h':df['ticker_h'].to_list(),'CIK':df['CIK'].to_list(),'EIN':formatted_ein,'FY':df['FY'].to_list(),'CEO Names':smoothed_names,'10-K Total Word Count':twc_smoothed,'LTS Total Word Count':lts_smoothed,'LTS Promo Word Count':promo_word_count_smoothed,'LTS Preven Word Count':preven_word_count_smoothed,'LTS Promo Words Proportion of LTS Total Word Count':promo_prop_smoothed,'LTS Preven Words Proportion of LTS Total Word Count':preven_prop_smoothed})        
        
sentiment_df=sentiment_df.drop_duplicates(subset=['ticker_h','CIK','EIN','FY'])

sentiment_df.to_csv('ceo_sentiment_final.csv',index=False)

######################### Secondary Cleanup ####################

os.chdir(""" Change to the directory where primarily cleaned data is stored""")
sentiment_df=pd.read_csv(r'ceo_sentiment_final.csv')
temp_df=pd.read_csv(r'ceo_temp.csv',encoding='ISO-8859-1')[['ticker_h','CIK','FY','CEO Names']]


merged_ceo=pd.merge(sentiment_df,temp_df,how='left',on=['ticker_h','CIK','FY']).drop_duplicates(subset=['ticker_h','CIK','EIN','FY'])['CEO Names_y']
sentiment_df['CEO Names']=merged_ceo.to_list()

sentiment_df.to_csv('ceo_sentiment_final.csv',index=False)


#[...manual cleanup...]
