## built-in modules
from datetime import datetime

import os
import typing

## custom modules
from modules.logger import logger


class fileHandler():

    """
    
    The handler that handles interactions with files.\n

    """
##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, logger:logger) -> None:

        """
        
        Initializes the fileHandler class.\n

        Parameters:\n
        self (object - fileHandler) : the fileHandler object.\n
        logger (object - logger) : The logger object.\n

        Returns:\n
        None.\n

        """

        self.logger = logger

##--------------------start-of-standard_create_directory()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def standard_create_directory(self, directory_path:str) -> None:

        """

        Creates a directory if it doesn't exist, as well as logs what was created.\n

        Parameters:\n
        self (object - fileHandler) : the fileHandler object.\n
        directory_path (str) : path to the directory to be created.\n

        Returns:\n
        None.\n

        """

        if(os.path.isdir(directory_path) == False):
            os.mkdir(directory_path)
            self.logger.log_action(directory_path + " created due to lack of the folder")

##--------------------start-of-modified_create_directory()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def modified_create_directory(self, directory_path:str, path_to_check:str) -> None:

        """

        Creates a directory if it doesn't exist or if the path provided is blank or empty, as well as logs what was created.\n

        Parameters:\n
        self (object - fileHandler) : the fileHandler object.\n
        directory_path (str) : path to the directory to be created.\n
        path_to_check (str) : path to check if it is blank.\n

        Returns:\n
        None.\n

        """

        if(os.path.isdir(directory_path) == False or os.path.getsize(path_to_check) == 0):
            os.mkdir(directory_path)
            self.logger.log_action(directory_path + " created due to lack of the folder or " + path_to_check + " was blank or empty")

##--------------------start-of-standard_create_file()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def standard_create_file(self, file_path:str) -> None:

        """

        Creates a file if it doesn't exist, truncates it,  as well as logs what was created.\n

        Parameters:\n
        self (object - fileHandler) : the fileHandler object.\n
        file_path (str) : path to the file to be created.\n

        Returns:\n
        None.\n

        """

        if(os.path.exists(file_path) == False):
            self.logger.log_action(file_path + " was created due to lack of the file")
            with open(file_path, "w+", encoding="utf-8") as file:
                file.truncate()

##--------------------start-of-modified_create_file()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def modified_create_file(self, file_path:str, content_to_write:str) -> None:

        """

        Creates a path if it doesn't exist or if it is blank or empty, writes to it,  as well as logs what was created.\n

        Parameters:\n
        self (object - fileHandler) : the fileHandler object.\n
        file_path (str) : path to the file to be created.\n
        content to write (str) : content to be written to the file.\n

        Returns:\n
        None.\n

        """

        if(os.path.exists(file_path) == False or os.path.getsize(file_path) == 0):
            self.logger.log_action(file_path + " was created due to lack of the file or because it is blank")
            with open(file_path, "w+", encoding="utf-8") as file:
                file.write(content_to_write)

##--------------------start-of-create_archive_dir()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def create_archive_dir(self ,type_of_archive:int) -> str:

        """
        
        Creates the archive directory based on the given type of archive.\n

        Parameters:\n
        self (object - fileHandler) : the fileHandler object.\n
        type_of_archive (int) : The type of archive.\n

        Returns:\n
        archive_directory (str) : The path to the newly created archive directory.\n

        """

        ##----------------------------------------------------------------dirs----------------------------------------------------------------

        ## the folder where all the config files are located
        config_dir = os.path.join(os.environ['USERPROFILE'],"SeisenConfig")

        ## archives for previous versions of Seisen txt files
        archives_dir = os.path.join(config_dir, "Archives")

        ## archives for the database files
        database_archives_dir = os.path.join(archives_dir, "Database")

        ## archives for the local files
        local_archives_dir = os.path.join(archives_dir, "Local")

        ##----------------------------------------------------------------other things----------------------------------------------------------------
        
        current_day = datetime.today().strftime('%Y-%m-%d')

        filePaths = {
            1: database_archives_dir,
            2: local_archives_dir
        }

        ## not really sure why it's flagged by pylance.
        archive_directory = os.path.join(filePaths[type_of_archive], current_day) # type: ignore

        self.standard_create_directory(archive_directory)

        return archive_directory
    
##--------------------start-of-write_sei_line()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def write_sei_line(self, sei_file_path:str, items_to_write:typing.List[str]) -> None:

        """
        
        Writes the given items to the given sei file.\n

        Parameters:\n
        self (object - fileHandler) : the fileHandler object.\n
        sei_file_path (str) : the path to the sei file.\n
        items_to_write (list - str) : the items to be written to the sei file.\n

        Returns:\n
        None.\n

        """

        line = ",".join(str(item) for item in items_to_write)
        
        with open(sei_file_path, "a+", encoding="utf-8") as file:
            file.write(line + ",\n")

##-------------------start-of-read_sei_file()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def edit_sei_line(self, file_path:str, target_line:int, column_number:int, value_to_replace_to:str) -> None:
        
        """

        Edits the given line in the given file.\n

        Parameters:\n
        self (object - fileHandler) : the fileHandler object.\n
        file_path (str) : The file being edited.\n
        target_line (int) : The line number of the file we are editing.\n
        column_number (int) : The column number we are editing.\n
        value_to_replace_to (str) : The value to replace the edit value with.\n

        Returns:\n
        None.\n

        """

        with open(file_path, "r+", encoding="utf8") as f:
            lines = f.readlines()

        line = lines[target_line - 1]
        items = line.split(",")

        items[column_number - 1] = value_to_replace_to

        new_line = ",".join(items)

        lines[target_line - 1] = new_line

        with open(file_path, "w", encoding="utf8") as file:
            file.writelines(lines)

##-------------------start-of-read_sei_file()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def read_sei_file(self, sei_file_path:str, target_line:int, column:int) -> str:

        """

        Reads the given sei file and returns the value of the given column.\n
        
        Parameters:\n
        self (object - fileHandler) : the fileHandler object.\n
        sei_file_path (str) : the path to the sei file.\n
        target_line (int) : the line number of the sei file.\n
        column (int) : the column we are reading.\n

        Returns:\n
        file_details[column-1] : the value of the given column.\n

        """

        i,ii = 0,0
        build_string = ""
        file_details = []

        with open(sei_file_path, "r", encoding="utf-8") as file:
            sei_file = file.readlines()

        sei_line = sei_file[target_line - 1]

        count = sei_line.count(',')

        while(i < count):
            if(sei_line[ii] != ","):
                build_string += sei_line[ii]
            else:
                file_details.append(build_string)
                build_string = ""
                i+=1
            ii+=1
            
        return file_details[column-1]

##-------------------start-of-delete_sei_line()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def delete_sei_line(self, sei_file_path:str, target_line:int) -> None:

        """

        Deletes the specified line from the given sei file.\n

        Parameters:\n
        self (object - fileHandler) : the fileHandler object.\n
        sei_file_path (str) : the path to the sei file.\n
        target_line (int) : the line number to be deleted.\n

        Returns:\n
        None.\n

        """

        with open(sei_file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        with open(sei_file_path, "w", encoding="utf-8") as file:
            for i, line in enumerate(lines, 1):
                if i != target_line:
                    file.write(line)

##--------------------start-of-delete_all_occurrences_of_id()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def delete_all_occurrences_of_id(self, file_path:str, id_index:int, id_value:int) -> None:

        """
        
        Delete all lines that match a given id.\n

        Parameters:\n
        self (object - fileHandler) : the fileHandler object.\n
        file_path (str) : the path to the file to search.\n
        id_index (int) : the index of where the id should be.\n
        id_value (str) : the id to look for.\n

        Returns:\n
        None.\n

        """

        i = 0

        with open(file_path, 'r') as file:
            lines = file.readlines()

        line_count = len(lines)

        while(i < line_count):

            if(int(self.read_sei_file(file_path, i + 1, id_index)) == id_value):
                self.delete_sei_line(file_path, i + 1)
                line_count -= 1
                
            else:
                i += 1

            if(i >= line_count):
                break

##--------------------start-of-get_new_id()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def get_new_id(self, id_list:typing.List[int]) -> int:

        """

        Generates a new id.\n 

        Parameters:\n
        self (object - fileHandler) : the fileHandler object.\n
        id_list (list - ints) : a list of already active ids.\n

        Returns:\n
        new_id (int) : a new id.\n

        """

        id_list = [id for id in id_list]

        new_id = 1

        for num in id_list:
            if(num < new_id):
                continue
            elif(num == new_id):
                new_id += 1
            else:
                return new_id
            
        return new_id