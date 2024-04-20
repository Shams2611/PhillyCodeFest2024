import boto3
from PIL import Image, ImageDraw, ImageFont
import io
import senti
import pprint

recog = boto3.client('rekognition', region_name='us-east-1')

class Counter:
    def __init__(self,c) -> None:
        self.c = c
    def changeC(self,k):
        self.c +=k
    def returnC(self):
        return self.c
    def reset(self):
        self.c = 0
    


count = Counter(0)

def faceSenti(path):
    img = path
    with (open(img,'rb')) as image_file:
            source = image_file.read()
    image = Image.open(io.BytesIO(source))
    detect = recog.detect_faces(Image={'Bytes':source},Attributes=['ALL'])
    try:
        emodict = [detect['FaceDetails'][0]['Landmarks'][0],detect['FaceDetails'][0]['Landmarks'][1]]
        pprint.pp(emodict)
        '''if (emodict['Value']==False and emodict['Confidence']>96) or (emodict['Value']==True and emodict['Confidence']<70):
            #print(emodict)
            count.changeC(1)
            #print(count.returnC())
        
        emotest = detect['FaceDetails'][0]['Emotions'] 
        max = {'Type':None,'Confidence':0}
        for i in emotest:
            if i['Confidence']>max['Confidence']:
                max = i
        #print(max)'''
    except IndexError:
        pass
    
    return None
#faceSenti(str("image.png"))

def faceSentiBytesSrc(source):

    detect = recog.detect_faces(Image={'Bytes':source},Attributes=['ALL'])
    try:
        emodict = [detect['FaceDetails'][0]['Landmarks'][0],detect['FaceDetails'][0]['Landmarks'][1]]
        pprint.pp(emodict)
        '''if (emodict['Value']==False and emodict['Confidence']>96) or (emodict['Value']==True and emodict['Confidence']<70):
            #print(emodict)
            count.changeC(1)
            #print(count.returnC())
        
        emotest = detect['FaceDetails'][0]['Emotions'] 
        max = {'Type':None,'Confidence':0}
        for i in emotest:
            if i['Confidence']>max['Confidence']:
                max = i
        #print(max)'''
    except IndexError:
        pass
    
    return None
#faceSenti(str("image.png"))