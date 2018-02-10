    def attention_data_process(self,faceList):
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
    def getThreeEmotions(self,xPos,yPos):
        faceList = self.recent_emotion_data
        errMrg = self.errorMargin
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

    def getAttentionRateForUser(self):
        rateList = self.attention_attri_label
        return rateList[len(rateList)-1]


    def emotion_data_process(self,faceList):
        #hardcode result if empty list
        emotionList = self.population_emotion_data
        if(len(faceList)==0):
            emotionList.append([True,True,False])
        happy = False
        normal = False
        sad = False
        for i in range(0,len(faceList)):
            #faceList: raw data returned by emotion API
            
        emotionList.append([happy,normal,sad])