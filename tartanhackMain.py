import numpy as np
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import requests 
import threading 


import decisonTree.py 
class backEndProcess(object):
    def __init__ (self):
        #a list that stores all sample picture path in the folder
        self.pictre_path = []
        #api keys
        self.emotion_key = "6e205c33cfde48eb88b1b1870d9957fe"
        self.attention_key = 'c650165254c94a4f9e5cdac99cf0c1fe'
        #length of picture path
        self.picture_count = 0
        #emotion data from last image for user call
        self.recent_emotion_data = None
        #attention data from last image for user call
        self.recent_attention_data = None
        #pre-trained decision tree model
        self.model = decisionTree.trainModel()
        #emotion attribute labels
        self.population_emotion_data = []
        #attention label
        self.population_attention_data = []
        self.user_requested_emotion = None

    def emotion_detection(image_path):
        emotion_key = self.emotion_key #"6e205c33cfde48eb88b1b1870d9957fe"
        assert emotion_key
        emotion_recognition_url = "https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize"
        image_data = open(image_path,"rb").read()
        headers  = {'Ocp-Apim-Subscription-Key': emotion_key, "Content-Type": "application/octet-stream" }
        response = requests.post(emotion_recognition_url, headers=headers, data=image_data)
        response.raise_for_status()
        emotion_analysis = response.json()
        storage = emotion_analysis
        self.emotion_data_process (storage) 
        print(emotion_analysis)

    def face_detection(path):
        subscription_key = attention_key #'c650165254c94a4f9e5cdac99cf0c1fe'
        filename = path
        uri_base = 'https://westcentralus.api.cognitive.microsoft.com'
        headers = {
             'Content-Type': 'application/octet-stream',
             'Ocp-Apim-Subscription-Key': subscription_key,
        }
        params = {
            'returnFaceId': 'true',
            'returnFaceAttributes': 'headPose',
        }
        path_to_face_api = '/face/v1.0/detect'
        with open(filename, 'rb') as f:
            img_data = f.read()
        try:
            response = requests.post(uri_base + path_to_face_api,
                                     data=img_data, 
                                     headers=headers,
                                     params=params)
            print ('Response:')
            parsed = response.json()
            storage = parsed
            self.attention_data_process(storage)
            # display the image analysis data
            print (parsed)
            #return parsed
        except Exception as e:
            storage = None
            self.attention_data_process(storage)
            print(e)

    def trigger_main(self, emotion_path, face_path):
        t1 = threading.Thread(target=emotion_detection, args=(emotion_path))
        t2 = threading.Thread(target=face_detection, args=(face_path))
        t1.start()
        t2.start() 

    def trigger_curr(self, x,y)
        t = threading.Thread(target=getThreeEmotions, args=(x,y))

    


def write(file,content):
    with open(file,"wt") as f:
                f.write(content)


def getAttentionRate(faceList,imageHeight,imageWidth):
    yawMargin = 15
    pitchMargin = 15
    rollmargin = 15

    centerX = imageHeight / 2
    centerY = imageWIdth / 2
    attentionTotal = 0
    total = len(faceList)
    faceDict = {}

    for i in range(0,faceList.len()):
        #left,top,pitch,row,yaw
        attention = True
        faceDict = faceList[i]
        left = faceDict["faceRectangle"]["left"]
        top = faceDict["faceRectangle"]["top"]
        faceId = faceDict["faceId"]
        pitch = faceDict["faceAttributes"]["headPose"]["pitch"]
        roll = faceDict["faceAttributes"]["headPose"]["pitch"]
        yaw = faceDict["faceAttributes"]["headPose"]["pitch"]
        print("pitch:%d,roll:%d,yaw:%d \n" % (pitch,roll,yaw))
        #need to determine angle
        if(left>centerY):
            #right of the screen
            if(yaw > yawMargin):
                attention = False;
                print("wrong yaw1\n")
        else:
            #left of the screen
            if(yaw < (-1*yawMargin)):
                attention = False;
                print("wrong yaw2\n")
        if(top>centerX):
            #bottom part of the screen
            if(pitch > pitchMargin):
                attention = False;
                print("wrong pitch1\n")
        else:
            #top part of the screen
            if(pitch < (-1*pitchMargin)):
                attention = False;
                print("wrong pitch2\n")
        if(abs(roll) > rollMargin):
            attention = False;
            print("wrong roll\n")

        if(attention):
            totalAttention = totalAttention + 1
        faceDict[faceId] = attention;

    attenRate = totalAttention/total
    return (faceDict,attentionRate)

def getThreeEmotions(faceList,xPos=,yPos):
    emotion1 = ""
    emotion2 = ""
    emotion3 = ""
    for i in range(0,len(faceList)):
        faceDict = faceList[i];
        left = faceDict["faceRectangle"]["left"]
        top = faceDict["faceRectangle"]["top"]
        width = faceDict["faceRectangle"]["width"]
        height = faceDict["faceRectangle"]["height"]
        right = left + width
        bottom = top + height
        score = faceDict["scores"]

        #need to determine coordinate
        if(y >= left && y <= right && x <= bottom && x >= top):
            first = 0;
            second = 0;
            third = 0;
            firstString = ""
            secondString = ""
            thirdString = ""
            for j in range(0,len(score)):
                curr = score[j]
                if( curr > first):
                    third = second
                    thirdString = secondString
                    second = first
                    secondString = firstString
                    first = curr
                    firstString = j
                else if( curr > second):
                    third = second
                    thirdString = secondString
                    second = curr
                    secondString = j
                else if( curr > thid):
                    third = curr
                    thirdString = j
            emotion1 = firstString
            emotion2 = secondString
            emotion3 = thirdString
            return (emotion1,emotion2,emotion3)

    return (emotion1,emotion2,emotion3)


#### max's functions below ####


def attention_data_process(faceList):
    # if raw data is empty, hard code
    rateList = self.population_attention_data
    if(len(faceList)==0):
        rateList.append(56)

    margin = 15
    centerX = imageHeight / 2
    centerY = imageWIdth / 2
    attentionTotal = 0
    total = len(faceList)
    faceDict = {}

    totalRoll = 0
    totalYaw = 0
    totalPitch = 0

    for i in range(0,faceList.len()):
        #left,top,pitch,row,yaw
        faceDict = faceList[i]
        left = faceDict["faceRectangle"]["left"]
        top = faceDict["faceRectangle"]["top"]
        faceId = faceDict["faceId"]
        pitch = faceDict["faceAttributes"]["headPose"]["pitch"]
        roll = faceDict["faceAttributes"]["headPose"]["pitch"]
        yaw = faceDict["faceAttributes"]["headPose"]["pitch"]
        #print("pitch:%d,roll:%d,yaw:%d \n" % (pitch,roll,yaw))
        totalYaw += abs(yaw)
        totalPitch += abs(pitch)
        totalRoll += abs(roll)
        # #need to determine angle
        # if(left>centerY):
        #     #right of the screen
        #     if(yaw > yawMargin):
        #         attention = False;
        #         print("wrong yaw1\n")
        # else:
        #     #left of the screen
        #     if(yaw < (-1*yawMargin)):
        #         attention = False;
        #         print("wrong yaw2\n")
        # if(top>centerX):
        #     #bottom part of the screen
        #     if(pitch > pitchMargin):
        #         attention = False;
        #         print("wrong pitch1\n")
        # else:
        #     #top part of the screen
        #     if(pitch < (-1*pitchMargin)):
        #         attention = False;
        #         print("wrong pitch2\n")
        # if(abs(roll) > rollMargin):
        #     attention = False;
        #     print("wrong roll\n")
    avgRoll = totalRoll/total
    avgYaw = totalYaw/total
    avgPitch = totalPitch/total

    for i in range(0,faceList.len()):
        #left,top,pitch,row,yaw
        attention = True
        faceDict = faceList[i]
        left = faceDict["faceRectangle"]["left"]
        top = faceDict["faceRectangle"]["top"]
        faceId = faceDict["faceId"]
        pitch = faceDict["faceAttributes"]["headPose"]["pitch"]
        roll = faceDict["faceAttributes"]["headPose"]["pitch"]
        yaw = faceDict["faceAttributes"]["headPose"]["pitch"]
        #print("pitch:%d,roll:%d,yaw:%d \n" % (pitch,roll,yaw))
        if(abs(pitch)>=avgPitch + margin):
            attention = False
        if(abs(yaw)>=avgYaw + margin):
            attention = False
        if(abs(roll)>=avgRoll + margin):
            attention = False
        if(attention):
            totalAttention = totalAttention + 1

    attenRate = totalAttention/total
    #append to field population_attention_data
    rateList.append(attentionRate)

#xPos and yPos should be positions in the original picture
def getThreeEmotions(xPos,yPos):
    faceList = self.recent_emotion_data
    errMrg = 10
    emotion1 = ""
    emotion2 = ""
    emotion3 = ""
    for i in range(0,len(faceList)):
        faceDict = faceList[i];
        left = faceDict["faceRectangle"]["left"]
        top = faceDict["faceRectangle"]["top"]
        width = faceDict["faceRectangle"]["width"]
        height = faceDict["faceRectangle"]["height"]
        right = left + width
        bottom = top + height
        score = faceDict["scores"]

        #need to determine coordinate
        if(yPos >= (left-errMrg) && yPos <= (right+errMrg) 
                        && xPos <= (bottom+errMrg) && xPos >= (top+errMrg)):
            first = 0;
            second = 0;
            third = 0;
            firstString = ""
            secondString = ""
            thirdString = ""
            for j in range(0,len(score)):
                curr = score[j]
                if( curr > first):
                    third = second
                    thirdString = secondString
                    second = first
                    secondString = firstString
                    first = curr
                    firstString = j
                else if( curr > second):
                    third = second
                    thirdString = secondString
                    second = curr
                    secondString = j
                else if( curr > thid):
                    third = curr
                    thirdString = j
            emotion1 = firstString
            emotion2 = secondString
            emotion3 = thirdString
            self.userRequestedEmotion = (emotion1,first,emotion2,second,emotion3,third)

        self.userRequestedEmotion = ("normal",87.5,"happy",5.5,"sad",7)

def getAttentionRateForUser():
    rateList = selfattention_attri_label
    return rateList[len(rateList)-1]


def emotion_data_process(faceList):
    #hardcode result if empty list
    emotionList = self.population_emotion_data
    if(len(faceList)==0):
        emotionList.append([True,True,False])
    total = len(faceList)
    happyCutoff = 0.4
    normalCutoff = 0.3
    sadCutoff = 0.4
    total = len(faceList)
    avghappy = 0
    avgnormal = 0
    avgsad = 0
    happyTotal = 0
    normalTotal = 0
    dataTotal = 0

    happy = False
    normal = False
    sad = False
    for i in range(0,len(faceList)):
        #faceList: raw data returned by emotion API
        faceDict = faceList[i]
        scoreDict = faceDict["scores"]
        happyTotal += scoreDict["happiness"]
        sadTotal += scoreDict["sadness"]
        normalTotal += scoreDict["neutral"]
    avgnormal = normalTotal/total
    avgsad = sadTotal/total
    avghappy = happyTotal/total
    if(avghappy>happyCutoff):
        happy = True
    if(avgsad>sadCutoff):
        sad = True
    if(avgnormal>normalCutoff):
        normal = True
    emotionList.append([happy,normal,sad])