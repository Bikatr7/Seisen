## built-in modules
import os
import time

class fileEnsurer:

   """
   
   The fileEnsurer class is used to ensure that the files needed to run the program are present.\n

   """

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   def __init__(self):

      """
      
      Initializes the fileEnsurer class.\n

      Parameters:\n
      None\n

      Returns:\n
      None\n

      """

      ## the folder where all the files are located
      self.config_dir = os.path.join(os.environ['USERPROFILE'],"SeisenConfig")

      ## the folder for all kana-related files are located
      self.kana_dir = os.path.join(self.config_dir, "Kana")

      ## the folder for all login related files are located
      self.logins_dir = os.path.join(self.config_dir, "Logins")

      ## the folder for all loop data related files are located
      self.loop_data_dir = os.path.join(self.config_dir, "Loop Data")

      ## the loop data file path itself
      self.loop_data_path = os.path.join(self.loop_data_dir, "loopData.txt")

      self.ensure_files()

##--------------------start-of-ensure_files()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   def ensure_files(self):

      """

      This function ensures that the files needed to run the program are present.\n
      
      Parameters:\n
      None\n

      Returns:\n
      None\n
      
      """

      self.create_needed_base_directories()

      self.ensure_loop_data_files()

      time.sleep(0.1)

      os.system('cls')

##--------------------start-of-create_needed_base_directories()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   def create_needed_base_directories(self):

      """
      
      Creates the needed base directories. Which contain all the config files\n

      Parameters:\n
      self (object - fileEnsurer) : the fileEnsurer object\n

      Returns:\n
      None\n
      
      """

      if(os.path.isdir(self.config_dir) == False):
         print(self.config_dir + " created due to lack of the folder")
         time.sleep(0.1)

      if(os.path.isdir(self.kana_dir) == False):
         os.mkdir(self.kana_dir, 0o666)
         print(self.kana_dir + " created due to lack of the folder")
         time.sleep(0.1)
      
      if(os.path.isdir(self.logins_dir) == False):
         os.mkdir(self.logins_dir, 0o666)
         print(self.logins_dir + " created due to lack of the folder")
         time.sleep(0.1)

      if(os.path.isdir(self.loop_data_dir) == False):
         os.mkdir(self.loop_data_dir, 0o666)
         print(self.loop_data_dir + " created due to lack of the folder")
         time.sleep(0.1)

##--------------------start-of-ensure_loop_data_files()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   def ensure_loop_data_files(self):

      """
      
      ensure that the files located in the loop data directory are present and ready to be used.\n

      Parameters:\n
      self (object - fileEnsurer) : the fileEnsurer object\n

      Returns:\n
      None\n

      """

      if(os.path.exists(self.loop_data_path) == False or os.path.getsize(self.loop_data_path) == 0):
         print(self.loop_data_path + " was created due to lack of the file")
         with open(self.loop_data_path, "w+", encoding="utf-8") as file:
            file.write("0,0,0,0,")