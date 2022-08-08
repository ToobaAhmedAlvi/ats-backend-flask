import pandas as pd
from flask import Flask,jsonify,request
import PyPDF2
import textract
#import re
import string
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import matplotlib.pyplot as plt
import pickle

app = Flask(__name__)


@app.route("/")
def home_view():
        return "Hello World!"

@app.route("/terms", methods=['GET'])
def get():
    Resume = open('sample.pdf', 'rb')
    #url = 'https://res.cloudinary.com/ayeshank/image/upload/v1659724511/CandidateResumes/uiqurnxe1sugezo1rjra.pdf'
    #Resume = {'somekey': 'somevalue'}

    #x = requests.post(url, json = Resume)
    #print the response text (the content of the requested file):
    #print(x.text)
        
    to_text = ""
    count = 0

    if Resume is not None:
        pdfReader = PyPDF2.PdfFileReader(Resume)
        num_pages = pdfReader.numPages
        # Extract text from every page on the file
        while count < num_pages:
            pageObj = pdfReader.getPage(count)
            count +=1
            to_text += pageObj.extractText()
            #st.write(to_text)
            to_text = to_text.lower()
            # Remove numbers
        # to_text = re.sub(r'\d+','',to_text)
            # Remove punctuation
            to_text = to_text.translate(str.maketrans('','',string.punctuation))
            #st.write(to_text)
    text=pd.DataFrame([to_text])

    transformer = TfidfTransformer()
    loaded_vec = CountVectorizer(decode_error="replace",vocabulary=pickle.load(open("svm-model.pkl", "rb")))
        #tfidf = transformer.fit_transform(loaded_vec.fit_transform(requiredText))
    test_feature = loaded_vec.transform([to_text])
    model = pickle.load(open("mnb_model.pkl","rb"))
    prediction = model.predict(test_feature)
    if prediction == 0:
        print("YOUR CV MATCHES APPLICATION CONSULTANT")
    elif prediction ==1:
        print("YOUR CV MATCHES DATA ANALYST")
    elif prediction ==2:
        print("YOUR CV MATCHES JAVA DEVELOPER")
    elif prediction ==3:
        print("YOUR CV MATCHES PROJECT MANAGER")
    else:
        print("Sorry,Your CV didnot match any of the available job openings") 
        
        


    terms = {     
            'ApplicationConsultant':['leadership','collaboration','ATM','conflict resolution','Digital Channels',
                                        'integration protocols','ATM/CCDM Controller','analytical','verbal',
                                        'ISO 8583 messages','IBFT','UBPS','Inter Bank Fund Transfers','Banking',
                                        'Utility Bill Payment Services ','banking','finance','7','7 years experience'
                                        'patient','reporting system','stake holder','Payments','client','satisfaction',
                                        'implementation','delivery','administration','agile','budget','cost','direction','feasibility analysis',                             'finance','kanban','leader','leadership','management','milestones','planning',
                                'pmi','pmp','problem','project','risk','schedule','scrum','stakeholders','operations','custom support','hardware','problem solving','database architecture',
        'programming skills','VMWare','Virtual Box','networking','Information System','Computer Engineering','TCP/IP','Customer Care Service','decision making',
        'cloud','solutions','designing','upgrading system','reporting system','associate application consultant'],
            
            
            'JAVADeveloper':['2 years experience ','JAVA','developer','development','rest','soap','api','REST','SOAP','API','Web Services','database structures',
                        'statistical analysis','analytical mindset','problem solving skills','api','application programming interface',
                        'verbal communication','excellent written skills','Java Programming Language','Ability to work','Software Engineeing','Computer Science','Masters in CS','fast pace environment','Bachelors','programming','coding','HTML','object oriented programming','OOP','java','java developer'],
        
            'DataAnalyst': [ 'model managment','database management','python','R','Data Science','Machine Learning','pandas','statistical analysis','analytical mindset','problem solving skills','Tableau','Hadoop',
                        'verbal communication','excellent written skills','SQL',' Programming Language','Ability to work','Software Engineeing','Computer Science','Masters in CS','fast pace environment','Bachelors','programming','coding','HTML','object oriented programming','OOP','java','python developer','python','streamlit']
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
                if word in to_text:
                    consultant+=1
            scores.append(consultant)
        elif area == 'JAVADeveloper':
            for word in terms[area]:
                if word in to_text:
                    developer+=1
            scores.append(developer)

        elif area == 'DataAnalyst':
            for word in terms[area]:
                if word in to_text:
                    analyst+=1
            scores.append(analyst)
        
        
        elif area =='ProjectManager':
            for word in terms[area]:
                if word in to_text:
                    manager +=1
            scores.append(manager)
        else:
            scores = 0
    summary = pd.DataFrame(scores,index=terms.keys(),columns=['score']).sort_values(by='score',ascending=False)
    print(summary)
    print(prediction)
    result= summary.to_json()
    cat=prediction.tolist()
    return jsonify(cat,result)