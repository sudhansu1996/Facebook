import openpyxl
import pandas as pd
from flask import request,Flask
from openpyxl import load_workbook
import requests
import json
app=Flask(__name__)
from flask import send_from_directory



@app.route('/',methods=["GET"])
def index():

    url = "http://65.2.11.36:32344/graphql"
    params = {"query":"{\n  facebookPosts {\n     id\n    story\n    message\n    is_popular\n    created_at\n    sentiment {\n      query\n      query_result\n      score\n    }\n  }\n}","variables":{}}
    response = requests.get(url,params) 
    response=json.loads(response.text)
    df1=[]
    data=response["data"]

    f=response["data"]
    for i in f["facebookPosts"]:
        df1.append([i["id"],i["message"]])
    d=pd.DataFrame(df1,columns=["user_id","user_message"])
    sdf=d["user_message"]
    m=[]
    n=[]
    o=[]

    for i in sdf:
        i=str(i)
        i=i.split("\n")
        w=""
        for s in i:
            w=w+s
        s1=[]
        w=w.split(" ")
        for z in w:
            for s in range(len(z)):
                if z[s]=="#" or z[s]=="@":
                    s1.append(z)
                if z[s:s+4]=="http":
                    s1.append(z)
        w=""
        for s in i:
            w=w+s
        for s in s1:
            w=w.replace(s,"")
        print(w)
            
        res = requests.post("http://localhost:5000/predict", json={"query":w})

        score=json.loads(res.text)["score"]
        query_result=json.loads(res.text)["query_result"]
        m.append(score)
        n.append(query_result)
        o.append(w)
        
        
    d.insert(2,"score",m)
    d.insert(3,"query_result",n)
    d.insert(4,"message1",o)
    d.to_excel("d.xlsx")
    file_name = 'app.xlsx'
    wb = openpyxl.load_workbook('d.xlsx')
    wb.save(file_name)
    

    return "Facebook"

if __name__ == '__main__':
    app.run(debug=True,port=1001,host="0.0.0.0" )