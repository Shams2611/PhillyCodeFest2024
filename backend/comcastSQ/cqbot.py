import boto3
from dotenv import load_dotenv
import replicate
import os
import csv

load_dotenv()
class ChatBot:
    def __init__(self) -> None:
        self.convo = ""
        self.context=""
        self.csvTable=""
    def setContext(self,k,m):
        self.context = k
        self.context2 = m
    def getOutput(self,prompt):
        out = ""
        input = {
            "top_p": 1,
            "prompt": f"{prompt}",
            "temperature": 0.5,
            "system_prompt": f"Dont be mean. We are having a conversation. this is the context of the conversation:{self.convo}. Here is information on the subject at hand we are talking about: {self.context}. Here is some extra information: {self.csvTable}",
            "max_new_tokens": 500
        }
        for event in replicate.stream(
            "meta/llama-2-70b-chat",
            input=input
            ):
            out += str(event)+" "
        self.convo += (out+" ")
        return out 
    
bot = ChatBot()
file_path = 'context.txt'
with open('PhillyCodeFest2024/backend/comcastSQ/context.txt', 'r') as file:
    lines = file.readlines()
    file_content = ''.join(lines)

reader = csv.DictReader(open('PhillyCodeFest2024/backend/comcastSQ/codefestSheet.csv', 'r'))

bot.setContext(file_content,str(reader))
while True:
    k = input()
    print(bot.getOutput(k))
    print("\n")