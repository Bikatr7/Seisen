import os
import sys

sys.path.insert(0, os.getcwd())

from SMFVF_S import *
from time import sleep

#-------------------Start-of-main()-------------------------------------------------

fileStoragePath = r'C:\ProgramData\SJLT'


if(os.path.isdir(fileStoragePath) == False):
    os.mkdir(fileStoragePath, 0o666)
    print("r'C:\ProgramData\SJLT' created due to lack of the folder")

sleep(0.1)
    
prompt = open(r'C:\ProgramData\SJLT\prompt.txt', "w+",encoding="utf8")

prompt.close()
   
if(os.path.exists(r'C:\ProgramData\SJLT\loopData.txt') == False):
   print("r'C:\ProgramData\SJLT\loopData.txt' was created due to lack of the file")
   loopData = open(r'C:\ProgramData\SJLT\loopData.txt', "w+",encoding="utf8")
   loopData.write("0,0,0,0,")
   loopData.close()

if(os.path.exists(r'C:\ProgramData\SJLT\sSchedule.txt') == False):
   print("r'C:\ProgramData\SJLT\sSchedule.txt' was created due to lack of the file")
   sSchedule = open(r'C:\ProgramData\SJLT\sSchedule.txt', "w+",encoding="utf8")
   sSchedule.close()

os.system('cls')
