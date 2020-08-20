
"""
Copyright (c) 2020, Yin Kwong John Lee
All rights reserved.

This is a script to parse the pre-determined Chief Executive Officers (CEO) sentiment from companies' annual reports. Due to large files'

"""

import os
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup 
from PyPDF2 import PdfFileReader
from nltk.stem import PorterStemmer 
from nltk.tokenize import word_tokenize 

#----------Set root working directory------------
report_path=""" directory where folders storing annual reports for all companies are stored """

#--------------Vocab Lists-----------------
    lts_outro=["President and CEO","President & CEO","President and Chief Executive Ofﬁcer","Chief Executive Officer","Sincerely","president and chief executive","Chairman and Chief Executive Ofﬁcer","Alcoa Chairman and CEO","chairman of the board and chief executive","Chairman of the Board and Chief Executive Officer","president & chief executive ofﬁcer"]
    lts_intro=["Dear Investors:","Dear Fellow Investors:","Dear fellow shareholders","To Our Fellow Shareholders","To our shareholders:","To our Stockholders:","Letter to shareholders","Dear Fellow Shareholders,","Dear AMN Healthcare Shareholders,","Building shareholder value","Dear Shareholders","To Our Fellow Shareholders:","CEO’s REVIEW AND OUTLOOK","CEO’S REVIEW","TO ALL SHAREHOLDERS,","FELLOW SHAREHOLDERS,","Letter from the chief executive officer","Message from Our CEO","Message from our Chairman, CEO and President","Letter From the Chairman","T O O U R F ELLOW S HAREHOLDERS","DEAR FELLOW UNITHOLDERS,","Dear fellow STOCKHOLDERS","Letter to STOCKHOLDERS","To Our Shareholders:","To Our Stockholders:","fellow shareholders","Dear Shareholder:","DEAR SHAREHOLDERS:","LETTER TO SHAREHOLDERS:","CHAIRMAN’S LETTER","To our Shareholders and Colleagues,","to the shareholders and employees of adm,","Shareholder Letter","Dear Arista Networks Stockholders:","From the Chairman, President and CEO","Talent as an Art","Management's Letter to Shareholders","Letter to Shareholders (unaudited)","Chairman’s report (unaudited)","chairman’s statement","A Note from Our CEO","A Message to Our Shareholders","To our Fellow Stakeholders, Clients and Brokers:","To Our Valued Shareholders:","TO OUR INVESTORS,","To AT&T Investors","Report to Shareholders","LETTER FR OM THE CHIEF EXECUTIVE OFFICER","Letter to our shareholders From our Chairman and CEO,","For Our Shareholders and Our Customers","To OurStockholders","Fellow Shareholders","Letter from the Chief Executive Officer","TO MY FELLOW SHAREHOLDERS","LETTER TO INVESTORS","DEAR FELLOW AVNET SHAREHOLDER","A Letter From the President","TO OUR SHAREHOLDERS, CUSTOMERS, PARTNERS AND EMPLOYEES:","To our shareholders, employees and customers:","Chairman’s review","Dear Ballantyne Strong Shareholders,","A Message from Chairman and Chief Executive Officer","MESSAGE TO SHAREHOLDERS","MESSAGE TO UNITHOLDERS","MESSAGE FROM THE PRESIDENT & CEO","REPORT TO SHAREHOLDERS","To our shareholders, customers and associates","To the Shareholders of Berkshire Hathaway Inc.:","A MESSAGE FROM HUBERT JOLY, CHAIRMAN & CEO","LETTER TO OUR OWNERS","TO THE SHAREHOLDERS AND EMPLOYEES OF THE BOEING COMPANY","D E A R C O L L E A G U E S A N D F E L L O W S T O C K H O L D E R S ,","TO OUR EMPLOYEES AND STOCKHOLDERS:","As we begin our 45th year of operations, Boyd Gaming Corporation is well-positioned for continued growth and success.","T o O u r S t o c k h o l d e r s a n d O w n e r s","MESSAGE FROM THE BUSINESS LEADER","Message from the Management","Dear Fellow Shareholders, Team Members, Guests, Franchise Partners and Supplier Partners,","To Our Shareholders, Team Members, Guests, Franchise Partners and Supplier Partners:","To all our stakeholders – team members, guests, supplier partners, franchise partners, and shareholders.","Letter from the Chairman and CEO","Dear Valued Cable ONE Stockholders,","To Our Fellow CACI SHAREHOLDERS","Dear Campbell Shareholder,","Fellow Shareowners,","Chairman’s Letter to Shareholders and Friends","Fellow Stockholders:","To Our Shareholders, Clients and Employees:","To Our Shareholders, Customers, and Employees","Dear Shareholders of Cardinal Health:","TO OUR CUSTOMERS, EMPLOYEES AND SHAREHOLDERS:","To Our Fellow Shareholders","TO OUR VALUED SHAREHOLDERS","2019 LETTER TO SHAREHOLDERS","2010 Annual Shareholder Letter","Letter from the CEO","Dear Wells Timberland REIT Stockholder:","To Our Stockholders:","Focusing on S m a r t G r o w t h in premier locations.","Dear Fellow Celanese Stockholders,","Dear Celanese Stockholders:","TO OUR SHAREHOLDERS, CUSTOMERS, SUPPLIERS AND EMPLOYEES","LETTER FROM THE CHAIRMAN","CEO’s Letter","Dear Fellow Stakeholder,","CHAIRMAN AND PRESIDENT/CHIEF EXECUTIVE","OFFICER’S MESSAGE","Dear Fellow CF INDUSTRIES SHAREHOLDERS:","Dear Partners,","Dear Shareowners, Customers, Employees and Friends,","Dear Shareowners, Employees and Friends,","TO ALL WORTHINGTON INDUSTRIES SHAREHOLDERS","To our stockholders, members, government and business partners, and associates:","Dear shareholders,  associates and customers:","Grainger Shareholders:","To my fellow Voya Financial shareholders:","Visteon Shareholders:","From the CEO","DEAR VERISIGN STOCKHOLDERS:","A Message from Our President and Chief Executive Officer","a message from our chairman","with you, the Tyson Shareholders, in mind.","DEAR TRIMAS SHAREHOLDERS","Dear Shareholders, Customers, Partners and Associates:","TO THE OWNERS OF OUR COMPANY:","To our valued shareholders,","Dear Shareholders and Friends,","Dear Fellow Tidewater Shareholders,","Shareholders’ Report","LETTER TO THE SHAREHOLDERS","To the Stockholders of The Dow Chemical Company:","Dear DowDuPont Shareholders,","Clorox Stakeholders:","Clorox Shareholders and Fellow Employees:","Fellow Shareholders and Employees","A Message from the Chairman","Chairman and CEO Letter to  AES Shareholders","DEAR FRIENDS,","To Our Shareowners, Employees and Customers:","DEAR UNITHOLDERS,","A message ¬om our President and CEO to our Shareholders:","A message from our Chairman to our Shareholders","A message from our CEO to our shareholders","A letter from our CEO to our shareholders:","A Letter from Gary B. Smith, President & CEO","A message from our President and CEO, David Cordani","DEAR COLGATE SHAREHOLDERS","DEAR SHAREHOLDERS, CUSTOMERS, PARTNERS AND EMPLOYEES","To Our Shareholders, Employees and Guests","DEAR SHAREHOLDERS, CUSTOMERS, PARTNERS AND EMPLOYEES","To Our Shareholders, Employees and Guests","Letter to Unitholders from the Chairman","Letter to Unitholders","Making a fairer information society","CEO Message","Dear Palo Alto Networks stockholders:","T O  O U R  S H A R E H O L D E R S","CEO’S LETTER TO AES SHAREHOLDERS","CEO’s Letter to AES Shareholders","C H A I R M A N  A N D  C E O  L E T T E R","Chairman and CEO Letter","To Alcoa Shareholders","fellow shareowners","fellow  shareowner","Management’s Reports to Alcoa Shareholders","Dear  Fellow  Shareholders"]
    prevention_raw_terms=['Accuracy','Afraid','Careful','Cautious','Cautiously','Caution','Anxious','Avoid','Avoids','Avoiding','Avoided','Conservative','Defend','Defends','Defended','Defending','Duty','Escape','Escapes','Escaping','Escaped','Evade','Evades','Evading','Evaded','Fail','Fails','Failing','Failed','Fear','Loss','Losing','Losses','Obligation','Ought','Pain','Prevent','Prevents','Prevented','Preventing','Protect','Protects','Protected','Protecting','Responsible','Responsibility','Risk','Risks','Risking','Risked','Safety','Security','Threat','Threats','Threatens','Threatening','Vigilance']
    promotion_raw_terms=['Accomplish','Accomplishes','Accomplished','Accomplishing','Achieve','Achieves','Achieved','Achieving','Advance','Advances','Advancing','Advanced','Advancement','Aspiration','Aspire','Aspires','Aspired','Aspiring','Attain','Attained','Attains','Attaining','Desire','Desired','Desires','Desiring','Earn','Earned','Earns','Earning','Expand','Expands','Expanded','Expanding','Gain','Gains','Gained','Gaining','Grow','Grows','Growing','Growth','Grew','Hope','Hopes','Hoping','Hoped','Ideal','Improve','Improved','Improving','Improves','Increase','Increases','Increased','Increasing','Momentum','Obtain','Obtains','Obtained','Obtaining','Optimistic','Optimism','Progress','Progresses','Progressing','Progressed','Promoting','Promote','Promotes','Promoted','Speed','Swift','Swiftly','Toward','Velocity','Wish','Wishes','Wishing','Wished']

lts_start=list(map(lambda x: x.replace(' ','').replace('/','').replace(r"’","").replace(',','').lower(), lts_intro))
lts_end=list(map(lambda x: x.replace(' ','').replace('/','').replace(r"’","").replace(',','').lower(), lts_outro))
# Word satndardization
prevention_terms=list(map(lambda x: x.replace(' ','').replace('/','').replace(r"’","").replace(',','').lower(), prevention_raw_terms))
promotion_terms=list(map(lambda x: x.replace(' ','').replace('/','').replace(r"’","").replace(',','').lower(), promotion_raw_terms))
# Word stemming
ps = PorterStemmer() 
prevention_stems=set([ps.stem(w) for w in prevention_terms])
promotion_stems=set([ps.stem(w) for w in promotion_terms])

# List storing all the files soon to be parsed
compName=[fn for fn in os.listdir(report_path)]

#----------------Parse Starts Here-------------------------------
# Create containers to store parse data
ticker=[]
cik=[]
ein=[]
ceo_names=[]
fiscal_year=[]
sec_word_count=[]
lts_word_count=[]
promotion_count=[]
prevention_count=[]
promotion_prop=[]
prevention_prop=[]

for cn in compName:
    os.chdir(os.path.join(report_path,cn))
    counter=0
    for ar in os.listdir(os.getcwd()):
        if (ar.endswith(".pdf") and re.compile(r"_(.*?)_").search(ar)):
            ticker_h=re.search("_(.*?)_",ar).group(1)
            ticker.append(ticker_h)
            fiscal_year.append(re.search(r"\d+",ar).group(0))   
            if(counter==0):
                
                try:
                    sec_landing_page=r"http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="+re.search("_(.*?)_",os.listdir(os.getcwd())[-1]).group(1)+"&type=10-k&dateb=&owner=exclude&count=100"
                        
                    # Seeking the company's CIK (Central Index Key) number
                    cik_number=re.search(r"(\d{10})",BeautifulSoup(requests.get(sec_landing_page).content,"html.parser").find("span",{"class":"companyName"}).text)[0]
                except:
                    cik_number=None
                try:
                    # Seeking the company's EIN/IRS
                    sec_filing_table=pd.read_html(str(BeautifulSoup(requests.get(sec_landing_page).content,"html.parser").find("table",{"class":"tableFile2"})))[0]
                    
                    an_accession_number=sec_filing_table[sec_filing_table["Filings"]=="10-K"].head(1).Description.str.extract(r"(\d{10}\-\d{2}\-\d{6})",expand=False).to_list()[0]
                    
                    a_filing_page=r"https://www.sec.gov/Archives/edgar/data/"+cik_number+r"/"+an_accession_number+r"-index.html"
                    
                    ein_number=BeautifulSoup(requests.get(a_filing_page).content,"html.parser").find("p",{"class":"identInfo"}).find("strong").text
                except:
                    ein_number=None
                
                counter=1
                
            cik.append(cik_number)
            ein.append(ein_number)
            try:
                with open(ar,'rb') as tenk:
                    reader =PyPDF2.PdfFileReader(tenk,strict=False)
                    ar_raw_contents=[]
                    ar_contents=[]
                    for pageNum in range(reader.getNumPages()):
                        try:
                            ar_raw_contents.append(reader.getPage(pageNum).extractText().replace('\n','').replace('€',' '))
                            ar_contents.append(reader.getPage(pageNum).extractText().replace('\n','').replace(' ','').replace('/','').replace(r"’","").replace('€',' ').lower())
                            
                        except:
                            ar_raw_contents.append('')
                            ar_contents.append('')  
                    tenk.close()
            except:
                sec_word_count.append(None)
                ceo_names.append(None)
                lts_word_count.append(None)
                promotion_count.append(None)
                prevention_count.append(None)
                promotion_prop.append(None)
                prevention_prop.append(None)
                continue
            # Seeking SEC 10-K word count
            try:
                sec_start_index =['UNITED STATESSECURITIES AND EXCHANGE COMMISSION'.replace('\n','').replace(' ','').lower() in ar_raw_contents[i] for i in range(len(ar_raw_contents))].index(True)
                this_sec_word_count=len(' '.join(ar_raw_contents[sec_start_index:len(ar_raw_contents)+1]).split())
                sec_word_count.append(this_sec_word_count)
            except:
                try:
                    sec_word_count.append(round(len(' '.join(ar_raw_contents).split())*(2/3)))
                except:
                    sec_word_count.append(None)
            
            # Seeking LTS word count
            lts_start_bool=[any(x in ar_contents[i] for x in lts_start) for i in range(len(ar_contents))]
            lts_end_bool=[any(x in ar_contents[i] for x in lts_end) for i in range(len(ar_contents))]
                                
            if(any(lts_start_bool) and any(lts_end_bool)):
                lts_start_true=[t for t, x in enumerate(lts_start_bool) if x]
                lts_end_true=[t for t, x in enumerate(lts_end_bool) if x]
                lts_start_index=lts_start_true[0]
                if(len([i for i in lts_end_true if i >= lts_start_index])>0):
                    lts_end_index=[i for i in lts_end_true if i >= lts_start_index][0]
                    # Seeking CEO name
                    import ner
                    tagger = ner.SocketNER(host='localhost', port=9192, output_format='slashTags')
                    tagged_text=tagger.tag_text(ar_raw_contents[lts_end_index])
                    tagged_tokens = [tuple(ttok.replace('//','/').split('/')) for ttok in tagged_text.split() ]
                    
                    continuous_chunk = []
                    current_chunk = []
                     
                    for token_tag in tagged_tokens:
                        if token_tag[-1] == "PERSON":
                           current_chunk.append((token_tag[-2], token_tag[-1]))
                        else:
                            if current_chunk: # if the current chunk is not empty
                                continuous_chunk.append(current_chunk)
                                current_chunk = []
                  # Flush the final current_chunk into the continuous_chunk, if any.
                    if current_chunk:
                        continuous_chunk.append(current_chunk)
                    try:            
                        ceo_names.append([" ".join([token for token, tag in ne]) for ne in  continuous_chunk][0])
                    except:
                        ceo_names.append(None)
                else:
                    lts_end_index=lts_start_index
                    # Seeking CEO name
                    import ner
                    tagger = ner.SocketNER(host='localhost', port=9192, output_format='slashTags')
                    tagged_text=tagger.tag_text(ar_raw_contents[lts_end_true[0]])
                    tagged_tokens = [tuple(ttok.replace('//','/').split('/')) for ttok in tagged_text.split() ]
                   
                    continuous_chunk = []
                    current_chunk = []
                    
                    for token_tag in tagged_tokens:
                        if token_tag[-1] == "PERSON":
                           current_chunk.append((token_tag[-2], token_tag[-1]))
                        else:
                            if current_chunk: # if the current chunk is not empty
                                continuous_chunk.append(current_chunk)
                                current_chunk = []
                  # Flush the final current_chunk into the continuous_chunk, if any.
                    if current_chunk:
                        continuous_chunk.append(current_chunk)
                    try:            
                        ceo_names.append([" ".join([token for token, tag in ne]) for ne in  continuous_chunk][0])
                    except:
                        ceo_names.append(None)
                        
                # Seeking promotion/prevention word count        
                lts_raw=' '.join(ar_raw_contents[lts_start_index:lts_end_index+1])
                this_lts_word_count=len(lts_raw.split())
                lts_word_count.append(this_lts_word_count)
                try:
                    promotion_count.append(sum([lts_raw.count(promo) for promo in promotion_stems]))
                except:
                    promotion_count.append(None)
                try:
                    promotion_prop.append(sum([lts_raw.count(promo) for promo in promotion_stems])/this_lts_word_count)
                except:
                    promotion_prop.append(None)
                try:
                    prevention_count.append(sum([lts_raw.count(preven) for preven in prevention_stems]))
                except:
                    prevention_count.append(None)
                try:
                    prevention_prop.append(sum([lts_raw.count(preven) for preven in prevention_stems])/this_lts_word_count)
                except:
                    prevention_prop.append(None)

            elif((not any(lts_start_bool)) and (any(lts_end_bool))):
                lts_end_true=[t for t, x in enumerate(lts_end_bool) if x]
            # Seeking CEO name
                import ner
                tagger = ner.SocketNER(host='localhost', port=9192, output_format='slashTags')
                tagged_text=tagger.tag_text(ar_raw_contents[lts_end_true[0]])
                tagged_tokens = [tuple(ttok.replace('//','/').split('/')) for ttok in tagged_text.split() ]
                 
                continuous_chunk = []
                current_chunk = []
                  
                for token_tag in tagged_tokens:
                    if token_tag[-1] == "PERSON":
                       current_chunk.append((token_tag[-2], token_tag[-1]))
                    else:
                        if current_chunk: # if the current chunk is not empty
                            continuous_chunk.append(current_chunk)
                            current_chunk = []
                # Flush the final current_chunk into the continuous_chunk, if any.
                if current_chunk:
                    continuous_chunk.append(current_chunk)
                try:            
                    ceo_names.append([" ".join([token for token, tag in ne]) for ne in  continuous_chunk][0])
                except:
                    ceo_names.append(None)    
                
                lts_word_count.append(None)
                promotion_count.append(None)
                promotion_prop.append(None)
                prevention_count.append(None)
                prevention_prop.append(None)
        
            else:
                ceo_names.append(None)   
                lts_word_count.append(None)
                promotion_count.append(None)
                promotion_prop.append(None)
                prevention_count.append(None)
                prevention_prop.append(None)
                                   

                        
# Construct data frame to store the results                 
sentiment_df=pd.DataFrame({'ticker_h':ticker,'CIK':cik,'IRS':ein,'FY':fiscal_year,'CEO Names':ceo_names,'10-K Total Word Count':sec_word_count,'LTS Total Word Count':lts_word_count,'LTS Promotion Word Count':promotion_count,'LTS Prevention Count':prevention_count,'LTS Promo Words % of LTS Total Word Count':promotion_prop,' LTS Preven Words % of LTS Total Word Count':prevention_prop})  
    

# save mined data to a path
               
sentiment_df.to_csv('ceo_sentiment_final.csv') ## change to the directory which you want to save the interpreted dataframe
     





