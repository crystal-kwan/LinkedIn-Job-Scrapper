#Step 0 : Install packages and import libraries
#--------------------------------------------------------------------
#pip install beautifulsoup4
#pip install wordcloud
import os
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import pandas as pd
import time
from random import uniform
from bs4 import BeautifulSoup
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

#Step 1 : Input search criteria and filters
#--------------------------------------------------------------------
#Input the position you're looking for
position = "Data Scientist"

#Input the job location you're looking for
location = "Hong Kong"

#Filter job posting date
#period = "2592000" #past month
#period = "604800" #past week
period = "86400" #past 24 hours

#Filter experience level
experience ="&f_E=1" #Internship
#experience ="&f_E=2" #Entry-level
#experience ="&f_E=3" #Associate
#experience ="&f_E=2%2C3" #Entry-level + Associate
#experience ="&f_E=4" #Mid-Senior level

position = position.replace(' ', "%20")
location = location.replace(' ', "%20")


#Step 2: Web scraping (Use public Linkedin search)
#--------------------------------------------------------------------
# Open browser
driver_path = "/Users/kwanw4/Downloads/chromedriver"
service = ChromeService(executable_path=driver_path)
browser = webdriver.Chrome(service=service)

# Open LinkedIn jobs search webpage
browser.get(f"https://www.linkedin.com/jobs/search/?keywords={position}&location={location}&geoId=102817007&f_TPR=r{period}{experience}&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0%27")

# waiting load
time.sleep(2)

#no_of_results= int(browser.find_element_by_xpath('//*[@id="main-content"]/div/h1/span[1]').text)

#This code helps scroll through the page to load more results
last_height = browser.execute_script('return document.body.scrollHeight')
for i in range(3):
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(5)
    new_height = browser.execute_script('return document.body.scrollHeight')
    last_height = new_height

the_list = browser.find_element_by_class_name('jobs-search__results-list')
jobs = the_list.find_elements_by_tag_name('li') # return a list of web elements


job_title = []
job_comp = []
job_function = []
job_seniority_level = []
job_industry = []
description = []
disc_list = []

for job in range(1,len(jobs)+1):
    try:
        job_click = browser.find_element_by_xpath(f'//*[@id="main-content"]/section[2]/ul/li[{job}]/div/a').click()
        time.sleep(7)   
        try:   
            job_title0 = browser.find_element_by_xpath('/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/a/h2').text
            job_title.append(job_title0)
        except:
            job_title.append('NIL')
            
        try:             
            job_comp0 = browser.find_element_by_xpath('/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/h4/div[1]/span[1]/a').text
            job_comp.append(job_comp0)
        except:
            job_comp.append('NIL')
            
        try:             
            job_function0 = browser.find_element_by_xpath('/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[3]/span').text
            job_function.append(job_function0)
        except:
            job_function.append('NIL')
            
        try:            
                
            job_seniority_level0 = browser.find_element_by_xpath('/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[1]/span').text
            job_seniority_level.append(job_seniority_level0)
        except:
            job_seniority_level.append('NIL')
        
        try:            
                
            job_industry0 = browser.find_element_by_xpath('/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[4]/span').text
            job_industry.append(job_industry0)
        except:
            job_industry.append('NIL')

        try:
            job_desc = browser.find_element_by_xpath('//*[@id="job-details"]').text
            soup = BeautifulSoup(job_desc.get_attribute(
            'outerHTML'), 'html.parser')
            disc_list.append(job_desc)
        except:
            disc_list.append("dd")
        
    except:
        pass
    
df = pd.DataFrame({
'Company': job_comp,
'Position': job_title,
'Level': job_seniority_level,
'Function': job_function,
'Industry':job_industry
})

        
df.to_csv(('keep_looking_for_jobs.csv'), index=False)

'''   
#Additional feature using BeautifulSoup for job description
        job_desc = browser.find_element_by_class_name('jobs-search__right-rail')
        soup = BeautifulSoup(job_desc.get_attribute(
            'outerHTML'), 'html.parser')
        disc_list.append(soup.text)
''' 
