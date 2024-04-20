import boto3 

comprehend = boto3.client('comprehend', region_name='us-east-1')

def detectSentiment(arg):       
    # Key phrases
    phrases = comprehend.detect_key_phrases(Text=arg, LanguageCode='en')
    # Entities
    entities = comprehend.detect_entities(Text=arg, LanguageCode='en')
    #Sentiments
    sentiments = comprehend.detect_sentiment(Text=arg, LanguageCode='en')
    #return sentiment
    return(sentiments['Sentiment'])

