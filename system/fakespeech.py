class Microphone(object):
    def __init__(self):
        self.mic = 0
    def __exit__(self, a, b, c):
        return True
    def __enter__(self):
        return True

class Recognizer(object):
    def __init__(self):
        self.rec = 0
    def recognize(self, a, p):
        return [{"text":a, "confidence":1}]
    def record(self, source):
        return raw_input ("speech> ")
    
