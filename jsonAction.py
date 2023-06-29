import json
class JsonAction:
    def __init__(self,fileName):
        self.fileName=fileName


    def json_read(self):
        with open(self.fileName)as f:
            return json.load(f)
        
    def json_write(self,dct):
            with open(self.fileName,"w")as f:
                json.dump(dct,f)