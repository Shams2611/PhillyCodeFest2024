#Original Code developed by Rishab Kattimani
#edited by Chibuike Nwume
import boto3
import pprint
from PIL import Image, ImageDraw, ImageFont
import io
import senti

recog = boto3.client('rekognition', region_name='us-east-1')
def recogImg(path):
    img = path

    with (open(img,'rb')) as image_file:
        source = image_file.read()
        
    image = Image.open(io.BytesIO(source))
    draw = ImageDraw.Draw(image)
        
    detect = recog.detect_labels(Image={'Bytes':source})
    for i in detect['Labels']:
        #print(f"{i['Name']} ; confidence: {i['Confidence']}")
        for instances in i['Instances']:
            if 'BoundingBox' in instances:

                box = instances["BoundingBox"]

                left = image.width * box['Left']
                top = image.height * box['Top']
                width = image.width * box['Width']
                height = image.height * box['Height']

                points = (
                            (left,top),
                            (left + width, top),
                            (left + width, top + height),
                            (left , top + height),
                            (left, top)
                        )
                draw.line(points, width=5, fill = "#69f5d9")

                shape = [(left - 2, top - 35), (width + 2 + left, top)]
                draw.rectangle(shape, fill = "#69f5d9")

                font = ImageFont.truetype("arial.ttf", 30)

                draw.text((left + 170, top - 30), i["Name"], font=font, fill='#000000')

    return image.show()


def sentimentLabels(path):
    out=[]
    img = path
    with (open(img,'rb')) as image_file:
        source = image_file.read()
    
    image = Image.open(io.BytesIO(source))
    detect = recog.detect_labels(Image={'Bytes':source})
    for i in detect['Labels']:
        out.append([i['Name'],senti.detectSentiment(str(i['Name']))])
    
    return out

def recogSentiment(path):
    sentiment_val = 0
    sentiment_arr = [0,0,0]
    imgSentiment = sentimentLabels(path)
    #print(imgSentiment)
    '''for i in imgSentiment:
        if i == "POSITVE":
            sentiment_arr[0]+=1
        elif i=="NEGATIVE":
            sentiment_arr[1]+=1
        else:
            sentiment_arr[2]+=1
    if max(sentiment_arr)==sentiment_arr[0]:
        return("POSITIVE")
    elif max(sentiment_arr)==sentiment_arr[1]:
        return("NEGATIVE")
    else:
        return("NEUTRAL")'''
    return imgSentiment[-1]
