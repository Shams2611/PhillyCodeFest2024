import cv2
import os
import rekog
import faceSentiment
import io

if not os.path.exists('frames'):
    folder= 'frames'
    os.mkdir(folder)

cam = cv2.VideoCapture(0)

def getFrame(sec):
    cam.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = cam.read()

    if hasFrames:
        #cv2.imwrite("image"+str(count)+".jpg", image)     # save frame as JPG file
        faceSentiment.faceSentiBytesSrc(cv2.imencode('.jpg', image)[1].tostring())
        #os.remove("image"+str(count)+".jpg")
    return hasFrames

def mainCam():
    if not cam.isOpened():
        print("Cannot open camera")
        exit()
    else:   
        sec = 0
        frameRate = 5
        count=1
        success = getFrame(sec)
        while success:
            count = count + 1
            sec = sec + frameRate
            sec = round(sec, 2)
            success = getFrame(sec)
            if cv2.waitKey(1) == ord('q'):
                break
                        
    cam.release()
    cv2.destroyAllWindows()
