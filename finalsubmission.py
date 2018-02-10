from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import sys, csv, math,copy,os
import time
import numpy as np
from builtins import len
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import requests 
import threading 
import random 




        
        
import csv, math,copy
def getSheet(inputFile):
    with open(inputFile) as csvfile:
        sheet = csv.reader(csvfile, delimiter = ',')
        newData = []
        for row in sheet:
            newData.append(row)
        val1 = newData[1][0]
        rows, cols = len(newData), len(newData[0])
        return newData


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
        return "[%d %s /%d %s]\n"%(N1,label1,N2,label2)
    else:
        splittingFeature=tree.splittingFeature
        (label1,label2)=(tree.labelName[0],tree.labelName[1])
        (N1,N2)=(tree.labelCount[0],tree.labelCount[1])
        featPos=tree.splitReference[0]
        featNeg=tree.splitReference[1]
        s2="[%d %s /%d %s]\n"%(N1,label1,N2,label2)
        s3="|  "*(depth+1)+"%s = %s: "%(splittingFeature,featPos)
        s4=printTree(tree.lTree,depth+1)
        s5="|  "*(depth+1)+"%s = %s: "%(splittingFeature,featNeg)
        s6=printTree(tree.rTree,depth+1)
        return s2+s3+s4+s5+s6



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






def train_tree():
    trainIn = getSheet("speechTrain.csv")
    trainLabel = getLabel(trainIn)
    depth = 5
    decisionTree = train(trainIn,0,depth)
    trainOut = predict(decisionTree,trainIn)
    trainErr = getErr(trainOut,trainLabel)
    outPutTree=printTree(decisionTree,0)
    print(outPutTree)
    print("train error:%f"%trainErr)  
    return (decisionTree,outPutTree,trainErr)    





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
        self.attentionMargin = 1
        #error for face finding
        self.errorMargin = 10
        self.inEmoMode = False
        
    
    
    
    def attention_data_process(self,faceList):
        if faceList == None or len(faceList) == 0:
            self.population_attention_data.append(0.23)
            return
        imageHeight=450
        imageWidth=600
        yawMargin = 15
        pitchMargin = 15
        rollMargin = 15
    
        centerY = imageHeight / 2
        centerX = imageWidth / 2
        totalAttention = 0
        total = len(faceList)
    
        for faceDict in faceList:
            #left,top,pitch,row,yaw
            attention = True
            left = faceDict["faceRectangle"]["left"]
            top = faceDict["faceRectangle"]["top"]
            width = faceDict["faceRectangle"]["width"]
            height = faceDict["faceRectangle"]["height"]
    
            pitch = faceDict["faceAttributes"]["headPose"]["pitch"]
            roll = faceDict["faceAttributes"]["headPose"]["roll"]
            yaw = faceDict["faceAttributes"]["headPose"]["yaw"]
            print("pitch:%d,roll:%d,yaw:%d \n" % (pitch,roll,yaw))
            
            x = left + width / 2
            y = top + height / 2
            #need to determine angle
            if(x>centerX):
                #right of the screen
                if(abs(yaw) > yawMargin):
                    attention = False
                    print("wrong yaw1")
            else:
                #left of the screen
                if(abs(yaw) > yawMargin):
                    attention = False
                    print("wrong yaw2")
                    
            print("here")
                    
    
            if(y>centerY):
                #bottom part of the screen
                if(abs(pitch) > pitchMargin):
                    attention = False
                    print("wrong pitch1")
            else:
                #top part of the screen
                if(abs(pitch) > pitchMargin):
                    attention = False
                    print("wrong pitch2")
                    
            print("here too")
    
            if(abs(roll) > rollMargin):
                attention = False
                print("wrong roll")
                
            print("here too too")
    
            if(attention):
                totalAttention = totalAttention + 1
        
        attenRate = totalAttention/(total*1.0)
        print(attenRate)
        self.population_attention_data.append(attenRate)
        
    def FaceBoundaries(self):
        faceList = self.recent_emotion_data
        return_list = []
        if faceList == None: return []
        for faceDict in faceList:
            x1=faceDict["faceRectangle"]["left"]
            y1=faceDict["faceRectangle"]["top"]
            x2=faceDict["faceRectangle"]["left"]+faceDict["faceRectangle"]["width"]
            y2=faceDict["faceRectangle"]["top"]+faceDict["faceRectangle"]["height"]
            return_list.append((x1*(3.0/4.0)+190,y1*(3.0/4.0)+237,x2*(3.0/4.0)+190,y2*(3.0/4.0)+237))
            
            
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

    def trigger_curr(self, x,y,front_connection,rect):
        t = threading.Thread(target=self.getThreeEmotions, args=(x,y,front_connection,rect))
        t.start()

    
        
    def getThreeEmotions(self,x,y,connection,rect):
        faceList = copy.deepcopy(self.recent_emotion_data)
        #print("00000000000000")
        emotion1 = ""
        emotion2 = ""
        emotion3 = ""
        margin = 20
        if (self.recent_emotion_data == None):
            return  
        for faceDict in faceList:
            left = faceDict["faceRectangle"]["left"]
            #print("Ok")
            top = faceDict["faceRectangle"]["top"]
            #print("ok")
            width = faceDict["faceRectangle"]["width"]
            #print("ok")
            height = faceDict["faceRectangle"]["height"]
            #print("ok")
            right = left + width
            bottom = top + height
            #print("left:%d top: %d width:%d height:%d x:%d y:%d"%(left,top,width,height,x,y))
            score = faceDict["scores"]
            #print("000000")

            #need to determine coordinate
            if(x >= (left - margin) and x <= (right + margin) and y <= (bottom + margin) and y >= (top - margin)):
                print("BullsEye")
                first = 0;
                second = 0;
                third = 0;
                firstString = ""
                secondString = ""
                thirdString = ""
                for j in score:
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
                    elif( curr > third):
                        third = curr
                        thirdString = j
                emotion1 = firstString
                emotion2 = secondString
                emotion3 = thirdString
                returnX = left
                returnY = top
                returnH = height
                returnW = width 
        connection[0] = emotion1
        connection[1] = emotion2
        connection[2] = emotion3
        rect[0] = returnX*0.75+190
        rect[1] = returnY*0.75+237
        rect[2] = returnX*0.75+190+returnW*0.75
        rect[3] = returnY*0.75+237+returnH*0.75
        #print(connection)

        


    #called by the front end
    def getAttentionRateForUser(self):
        rateList = self.attention_attri_label
        return rateList[-1]
    
    def emotion_data_process(self,faceList):
        if not self.inEmoMode:
            self.recent_emotion_data = faceList 
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
        
def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)
    

    
    
def init(data):
    data.treeCounter=0
    data.tree,data.treeContent,data.trainError=train_tree()
    data.att_rate_window_left = 840-65
    data.att_rate_window_top =  107
    data.att_rate_window_right = 840+65
    data.att_rate_window_bottom = 243

    data.succ_rate_window_left = 843-68
    data.succ_rate_window_top =  300
    data.succ_rate_window_right = 843+68
    data.succ_rate_window_bottom = 436
    
    data.emo_det_window_left = 720
    data.emo_det_window_top =  500
    data.emo_det_window_right = 720+240
    data.emo_det_window_bottom = 575
    
    data.counter = 0
    data.image_count = 0
    data.emotion_count = 0
    data.frame_num = 20
    data.output_path = "./"
    
    data.cam = cv2.VideoCapture(0)
    data.image = NONE
    data.tkimage = NONE
    data.emoimage = NONE
    data.var=random.choice([True,False])
    data.att_rate = 0.25
    data.att_show = False
    data.succ_rate = 0.57
    data.in_emo_det = False
    data.in_succ_ana = False 
    data.threeEmotions = ["","",""]
    data.outLine = [0,0,0,0]
    data.emo_x = NONE
    data.emo_y = NONE
    data.ImgWid = 600
    data.ImgHei = 450
    data.reduWid = 450
    data.redHei = 338
    data.att_show=False 
    
    data.spotlight = NONE
    
    #initiate class backEndProcess
    data.backEndProcess = backEndProcess()
    

def saveImage(data):
    filename = "pic{}.jpg".format(data.image_count)  # construct filename
    p = os.path.join(data.output_path, filename)  # construct output path
    data.image.save(p, "JPEG")  # save image as jpeg file
    #image_to_analyze = data.image
    print("[INFO] saved {}".format(filename))
    
    #change: trigger_main
    data.ImgWid,data.ImgHei = data.image.size
    data.backEndProcess.trigger_main(p)
  
    
# def saveEmoImage(data):
#     filename = "emo{}.jpg".format(data.emotion_count)  # construct filename
#     p = os.path.join(data.output_path, filename)  # construct output path
#     data.image.save(p, "JPEG")  # save image as jpeg file
#     print("[INFO] saved {}".format(filename))


def succRatePressed(event,data):
    data.in_succ_ana = not data.in_succ_ana
    data.percentage = (random.random())*0.4+0.6
    if not data.in_succ_ana: data.treeCounter=0
    

def attRatePressed(event,data):
    data.att_show = not data.att_show


def emoDetPressed(event,data):
    data.in_emo_det = not data.in_emo_det
    data.backEndProcess.inEmoMode = False
    data.in_emo_ana = False
    data.threeEmotions = ["","",""]
    data.outLine=[0,0,0,0]
    if data.in_emo_det:
        # data.emotion_count += 1
        # saveEmoImage(data)
        if data.image_count == 0:
            img = data.image
        else:
            filename = "pic{}.jpg".format(data.image_count)  # construct filename
            p = os.path.join(data.output_path, filename)  # construct output path
            print("[INFO] opened "+p)
            img = Image.open(p)
        
        #resize image
        img = img.resize((450,338),Image.ANTIALIAS)
        #converts to tkinter image
        tkImg=ImageTk.PhotoImage(image=img)
        imageLabel._image_cache=tkImg
        data.emoimage = tkImg
        


def emoAnaPressed(event, data):
    if data.in_emo_det:
        data.in_emo_ana = True
        data.backEndProcess.inEmoMode = True 
        data.emo_x = event.x
        data.emo_y = event.y 
    
        #change trigger_curr
        x = (event.x-190)*(4.0/3.0)#*float(600)/450
        y = (event.y-237)*(4.0/3.0)#*float(450)/338
        #data.threeEmotions = NONE
        data.backEndProcess.trigger_curr(x,y,data.threeEmotions,data.outLine)
        #print("mouse pressed")
        
def mousePressed(event, data):
    # use event.x and event.y

    
    if(data.att_rate_window_left <= event.x and event.x <= data.att_rate_window_right
    and data.att_rate_window_top <= event.y and event.y <= data.att_rate_window_bottom):
        attRatePressed(event, data)
    
    if(data.succ_rate_window_left <= event.x and event.x <= data.succ_rate_window_right
    and data.succ_rate_window_top <= event.y and event.y <= data.succ_rate_window_bottom):
        succRatePressed(event, data)
    
    if(data.emo_det_window_left <= event.x and event.x <= data.emo_det_window_right
    and data.emo_det_window_top <= event.y and event.y <= data.emo_det_window_bottom):
        emoDetPressed(event, data)
    
    if(190 <= event.x and event.x <= 640 
    and 237 <= event.y and event.y <= 575):
        emoAnaPressed(event, data)

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def updateImage(data):
    #gets new frame from webcam feed every time it's called
    ret,frame=data.cam.read()
    frame=cv2.flip(frame,1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img=Image.fromarray(cv2image)
    h=450
    desiredW=600
    img=img.crop((0,0,desiredW,h))
    #data.ImgWid,data.ImgHei = img.size
    #print(data.ImgWid,data.ImgHei)
    data.image=img
    #converts to tkinter image
    tkImg=ImageTk.PhotoImage(image=img)
    imageLabel._image_cache=tkImg
    data.tkimage = tkImg


def timerFired(data):
    if data.in_succ_ana:
        data.treeCounter+=1
        #change
    if data.counter == 0:
        img = Image.open("bullshit.png")
        #resize image
        img = img.resize((100,85),Image.ANTIALIAS).convert('RGB')
        #converts to tkinter image
        tkImg=ImageTk.PhotoImage(image=img)
        imageLabel._image_cache=tkImg
        data.spotlight = tkImg
            
    #update counter
    data.counter += 1
    #save image
    if data.counter % data.frame_num == 0:
        data.image_count += 1
        saveImage(data)
    #update image
    updateImage(data)
    #change update att rate
    if (len(data.backEndProcess.population_attention_data) != 0):
        data.att_rate = data.backEndProcess.population_attention_data[-1]
        #if (data.counter%10 == 0):
        #    data.att_rate = random.choice([1,-1])*random.random()*0.01*data.att_rate + data.att_rate
        
    
    
def drawBackground(canvas,data):
    #draws the background around the image    
    color=rgbString(23,24,20)
    rectW,rectH=1200,800
    canvas.create_rectangle(0,0,rectW*2,rectH*2,fill=color,width=0)
    # if data.spotlight != NONE:
    #     canvas.create_image(0,0,anchor=NW,image=data.spotlight)
    
    
def drawMiddleLine(canvas,data):
    color = rgbString(218, 218, 218)
    canvas.create_line(680,0,680,750, fill = color, width = 2)
    
def drawSuccRateWindow(canvas,data):
    red = int(96 * (data.succ_rate / 1.0))
    green = int(202 * (data.succ_rate / 1.0))
    blue = int(247 * (data.succ_rate / 1.0))
    fillColor=rgbString(red,green,blue)
    
    color=rgbString(23,24,20)
    
    textColor=rgbString(225,225,225)
    x0=data.succ_rate_window_left
    y0=data.succ_rate_window_top
    x1=data.succ_rate_window_right
    y1=data.succ_rate_window_bottom
    r=20

    x2=x0+r
    y2=y0+r
    x3=x1-r
    y3=y1-r
    

    canvas.create_arc(x0,y0,x1,y1,outline="",fill=fillColor,style=tk.PIESLICE,start=90,extent=(-data.succ_rate*(359)),width=0)
    canvas.create_arc(x2,y2,x3,y3,outline="",fill=color,style=tk.PIESLICE,start=90,extent=(-data.succ_rate*(359)),width=0)
    canvas.create_text((x0+x1)/2,(y0+y1)/2,text="Success: "+str(int(data.succ_rate*100))+"%",fill=textColor)


def drawAttRateWindow(canvas,data):
    
    red = int(96 * (data.succ_rate / 1.0))
    green =int(202 * (data.succ_rate / 1.0))
    blue = int(247 * (data.succ_rate / 1.0))
    fillColor=rgbString(red,green,blue)
    color=rgbString(23,24,20)
    textColor=rgbString(225,225,225)
    x0=data.att_rate_window_left
    y0=data.att_rate_window_top
    x1=data.att_rate_window_right
    y1=data.att_rate_window_bottom
    r=20
    
    x2=x0+r
    y2=y0+r
    x3=x1-r
    y3=y1-r
    

    canvas.create_arc(x0,y0,x1,y1,outline="",fill=fillColor,style=tk.PIESLICE,start=90,extent=-data.att_rate*359,width=0)
    canvas.create_arc(x2,y2,x3,y3,outline="",fill=color,style=tk.PIESLICE,start=90,extent=-data.att_rate*359,width=0)
    canvas.create_text((x0+x1)/2,(y0+y1)/2,text="Attention: "+str(int(data.att_rate*100))+"%",fill=textColor)
    

def drawEmoDetWindow(canvas,data):
    fillColor=rgbString(108,109,105)
    textColor=rgbString(225,225,225)
    x0=data.emo_det_window_left
    y0=data.emo_det_window_top
    x1=data.emo_det_window_right
    y1=data.emo_det_window_bottom
    r=3

    x2=x0+r
    y2=y0
    x3=x1-r
    y3=y1
    canvas.create_rectangle(x2,y2,x3,y3,fill=fillColor,width=0)

    x4=x0
    y4=y0+r
    x5=x1
    y5=y1-r
    canvas.create_rectangle(x4,y4,x5,y5,fill=fillColor,width=0)

    x6=x0
    y6=y0
    x7=x6+2*r
    y7=y6+2*r
    canvas.create_oval(x6,y6,x7,y7,fill=fillColor,width=0)

    x8=x1-2*r
    y8=y0
    x9=x8+2*r
    y9=y8+2*r
    canvas.create_oval(x8,y8,x9,y9,fill=fillColor,width=0)

    x10=x0
    y10=y1-2*r
    x11=x10+2*r
    y11=y10+2*r
    canvas.create_oval(x10,y10,x11,y11,fill=fillColor,width=0)

    x12=x1-2*r
    y12=y1-2*r
    x13=x1
    y13=y1
    canvas.create_oval(x12,y12,x13,y13,fill=fillColor,width=0)

    canvas.create_text((x0+x1)/2,(y0+y1)/2,text="Emotion Detection",fill=textColor)
    
    
def drawVideoWindowNotEmo(canvas,data):
    color=rgbString(218, 218, 218)
    canvas.create_rectangle(40,125,640,575, fill = color, width = 3,outline="grey")
    canvas.create_image(40,125,anchor=NW,image=data.tkimage)
    
    if data.att_show:
        face_list = data.backEndProcess.FaceBoundaries()
        if face_list==None:return
        for n in face_list:
            print("0000000000000")
            (x0,y0,x1,y1)=n
            outline_color = "green"
            canvas.create_rectangle(x0,y0,x1,y1,outline = outline_color) 
    
def predictResult(data):
    #high/low concentration 
    list1 = copy.deepcopy(data.backEndProcess.population_attention_data)
    #happy, normal, sad
    list2 = copy.deepcopy(data.backEndProcess.population_emotion_data)
    new_list=[["attention","happy","normal","sad","attentionVariance","Interest"]]
    for i in range(min(len(list1),len(list2))):
        new_list.append([list1[i]>=0.5,list2[i][0],list2[i][1],list2[i][2],data.var])
    results=predict(data.tree,new_list)
    return results 
    
def drawTree(canvas,data):
    strings=data.treeContent.splitlines()
    lines=min(data.treeCounter,len(strings))
    textColor = rgbString(96,202,247)
    if data.treeCounter>=3*len(strings):
        results = predictResult(data)
        
        percentage =( float(results.count("Y"))/(len(results)))*100
        canvas.create_text(200,700,text="your success prediction is %f" %percentage,fill=textColor,font=50)
        data.succ_rate = data.percentage
        
    else:
        for i in range(lines):
            canvas.create_text(200,800+20*i-data.treeCounter*15,text=strings[i],fill=textColor,font=28)
            

    
def drawVideoWindowEmo(canvas,data):
    #resize image
    img=data.image.resize((150,112),Image.ANTIALIAS)
    #converts to tkinter image
    tkImg=ImageTk.PhotoImage(image=img)
    imageLabel._image_cache=tkImg
    
    #draw
    color=rgbString(218, 218, 218)
    canvas.create_rectangle(40,125,640,575, fill = color, width = 3,outline="grey")
    canvas.create_image(40,125,anchor=NW,image=tkImg)
    
    
    
def drawEmoImgWindow(canvas,data):    
    #draw
    color=rgbString(218, 218, 218)
    textColor=rgbString(225,225,225)
    canvas.create_rectangle(190,237,640,575, fill = color, width = 3,outline="grey")
    canvas.create_image(190,237,anchor=NW,image=data.emoimage)
    
    #change three emotions
    if data.threeEmotions[0] != "":
        print("we are here")
        x = data.emo_x
        y = data.emo_y
        #print(data.threeEmotions)
        canvas.create_text(x+40, y-20, text=data.threeEmotions[0],fill=textColor,font=15)
        canvas.create_text(x+40, y, text=data.threeEmotions[1],fill=textColor,font=15)
        canvas.create_text(x+40, y+20, text=data.threeEmotions[2],fill=textColor,font=15)
        canvas.create_rectangle(data.outLine[0],data.outLine[1],data.outLine[2],data.outLine[3],outline = color,width=3)
    
    
def redrawAllEmo(canvas, data):
    drawBackground(canvas,data)
    drawMiddleLine(canvas,data)
    drawSuccRateWindow(canvas,data)
    drawAttRateWindow(canvas,data)
    drawEmoDetWindow(canvas,data)
    drawVideoWindowEmo(canvas,data)
    drawEmoImgWindow(canvas,data)


def redrawAllNotEmo(canvas, data):
    drawBackground(canvas,data)
    drawMiddleLine(canvas,data)
    drawSuccRateWindow(canvas,data)
    drawAttRateWindow(canvas,data)
    drawEmoDetWindow(canvas,data)
    drawVideoWindowNotEmo(canvas,data)
    

        
    

def redrawAllSucc(canvas,data):
    drawBackground(canvas,data)
    drawMiddleLine(canvas,data)
    drawSuccRateWindow(canvas,data)
    drawAttRateWindow(canvas,data)
    drawEmoDetWindow(canvas,data)
    drawTree(canvas,data)
    drawVideoWindowNotEmo(canvas,data)


def redrawAll(canvas, data):
    # draw in canvas
    if data.in_succ_ana:
        redrawAllSucc(canvas,data)
    elif data.in_emo_det:
        redrawAllEmo(canvas, data)
    else:
        redrawAllNotEmo(canvas, data)
    


####################################
# use the run function as-is
####################################

def run(width=1000, height=750):
    global root, imageLabel, canvas
    
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = tk.Toplevel()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    imageLabel = tk.Label(root)
    imageLabel.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run()
cv2.VideoCapture(0).release()
'''
def test():
    testInstance = backEndProcess()
    testInstance.trigger_main("trump.jpg")
    time.sleep(2)
    print(testInstance.population_emotion_data)
    print(testInstance.population_attention_data)


#test()
tree=train_tree()
'''