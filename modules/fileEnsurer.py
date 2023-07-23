## built-in modules
import os
import shutil

## custom modules
from modules import util

from modules.logger import logger

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

      ## lib files for remoteHandler.py
      self.remote_lib_dir = os.path.join(self.lib_dir, "remote")

      ##----------------------------------------------------------------paths----------------------------------------------------------------

      ## log file
      self.log_path = os.path.join(self.config_dir, "log.txt")

      ##----------------------------------------------------------------functions----------------------------------------------------------------

      ## makes config dir where log sits, if not already there

      try:
         os.mkdir(self.config_dir)
      except:
         pass

      ## make log path
      with open(self.log_path, "w+", encoding="utf-8") as file:
         file.truncate()

##--------------------start-of-ensure_files()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   def ensure_files(self, logger:logger) -> None:

      """

      This function ensures that the files needed to run the program are present and ready to be used.\n
      
      Parameters:\n
      self (object - fileEnsurer) : the fileEnsurer object.\n
      logger (object - logger) : the logger object.\n

      Returns:\n
      None\n
      
      """

      self.logger = logger

      self.create_needed_base_directories()

      self.ensure_loop_data_files()

      self.ensure_kana_files()

      self.ensure_vocab_files()

      self.ensure_lib_files()

      self.ensure_archive_files()

      self.logger.push_batch()

##--------------------start-of-create_needed_base_directories()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   def create_needed_base_directories(self) -> None:

      """
      
      Creates the needed base directories.\n

      Parameters:\n
      self (object - fileEnsurer) : the fileEnsurer object.\n

      Returns:\n
      None\n
      
      """

      util.standard_create_directory(self.logins_dir, self.logger)
      util.standard_create_directory(self.lib_dir, self.logger)
      util.standard_create_directory(self.kana_dir, self.logger)
      util.standard_create_directory(self.vocab_dir, self.logger)
      util.standard_create_directory(self.remote_lib_dir, self.logger)
               
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

      util.standard_create_directory(loop_data_dir, self.logger)

      util.modified_create_file(loop_data_path, "0,0,0,0,", self.logger)

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

      util.standard_create_file(kana_typos_path, self.logger)

      util.standard_create_file(kana_incorrect_typos_path, self.logger)

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

      util.standard_create_file(vocab_typos_path, self.logger)

      util.standard_create_file(vocab_incorrect_typos_path, self.logger)

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

      kana_csep_actual_path = os.path.join(self.kana_dir, "kana csep.txt")

      ## the path where the actual vocab file is located, the one used for testing
      vocab_actual_path = os.path.join(self.vocab_dir, "vocab.txt")

      vocab_csep_actual_path = os.path.join(self.vocab_dir, "vocab csep.txt")

      ##----------------------------------------------------------------other things----------------------------------------------------------------

      self.ensure_remote_lib_files()

      if(os.path.exists(kana_actual_path) == False or os.path.getsize(kana_actual_path) == 0 or os.path.exists(kana_csep_actual_path) == False or os.path.getsize(kana_csep_actual_path) == 0):
         self.ensure_kana_local_lib_files(kana_actual_path, kana_csep_actual_path)

      if(os.path.exists(vocab_actual_path) == False or os.path.getsize(vocab_actual_path) == 0):
         self.ensure_vocab_local_lib_files(vocab_actual_path, vocab_csep_actual_path)

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

      ##----------------------------------------------------------------paths----------------------------------------------------------------

      ## if remoteHandler failed to make a database connection
      database_connection_failed_path = os.path.join(self.remote_lib_dir, "isConnectionFailed.txt")

      ##----------------------------------------------------------------other things----------------------------------------------------------------

      util.modified_create_file(database_connection_failed_path, "false", self.logger)

##--------------------start-of-ensure_kana_local_lib_files()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   def ensure_kana_local_lib_files(self, kana_actual_path:str, kana_csep_actual_path:str):

      """
      
      ensure that the local lib kana files are present and ready to be used.\n

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

      kana_csep_path = os.path.join(local_kana_lib_dir_path, "kana csep.txt")

      ##----------------------------------------------------------------other things----------------------------------------------------------------

      self.logger.log_action("Local kana files were reset to default using local lib")

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
         

      with open(kana_csep_path, 'r', encoding="utf-8") as file:
         kana_csep = file.readlines()

      for i, csep in enumerate(kana_csep,start=1):

         kana_csep_insert_values = [str(i), str(i), csep.rstrip(',\n'), "2"]

         util.write_sei_line(kana_csep_actual_path, kana_csep_insert_values)

##--------------------start-of-ensure_vocab_local_lib_files()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   def ensure_vocab_local_lib_files(self, vocab_actual_path, vocab_csep_actual_path):

      """
      
      ensure that the local lib vocab files are present and ready to be used.\n

      Parameters:\n
      self (object - fileEnsurer) : the fileEnsurer object\n
      vocab_actual_path (str) : the path to the vocab.txt file that is used for testing purposes\n
      vocab_csep_actual_path (str) : the path to the vocab csep.txt file that is used for testing purposes\n

      Returns:\n
      None\n

      """

      ##----------------------------------------------------------------dirs----------------------------------------------------------------

      ## where the lib files for the local handler are located
      local_lib_dir_path = os.path.join(self.lib_dir, "local")

      ## where the local kana files are located
      local_vocab_lib_dir_path = os.path.join(local_lib_dir_path, "vocab")

      ##----------------------------------------------------------------paths----------------------------------------------------------------

      local_vocab_lib_path = os.path.join(local_vocab_lib_dir_path, "vocab.txt")

      local_vocab_csep_lib_path = os.path.join(local_vocab_lib_dir_path, "vocab csep.txt")

      ##----------------------------------------------------------------other things----------------------------------------------------------------

      self.logger.log_action("Local vocab files were reset using to default using local lib")

      shutil.copy2(local_vocab_lib_path, vocab_actual_path)
      shutil.copy2(local_vocab_csep_lib_path, vocab_csep_actual_path)

##--------------------start-of-ensure_archive_files()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   def ensure_archive_files(self):
      
      """
      
      ensure that the files located in the archives directory are present and ready to be used.\n
z
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

      ## contains a more accurate timestamp of the last time the database was overwritten with local
      last_local_remote_backup_accurate_path = os.path.join(local_remote_archives_dir, "last_local_remote_backup_accurate.txt")

      ##----------------------------------------------------------------other things----------------------------------------------------------------

      util.standard_create_directory(archives_dir, self.logger)
      util.standard_create_directory(database_archives_dir, self.logger)
      util.standard_create_directory(local_archives_dir, self.logger)
      util.standard_create_directory(local_remote_archives_dir, self.logger)

      util.standard_create_file(last_local_backup_file, self.logger)
      util.standard_create_file(last_remote_backup_file, self.logger)
      util.standard_create_file(last_local_remote_backup_file, self.logger)
      util.standard_create_file(last_local_remote_backup_accurate_path, self.logger)