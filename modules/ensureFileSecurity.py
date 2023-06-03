## built-in modules
import os
import time

##--------------------start-of-ensure_files()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def ensure_files():

   """

   This function ensures that the files needed to run the program are present.\n
   
   Parameters:\n
   None\n

   Returns:\n
   None\n
   
   """

   config_dir = os.path.join(os.environ['USERPROFILE'],"SeisenConfig")

   kana_dir = os.path.join(config_dir, "Kana")
   logins_dir = os.path.join(config_dir, "Logins")
   loop_data_dir = os.path.join(config_dir, "Loop Data")

   loop_data_path = os.path.join(loop_data_dir, "loopData.txt")

   if(os.path.isdir(config_dir) == False):
      print(config_dir + " created due to lack of the folder")
      time.sleep(0.1)

   if(os.path.isdir(kana_dir) == False):
      os.mkdir(kana_dir, 0o666)
      print(kana_dir + " created due to lack of the folder")
      time.sleep(0.1)
   
   if(os.path.isdir(logins_dir) == False):
      os.mkdir(logins_dir, 0o666)
      print(logins_dir + " created due to lack of the folder")
      time.sleep(0.1)

   if(os.path.exists(loop_data_path) == False or os.path.getsize(loop_data_path) == 0):
      print(loop_data_path + " was created due to lack of the file")
      with open(loop_data_path, "w+", encoding="utf-8") as file:
         file.write("0,0,0,0,")

   os.system('cls')
