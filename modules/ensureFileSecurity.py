## built-in modules
import os
import time

class fileEnsurer:

   """
   
   The fileEnsurer class is used to ensure that the files needed to run the program are present.\n

   """

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   def __init__(self) -> None:

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

      ## the path where the actual kana file is located
      self.kana_actual_path = os.path.join(self.kana_dir, "kana.txt")

      ## the kana seisen uses to determine if a word is kanji or not
      self.kana_filter_path_kana = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), os.path.join("lib"), "kana.txt")

      ## the readings for the kana in the file path above
      self.kana_filter_path_readings = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), os.path.join("lib"), "kana readings.txt")

      ## the path to where the typos for the kana file are located
      self.kana_typos_path = os.path.join(self.kana_dir, "kana typos.txt")

      ## the path to where the incorrect typos for the kana file are located
      self.kana_incorrect_typos_path = os.path.join(self.kana_dir, "kana incorrect typos.txt")

      self.ensure_files()

##--------------------start-of-ensure_files()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   def ensure_files(self) -> None:

      """

      This function ensures that the files needed to run the program are present.\n
      
      Parameters:\n
      None\n

      Returns:\n
      None\n
      
      """

      self.create_needed_base_directories()

      self.ensure_loop_data_files()

      if(os.path.exists(self.kana_actual_path) == False or os.path.getsize(self.kana_actual_path) == 0):
         self.ensure_actual_kana_file()

      self.ensure_kana_files()

      time.sleep(0.1)

      os.system('cls')

##--------------------start-of-create_needed_base_directories()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   def create_needed_base_directories(self) -> None:

      """
      
      Creates the needed base directories. Which contain all the config files\n

      Parameters:\n
      self (object - fileEnsurer) : the fileEnsurer object\n

      Returns:\n
      None\n
      
      """

      if(os.path.isdir(self.config_dir) == False):
         os.mkdir(self.config_dir)
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

   def ensure_loop_data_files(self) -> None:

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

##--------------------start-of-ensure_actual_kana_file()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   def ensure_actual_kana_file(self) -> None:

      """
      
      ensure that the files located in the kana directory are present and ready to be used.\n

      Parameters:\n
      self (object - fileEnsurer) : the fileEnsurer object\n

      Returns:\n
      None\n

      """

      black_list_characters_kana = ['ヶ', 'ョ', 'ゃ', 'ァ', 'ィ', 'ゥ', 'ェ', 'ォ', 'ァ', 'ゅ', 'ょ', 'ぉ', '-', 'ヱ', 'ゐ', 'ヰ', 'ー', 'ッ','っ']

      default_kana_to_write = ""
      kana_readings = []
      i = 0

      with open(self.kana_filter_path_readings, 'r', encoding="utf-8") as file:
         kana_readings = file.readlines()

      with open(self.kana_filter_path_kana, 'r', encoding="utf-8") as file:
         for line in file:
            i+=1
            if(line.strip() not in black_list_characters_kana):
               default_kana_to_write += str(i) + "," + line.strip() + "," + kana_readings[i-1].strip() + ",0,0,\n"

      with open(self.kana_actual_path, 'w+', encoding="utf-8") as file:
         file.write(default_kana_to_write)

##--------------------start-of-ensure_kana_files()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   def ensure_kana_files(self) -> None:

      if(os.path.exists(self.kana_typos_path) == False):
         print(self.kana_typos_path + " was created due to lack of the file")
         with open(self.kana_typos_path, "w+", encoding="utf-8") as file:
            file.truncate()

      if(os.path.exists(self.kana_incorrect_typos_path) == False):
         print(self.kana_incorrect_typos_path + " was created due to lack of the file")
         with open(self.kana_incorrect_typos_path, "w+", encoding="utf-8") as file:
            file.truncate()