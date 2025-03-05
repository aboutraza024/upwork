import json
import pandas as pd
from botasaurus.soupify import soupify
from botasaurus.request import request,Request
import re
import time
import random

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
}
data_list=[]
urls=[]

def read_url_from_csv():
    data = pd.read_csv("upwork_profiles.csv")
    urls = data['URL']
    print(urls)
    for u in urls:
        print(u)



@request
def scrape_profile(request:Request,data):
    k=1
    working_history=[]
    data = pd.read_csv("upwork_profiles.csv")
    urls = data['URL'].head(1041)

    # url=['https://www.upwork.com/en-gb/freelancers/~01562107fdb81c466e?referrer_url_path=/nx/search/talent/','https://www.upwork.com/en-gb/freelancers/~01304525e8d69b9775?referrer_url_path=/nx/search/talent/']
    for u in urls:
        time.sleep(random.uniform(1, 2))
        print(f"count {k}")
        k=k+1
        data = {}
        response = request.get(u,
                               headers=headers)
        soup = soupify(response)
        title = soup.find('title').text
        if title:
            data["Title"] = title

        skills = []
        skill = soup.find_all(('a', 'span'), class_=[
            'up-n-link skill-name cursor-pointer d-flex vertical-align-middle air3-token nowrap',
            'skill-name d-flex vertical-align-middle air3-token nowrap'])
        for s in skill:
            skills.append(s.text.strip())
        if skills:
            data["Skills"] = skills
        time.sleep(random.uniform(0, 1))
        try:
            description = soup.find('span', class_='text-pre-line break').get_text()

            if description:
                data["Description"] = description
        except:
            description=""

        # finding
        # work_historys = []
        # work_hist = soup.find_all('div', class_='air3-tabs d-flex w-100')
        # for w in work_hist:
        #     text_lines = w.get_text("\n", strip=True).split("\n")
        #     cleaned_text = "\n".join(text_lines[1:3])
        #     work_historys.append(cleaned_text)
        # if work_historys:
        #     data["Work History"] = work_historys

#new code
        tot_jobs = []
        completed_jobs = soup.find('div', class_="has-border air3-tabs-horizontal")
        if completed_jobs:
            text = completed_jobs.text.strip()  # Remove extra spaces
            import re
            match = re.findall(r'(\w+\s\w+)\s\((\d+)\)', text)
            job_counts = {key: int(value) for key, value in match}
            completed = "Completed Jobs:", job_counts.get("Completed jobs", 0)
            progress = "In Progress:", job_counts.get("In progress", 0)
            if completed or progress:
                tot_jobs.append(completed)
                tot_jobs.append(progress)
                data["Total Jobs"] = tot_jobs



        else:
            print("No data found")

        # try:
        #     total_jobs = soup.find('div', class_='stat-amount h5').get_text()
        #     if total_jobs:
        #         data["Total Jobs"] = total_jobs
        # except:
        #     total_jobs=""


        # new updated code
        try:
            time.sleep(random.uniform(1, 3))
            total_hour = soup.find_all('div', class_="stat-amount h5")  # update this in new code
            total_job=total_hour[0].text
            total_hour=total_hour[1].text
            data["Total Jobs "] = total_job
            data["Total Hour "] = total_hour
        except:
            total_hour=[]


        try:
            price = soup.find('h3', role='presentation')
            price_per_hour = price.find('span').text

            if price_per_hour:
                data["Price Per Hour"] = price_per_hour.strip()
        except:
            price_per_hour=""




        # new code for work history


        try:
            x = soup.find_all('div', class_="span-12")  # Returns a list
            j = 10
            for i in range(3):
                text = x[j].get_text(strip=True)  # Removes extra spaces & new lines
                j = j + 1
                title_match = re.search(r'^(.*?)\s*Rating is', text, re.DOTALL)
                title = title_match.group(1).strip() if title_match else "Not Found"

                # Extract rating
                rating_match = re.search(r'Rating is (\d+\.\d+) out of 5', text)
                if rating_match:
                    rating = rating_match.group(0) if rating_match else ""
                else:
                    rating = ""

                # print("JOB Title :",title)
                title1 = f" Title :{title}"
                # print("JOB RATING :",rating)
                rating1 = f" Rating :{rating}"
                time.sleep(random.uniform(1, 2))
                if title != "Not Found":
                    working_history.append(title1)
                else:
                    title1 = ""
                if rating:
                    working_history.append(rating1)
                else:
                    rating = ""
        except:
            title1=""
            rating1=""
            working_history.append(title1)
            working_history.append(rating1)



        # print(working_history)
        data["Working History"]=working_history
        print("\n\n\n\nJSON", data)




        data_list.append(data)
    write_data_in_json(data_list)


def write_data_in_json(data):
    with open('profile2.json','w',encoding='utf-8') as f:
        json.dump(data,f,indent=4)

#hi

# verify
#
# import json
#
# # Open and read the JSON file
# with open('profile1.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)  # Load JSON data into a Python dictionary or list
#
# # Print the data
# print(len(data))
# print(data[1011])



# scrape_profile()



# read_url_from_csv()