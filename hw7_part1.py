# 507/206 Homework 7 Part 1
import requests
import json
from bs4 import BeautifulSoup

#### Your Part 1 solution goes here ####

#Implement Cache
CACHE_FNAME = 'umsi_cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

except:
    CACHE_DICTION = {}

def make_request_using_cache(url):
    unique_ident = url
    headers = {'User-Agent': 'SI_CLASS'}

    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]
    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(url, headers=headers)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]

#get faculty information from contact link
def get_fac_info(node):
	base_url = "https://www.si.umich.edu"
	contact_url = base_url + node
	page_text = make_request_using_cache(contact_url)
	faculty_soup = BeautifulSoup(page_text, "html.parser")

	fac_name = faculty_soup.find(class_="field-name-title").text

	email_div = faculty_soup.find(class_="field-name-field-person-email")
	fac_email = email_div.find(class_="field-item even").text

	fac_title = faculty_soup.find(class_="field-name-field-person-titles").text
	
	return(fac_name, fac_title, fac_email)

#get number of pages
def get_pages(url):
	page_text = make_request_using_cache(url)
	soup = BeautifulSoup(page_text, "html.parser")

	current_page_div = soup.find(class_="item-list")
	current_page = current_page_div.find(class_="pager-current").text
	total_pages = int(current_page[5:])

	return total_pages

#insert all faculty data into dictionary
def get_umsi_data(page):
    base_url = "https://www.si.umich.edu"
    dir_page = "/directory?rid=All&page="
    page_url = base_url + dir_page + str(page)

    page_text = make_request_using_cache(page_url)
    soup = BeautifulSoup(page_text, "html.parser")

    fac_list = soup.find(class_="view-content")
    contact_links = fac_list.find_all(class_="field-name-contact-details")

    umsi_titles = {}
    for l in contact_links:
    	node = l.find("a")["href"]
    	fac_info = get_fac_info(node)
    	umsi_titles[fac_info[0]] = {"title": fac_info[1], "email": fac_info[2]}

    return(umsi_titles)


#### Execute funciton, get_umsi_data, here ####

directory = "https://www.si.umich.edu/directory?rid=All&page="
num_pages = get_pages(directory)
umsi_titles = {}

for p in range(num_pages):
	fac_data = get_umsi_data(p)
	for k in fac_data.keys():
		umsi_titles[k] = fac_data[k]

# print(umsi_titles)


#### Write out file here #####

umsi_file = open("directory_dict.json", "w")
umsi_file.write(json.dumps(umsi_titles))
umsi_file.close()
print("Complete")










