def attention_data_process(faceList):

    if (len(faceList)==0):
        return

    else:
        margin= 2
        attentionTotal = 0
        total = len(faceList)

        totalRoll = 0
        totalYaw = 0
        totalPitch = 0

        for faceDict in faceList:
            left = faceDict["faceRectangle"]["left"]
            top = faceDict["faceRectangle"]["top"]
            faceId = faceDict["faceId"]
            pitch = faceDict["faceAttributes"]["headPose"]["pitch"]
            roll = faceDict["faceAttributes"]["headPose"]["roll"]
            yaw = faceDict["faceAttributes"]["headPose"]["yaw"]
            totalYaw += abs(yaw)
            totalPitch += abs(pitch)
            totalRoll += abs(roll)

        avgRoll = totalRoll/total
        avgYaw = totalYaw/total
        avgPitch = totalPitch/total

        rollOff = False
        yawOff = False
        pitchOff = False
        
        for faceDict in faceList:
            #left,top,pitch,row,yaw
            attention = True
            left = faceDict["faceRectangle"]["left"]
            top = faceDict["faceRectangle"]["top"]
            faceId = faceDict["faceId"]
            pitch = faceDict["faceAttributes"]["headPose"]["pitch"]
            roll = faceDict["faceAttributes"]["headPose"]["roll"]
            yaw = faceDict["faceAttributes"]["headPose"]["yaw"]
            print("avgpitch:%d,avgroll:%d,avgyaw:%d \n" % (avgPitch,avgRoll,avgYaw))
            print("pitch:%d,roll:%d,yaw:%d \n" % (pitch,roll,yaw))
            if(abs(pitch)>=avgPitch + margin):
                rollOff = True
            if(abs(yaw)>=avgYaw + margin):
                yawOff = True
            if(abs(roll)>=(avgRoll + margin)):
                pitchOff = True
            if(rollOff):
                if(yawOff):
                    attention = False
                else:
                    if(pitchOff):
                        attention = False
                    else:
                        attention = True
            else:
                if(yawOff):
                    if(pitchOff):
                        attention = False
                    else:
                        attention = True
                else:
                    attention = True

            print(attention)
            if(attention):
                print("adding attentionTotal")
                attentionTotal = attentionTotal + 1

        attentionRate = attentionTotal/(total*1.0)
        #append to field population_attention_data
        print(attentionRate)

def test():
    faceList = [{'faceId': '3caf5889-d79b-4cb9-8014-df9cc2c75f98', 'faceRectangle': {'top': 339, 'left': 384, 'width': 51, 'height': 51}, 'faceAttributes': {'headPose': {'pitch': 0.0, 'roll': 10.3, 'yaw': -0.2}}}, {'faceId': 'c104fb1e-d69f-4466-8eda-3a934437c78c', 'faceRectangle': {'top': 314, 'left': 59, 'width': 41, 'height': 41}, 'faceAttributes': {'headPose': {'pitch': 0.0, 'roll': 23.2, 'yaw': -26.5}}}, {'faceId': '038111c2-1171-4843-a12c-814a5f1baf42', 'faceRectangle': {'top': 236, 'left': 173, 'width': 38, 'height': 38}, 'faceAttributes': {'headPose': {'pitch': 0.0, 'roll': 0.1, 'yaw': -1.6}}}, {'faceId': 'b66560da-fb4c-477f-adb3-26e5d65ebfa2', 'faceRectangle': {'top': 257, 'left': 417, 'width': 36, 'height': 36}, 'faceAttributes': {'headPose': {'pitch': 0.0, 'roll': 1.4, 'yaw': -24.4}}}, {'faceId': '9790cf42-98b0-4d50-aafb-07ca568727d5', 'faceRectangle': {'top': 351, 'left': 232, 'width': 36, 'height': 36}, 'faceAttributes': {'headPose': {'pitch': 0.0, 'roll': -5.6, 'yaw': -11.9}}}]
    attention_data_process(faceList)
    faceList = [{'faceId': '939ea0f1-93f5-4d3c-a1fe-facb016e2daa', 'faceRectangle': {'top': 282, 'left': 670, 'width': 148, 'height': 148}, 'faceAttributes': {'headPose': {'pitch': 0.0, 'roll': -9.4, 'yaw': -0.1}}}, {'faceId': 'e95735a4-cace-46cc-a257-304353a44cc3', 'faceRectangle': {'top': 119, 'left': 1051, 'width': 111, 'height': 111}, 'faceAttributes': {'headPose': {'pitch': 0.0, 'roll': -12.8, 'yaw': 15.2}}}, {'faceId': '85a82ab9-d43d-41da-97cc-589306a777dc', 'faceRectangle': {'top': 138, 'left': 1334, 'width': 108, 'height': 108}, 'faceAttributes': {'headPose': {'pitch': 0.0, 'roll': 7.3, 'yaw': -4.2}}}, {'faceId': '6245670d-9a99-43c5-b242-19689586d549', 'faceRectangle': {'top': 104, 'left': 173, 'width': 105, 'height':105}, 'faceAttributes': {'headPose': {'pitch': 0.0, 'roll': 5.5, 'yaw': 33.2}}}, {'faceId': '9c64ac10-2aa7-4066-9dc1-7e8e506d6ba7', 'faceRectangle': {'top': 98, 'left': 673, 'width': 97, 'height': 97}, 'faceAttributes': {'headPose': {'pitch': 0.0, 'roll': -9.5, 'yaw': 2.2}}}, {'faceId': 'b0ec223f-1828-4b20-8e71-238fb514103e', 'faceRectangle': {'top': 159, 'left': 411, 'width': 92, 'height': 92}, 'faceAttributes': {'headPose': {'pitch': 0.0, 'roll': -1.4, 'yaw': 10.5}}}]
    attention_data_process(faceList)


test()