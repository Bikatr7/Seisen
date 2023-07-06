## built-in modules
import os
import time

## custom modules
from modules import util

class fileEnsurer:

   """
   
   The fileEnsurer class is used to ensure that the files needed to run the program are present and ready to be used.\n

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

      ##----------------------------------------------------------------dirs----------------------------------------------------------------

      ## the folder where all the config files are located
      self.config_dir = os.path.join(os.environ['USERPROFILE'],"SeisenConfig")

      ## the folder for all login related files are located
      self.logins_dir = os.path.join(self.config_dir, "Logins")

      ## the directory where all the lib files are located.
      self.lib_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "lib")

      ## the folder for all kana-related files are located
      self.kana_dir = os.path.join(self.config_dir, "Kana")

      ## the folder for all vocab-related files are located
      self.vocab_dir = os.path.join(self.config_dir, "Vocab")

      ##----------------------------------------------------------------paths----------------------------------------------------------------


      ##----------------------------------------------------------------functions----------------------------------------------------------------

      self.ensure_files()

##--------------------start-of-ensure_files()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   def ensure_files(self) -> None:

      """

      This function ensures that the files needed to run the program are present and ready to be used.\n
      
      Parameters:\n
      None\n

      Returns:\n
      None\n
      
      """

      self.create_needed_base_directories()

      self.ensure_loop_data_files()

      self.ensure_kana_files()

      self.ensure_vocab_files()

      self.ensure_lib_files()

      self.ensure_archive_files()

      time.sleep(0.1)

      os.system('cls')

##--------------------start-of-create_needed_base_directories()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   def create_needed_base_directories(self) -> None:

      """
      
      Creates the needed base directories.\n

      Parameters:\n
      self (object - fileEnsurer) : the fileEnsurer object\n

      Returns:\n
      None\n
      
      """

      util.standard_create_directory(self.config_dir)
      util.standard_create_directory(self.logins_dir)
      util.standard_create_directory(self.lib_dir)
      util.standard_create_directory(self.kana_dir)
      util.standard_create_directory(self.vocab_dir)
               
##--------------------start-of-ensure_loop_data_files()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   def ensure_loop_data_files(self) -> None:

      """
      
      ensure that the files located in the loop data directory are present and ready to be used.\n

      Parameters:\n
      self (object - fileEnsurer) : the fileEnsurer object\n

      Returns:\n
      None\n

      """

      ##----------------------------------------------------------------dirs----------------------------------------------------------------

      ## the folder for all loop data related files are located
      loop_data_dir = os.path.join(self.config_dir, "Loop Data")

      ##----------------------------------------------------------------paths----------------------------------------------------------------

      ## the loop data file path itself
      loop_data_path = os.path.join(loop_data_dir, "loopData.txt")
   
      ##----------------------------------------------------------------other things----------------------------------------------------------------


      util.standard_create_directory(loop_data_dir)

      util.modified_create_file(loop_data_path, "0,0,0,0,")

##--------------------start-of-ensure_kana_files()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   def ensure_kana_files(self) -> None:

      """"
      
      Ensures that the kana files are present and read to be used.\n

      Parameters:\n
      self (object - fileEnsurer) : the fileEnsurer object\n

      Returns:\n
      None.\n

      """

      ##----------------------------------------------------------------paths----------------------------------------------------------------

      ## the path to where the typos for the kana file are located
      kana_typos_path = os.path.join(self.kana_dir, "kana typos.txt")

      ## the path to where the incorrect typos for the kana file are located
      kana_incorrect_typos_path = os.path.join(self.kana_dir, "kana incorrect typos.txt")

      ##----------------------------------------------------------------other things----------------------------------------------------------------

      util.standard_create_file(kana_typos_path)

      util.standard_create_file(kana_incorrect_typos_path)


##--------------------start-of-ensure_kana_files()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   def ensure_vocab_files(self) -> None:

      """"
      
      Ensures that the vocab files are present and read to be used.\n

      Parameters:\n
      self (object - fileEnsurer) : the fileEnsurer object\n

      Returns:\n
      None.\n

      """

      ##----------------------------------------------------------------paths----------------------------------------------------------------

      ## the path to where the typos for the vocab file are located
      vocab_typos_path = os.path.join(self.vocab_dir, "vocab typos.txt")

      ## the path to where the incorrect typos for the vocab file are located
      vocab_incorrect_typos_path = os.path.join(self.vocab_dir, "vocab incorrect typos.txt")

      ##----------------------------------------------------------------other things----------------------------------------------------------------

      util.standard_create_file(vocab_typos_path)

      util.standard_create_file(vocab_incorrect_typos_path)

##--------------------start-of-ensure_lib_files()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   def ensure_lib_files(self):

      """

      ensures that the lib files are present and ready to be used.\n

      Parameters:\n
      self (object - fileEnsurer) : the fileEnsurer object\n

      Returns:\n
      None\n
      

      """

      ##----------------------------------------------------------------paths----------------------------------------------------------------

      ## the path where the actual kana file is located, the one used for testing
      kana_actual_path = os.path.join(self.kana_dir, "kana.txt")

      ##----------------------------------------------------------------other things----------------------------------------------------------------

      self.ensure_remote_lib_files()

      if(os.path.exists(kana_actual_path) == False or os.path.getsize(kana_actual_path) == 0):
         self.ensure_local_lib_files(kana_actual_path)

##--------------------start-of-ensure_remote_lib_files()------- -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   def ensure_remote_lib_files(self):

      """

      ensures that the lib files for the remote handler are present and ready to be used\n

      Parameters:\n
      self (object - fileEnsurer) : the fileEnsurer object\n

      Returns:\n
      None\n
      
      """

      ##----------------------------------------------------------------dirs----------------------------------------------------------------

      ## lib files for remoteHandler.py
      remote_lib_dir = os.path.join(self.lib_dir, "remote")

      ##----------------------------------------------------------------paths----------------------------------------------------------------

      ## if remoteHandler failed to make a database connection
      database_connection_failed = os.path.join(remote_lib_dir, "isConnectionFailed.txt")

      ##----------------------------------------------------------------other things----------------------------------------------------------------

      util.standard_create_directory(remote_lib_dir)

      util.modified_create_file(database_connection_failed, "false")

##--------------------start-of-ensure_local_lib_files()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   def ensure_local_lib_files(self, kana_actual_path):

      """
      
      ensure that the files located in the kana directory are present and ready to be used.\n

      Parameters:\n
      self (object - fileEnsurer) : the fileEnsurer object\n
      kana_actual_path (str) : the path to the kana.txt file that is used for testing purposes\n

      Returns:\n
      None\n

      """

      ##----------------------------------------------------------------dirs----------------------------------------------------------------

      ## where the lib files for the local handler are located
      local_lib_dir_path = os.path.join(self.lib_dir, "local")

      ## where the local kana files are located
      local_kana_lib_dir_path = os.path.join(local_lib_dir_path, "kana")

      ##----------------------------------------------------------------paths----------------------------------------------------------------

      ## the kana seisen uses to determine if a word is kanji or not
      kana_filter_path_kana = os.path.join(local_kana_lib_dir_path, "kana.txt")

      ## the readings for the kana in the file path above
      kana_filter_path_readings = os.path.join(local_kana_lib_dir_path, "kana readings.txt")

      ##----------------------------------------------------------------other things----------------------------------------------------------------

      util.standard_create_directory(local_lib_dir_path)
      util.standard_create_directory(local_kana_lib_dir_path)

      black_list_characters_kana = ['ヶ', 'ョ', 'ゃ', 'ァ', 'ィ', 'ゥ', 'ェ', 'ォ', 'ァ', 'ゅ', 'ょ', 'ぉ', '-', 'ヱ', 'ゐ', 'ヰ', 'ー', 'ッ','っ']

      default_kana_to_write = ""
      kana_readings = []
      i = 0

      with open(kana_filter_path_readings, 'r', encoding="utf-8") as file:
         kana_readings = file.readlines()

      with open(kana_filter_path_kana, 'r', encoding="utf-8") as file:
         for line in file:
            i+=1
            if(line.strip() not in black_list_characters_kana):
               default_kana_to_write += str(i) + "," + line.strip() + "," + kana_readings[i-1].strip() + ",0,0,\n"

      with open(kana_actual_path, 'w+', encoding="utf-8") as file:
         file.write(default_kana_to_write)


##--------------------start-of-ensure_archive_files()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   def ensure_archive_files(self):
      
      """
      
      ensure that the files located in the archives directory are present and ready to be used.\n

      Parameters:\n
      self (object - fileEnsurer) : the fileEnsurer object\n

      Returns:\n
      None\n

      """

      ##----------------------------------------------------------------dirs----------------------------------------------------------------

      ## archives for previous versions of Seisen txt files
      archives_dir = os.path.join(self.config_dir, "Archives")

      ## archives for the database files
      database_archives_dir = os.path.join(archives_dir, "Database")

      ## archives for the local files
      local_archives_dir = os.path.join(archives_dir, "Local")

      ## archives for the database files
      remote_archives_dir = os.path.join(archives_dir, "Database")

      ## archives for the local-Database files
      local_remote_archives_dir = os.path.join(archives_dir, "LocalRemote")

      ##----------------------------------------------------------------paths----------------------------------------------------------------

      ## contains the date of the last local backup
      last_local_backup_file = os.path.join(local_archives_dir, "last_local_backup.txt")

      ## contains the date of the last database backup
      last_remote_backup_file = os.path.join(remote_archives_dir, "last_remote_backup.txt")

      ## contains the date of the last time the database was overwritten with local
      last_local_remote_backup_file = os.path.join(local_remote_archives_dir, "last_local_remote_backup.txt")

      ##----------------------------------------------------------------other things----------------------------------------------------------------

      util.standard_create_directory(archives_dir)
      util.standard_create_directory(database_archives_dir)
      util.standard_create_directory(local_archives_dir)
      util.standard_create_directory(local_remote_archives_dir)

      util.standard_create_file(last_local_backup_file)
      util.standard_create_file(last_remote_backup_file)
      util.standard_create_file(last_local_remote_backup_file)