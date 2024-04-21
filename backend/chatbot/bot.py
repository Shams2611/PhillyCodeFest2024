import replicate
import csv

class ChatBot:
    def __init__(self):
        self.context = None

        try:
            with open("./context.txt", "r") as file:
                self.context = file.read()
        except:
            pass

    def getOutput(self, prompt):
        out = ""

        if self.context is not None:
            sys_prompt = f"Dont be mean. We are having a conversation.\n\nHere is information on the subject at hand we are talking about: {self.context}\n\nPlease respond in a helpful matter that properly addresses any questions asked."
        else:
            sys_prompt = f"Dont be mean. We are having a conversation. Please respond in a helpful matter that properly addresses any questions asked."

        input = {
            "top_p": 1,
            "prompt": prompt,
            # "prompt": f"i am a highschool senior/college student{" named " + addinfo if addinfo is not None else ""}. Why do you think {studycenter} is a good place to study? Please tell me only 60 words and be a bit specific about the building and talk about which college majors usually study there",
            "temperature": 0.5,
            "system_prompt": sys_prompt,
            "max_new_tokens": 500,
        }

        for event in replicate.stream("meta/llama-2-70b-chat", input=input):
            out += str(event)

        return out
