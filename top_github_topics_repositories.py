'''
Project TO-Do List.
----->> 1: pick your site
----->> 2: what you want to scrap.
----->> 3: use the request library to download web pages from the picked site.
----->> 4: use beautiful soup to parse and extract information.
----->> 5: create a csv file with the extracted info.
'''

'''
--->> scraping: https://github.com/topics
--->> headers to grab: topic title, page url, description.
--->> we'll get the top 25 repositories from each topic in the topics page.
--->> for each repos we grab: repo name, username, stars, repo url.
--->> drop info in csv file.
'''

'''
Steps:
    import requests
'''
import requests
import pandas as pd
from bs4 import BeautifulSoup as soup
topics_url = 'https://github.com/topics'
# to get/download the web page.
response = requests.get(topics_url)
# to check if request was successful or not, note (200 means successful.)
# print(response.status_code)
# to get the total length of the whole content in the  webpage.
# print(len(response.text))

page_content = response.text
doc = soup(page_content, 'html.parser')

# finding topic description
p_tags = doc.find_all('p')
# --> how to find a particular tag you are looking for, u should use indexing... [:5] --> gets 1st 5 occurrence of the tag.
        # what i am looking for is at the 8th index.
        # print(p_tags[:10])
        # print(p_tags[8])

# getting the tag class.
# this also gives us list of all topics and descriptions in the particular topic_page
topics_descriptions = doc.find_all('p', {'class': "f5 color-fg-muted mb-0 mt-1"})
topics_titles = doc.find_all('p', {'class': 'f3 lh-condensed mb-0 mt-1 Link--primary'})

# --> we can use the .parent to get more contents or elements in a tag or being housed in a tag
        # topics_title_tag0 = topics_title[0]
        # print(topics_title_tag0.parent.parent)
# getting the topics url.
topics_urls = doc.find_all('a', {'class': 'no-underline flex-grow-0'})


# cleaning up code, ie: by storing each results in a list.
topics_title_list = []
topics_descriptions_list = []
topics_urls_list = []

for titles, descriptions, urls in zip(topics_titles, topics_descriptions, topics_urls):
    topics_title_list.append(titles.text)
    topics_descriptions_list.append(descriptions.text.strip())
    topics_urls_list.append('https://github.com'+urls['href'])
    # print(titles.text + ':', '\n' + descriptions.text.strip(), '\n' + 'https://github.com'+urls['href'])
#     # print('')
# # print(topics_title_list)
# # print(topics_descriptions_list)
# # print(topics_urls_list)
#
#
# # saving results into a csv file using pandas
# # we use a dictionary to create a {key:value} pair which act as {column_name:item} for our csv file.
# topics_dict = {'title': topics_title_list,
#                'description': topics_descriptions_list,
#                'url': topics_urls_list
#                }
#
# topic_dataframe = pd.DataFrame(topics_dict)
# # print(topic_dataframe)
# # converting the pandas values to csv
# topics_df_to_csv = topic_dataframe.to_csv('topics.csv', index=None)



# ------------>>> project STEP 2
# Getting information out of each topic pag, ie. username, repo name, stars.
# for topic 1 ie '3d'
topic_page_url = topics_urls_list[0]

# step 1, getting the page html info using requests
page_response = requests.get(topic_page_url)
# print(len(page_response.text))
# putting info into beautiful soup.
topic_doc = soup(page_response.text, 'html.parser')

# getting usernames, repo names, repo url and stars info.
# we call this repo_tag because it houses all needed info
repo_tags = topic_doc.find_all('h3', {'class': "f3 color-fg-muted text-normal lh-condensed"})
# print(repo_tags[0])
# repo_tags[0].find_all('a')      ---->  username, repo name and url for the 1st topic repo, use indexing to access others.
# print(repo_tags[0].find_all('a'))    ---> all raw (username, repo name and url) for the 1st topic repo, use indexing to access others.
a_tags = repo_tags[0].find_all('a')
# print(a_tags)      # contains entire repo info except star info, for 1st topic repo (mrdoob).
# username tags
username_tag = a_tags[0].text.strip()
# print(username_tag)
un_all = repo_tags

# repo names
repo_name = a_tags[1].text.strip()
# href links ie, repo url.
base_url = 'https://github.com'
repo_url = base_url + a_tags[1]['href']
# stars info.
star_tags = topic_doc.find_all('span', {'class': "Counter js-social-count"})
# star_tags[0].text      ----> contains 1st repo star info, use indexing to access others.
# print(star_tag[0])
# create a function to convert the value of star to number.
def parse_star_count(stars_str):
    if 'k' in stars_str:
        return int(float(stars_str[:-1]) * 1000)
    else:
        return int(stars_str)
# print(parse_star_count(star_tags[0].text))


# create a function to get the whole repo info at once.
def get_repo_info(h3_tag, star_tagg):
    # returns all required info about each topic.
    a_tags = h3_tag.find_all('a')
    username = a_tags[0].text.strip()
    repo_na = a_tags[1].text.strip()
    repo_ur = base_url + a_tags[1]['href']
    repo_str = parse_star_count(star_tagg.text)
    return username, repo_na, repo_str, repo_ur
# print(get_repo_info(repo_tags[10], star_tags[10]))

# to get all repo info for topics 3d:
# create a dict to store infos.
topic_repos_dict = {
                        'username': [],
                        'repo_name': [],
                        'stars': [],
                        'repo_url': []
                   }
# print(range(len(repo_tags)))

# for i in range(len(repo_tags)):
#     repo_info = get_repo_info(repo_tags[i], star_tags[i])
#     topic_repos_dict['username'].append(repo_info[0])
#     topic_repos_dict['repo_name'].append(repo_info[1])
#     topic_repos_dict['stars'].append(repo_info[2])
#     topic_repos_dict['repo_url'].append(repo_info[3])
# # print(topic_repos_dict)
# # put info into csv file using pandas.
# topic_repos_df = pd.DataFrame(topic_repos_dict)
# df = topic_repos_df.to_csv('topics_repo.csv', index=None)
# print(topic_repos_df)





# creating a function to loop through topics in the main page.
def get_topic_page(topic_url):
    # download the page.
    response = requests.get(topic_url)
    # check success response.
    if response.status_code != 200:
        raise Exception(f'Failed to load page {topic_url}')
    # parse using beautiful soup.
    topic_doc = soup(response.text, 'html.parser')
    return topic_doc

def get_topic_repos(topic_doc):
    # we need tags containing repo title, name, url and username
    repo_tags = topic_doc.find_all('h3', {'class': "f3 color-fg-muted text-normal lh-condensed"})
    # getting star tags.
    star_tags = topic_doc.find_all('span', {'class': "Counter js-social-count"})

    # create a topic_repo_dict
    topic_repos_dict = {
        'username': [],
        'repo_name': [],
        'stars': [],
        'repo_url': []
    }

    # getting repo info
    for i in range(len(repo_tags)):
        repo_info = get_repo_info(repo_tags[i], star_tags[i])
        topic_repos_dict['username'].append(repo_info[0])
        topic_repos_dict['repo_name'].append(repo_info[1])
        topic_repos_dict['stars'].append(repo_info[2])
        topic_repos_dict['repo_url'].append(repo_info[3])

    return pd.DataFrame(topic_repos_dict)

# insert any url link from 'topics_urls_list' to see the  info.

print(get_topic_repos(get_topic_page(topics_urls_list[6])))