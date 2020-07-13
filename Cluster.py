import requests
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as p
import numpy as np
import math
import operator

message="Alert Alert......"
email=['shivgarg413@gmail.com',"siddharthjuyal066@gmail.com"]

def WeatherAPI(city):    #Getting Weather Info Using weather api
        address = 'https://api.openweathermap.org/data/2.5/forecast?appid=aca57137552879f354a4dc269050f1e4&q='
        url = address + city   #Merging city name with the api key and making a url
        output = requests.get(url).json()  #requesting weather report in json format

        if output == {'cod': '404', 'message': 'city not found'}:
            #checking whether entered city name is valid or not
            print("Error: enter valid city name\n")

        data = output['list'] #now converting json format to list
        lt = []
        lt1 = []


                  
        for x in data:   #reading the data
            if "rain" in x:   #getting the data labeled with key="rain"
                lt=x['rain']  #trandferng the list to lt
                for y in lt:  
                    if '3h' in y:  #getting the amt of rain every 3h
                        lt1.insert(-1 , lt['3h'])
        sum=0
        x=0
        for z in lt1: 
            if x<7:  #getting the first 8 rain amt for every day
                sum+=z
                x+=1

            else:
                break
            
        return sum/8  #getting mean rain fall for a day and returning it
        

def calc_Distance(p1,p2):
    d = math.sqrt(pow((p2[0] - p1[0]),2)+pow((p1[1] - p2[1]),2))
    return d


def dataSet():  #reading info from file and grouping it into a same file
    #below portion is to be change depending upon cloud connectivity
    x = np.array(p.read_csv("q1x.txt"))
    y = np.array(p.read_csv("q1y.txt"))
    for i in range(len(x)):
        t = [x[i][0],y[i][0],None]
        data.append(t)
    gp = [5.0269, -2.6807, 0]
    rp = [18.959, 17.054000000000002, 1]
    
    for i in range(len(data)):
        dist1 = calc_Distance(gp,data[i])
        dist2 = calc_Distance(rp,data[i])
        if dist1 < dist2:
            data[i][2]=0
        else:
            data[i][2]=1
     

def euclideanDistance(instance,instance1): #this function calculates euclidean
                                           #distance b/w two points 
    distance=0
    for x in range(len(instance)):
        distance+=pow(instance[x] - instance1[x] , 2)
    return math.sqrt(distance)
    
def getNeighbours(distance,k):  
    distance.sort(key=operator.itemgetter(1))  #sorting the distance calculated
                                               #in ascending order
    neighbours = []
    for x in range(k):
        neighbours.append(distance[x][0])  #getting all the closest neighbour
    return neighbours


def getResponse(neighbours): #now finding the cluster the data point is going to
                             #be a part
    Votes=0
    for i in range(len(neighbours)):
        if neighbours[i]==0:
                Votes+=-1
        else:
                Votes+=1
    return Votes
                     

def msg_Send():  #If there is a condition of flood msg is going to be send
        s=smtplib.SMTP(host='smtp.gmail.com',port=587)
        s.starttls()
        s.login('shivgarg413@gmail.com','22111999')
#setup is complete with smtp server and admin is logged in and ready to send msg
        for name in email:
            msg=MIMEMultipart()
            #print(message)
            msg['From']='shivgarg413@gmail.com'
            msg['To']=name
            msg['Subject']="This is test"
            msg.attach(MIMEText(message,'plain'))
            s.send_message(msg)
            del msg

        s.quit()
        
def main():
    
    city = input("city name: ")
    while(1):
            print("Running")
            a=10#int(input("Enter points"))
            b=WeatherAPI()
            instance=[a,b]
            distance=[]
            for x in range(len(data)):
                distance.append((data[x][2],euclideanDistance(instance,data[x])))
            k=int(math.sqrt(len(data)))
            neighbours=getNeighbours(distance,k)
            sortedVote=getResponse(neighbours)
            if sortedVote == 1:
                    msg_Send()
                    print("Task Done")
                    
            time.sleep(60)
        
main()

    
