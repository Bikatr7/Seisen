## built-in modules
import os
import time

#-------------------Start-of-main()-------------------------------------------------

config_dir = os.path.join(os.environ['USERPROFILE'],"SeisenConfig")

if(os.path.isdir(config_dir) == False):
    os.mkdir(config_dir, 0o666)
    print(config_dir + " created due to lack of the folder")
    time.sleep(0.1)

    
prompt_path = os.path.join(config_dir, "prompt.txt")
loop_data_path = os.path.join(config_dir, "loopData.txt")
sSchedule_path = os.path.join(config_dir, "schedule.txt")
   
if(os.path.exists(prompt_path) == False or os.path.getsize(prompt_path) == 0):
   print(prompt_path + " was created due to lack of the file")
   with open(prompt_path, "w+", encoding="utf-8") as file:
      pass

if(os.path.exists(loop_data_path) == False or os.path.getsize(loop_data_path) == 0):
   print(loop_data_path + " was created due to lack of the file")
   with open(loop_data_path, "w+", encoding="utf-8") as file:
      file.write("0,0,0,0,")

if(os.path.exists(sSchedule_path) == False or os.path.getsize(sSchedule_path) == 0):
   print(sSchedule_path + " was created due to lack of the file")
   with open(sSchedule_path, "w+", encoding="utf-8") as file:
      pass

os.system('cls')
