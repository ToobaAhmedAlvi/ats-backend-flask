
import PyPDF2
import textract
import re
import string
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask,jsonify
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import matplotlib.pyplot as plt
import pickle
import json
from pymongo import MongoClient
import pymongo
import requests
app = Flask(__name__)

# Initialize a text empty etring variable
text = ""
from dotenv import load_dotenv
load_dotenv()

import cloudinary
import cloudinary.uploader
import cloudinary.api
"""
myclient = pymongo.MongoClient("mongodb+srv://ayesha_user-21:757001ank@cluster0.lvksl.mongodb.net/AIATSDB?retryWrites=true&w=majority")
# DatabseName
mydb = myclient["AIATSDB"]
print(mydb)

#db=myclient.AIATSDB
# Issue the serverStatus command and print the results
##serverStatusResult=db.command("serverStatus")
#print(serverStatusResult)

"""

item_1 = {
    "cand_id": "EUR-C-345",
    "job_id": "EUR-JD-456",
    "resume_rank": "4",
    "resume_url": "abs@cloudinary.com"
}
"""
# Table name
mycol = mydb["shortlistedresume"] 


x = mycol.insert_one(item_1)
print(x)
print(x.inserted_id)

# collection_name = dbname["AIATS"]

url="https://atsbackend.herokuapp.com/api/shortlistresume/shortlistnewresume"
headers = {"Content-Type": "application/json; charset=utf-8"}
response = requests.post(url, headers=headers, json=item_1)
print("Status Code", response.status_code)
print("JSON Response ", response.json())
"""
url="https://atsbackend.herokuapp.com/api/shortlistresume/shortlistnewresume"
headers = {"Content-Type": "application/json"}
response = requests.post(url, headers=headers, json=item_1)
print("Status Code", response.status_code)
print("JSON Response ", response.json())
'''
url="https://atsbackend.herokuapp.com/api/shortlistresume/shortlistnewresume"
headers = {"Content-Type": "application/json"}
response = requests.post(url, headers=headers, json=item_1)
print("Status Code", response.status_code)
print("JSON Response ", response.json())
#json_string=json.dumps(item_1)
#print(json_string)
#x = requests.post(url, data)

#print(x.text)

'''

@app.route("/")
def home_view():
        return "Hello World!"

#@app.route("/terms", methods=['GET'])
def get():
    return jsonify(cat,result)


@app.route('/data', methods = ['POST'])
def post():
    posted_data = request.get_json()
    MLcand_id=posted_data['MLcand_id']
    MLjob_id=posted_data['MLjob_id']
    cloudpublic_id=posted_data['cloudpublic_id']
    cloud_resume_url=posted_data['secure_url']
    candshortlisted_id=posted_data['candshortlisted_id']
    
    return jsonify(MLcand_id,MLjob_id,cloudpublic_id,cloud_resume_url,candshortlisted_id)

var = cloudinary.api.resource("hmwbckieimbjzs9lwdkh")
data=var['info']['ocr']['adv_ocr']['data']
text=data[0]['fullTextAnnotation']['text']
print(text)
print(type(text))
    


count = 0
to_text=""
if text is not None:
       
    
    to_text = text.lower()
            # Remove numbers
    to_text = re.sub(r'\d+','',text)
            # Remove punctuation
    to_text = text.translate(str.maketrans('','',string.punctuation))
    to_text = re.sub(r'\d+','',to_text)
    to_text = text.lower()
# Remove punctuation
    to_text = to_text.translate(str.maketrans('','',string.punctuation))
    to_text= to_text.replace("\n","")
    print(to_text)

terms = {     
         'ApplicationConsultant':['leadership','collaboration','ATM','conflict resolution','Digital Channels',
                                       'integration protocols','ATM/CCDM Controller','analytical','verbal',
                                       'ISO 8583 messages','IBFT','UBPS','Inter Bank Fund Transfers','Banking',
                                       'Utility Bill Payment Services ','banking','finance','7','7 years experience'
                                       'patient','reporting system','stake holder','Payments','client','satisfaction',
                                       'implementation','delivery','administration','agile','budget','cost','direction','feasibility analysis',                             'finance','kanban','leader','leadership','management','milestones','planning',
                              'pmi','pmp','problem','project','risk','schedule','scrum','stakeholders','operations','custom support','hardware','problem solving','database architecture','bachelors','html','oop','goal oriented',
       'programming skills','VMWare','Virtual Box','networking','Information System','Computer Engineering','TCP/IP','Customer Care Service','decision making','management','computer science','python','frondend','problem solving','networking',
       'cloud','solutions','designing','upgrading system','reporting system','associate application consultant'],
         
        
        'JAVADeveloper':['2 years experience ','JAVA','developer','development','rest','soap','api','REST','SOAP','API','Web Services','statistical analysis','analytical mindset','api','application programming interface',
                      'verbal communication','excellent written skills','Java Programming Language','Ability to work','Software Engineeing','Computer Science','Masters in CS','fast pace environment','Bachelors','programming','coding','java','java developer'],
    
        'DataAnalyst': [ 'model managment','database management','python','R','Data Science','Machine Learning','pandas','statistical analysis','analytical mindset','Tableau','Hadoop','verbal communication','Pogramming Language','Ability to work','Computer Science','Masters in CS','fast pace environment','Bachelors','object oriented programming','OOP','java']
    ,
    'ProjectManager':['Team Lead','Team Work','Milestone','Communication','Risk Management','MS office','Agile','3 years of experience',
                     'SAP Training ','PMP Certification','MS Excel','Bachelors','MS Word','verbal skills','time management',
                      'resource planning','Sprint','Project','Issues','Masters'
                     
                      ]}
    
    
            

       
developer = 0
consultant = 0
analyst = 0
manager = 0
# Create an empty list where the scores will be stored
scores = []

# Obtain the scores for each area
for area in terms.keys():
    if area == 'ApplicationConsultant':
        for word in terms[area]:
            if word in text:
              consultant+=1
        scores.append(consultant)
        
    elif area == 'JAVADeveloper': 
        for word in terms[area]:
            if word in text:
              developer +=1
        scores.append(developer)
     
    
    elif area == 'DataAnalyst':
        for word in terms[area]:
            if word in text:
              analyst+=1
        scores.append(analyst)
        
    elif area == 'ProjectManager':
        for word in terms[area]:
            if word in text:
              manager +=1
        scores.append(manager)
        
        
    else:
      scores=0
    
transformer = TfidfTransformer()
loaded_vec = CountVectorizer(decode_error="replace",vocabulary=pickle.load(open("svm-model.pkl", "rb")))
        #tfidf = transformer.fit_transform(loaded_vec.fit_transform(requiredText))
test_feature = loaded_vec.transform([to_text])
model = pickle.load(open("mnb_model.pkl","rb"))
prediction = model.predict(test_feature)
model_val=""
print("AI MODEL RESULTS:\n")
if prediction == 0:
  model_val="Application Consultant"
  print("YOUR CV MATCHES\t"+model_val)
elif prediction ==1:
  model_val="Data Analyst"
  print("YOUR CV MATCHES\t"+model_val)
elif prediction ==2:
  model_val="Java Developer"
  print("YOUR CV MATCHES\t"+model_val)
elif prediction ==3:
  model_val="Project Manager"
  print("YOUR CV MATCHES\t"+model_val)
else:
  model_val="No job found"
  print("Sorry,Your CV didnot match any of the available job openings"+model_val) 
              
summary = pd.DataFrame(scores,index=terms.keys(),columns=['score'])
#.sort_values(by='score',ascending=None)
print(summary.iloc[prediction]) 
print(summary)

pie = plt.figure(figsize=(10,10))
plt.pie(summary['score'], labels=summary.index, explode = (0.1,0), autopct='%1.0f%%',shadow=True,startangle=90)
plt.title('EURONET Hiring Candidate - Resume Decomposition by Areas')
plt.axis('equal')
plt.show()




