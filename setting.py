import jsonAction
import sys
import datetime

class Setting:
    
    def __init__(self):
        
        self.app_path=sys.path[0].replace('\\','/')
        self.json_obj=jsonAction.JsonAction(self.app_path + "/setting.json")
        
        try:
            self.setting_dct=self.json_obj.json_read()
        except:
            self.write_defullt_setting()

    def get_Stile(self,object_name):
        return self.setting_dct[object_name]


    def set_Stile(self,dic):
        self.setting_dct=dic
        self.json_obj.json_write(self.setting_dct)


    def write_defullt_setting(self):
        self.setting_dct={
            "form":     {"background": "gray94" },
            "button":   {"background": "gray89"     , "foreground": "black" , "font": ["tahma", 9]},
            "entry":    {"background": "ivory1"     , "foreground": "black" , "font": ["tahma", 9]}, 
            "label":    {"background": "gray94"     , "foreground": "black" , "font": ["tahma", 9]},
            "path":     {"dbpath"    : self.app_path + "/Shop.db"},
            "datetime": {"lastrun"  : "first"}
            }
        self.json_obj.json_write(self.setting_dct)
   

    def set_last_runapp(self):
        self.setting_dct["datetime"]={"lastrun"  : str(datetime.datetime.now())}
        self.set_Stile(self.setting_dct)



