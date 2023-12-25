## built-in libraries
import os
import shutil

## custom modules
from handlers.fileHandler import FileHandler

from modules.logger import Logger

class FileEnsurer:

   """
   
   The FileEnsurer class is used to ensure that the files needed to run the program are present and ready to be used.

   """

   ## main dirs
   if(os.name == 'nt'):  ## Windows
      config_dir = os.path.join(os.environ['USERPROFILE'],"KudasaiConfig")
   else:  ## Linux
      config_dir = os.path.join(os.path.expanduser("~"), "KudasaiConfig")
      
   script_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

   log_path = os.path.join(config_dir, "log.txt")

   ##----------------------------------/

   ## sub dirs
   logins_dir = os.path.join(config_dir, "Logins")
   kana_dir = os.path.join(config_dir, "Kana")
   vocab_dir = os.path.join(config_dir, "Vocab")
   loop_data_dir = os.path.join(config_dir, "Loop Data")

   lib_dir = os.path.join(script_dir, "lib")

   remote_lib_dir = os.path.join(lib_dir, "remote")

   ##----------------------------------/

   ## paths
   loop_data_path = os.path.join(loop_data_dir, "loopData.txt")

##--------------------start-of-ensure_files()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   @staticmethod
   def ensure_files() -> None:

      """

      This function ensures that the files needed to run the program are present and ready to be used.
            
      """

      

      FileEnsurer.create_needed_base_directories()

      FileEnsurer.ensure_loop_data_files()

      FileEnsurer.ensure_kana_files()

      FileEnsurer.ensure_vocab_files()

      FileEnsurer.ensure_lib_files()

      FileEnsurer.ensure_archive_files()

##--------------------start-of-create_needed_base_directories()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   @staticmethod
   def create_needed_base_directories() -> None:

      """
      
      Creates the needed base directories.

      """

      FileHandler.standard_create_directory(FileEnsurer.logins_dir)
      FileHandler.standard_create_directory(FileEnsurer.lib_dir)
      FileHandler.standard_create_directory(FileEnsurer.kana_dir)
      FileHandler.standard_create_directory(FileEnsurer.vocab_dir)
      FileHandler.standard_create_directory(FileEnsurer.remote_lib_dir)
               
##--------------------start-of-ensure_loop_data_files()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   @staticmethod
   def ensure_loop_data_files() -> None:

      """
      
      Ensures that the files located in the loop data directory are present and ready to be used.

      """

      FileHandler.standard_create_directory(FileEnsurer.loop_data_dir)

      FileHandler.modified_create_file(FileEnsurer.loop_data_path, "0,0,0,0,")

##--------------------start-of-ensure_kana_files()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   @staticmethod
   def ensure_kana_files() -> None:

      """"
      
      Ensures that the kana files are present and ready to be used.

      """

      ##----------------------------------------------------------------paths----------------------------------------------------------------

      ## the path to where the typos for the kana file are located
      kana_typos_path = os.path.join(FileEnsurer.kana_dir, "kana typos.txt")

      ## the path to where the incorrect typos for the kana file are located
      kana_incorrect_typos_path = os.path.join(FileEnsurer.kana_dir, "kana incorrect typos.txt")

      ##----------------------------------------------------------------other things----------------------------------------------------------------

      FileHandler.standard_create_file(kana_typos_path)

      FileHandler.standard_create_file(kana_incorrect_typos_path)

##--------------------start-of-ensure_kana_files()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   @staticmethod
   def ensure_vocab_files() -> None:

      """"
      
      Ensures that the vocab files are present and ready to be used.

      """

      ##----------------------------------------------------------------paths----------------------------------------------------------------

      ## the path to where the typos for the vocab file are located
      vocab_typos_path = os.path.join(FileEnsurer.vocab_dir, "vocab typos.txt")

      ## the path to where the incorrect typos for the vocab file are located
      vocab_incorrect_typos_path = os.path.join(FileEnsurer.vocab_dir, "vocab incorrect typos.txt")

      ##----------------------------------------------------------------other things----------------------------------------------------------------

      FileHandler.standard_create_file(vocab_typos_path)

      FileHandler.standard_create_file(vocab_incorrect_typos_path)

##--------------------start-of-ensure_lib_files()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   @staticmethod
   def ensure_lib_files() -> None:

      """

      Ensures that the lib files are present and ready to be used.\n

      """

      ##----------------------------------------------------------------paths----------------------------------------------------------------

      ## the path where the actual kana file is located, the one used for testing
      kana_actual_path = os.path.join(FileEnsurer.kana_dir, "kana.txt")

      ## the path where the actual kana csep file is located, the one used for testing
      kana_csep_actual_path = os.path.join(FileEnsurer.kana_dir, "kana csep.txt")

      ## the path where the actual vocab file is located, the one used for testing
      vocab_actual_path = os.path.join(FileEnsurer.vocab_dir, "vocab.txt")

      ## the path where the actual vocab csep file is located, the one used for testing
      vocab_csep_actual_path = os.path.join(FileEnsurer.vocab_dir, "vocab csep.txt")

      ##----------------------------------------------------------------other things----------------------------------------------------------------

      FileEnsurer.ensure_remote_lib_files()

      ## if kana testing files are damaged or empty, then repair them
      if(os.path.exists(kana_actual_path) == False or os.path.getsize(kana_actual_path) == 0 or os.path.exists(kana_csep_actual_path) == False or os.path.getsize(kana_csep_actual_path) == 0):
         FileEnsurer.ensure_kana_local_lib_files(kana_actual_path, kana_csep_actual_path)

      ## if vocab testing files are damaged or empty, then repair them
      if(os.path.exists(vocab_actual_path) == False or os.path.getsize(vocab_actual_path) == 0 or os.path.exists(vocab_csep_actual_path) == False or os.path.getsize(vocab_csep_actual_path) == 0):
         FileEnsurer.ensure_vocab_local_lib_files(vocab_actual_path, vocab_csep_actual_path)

##--------------------start-of-ensure_remote_lib_files()------- -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   @staticmethod
   def ensure_remote_lib_files() -> None:

      """

      Ensures that the remote lib files for the remote handler are present and ready to be used.
      
      """

      ##----------------------------------------------------------------dirs----------------------------------------------------------------

      ##----------------------------------------------------------------paths----------------------------------------------------------------

      ## if remoteHandler failed to make a database connection
      database_connection_failed_path = os.path.join(FileEnsurer.remote_lib_dir, "isConnectionFailed.txt")

      ##----------------------------------------------------------------other things----------------------------------------------------------------

      ## needs to be false so that connectionHandler.py will attempt to connect
      FileHandler.modified_create_file(database_connection_failed_path, "false")

##--------------------start-of-ensure_kana_local_lib_files()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   @staticmethod
   def ensure_kana_local_lib_files(kana_actual_path:str, kana_csep_actual_path:str) -> None:

      """
      
      Ensures that the local lib kana files are present and ready to be used.

      Parameters:\n
      kana_actual_path (str) : the path to the kana.txt file that is used for testing purposes.
      kana_csep_actual_path (str) : the path to the kana csep.txt file that is used for testing purposes.

      """

      ##----------------------------------------------------------------dirs----------------------------------------------------------------

      ## where the lib files for the local handler are located
      local_lib_dir_path = os.path.join(FileEnsurer.lib_dir, "local")

      ## where the local kana files are located
      local_kana_lib_dir_path = os.path.join(local_lib_dir_path, "kana")

      ##----------------------------------------------------------------paths----------------------------------------------------------------

      ## the kana seisen uses to determine if a word is kanji or not
      kana_filter_path_kana = os.path.join(local_kana_lib_dir_path, "kana.txt")

      ## the readings for the kana in the file path above
      kana_filter_path_readings = os.path.join(local_kana_lib_dir_path, "kana readings.txt")

      ## the answers for the kana in file path above
      kana_csep_path = os.path.join(local_kana_lib_dir_path, "kana csep.txt")

      ##----------------------------------------------------------------other things----------------------------------------------------------------

      Logger.log_action("Local kana files were reset to default using local lib")

      ## kana black list, small kana and symbols
      black_list_characters_kana = ['ヶ', 'ョ', 'ゃ', 'ァ', 'ィ', 'ゥ', 'ェ', 'ォ', 'ァ', 'ゅ', 'ょ', 'ぉ', '-', 'ヱ', 'ゐ', 'ヰ', 'ー', 'ッ','っ']

      black_list_indexes = []

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
            else:
               black_list_indexes.append(i)

      with open(kana_actual_path, 'w+', encoding="utf-8") as file:
         file.write(default_kana_to_write)
         

      with open(kana_csep_path, 'r', encoding="utf-8") as file:
         kana_csep = file.readlines()

      for i, csep in enumerate(kana_csep,start=1):

         if(i not in black_list_indexes):
            kana_csep_insert_values = [str(i), str(i), csep.rstrip(',\n'), "2"]

            FileHandler.write_sei_line(kana_csep_actual_path, kana_csep_insert_values)

##--------------------start-of-ensure_vocab_local_lib_files()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   @staticmethod
   def ensure_vocab_local_lib_files(vocab_actual_path, vocab_csep_actual_path) -> None:

      """
      
      Ensures that the local lib vocab files are present and ready to be used.

      Parameters:
      vocab_actual_path (str) : the path to the vocab.txt file that is used for testing purposes.
      vocab_csep_actual_path (str) : the path to the vocab csep.txt file that is used for testing purposes.

      """

      ##----------------------------------------------------------------dirs----------------------------------------------------------------

      ## where the lib files for the local handler are located
      local_lib_dir_path = os.path.join(FileEnsurer.lib_dir, "local")

      ## where the local kana files are located
      local_vocab_lib_dir_path = os.path.join(local_lib_dir_path, "vocab")

      ##----------------------------------------------------------------paths----------------------------------------------------------------

      ## path to the starter vocab.txt file that is used for testing purposes
      local_vocab_lib_path = os.path.join(local_vocab_lib_dir_path, "vocab.txt")

      ## path to the starter vocab csep.txt file that is used for testing purposes
      local_vocab_csep_lib_path = os.path.join(local_vocab_lib_dir_path, "vocab csep.txt")

      ##----------------------------------------------------------------other things----------------------------------------------------------------

      Logger.log_action("Local vocab files were reset using to default using local lib")

      ## directly copy the files from the local lib to the actual files
      shutil.copy2(local_vocab_lib_path, vocab_actual_path)
      shutil.copy2(local_vocab_csep_lib_path, vocab_csep_actual_path)

##--------------------start-of-ensure_archive_files()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   @staticmethod
   def ensure_archive_files() -> None:
      
      """
      
      Ensures that the files located in the archives directory are present and ready to be used.

      """

      ##----------------------------------------------------------------dirs----------------------------------------------------------------

      ## archives for previous versions of Seisen txt files
      archives_dir = os.path.join(FileEnsurer.config_dir, "Archives")

      ## archives for the database files
      database_archives_dir = os.path.join(archives_dir, "Database")

      ## archives for the local files
      local_archives_dir = os.path.join(archives_dir, "Local")

      ## archives for the database files
      remote_archives_dir = os.path.join(archives_dir, "Database")

      ## archives for the local-remote files
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

      FileHandler.standard_create_directory(archives_dir)
      FileHandler.standard_create_directory(database_archives_dir)
      FileHandler.standard_create_directory(local_archives_dir)
      FileHandler.standard_create_directory(local_remote_archives_dir)

      FileHandler.standard_create_file(last_local_backup_file)
      FileHandler.standard_create_file(last_remote_backup_file)
      FileHandler.standard_create_file(last_local_remote_backup_file)
      FileHandler.standard_create_file(last_local_remote_backup_accurate_path)

