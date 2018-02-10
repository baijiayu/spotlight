from tkinter import *
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import os

def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)
    
def init(data):
    data.att_rate_window_left = 720
    data.att_rate_window_top =  150
    data.att_rate_window_right = 720+240
    data.att_rate_window_bottom = 300

    data.succ_rate_window_left = 720
    data.succ_rate_window_top =  450
    data.succ_rate_window_right = 720+240
    data.succ_rate_window_bottom = 600

    data.mousePressedPosn = (None,None)
    data.mousePressedInVideo = False
    data.mousePressedIsHead = False

    data.drawEmotionRect = False
    
    data.counter = 0
    data.image_count = 0
    data.emotion_count = 0
    data.frame_num = 60
    data.output_path = "./"

def drawBackground(canvas,data):
    #draws the background around the image    
    color=rgbString(23,24,20)
    rectW,rectH=1200,800
    data.offset=50
    offset=data.offset
    canvas.create_rectangle(0,0,rectW*2,rectH*2,fill=color,width=0)
    
def drawSuccRateWindow(canvas,data):
    fillColor=rgbString(52,52,45)
    textColor=rgbString(225,225,225)
    x0=data.succ_rate_window_left
    y0=data.succ_rate_window_top
    x1=data.succ_rate_window_right
    y1=data.succ_rate_window_bottom
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

    canvas.create_text((x0+x1)/2,(y0+y1)/2,text="Att Rate",fill=textColor)


def drawAttRateWindow(canvas,data):
    fillColor=rgbString(52,52,45)
    textColor=rgbString(225,225,225)
    x0=data.att_rate_window_left
    y0=data.att_rate_window_top
    x1=data.att_rate_window_right
    y1=data.att_rate_window_bottom
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

    canvas.create_text((x0+x1)/2,(y0+y1)/2,text="Succ Rate",fill=textColor)


def drawMiddleLine(canvas,data):
    color = rgbString(218, 218, 218)
    canvas.create_line(680,0,680,750, fill = color, width = 2)
    
# def drawFaceRectangle(canvas,data,img):
#     #Tkinter, draws a rectangle around the face
#     offset=data.offset
#     x,y,w,h=data.facerect
#     canvas.create_rectangle(x+offset,y+offset,x+w+offset,y+h+offset,
#         outline="red",width=3)

def drawFrame(canvas,data,img):
    #draws the webcam feed
    offset=data.offset
    canvas.create_image(offset,offset,anchor=NW,image=img)

def updateImage():
    #gets new frame from webcam feed every time it's called
    ret,frame=cap.read()
    frame=cv2.flip(frame,1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img=Image.fromarray(cv2image)
    h=450
    desiredW=600
    img=img.crop((0,0,desiredW,h))
    #converts to tkinter image
    tkImg=ImageTk.PhotoImage(image=img)
    imageLabel._image_cache=tkImg
    return (tkImg,img)
 
    
def saveImage(data,img):    
    filename = "pic{}.jpg".format(data.image_count)  # construct filename
    p = os.path.join(data.output_path, filename)  # construct output path
    img.save(p, "JPEG")  # save image as jpeg file
    print("[INFO] saved {}".format(filename))


def redrawAll(canvas,data):
    #continually updates the function
    data.counter += 1
    (tkImg,img) = updateImage()
    #saves image every data.frame_num frames
    if data.counter % data.frame_num == 0:
        data.image_count += 1
        saveImage(data,img)        
    root.after(30,func=lambda:redrawAll(canvas,data))
    drawFrame(canvas,data,tkImg)


def mousePressedWrapper(event, canvas, data):
    mousePressed(event,data,canvas)
    redrawAll(canvas,data)


def mousePressed(event,data,canvas):
    data.emotion_count += 1
    (tkImg,img) = updateImage()
    filename = "emo{}.jpg".format(data.emotion_count)  # construct filename
    p = os.path.join(data.output_path, filename)  # construct output path
    img.save(p, "JPEG")  # save image as jpeg file
    print("[INFO] saved {}".format(filename))
    
    
def run():
    width, height = 600, 450
    global cap, root, imageLabel, canvas
    cap = cv2.VideoCapture(0)
    cap.set(3, width)
    cap.set(4, height)
    root = tk.Toplevel()
    root.bind('<Escape>', lambda e: root.quit())
    imageLabel=tk.Label(root)
    imageLabel.pack()
    canvas=Canvas(root,width=1000,height=750)
    canvas.pack()
    class Struct: pass
    data=Struct()
    init(data)
    drawBackground(canvas,data)
    drawMiddleLine(canvas,data)
    drawAttRateWindow(canvas,data)
    drawSuccRateWindow(canvas,data)
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.after(0,func=lambda:redrawAll(canvas,data))
    (tkImg,img) = updateImage()
    drawFrame(canvas,data,tkImg)
    root.mainloop()
   
   
run()