## built-in modules
from datetime import datetime

import os
import typing

## custom modules
from modules.logger import Logger


class FileHandler():

    """
    
    The handler that handles interactions with files.

    """

##--------------------start-of-standard_create_directory()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def standard_create_directory(directory_path:str) -> None:

        """

        Creates a directory if it doesn't exist, as well as logs what was created.

        Parameters:
        directory_path (str) : path to the directory to be created.

        """

        if(os.path.isdir(directory_path) == False):
            os.mkdir(directory_path)
            Logger.log_action(directory_path + " created due to lack of the folder")

##--------------------start-of-modified_create_directory()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def modified_create_directory(directory_path:str, path_to_check:str) -> None:

        """

        Creates a directory if it doesn't exist or if the path provided is blank or empty, as well as logs what was created.

        Parameters:
        directory_path (str) : path to the directory to be created.
        path_to_check (str) : path to check if it is blank.

        """

        if(os.path.isdir(directory_path) == False or os.path.getsize(path_to_check) == 0):
            os.mkdir(directory_path)
            Logger.log_action(directory_path + " created due to lack of the folder or " + path_to_check + " was blank or empty")

##--------------------start-of-standard_create_file()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def standard_create_file(file_path:str) -> None:

        """

        Creates a file if it doesn't exist, truncates it,  as well as logs what was created.

        Parameters:
        file_path (str) : path to the file to be created.

        """

        if(os.path.exists(file_path) == False):
            Logger.log_action(file_path + " was created due to lack of the file")
            with open(file_path, "w+", encoding="utf-8") as file:
                file.truncate()

##--------------------start-of-modified_create_file()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def modified_create_file(file_path:str, content_to_write:str) -> bool:

        """

        Creates a path if it doesn't exist or if it is blank or empty, writes to it, as well as logs what was created.

        Parameters:
        file_path (str) : path to the file to be created.
        content to write (str) : content to be written to the file.

        Returns:
        bool : whether or not the file was overwritten.

        """

        did_overwrite = False

        if(os.path.exists(file_path) == False or os.path.getsize(file_path) == 0):
            Logger.log_action(file_path + " was created due to lack of the file or because it is blank")
            with open(file_path, "w+", encoding="utf-8") as file:
                file.write(content_to_write)

            did_overwrite = True

        return did_overwrite
    
##--------------------start-of-write_sei_line()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def write_sei_line(sei_file_path:str, items_to_write:typing.List[str]) -> None:

        """
        
        Writes the given items to the given sei file.

        Parameters:
        sei_file_path (str) : the path to the sei file.
        items_to_write (list - str) : the items to be written to the sei file.

        """

        line = ",".join(str(item) for item in items_to_write)
        
        with open(sei_file_path, "a+", encoding="utf-8") as file:
            file.write(line + ",\n")

##-------------------start-of-read_sei_file()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def edit_sei_line(file_path:str, target_line:int, column_number:int, value_to_replace_to:str) -> None:
        
        """

        Edits the given line in the given file.

        Parameters:
        file_path (str) : The file being edited.
        target_line (int) : The line number of the file we are editing.
        column_number (int) : The column number we are editing.
        value_to_replace_to (str) : The value to replace the edit value with.

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

    @staticmethod
    def read_sei_file(sei_file_path:str, target_line:int, column:int) -> str:

        """

        Reads the given sei file and returns the value of the given column.
        
        Parameters:\n
        sei_file_path (str) : the path to the sei file.
        target_line (int) : the line number of the sei file.
        column (int) : the column we are reading.

        Returns:
        file_details[column-1] : the value of the given column.

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

    @staticmethod
    def delete_sei_line(sei_file_path:str, target_line:int) -> None:

        """

        Deletes the specified line from the given sei file.

        Parameters:
        sei_file_path (str) : the path to the sei file.
        target_line (int) : the line number to be deleted.

        """

        with open(sei_file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        with open(sei_file_path, "w", encoding="utf-8") as file:
            for i, line in enumerate(lines, 1):
                if i != target_line:
                    file.write(line)

##--------------------start-of-delete_all_occurrences_of_id()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def delete_all_occurrences_of_id(file_path:str, id_index:int, id_value:int) -> None:

        """
        
        Delete all lines that match a given id.

        Parameters:
        file_path (str) : the path to the file to search.
        id_index (int) : the index of where the id should be.
        id_value (str) : the id to look for.

        """

        i = 0

        with open(file_path, 'r') as file:
            lines = file.readlines()

        line_count = len(lines)

        while(i < line_count):

            if(int(FileHandler.read_sei_file(file_path, i + 1, id_index)) == id_value):
                FileHandler.delete_sei_line(file_path, i + 1)
                line_count -= 1
                
            else:
                i += 1

            if(i >= line_count):
                break

##--------------------start-of-get_new_id()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_new_id(id_list:typing.List[int]) -> int:

        """

        Generates a new id.

        Parameters:
        id_list (list - ints) : a list of already active ids.

        Returns:
        new_id (int) : a new id.

        """

        id_list = [id for id in id_list]

        id_list.sort()

        new_id = 1

        for num in id_list:
            if(num < new_id):
                continue
            elif(num == new_id):
                new_id += 1
            else:
                return new_id
            
        return new_id