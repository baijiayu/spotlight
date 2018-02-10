import sys, csv, math,copy
import time
import numpy as np
from builtins import len
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import requests 
import threading 


def getSheet(inputFile):
    with open(inputFile) as csvfile:
        sheet = csv.reader(csvfile, delimiter = ',')
        newData = []
        for row in sheet:
            newData.append(row)
        val1 = newData[1][0]
        rows, cols = len(newData), len(newData[0])
        return newData

def write(file,content):
    with open(file,"wt") as f:
                f.write(content)





def entropy(p):
    if abs(p-0)<0.00001:
        return 0
    else:
        return -p*math.log(p,2)


def getMutualInfo(data,splittingFeature):
    pos = []
    neg = []
    N = len(data)-1
    index = data[0].index(splittingFeature)
    posRef = data[1][index]
    label1 = 0
    label2 = 0
    labelRef = data[1][-1]
    for i in range(N):
        if data[i+1][index] == posRef:
            pos.append(i+1)
        if data[i+1][-1] == labelRef:
            label1+=1
        if data[i+1][index] != posRef:
            neg.append(i+1)
        if data[i+1][-1] != labelRef:
            label2+=1
    (p1, p2) = (float(label1)/N, float(label2)/N)
    H_Y = entropy(p1)+entropy(p2)
    label1_pos = 0
    label2_pos = 0
    label1_neg = 0
    label2_neg = 0
    N_pos = len(pos)
    N_neg = len(neg)
    for i in pos:
        if data[i][-1] == labelRef:
            label1_pos+=1
        else:
            label2_pos+=1
    for i in neg:
        if data[i][-1] == labelRef:
            label1_neg+=1
        else:
            label2_neg+=1
    (p1_pos,p2_pos) = (float(label1_pos)/N_pos,float(label2_pos)/N_pos) if N_pos != 0 else (0,0)
    (p1_neg,p2_neg) = (float(label1_neg)/N_neg,float(label2_neg)/N_neg) if N_neg != 0 else (0,0)
    H_YX = (float(N_pos)/N)*(entropy(p1_pos)+entropy(p2_pos))+(float(N_neg)/N)*(entropy(p1_neg)+entropy(p2_neg))
    return (H_Y-H_YX)

def partition(data,feature):
    posData = [data[0]]
    negData = [data[0]]
    featIndex = data[0].index(feature)
    posResponse = data[1][featIndex]
    negResponse = ""
    for i in range(len(data)-1):
        if data[i+1][featIndex]==posResponse:
            posData.append(data[i+1])
        else:
            if negResponse == "":
                negResponse=data[i+1][featIndex]
            negData.append(data[i+1])
    return(posData, negData, posResponse, negResponse)


class Tree(object):
    def __init__(self,data,labelName=[],leaf=False):
        self.lTree=None
        self.rTree=None
        #all relevant data for next depth
        self.data=data
        #the name of the two categories of splitting feature
        self.splitReference = []
        #the names of the two possible outcomes 
        self.labelName = []
        #the number of each of the two outcomes at this level
        self.labelCount = []
        #the name of the splitting feature
        self.splittingFeature=None
        #indication of leaf node
        self.leaf=leaf

def labelNumbers(data,label1,label2):
    label1N=0
    label2N=0
    for i in range(len(data)-1):
        if data[i+1][-1]==label1: label1N+=1
        else: label2N+=1
    return(label1N,label2N)

def cancelFeature(data,feature):
    
    newData=copy.deepcopy(data)
    index=data[0].index(feature)
    rows=len(data)
    for i in range(rows):
        newData[i][index:index+1]=[]
        
    return newData


def printTree(tree,depth):
    if tree == None: return
    if tree.leaf:
        (label1,label2)=(tree.labelName[0],tree.labelName[1])
        (N1,N2)=(tree.labelCount[0],tree.labelCount[1])
        print("[%d %s /%d %s]\n"%(N1,label1,N2,label2))
    else:
        splittingFeature=tree.splittingFeature
        (label1,label2)=(tree.labelName[0],tree.labelName[1])
        (N1,N2)=(tree.labelCount[0],tree.labelCount[1])
        featPos=tree.splitReference[0]
        featNeg=tree.splitReference[1]
        print("[%d %s /%d %s]\n"%(N1,label1,N2,label2))
        print("|"*(depth+1)+"%s = %s: "%(splittingFeature,featPos))
        printTree(tree.lTree,depth+1)
        print("|"*(depth+1)+"%s = %s: "%(splittingFeature,featNeg))
        printTree(tree.rTree,depth+1)




def train(data,depth, maxDepth,labelName=[]):
    decisionTree=Tree(data)
    if labelName==[]:
        label1 = data[1][-1]
        label2 = ""
        count = 2
        while (label2 == "" or label2 == label1) and count<(len(data)):
            label2 = data[count][-1]
            count+=1
        labelName=[label1,label2]
    decisionTree.labelName=labelName
    (N1,N2)=labelNumbers(data,labelName[0],labelName[1])
    labelCount=[0,0]
    labelCount[0]=N1
    labelCount[1]=N2
    decisionTree.labelCount=labelCount
    if N1==0 or N2==0:
        decisionTree.leaf=True
        return decisionTree
    if depth<maxDepth:
        maxI = 0
        maxFeature = ""
        features = copy.deepcopy(data[0][:-1])
        for i in features:
            I = getMutualInfo(data,i)
            if I>maxI:
                maxI = I
                maxFeature = i
        if maxFeature == "":
            decisionTree.leaf=True 
            return decisionTree
        (lTreeData, rTreeData, lResponse, rResponse)=partition(data,maxFeature)
        newLData=cancelFeature(lTreeData,maxFeature)
        newRData=cancelFeature(rTreeData,maxFeature)
        decisionTree.splitReference = [lResponse, rResponse]
        decisionTree.splittingFeature = maxFeature
        if len(newLData)==1 or len(newRData)==1:
            decisionTree.leaf=True
            return decisionTree
        newLTree=train(newLData,depth+1,maxDepth,labelName)
        newRTree=train(newRData,depth+1,maxDepth,labelName)
        decisionTree.lTree=newLTree
        decisionTree.rTree=newRTree
        return decisionTree
    else:
        decisionTree.leaf=True
        return decisionTree 

        
def getMajority(tree):
    label1=tree.labelName[0]
    label2=tree.labelName[1]
    N1=tree.labelCount[0]
    N2=tree.labelCount[1]
    
    if N1>=N2:
        return label1
    else:
        return label2 

    

def predictOne(tree,data,features):
    if tree.leaf:
        return getMajority(tree)
    else:
        keyFeature = tree.splittingFeature
        featIndex=features.index(keyFeature)
        lReference=tree.splitReference[0]
        rReference=tree.splitReference[1]
        if data[featIndex] == lReference:
            return predictOne(tree.lTree, data, features)
        else:
            return predictOne(tree.rTree, data, features)
   
def predict(tree,data):
    results = []
    for i in range(len(data)-1):
        results.append(predictOne(tree,data[i+1],data[0]))
    return results

def getErr(L1, L2):
    N = len(L2)
    Err = 0
    for i in range(N):
        if L1[i] != L2[i]:
            Err+=1
    return float(Err)/N

def getLabel(data):
    N = len(data)-1
    labels = []
    for i in range(N):
        labels.append(data[i+1][-1])
    return labels 




def main():
    trainIn = getSheet("speechTrain.csv")
    trainLabel = getLabel(trainIn)
    testLabel = getLabel(testIn)
    depth = 3
    decisionTree = train(trainIn,0,depth)
    printTree(decisionTree,0)
    trainOut = predict(decisionTree,trainIn)
    trainErr = getErr(trainOut,trainLabel)
    print("train error:%f"%trainErr)  
    return decisonTree     

        

#import decisonTree.py 
class backEndProcess(object):
    def __init__ (self):
        #a list that stores all sample picture path in the folder
        self.pictre_path = []
        self.picture=None
        #api keys
        self.emotion_key = "6e205c33cfde48eb88b1b1870d9957fe"
        self.attention_key = "c650165254c94a4f9e5cdac99cf0c1fe"
        #length of picture path
        self.picture_count = 0
        #emotion data from last image for user call
        self.recent_emotion_data = None
        #attention data from last image for user call
        self.recent_attention_data = None
        #pre-trained decision tree model
        #self.model = decisionTree.trainModel()
        #emotion attribute labels
        self.population_emotion_data = []
        #attention label
        self.population_attention_data = []
        self.user_requested_emotion = None

        #default attention rate
        self.defaultAttentionRate = 56
        #margin for attention rate
        self.attentionMargin = 11.9
        #error for face finding
        self.errorMargin = 10
    
    def attention_data_process(self,faceList):
        #rateList=self.population_attention_data
        print(faceList)
        if (faceList == None or (len(faceList)==0)):
            self.population_attention_data.append(self.defaultAttentionRate)
            return

        else:
            #print("here too")
            margin= self.attentionMargin
            #centerX = imageHeight / 2
            #centerY = imageWIdth / 2
            attentionTotal = 0
            total = len(faceList)
            #faceDict = {}

            totalRoll = 0
            totalYaw = 0
            totalPitch = 0

            for faceDict in faceList:
            #left,top,pitch,row,yaw
                #faceDict = faceList[i]
                left = faceDict["faceRectangle"]["left"]
                top = faceDict["faceRectangle"]["top"]
                faceId = faceDict["faceId"]
                pitch = faceDict["faceAttributes"]["headPose"]["pitch"]
                roll = faceDict["faceAttributes"]["headPose"]["row"]
                yaw = faceDict["faceAttributes"]["headPose"]["yaw"]
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
            print(total)
            avgRoll = totalRoll/total
            avgYaw = totalYaw/total
            avgPitch = totalPitch/total
            
            for factDict in faceList:
                #left,top,pitch,row,yaw
                attention = True
                print("i told you so")
                left = faceDict["faceRectangle"]["left"]
                print("got left")
                top = faceDict["faceRectangle"]["top"]
                print("got top")
                faceId = faceDict["faceId"]
                pitch = faceDict["faceAttributes"]["headPose"]["pitch"]
                print("got pitch")
                roll = faceDict["faceAttributes"]["headPose"]["roll"]
                print("got roll")
                yaw = faceDict["faceAttributes"]["headPose"]["yaw"]
                print("got yaw")
                #print("pitch:%d,roll:%d,yaw:%d \n" % (pitch,roll,yaw))
                if(abs(pitch)>=avgPitch + margin):
                    attention = False
                if(abs(yaw)>=avgYaw + margin):
                    attention = False
                print("bullshit")
                if(abs(roll)>=(avgRoll + margin)):
                    attention = False
                print("0000000000000000")
                if(attention):
                    attentionTotal = attentionTotal + 1
                print("also bullshit")
            attentionRate = attentionTotal/total
            #append to field population_attention_data
            self.population_attention_data.append(attentionRate)
            print("whats wrong?")
    
            
            
    def emotion_detection(self):
        emotion_key = self.emotion_key #"6e205c33cfde48eb88b1b1870d9957fe"
        assert emotion_key
        emotion_recognition_url = "https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize"
        image_data = self.picture
        headers  = {'Ocp-Apim-Subscription-Key': emotion_key, "Content-Type": "application/octet-stream" }
        response = requests.post(emotion_recognition_url, headers=headers, data=image_data)
        response.raise_for_status()
        emotion_analysis = response.json()
        storage = emotion_analysis
        #print(emotion_analysis)
        self.emotion_data_process (storage) 

    def face_detection(self):
        subscription_key = self.attention_key #'c650165254c94a4f9e5cdac99cf0c1fe'
        filename = self.picture
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
        
        img_data = filename
        try:
            response = requests.post(uri_base + path_to_face_api,
                                     data=img_data, 
                                     headers=headers,
                                     params=params)
            #print ('Response:')
            parsed = response.json()
            storage = parsed
            #print (parsed)
            self.attention_data_process(storage)
            #print("no error !!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            return
            # display the image analysis data
            #return parsed
        except Exception as e:
            storage = None
            #print("000000000000000000000000000000000000000")
            self.attention_data_process(storage)
            #print(e)

    def trigger_main(self, path):
        self.picture_count+=1
        self.picture = open(path,"rb").read()
        t1 = threading.Thread(target=self.emotion_detection)
        t2 = threading.Thread(target=self.face_detection)
        t1.start()
        t2.start() 

    def trigger_curr(self, x,y,front_connection):
        t = threading.Thread(target=self.getThreeEmotions, args=(x,y,front_connection))

    
        
    def getThreeEmotions(self,faceList,xPos,yPos,connection):
        emotion1 = "neutral"
        emotion2 = "surprised"
        emotion3 = "happy"
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
            if(y >= left and y <= right and x <= bottom and x >= top):
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
                    elif( curr > second):
                        third = second
                        thirdString = secondString
                        second = curr
                        secondString = j
                    elif( curr > thid):
                        third = curr
                        thirdString = j
                emotion1 = firstString
                emotion2 = secondString
                emotion3 = thirdString
        connection = (emotion1,emotion2,emotion3)

        


    #called by the front end
    def getAttentionRateForUser(self):
        rateList = self.attention_attri_label
        return rateList[-1]
    
    def emotion_data_process(self,faceList):
        emotionList = self.population_emotion_data
        if(len(faceList)==0):
            emotionList.append([True,True,False])
            return
        total = len(faceList)
        happyCutoff = 0.3
        normalCutoff = 0.45
        sadCutoff = 0.3
        total = len(faceList)
        avghappy = 0
        avgnormal = 0
        avgsad = 0
        happyTotal = 0
        normalTotal = 0
        sadTotal = 0

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
'''
    def getThreeEmotions(self,xPos,yPos):
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
            if(yPos >= (left-errMrg) and yPos <= (right+errMrg) and xPos <= (bottom+errMrg) and xPos >= (top+errMrg)):
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
                    elif( curr > second):
                        third = second
                        thirdString = secondString
                        second = curr
                        secondString = j
                    elif( curr > thid):
                        third = curr
                        thirdString = j
                emotion1 = firstString
                emotion2 = secondString
                emotion3 = thirdString
                self.userRequestedEmotion = (emotion1,first,emotion2,second,emotion3,third)
                return
            else:
                self.userRequestedEmotion = ("normal",87.5,"happy",5.5,"sad",7)
                
                return
'''
'''

    #xPos and yPos should be positions in the original picture
    def getThreeEmotions(self,xPos,yPos):
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
            if(yPos >= (left-errMrg) and yPos <= (right+errMrg) and xPos <= (bottom+errMrg) and xPos >= (top+errMrg)):
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
                    elif( curr > second):
                        third = second
                        thirdString = secondString
                        second = curr
                        secondString = j
                    elif( curr > thid):
                        third = curr
                        thirdString = j
                emotion1 = firstString
                emotion2 = secondString
                emotion3 = thirdString
                self.userRequestedEmotion = (emotion1,first,emotion2,second,emotion3,third)
            else:
                self.userRequestedEmotion = ("normal",87.5,"happy",5.5,"sad",7)
'''

def test():
    testInstance = backEndProcess()
    testInstance.trigger_main("trump.jpg")
    time.sleep(2)
    print(testInstance.population_emotion_data)
    print(testInstance.population_attention_data)


#test()