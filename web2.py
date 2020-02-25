from flask import Flask
import flask
import threading
import random
import string
import time
from queue import Queue
import requests
import random
import string
from zipfile import ZipFile
import os


app = Flask(__name__)

bigcombo = Queue()



def randomSSN(size=32, chars=string.digits):        #random Code generator
    return ''.join(random.choice(chars) for i in range(size))

dic={}
    
def login(input, fielcode):
    global dic
    while input.qsize() > 1:
        line = input.get() 
        line = line.strip() #formats the input
        
        try:
            mail = line.split(":")[0]  #splits everything
            pw = line.split(":")[1]
            pwfb = pw.capitalize()  
        except: 
            print("F")
            continue
            
        if "@gmail.com" in mail:    #checks if the email is from gmail
            newmail = mail
        elif "@" in mail:
            gmail = mail.split("@")[0]
            newmail = gmail + "@gmail.com"
        else:
            mail = mail
        #
        file = open(fielcode + "_edited.txt", "a+", encoding="UTF-8") #creates a new text file for the edited combo
        file.write(mail + ":" + pw + "1" + "\n")
        file.write(mail + ":" + pw + "123" + "\n")
        file.write(mail + ":" + pw + "!" + "\n")
        file.write(mail + ":" + pwfb + "\n")
        file.write(mail + ":" + pwfb + "1" + "\n")
        file.write(mail + ":" + pwfb + "123" + "\n")
        file.write(mail + ":" + pwfb + "!" + "\n")
        file.write(mail + ":" + pwfb + "." + "\n")
        file.write(mail + ":" + pw + "." + "\n")
        file.write(mail + ":" + pw + "@" + "\n")
        file.write(mail + ":" + pwfb + "@" + "\n")
        file.write(mail + ":" + pw + "$" + "\n")
        file.write(mail + ":" + pwfb + "$" + "\n")
        try:
            file.write(newmail + ":" + pw + "\n")   #adds lines to the combo
        except:
            continue
    time.sleep(2)
    dic[fielcode] = True

@app.route("/comboapi")
def index():
    global dic
    fielcode = randomSSN()
    url = flask.request.args.get("url")
    r = requests.get(url)

    open(fielcode+".txt", "ab+").write(r.content)
    print(url)
    with open(fielcode + ".txt", "r",encoding="UTF-8") as file:   # Add Codes to a List
        for line in file.readlines():
            bigcombo.put(line)
    num = 0
    dic[fielcode] = False
    while num < 25:
        num += 1
        threading.Thread(target=login,args=[bigcombo,fielcode]).start()  # Start Threads
    while not dic[fielcode]:
        time.sleep(3)
    os.system("zip " + fielcode + '_edited.zip ' + fielcode +"_edited.txt")

    
    files = {
        'file': ('./' + fielcode + '_edited.zip', open('./' + fielcode + '_edited.zip', 'rb')),}
    response = requests.post('https://x0.at/', files=files)
    try:
        os.remove("./" + fielcode + ".txt")
        os.remove("./" + fielcode + "_edited.txt")
        os.remove("./" + fielcode + "_edited.zip")
    except:
        pass
    return response.text



if __name__ == '__main__':    app.run(port=1340)