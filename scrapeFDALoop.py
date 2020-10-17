#!/usr/bin/env python
# coding: utf-8

# In[7]:


from string import ascii_lowercase
from lxml.html import document_fromstring
import re
import csv  
import requests




# with open(filename, 'w') as csvfile:  
#     csvwriter = csv.writer(csvfile) 
#     csvwriter.writerow(fields)  


def cleanstring(query):
    query = query.strip()
    query = re.sub('\s{2,}', ' ', query)
    query = re.sub(r'^"|"$', '', query)
    return query

base_path = 'https://www.accessdata.fda.gov'
url_letter_drug_list = base_path + '/scripts/cder/daf/index.cfm?event=browseByLetter.page&productLetter='


def get_drug_urls(letter):
    headers = {
        'authority': 'www.accessdata.fda.gov',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': '_ga=GA1.2.1366941960.1599163405; _gid=GA1.2.935261669.1599163405; BIGipServerPOOL-207.97.254.104-81=2353899712.20736.0000',
    }
    response = requests.get(url_letter_drug_list + letter, headers=headers)
    doc = document_fromstring(response.content)
    list_drugs_html = doc.xpath("//table//li/a/@href")
    return list_drugs_html



# list_drug_url_a = get_drug_urls('a')


# list_drug_url_a


def get_drug_data(app_path):
    # print(app_path)
    headers = {
        'authority': 'www.accessdata.fda.gov',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': '_ga=GA1.2.1366941960.1599163405; _gid=GA1.2.935261669.1599163405; BIGipServerPOOL-207.97.254.104-81=2353899712.20736.0000',
    }

    drug_response = requests.get(app_path, headers=headers)
    drug_doc = document_fromstring(drug_response.content)
    company_name = drug_doc.xpath("//div[contains(@class, 'panel-group')]//span[contains(@class, 'appl-details-top')]")[1].text_content()
    company_name = cleanstring(company_name)
    # company_name

    application_type = drug_doc.xpath("//div[contains(@class, 'panel-group')]//span[contains(@class, 'prodBoldText')]")[0].text_content()
    application_type = cleanstring(application_type)
    # application_type

    application_number = drug_doc.xpath("//div[contains(@class, 'panel-group')]//span[contains(@class, 'appl-details-top')]")[0].text_content()
    application_number = cleanstring(application_number)
    # application_number
    
    tables_drug_data = drug_doc.xpath("//div[contains(@class, 'panel-info')]//tbody")
    variety_of_drugs_table = tables_drug_data[0]
    variety_of_drugs_table
    variety_type = variety_of_drugs_table.xpath(".//tr")
    try:
        fda_application_of_drugs_table = tables_drug_data[1]
        fda_application_of_drugs_table
        original_submission_details = fda_application_of_drugs_table.xpath(".//tr")

        osd = original_submission_details[0]
        action_date=cleanstring(osd.xpath("./td")[0].text_content())
        submission=cleanstring(osd.xpath("./td")[1].text_content())
        action_type=cleanstring(osd.xpath("./td")[2].text_content())
        submission_classification=cleanstring(osd.xpath("./td")[3].text_content())
        review_priority_orphan_status=cleanstring(osd.xpath("./td")[4].text_content())
        notes=cleanstring(osd.xpath("./td")[6].text_content())
        try:
            org_label_path = osd.xpath(".//td")[5].xpath(".//a[contains(@title,'Links to Label')]/@href")[0]
        except:
            org_label_path = "NA"
        try:
            org_letter_path = osd.xpath(".//td")[5].xpath(".//a[contains(@title,'Links to Letter')]/@href")[0]
        except:
            org_letter_path = "NA"
        try:
            org_review_path = osd.xpath(".//td")[5].xpath(".//a[contains(@title,'Links to Review')]/@href")[0]
        except:
            org_review_path = "NA"
    except:
        action_date = "NA"
        submission= "NA"
        action_type= "NA"
        submission_classification= "NA"
        review_priority_orphan_status= "NA"
        org_label_path= "NA"
        org_letter_path= "NA"
        org_review_path = "NA"


    drug_data_all = []

    
    
    for var in variety_type:
        drug_name=cleanstring(var.xpath("./td")[0].text_content())
        active_ingredients=cleanstring(var.xpath("./td")[1].text_content())
        strength=cleanstring(var.xpath("./td")[2].text_content())
        form_route=cleanstring(var.xpath("./td")[3].text_content())
        marketing_status=cleanstring(var.xpath("./td")[4].text_content())
        te_code=cleanstring(var.xpath("./td")[5].text_content())
        rld=cleanstring(var.xpath("./td")[6].text_content())
        rs=cleanstring(var.xpath("./td")[7].text_content())
        drug_data_all.append([app_path, 
                        company_name, 
                        drug_name, 
                        application_type, 
                        active_ingredients,
                        strength,
                        form_route,
                        marketing_status,
                        te_code,
                        rld,
                        rs,
                        application_number,
                        action_date,
                        submission,
                        action_type,
                        submission_classification,
                        review_priority_orphan_status,
                        org_label_path,
                        org_letter_path,
                        org_review_path
                         ])
    return drug_data_all
        # print(drug_data)
    


def scrape_all():
    fields = ['drug_fda_url','company', 
        'drug_name', 
        'app_type', 
        'active_ingredients',
        'strength',
        'form_route',
        'marketing_status',
        'te_code',
        'rld',
        'rs',
         'app_number',
         'submission_data',
         'submission',
         'action_type',
         'submission_classification',
         'review_priority_orphan_status',
         'label_path',
         'letter_path',
         'review_path'
         ]  

    with open('drug_data_fda.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(fields)
        # i = 0 
        # writer.writerow([1, "Linus Torvalds", "Linux Kernel"])
        for letter in ascii_lowercase:
            list_drug_url = get_drug_urls(letter)
            total_in_letter = len(list_drug_url)
            i = 0 
            for path in list_drug_url:
                # if i <= 40:
                app_path = base_path + path
                data_drug = get_drug_data(app_path)
                for data in data_drug:
                    writer.writerow(data)
                i = i + 1
                print(letter + ' | ' + str(i) + '/' + str(total_in_letter) + ' complete')
                        # i = i + 1





# filename = "drug_fda_records.csv"

# with open('drug_data.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(fields)




# %%
