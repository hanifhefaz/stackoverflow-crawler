#----------------------------------
#----------------------------------
#---Stack Over Flow Crawler--------
#---Author: Hanif Hefaz------------
#---Date: 2019-10-11---------------
#----------------------------------
#----------------------------------


from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import re
import datetime

all_jobs = []

#using range I will be able to look for a specific range in url.
for page in range(1, 100):
    url = "https://stackoverflow.com/questions?tab=unanswered&page={}".format(page)
    html = urlopen(url)
    soup = BeautifulSoup(html,"html.parser")

    # find the div which is responsible for each question's placement.
    Container = soup.find_all("div", {"class":"question-summary"})
    for i in Container:
        try:
            # look for wanted element or tag in the container.

            # this code is returning all the titles of the questions.
            title = i.find("a", {"class":"question-hyperlink"}).get_text()

            #ths code is returning all the description of the questions.
            det = i.find("div", {"class":"excerpt"}).get_text()

            # this will return all the tags used in the quesitnos.
            tags = i.find("div",{"class":"tags"}).get_text()

            # this will give us all the votes each question have.
            votes = i.find("span",{"class":"vote-count-post"}).get_text()

            # returns the number of answers for each question.
            ans = i.find("div",{"class":"status"}).find('strong').get_text()

            # give us the number of views each question have.
            views = i.find("div",{"class":"views"})["title"]

            # to get the date format correctly, i looks for my specified date format
            # and then save it into json.
            s = i.find("span",{"class":"relativetime"})["title"]
            match = re.search('\d{4}-\d{2}-\d{2}', s)
            date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
            time = date

            # this will print us the result in the prompt.
            print(title, det, tags, votes, ans, views, time )

            # here I assign the related data to its place to be saved.
            job_dict = {}
            job_dict['Title'] = title
            job_dict['Description'] = det
            job_dict['Tags'] = tags
            job_dict['Votes'] = votes
            job_dict['Answers'] = ans
            job_dict['Views'] = views
            job_dict['Time'] = time
            
            all_jobs.append(job_dict)

        except AttributeError as ex:
            print('Error:', ex)
# now when the loop is completed, i here export the data into JSON
f = open('output.json', 'w')
f.write(json.dumps(all_jobs, indent=4, sort_keys=True, default=str))
f.close()