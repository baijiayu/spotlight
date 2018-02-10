def getAttentionRate(self,faceList,imageHeight,imageWidth):
    yawMargin = 15
    pitchMargin = 15
    rollmargin = 15

    centerX = imageHeight / 2
    centerY = imageWIdth / 2
    totalAttention = 0
    total = len(faceList)

    for i in range(0,faceList.len()):
        #left,top,pitch,row,yaw
        attention = True
        faceDict = faceList[i]
        left = faceDict["faceRectangle"]["left"]
        top = faceDict["faceRectangle"]["top"]
        width = faceDict["faceRectangle"]["width"]
        height = faceDict["faceRectangle"]["height"]

        pitch = faceDict["faceAttributes"]["headPose"]["pitch"]
        roll = faceDict["faceAttributes"]["headPose"]["roll"]
        yaw = faceDict["faceAttributes"]["headPose"]["yaw"]
        print("pitch:%d,roll:%d,yaw:%d \n" % (pitch,roll,yaw))
        
        y = left + width / 2
        x = top + height / 2
        #need to determine angle
        if(y>centerY):
            #right of the screen
            if(yaw > yawMargin):
                attention = False;
                print("wrong yaw1\n")
        else:
            #left of the screen
            if(yaw < (-1*yawMargin)):
                attention = False;
                print("wrong yaw2\n")

        if(x>centerX):
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

    attenRate = totalAttention/(total*1.0)
    self.population_attention_data.append(attenRate)