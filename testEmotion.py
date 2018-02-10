def getThreeEmotions(self,faceList,xPos,yPos,connection):
        faceList = self.recent_emotion_data
        emotion1 = "neutral"
        emotion2 = "surprised"
        emotion3 = "happy"
        margin = self.
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
            #!!!!!!add margin
            if(y >= left - margin and y <= right + margin and x <= bottom + margin and x >= top -  margin):
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
                    elif( curr > thid):
                        third = curr
                        thirdString = j
                emotion1 = firstString
                emotion2 = secondString
                emotion3 = thirdString
        connection = (emotion1,emotion2,emotion3)