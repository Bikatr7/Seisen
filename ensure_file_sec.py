import os

from time import sleep

#-------------------Start-of-main()-------------------------------------------------

fileStoragePath = r'C:\ProgramData\SJLT'

if(os.path.isdir(fileStoragePath) == False):
    os.mkdir(fileStoragePath, 0o666)
    print("r'C:\ProgramData\SJLT' created due to lack of the folder")
    sleep(0.1)

    
prompt = r'C:\ProgramData\SJLT\prompt.txt'
loopData = r'C:\ProgramData\SJLT\loopData.txt'
sSchedule = r'C:\ProgramData\SJLT\sSchedule.txt'
   
if(os.path.exists(prompt) == False or os.path.getsize(prompt) == 0):
   print(prompt + " was created due to lack of the file")
   with open(prompt, "w+", encoding="utf-8") as file:
      pass

if(os.path.exists(loopData) == False or os.path.getsize(loopData) == 0):
   print(loopData + " was created due to lack of the file")
   with open(loopData, "w+", encoding="utf-8") as file:
      file.write("0,0,0,0,")

if(os.path.exists(sSchedule) == False or os.path.getsize(sSchedule) == 0):
   print(sSchedule + " was created due to lack of the file")
   with open(sSchedule, "w+", encoding="utf-8") as file:
      pass

os.system('cls')
