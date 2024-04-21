import boto3

# from PIL import Image, ImageDraw, ImageFont
# import io
# import senti
import pprint
import os


class Counter:
    def __init__(self, c) -> None:
        self.c = c

    def changeC(self, k):
        self.c += k

    def returnC(self):
        return self.c

    def reset(self):
        self.c = 0


class DrowsyDetection:
    def __init__(self):
        self.__recog = boto3.client(
            "rekognition",
            region_name="us-east-1",
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        )
        self.__count = Counter(0)

    def faceSentiBytesSrc(self, source):
        detect = self.__recog.detect_faces(Image={"Bytes": source}, Attributes=["ALL"])
        try:
            emodict = detect["FaceDetails"][0]["EyesOpen"]
            emotest = detect["FaceDetails"][0]["Emotions"]
            max = {"Type": None, "Confidence": 0}
            for i in emotest:
                if i["Confidence"] > max["Confidence"]:
                    max = i
            print(max)
            # pprint.pp(emodict)
            return (
                (emodict["Value"] == False and emodict["Confidence"] > 96)
                or (emodict["Value"] == True and emodict["Confidence"] < 70)
                and (max["Type"] or max["Type"] == "CALM")
            )

        except:
            return 0

    def getCount(self):
        return self.__count.returnC()

    def reset(self):
        self.__count.reset()


# count = Counter(0)
"""
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
"""
