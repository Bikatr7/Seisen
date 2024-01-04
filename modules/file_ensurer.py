## built-in libraries
from datetime import datetime

import os
import shutil

## custom modules
from handlers.file_handler import FileHandler

from modules.logger import Logger

class FileEnsurer:

   """
   
   The FileEnsurer class is used to ensure that the files needed to run the program are present and ready to be used.

   """

   ## main dirs
   if(os.name == 'nt'):  ## Windows
      config_dir = os.path.join(os.environ['USERPROFILE'],"SeisenConfig")
   else:  ## Linux
      config_dir = os.path.join(os.path.expanduser("~"), "SeisenConfig")
      
   script_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

   log_path = os.path.join(config_dir, "log.txt")

   Logger.log_file_path = log_path

   ##----------------------------------/

   ## sub dirs
   logins_dir = os.path.join(config_dir, "logins")
   kana_dir = os.path.join(config_dir, "kana")
   vocab_dir = os.path.join(config_dir, "vocab")
   loop_data_dir = os.path.join(config_dir, "loopdata")
   archives_dir = os.path.join(config_dir, "archives")

   lib_dir = os.path.join(script_dir, "lib")

   local_lib_dir = os.path.join(lib_dir, "local")
   remote_lib_dir = os.path.join(lib_dir, "remote")

   local_archives_dir = os.path.join(archives_dir, "local")
   remote_archives_dir = os.path.join(archives_dir, "remote")
   local_remote_archives_dir = os.path.join(archives_dir, "localremote")

   ##----------------------------------/

   credentials_path = os.path.join(logins_dir, "credentials.txt")

   ##----------------------------------/

   ## loop data
   loop_data_path = os.path.join(loop_data_dir, "loop_data.txt")

   ## kana
   kana_path = os.path.join(kana_dir, "kana.txt")
   kana_synonyms_path = os.path.join(kana_dir, "kana_synonyms.txt")
   kana_typos_path = os.path.join(kana_dir, "kana_typos.txt")
   kana_incorrect_typos_path = os.path.join(kana_dir, "kana_incorrect_typos.txt")

   ## vocab
   vocab_path = os.path.join(vocab_dir, "vocab.txt")
   vocab_synonyms_path = os.path.join(vocab_dir, "vocab_synonyms.txt")
   vocab_typos_path = os.path.join(vocab_dir, "vocab_typos.txt")
   vocab_incorrect_typos_path = os.path.join(vocab_dir, "vocab_incorrect_typos.txt")

   ##----------------------------------/

   ## kana local lib

   ## where the local kana files are located
   local_kana_lib_dir = os.path.join(local_lib_dir, "kana")

   ## the kana seisen uses to determine if a word is kanji or not
   all_kana_path = os.path.join(local_kana_lib_dir, "kana.txt")

   ## the readings for the kana in the file path above
   all_kana_readings_path = os.path.join(local_kana_lib_dir, "kana_readings.txt")

   ## the answers for the kana in file path above
   all_kana_synonyms_path = os.path.join(local_kana_lib_dir, "kana_synonyms.txt")

   ##----------------------------------/

   ## vocab local lib

   ## where the local vocab files are located
   local_vocab_lib_dir = os.path.join(local_lib_dir, "vocab")

   ## path to the starter vocab.txt file that is used for testing purposes
   local_vocab_lib_path = os.path.join(local_vocab_lib_dir, "vocab.txt")

   ## path to the starter vocab synonym.txt file that is used for testing purposes
   local_vocab_synonyms_lib_path = os.path.join(local_vocab_lib_dir, "vocab_synonyms.txt")

   ##----------------------------------/

   ## contains the date of the last local backup
   last_local_backup_path = os.path.join(local_archives_dir, "last_local_backup.txt")

   ## contains the date of the last remote backup
   last_remote_backup_path = os.path.join(remote_archives_dir, "last_remote_backup.txt")

   ##contains the date of the last time remote was overwritten with local
   last_local_remote_backup_path = os.path.join(local_remote_archives_dir, "last_local_remote_overwrite.txt")

   ## contains a more accurate timestamp of the last time that remote was overwritten with local
   last_local_remote_overwrite_accurate_path = os.path.join(local_remote_archives_dir, "last_local_remote_overwrite_accurate.txt")
   
   ##----------------------------------/

   ## remote lib
   has_database_connection_failed_path = os.path.join(remote_lib_dir, "has_connection_failed.txt")

   kana_filter = []

   with open(all_kana_path, 'r', encoding="utf-8") as file:
      kana_filter = file.readlines()

##--------------------start-of-exit_seisen()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   @staticmethod
   def exit_seisen():

      """
      
      Pushes the log batch to the log and exits.

      """

      Logger.push_batch()

      exit()

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
      FileHandler.standard_create_directory(FileEnsurer.archives_dir)
               
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

      FileHandler.standard_create_file(FileEnsurer.kana_typos_path)

      FileHandler.standard_create_file(FileEnsurer.kana_incorrect_typos_path)

##--------------------start-of-ensure_kana_files()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   @staticmethod
   def ensure_vocab_files() -> None:

      """"
      
      Ensures that the vocab files are present and ready to be used.

      """

      FileHandler.standard_create_file(FileEnsurer.vocab_typos_path)

      FileHandler.standard_create_file(FileEnsurer.vocab_incorrect_typos_path)

##--------------------start-of-ensure_lib_files()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   @staticmethod
   def ensure_lib_files() -> None:

      """

      Ensures that the lib files are present and ready to be used.

      """

      FileEnsurer.ensure_remote_lib_files()

      ## if kana testing files are damaged or empty, then repair them
      if(os.path.exists(FileEnsurer.kana_path) == False or os.path.getsize(FileEnsurer.kana_path) == 0 or os.path.exists(FileEnsurer.kana_synonyms_path) == False or os.path.getsize(FileEnsurer.kana_synonyms_path) == 0):
         FileEnsurer.repair_kana()

      ## if vocab testing files are damaged or empty, then repair them
      if(os.path.exists(FileEnsurer.vocab_path) == False or os.path.getsize(FileEnsurer.vocab_path) == 0 or os.path.exists(FileEnsurer.vocab_synonyms_path) == False or os.path.getsize(FileEnsurer.vocab_synonyms_path) == 0):
         FileEnsurer.repair_vocab()

##--------------------start-of-ensure_remote_lib_files()------- -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   @staticmethod
   def ensure_remote_lib_files() -> None:

      """

      Ensures that the remote lib files for the remote handler are present and ready to be used.
      
      """

      ## needs to be false so that connectionHandler.py will attempt to connect, only if it doesn't exist
      FileHandler.modified_create_file(FileEnsurer.has_database_connection_failed_path, "false")

##--------------------start-of-ensure_kana_local_lib_files()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   @staticmethod
   def repair_kana() -> None:

      """
      
      Fixes the kana files using the local lib files.

      """

      ## kana black list, small kana and symbols
      black_list_characters_kana = ['ヶ', 'ョ', 'ゃ', 'ァ', 'ィ', 'ゥ', 'ェ', 'ォ', 'ァ', 'ゅ', 'ょ', 'ぉ', '-', 'ヱ', 'ゐ', 'ヰ', 'ー', 'ッ','っ']

      black_list_indexes = []
      kana_readings = []

      default_kana_to_write = ""

      i = 0

      ## raw readings
      with open(FileEnsurer.all_kana_readings_path, 'r', encoding="utf-8") as file:
         kana_readings = file.readlines()

      ## kana characters
      with open(FileEnsurer.all_kana_path, 'r', encoding="utf-8") as file:

         for line in file:

            i+=1

            if(line.strip() not in black_list_characters_kana):
               default_kana_to_write += str(i) + "," + line.strip() + "," + kana_readings[i-1].strip() + ",0,0,\n"

            else:
               black_list_indexes.append(i)

      with open(FileEnsurer.kana_path, 'w+', encoding="utf-8") as file:
         file.write(default_kana_to_write)
      
      with open(FileEnsurer.all_kana_readings_path, 'r', encoding="utf-8") as file:
         kana_synonyms = file.readlines()

      for i, synonym in enumerate(kana_synonyms,start=1):

         if(i not in black_list_indexes):
            kana_csep_insert_values = [str(i), str(i), synonym.rstrip(',\n'), "kana"]

            FileHandler.write_sei_line(FileEnsurer.kana_synonyms_path, kana_csep_insert_values)

      Logger.log_action("Kana files repaired.")

##--------------------start-of-ensure_vocab_local_lib_files()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   @staticmethod
   def repair_vocab() -> None:

      """
      
      Fixes the vocab files using local lib files.

      """

      ## directly copy the files from the local lib to the actual files
      shutil.copy2(FileEnsurer.local_vocab_lib_path, FileEnsurer.vocab_path)
      shutil.copy2(FileEnsurer.local_vocab_synonyms_lib_path, FileEnsurer.vocab_synonyms_path)

      Logger.log_action("Vocab files repaired.")

##--------------------start-of-ensure_archive_files()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   @staticmethod
   def ensure_archive_files() -> None:
      
      """
      
      Ensures that the files located in the archives directory are present and ready to be used.

      """

      FileHandler.standard_create_directory(FileEnsurer.remote_archives_dir)
      FileHandler.standard_create_directory(FileEnsurer.local_archives_dir)
      FileHandler.standard_create_directory(FileEnsurer.local_remote_archives_dir)

      FileHandler.standard_create_file(FileEnsurer.last_local_backup_path)
      FileHandler.standard_create_file(FileEnsurer.last_remote_backup_path)

      FileHandler.standard_create_file(FileEnsurer.last_local_remote_backup_path)
      FileHandler.standard_create_file(FileEnsurer.last_local_remote_overwrite_accurate_path)

##--------------------start-of-create_archive_dir()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   @staticmethod
   def create_archive_dir(type_of_archive:int) -> str:

      """
      
      Creates the archive directory based on the given type of archive.

      Parameters:
      type_of_archive (int) : The type of archive. 1 for database, 2 for local.

      Returns:
      archive_directory (str) : The path to the newly created archive directory.

      """
      
      current_day = datetime.today().strftime('%Y-%m-%d')

      filePaths = {
         1: FileEnsurer.remote_archives_dir,
         2: FileEnsurer.local_archives_dir
      }

      archive_directory = os.path.join(filePaths[type_of_archive], current_day) 

      FileHandler.standard_create_directory(archive_directory)

      return archive_directory