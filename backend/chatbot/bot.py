import replicate

class ChatBot:
    def __init__(self) -> None:
        pass

    def getOutput(self, studycenter, addinfo=None):
        out = ""
        input = {
            "top_p": 1,
            "prompt": f"i am a highschool senior/college student{" named " + addinfo if addinfo is not None else ""}. Why do you think {studycenter} is a good place to study? Please tell me only 60 words and be a bit specific about the building and talk about which college majors usually study there",
            "temperature": 0.5,
            "system_prompt": "answer my question without being mean or unhelpful and dont give any preambles",
            "max_new_tokens": 500,
        }

        for event in replicate.stream("meta/llama-2-70b-chat", input=input):
            out += str(event)

        return out
