## built-in libraries
import os
import typing

## custom modules
from modules.logger import Logger

class FileHandler():

    """
    
    The FileHandler class contains methods for handling files. As well as ID generation and deletion.

    """

##--------------------start-of-standard_create_directory()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def standard_create_directory(directory_path:str) -> None:

        """

        Creates a directory if it doesn't exist, as well as logs what was created.

        Parameters:
        directory_path (str) : Path to the directory to be created.

        """

        if(os.path.isdir(directory_path) == False):
            os.mkdir(directory_path)
            Logger.log_action(directory_path + " was created due to lack of the folder.")

##--------------------start-of-modified_create_directory()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def modified_create_directory(directory_path:str, path_to_check:str) -> None:

        """

        Creates a directory if it doesn't exist or if the path provided is blank or empty, as well as logs what was created.

        Parameters:
        directory_path (str) : Path to the directory to be created.
        path_to_check (str) : Path to check if it is blank.

        """

        if(os.path.isdir(directory_path) == False or os.path.getsize(path_to_check) == 0 or os.path.exists(path_to_check) == False):
            os.mkdir(directory_path)

            reason = f"was created due to lack of {directory_path}." if os.path.isdir(directory_path) == False else f"was created due to {path_to_check} being blank or empty."

            Logger.log_action(directory_path + " " + reason)

##--------------------start-of-standard_create_file()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def standard_create_file(file_path:str) -> None:

        """

        Creates a file if it doesn't exist, truncates it, as well as logs what was created.

        Parameters:
        file_path (str) : Path to the file to be created.

        """

        if(os.path.exists(file_path) == False):
            Logger.log_action(file_path + " was created due to lack of the file.")
            with open(file_path, "w+", encoding="utf-8") as file:
                file.truncate()

##--------------------start-of-modified_create_file()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def modified_create_file(file_path:str, content_to_write:str, omit:bool=True) -> bool:

        """

        Creates a path if it doesn't exist or if it is blank or empty, writes to it, as well as logs what was created and written.

        Parameters:
        file_path (str) : Path to the file to be created.
        content to write (str) : Content to be written to the file.
        omit (bool | optional | default = True) : Whether to omit the content written to the file in the log.

        Returns:
        did_overwrite (bool) : Whether the file was created.

        """

        did_overwrite = False

        if(os.path.exists(file_path) == False or os.path.getsize(file_path) == 0):
            Logger.log_action(file_path + " was created due to lack of the file or because it is blank.")
            with open(file_path, "w+", encoding="utf-8") as file:
                file.write(content_to_write)

                if(omit):
                    content_to_write = "(Content was omitted.)"
                Logger.log_action(file_path + " was written to with the following content: " + content_to_write)

            did_overwrite = True

        return did_overwrite
    
##--------------------start-of-standard_overwrite_file()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def standard_overwrite_file(file_path:str, content_to_write:typing.Union[str, typing.List[str]], omit:bool = True) -> None:

        """

        Writes to a file, creates it if it doesn't exist, overwrites it if it does, as well as logs what was written.

        Parameters:
        file_path (str) : Path to the file to be overwritten.
        content to write (str | list - str) : Content to be written to the file.
        omit (bool | optional | default = True) : Whether to omit the content written to the file in the log.

        """

        if(isinstance(content_to_write, list)):
            content_to_write = "\n".join(content_to_write)

        with open(file_path, "w+", encoding="utf-8") as file:
            file.write(content_to_write)

        if(omit):
            content_to_write = "(Content was omitted.)"
        
        Logger.log_action(file_path + " was overwritten with the following content: " + content_to_write)

##--------------------start-of-clear_file()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def clear_file(file_path:str) -> None:

        """

        Clears a file, as well as logs what was cleared.

        Parameters:
        file_path (str) : Path to the file to be cleared.

        """

        with open(file_path, "w+", encoding="utf-8") as file:
            file.truncate()

        Logger.log_action(file_path + " was cleared.")

##--------------------start-of-standard_read_file()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def standard_read_file(file_path:str) -> str:

        """

        Reads a file and returns its content.

        Parameters:
        file_path (str) : Path to the file to be read.

        Returns:
        content (str) : The content of the file.

        """

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        return content

##--------------------start-of-write_seisen_line()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def write_seisen_line(seisen_file_path:str, items_to_write:typing.List[typing.Any]) -> None:

        """
        
        Writes the given items to the given seisen file.

        Parameters:
        seisen_file_path (str) : The path to the seisen file.
        items_to_write (list - Any) : The items to be written to the seisen file.

        """

        items_to_write = [str(item).replace(",","'COMMALITERAL'") for item in items_to_write]

        line = ",".join(str(item) for item in items_to_write)
        
        with open(seisen_file_path, "a+", encoding="utf-8") as file:
            file.write(line + ",\n")

##-------------------start-of-edit_sei_file()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def edit_seisen_line(file_path:str, target_line:int, column_number:int, value_to_replace_to:typing.Any) -> None:
        
        """

        Edits the given line in the given file.

        Parameters:
        file_path (str) : The file being edited.
        target_line (int) : The line number we are editing.
        column_number (int) : The column number we are editing.
        value_to_replace_to (Any) : The value to replace the edit value with.

        """

        value_to_replace_to = str(value_to_replace_to).replace(",","'COMMALITERAL'")

        with open(file_path, "r+", encoding="utf8") as file:
            lines = file.readlines()

        line = lines[target_line - 1]
        items = line.split(",")

        items[column_number - 1] = value_to_replace_to

        new_line = ",".join(items)

        lines[target_line - 1] = new_line

        with open(file_path, "w", encoding="utf8") as file:
            file.writelines(lines)

##-------------------start-of-read_seisen_line()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def read_seisen_line(seisen_file_path:str, target_line:int, column:int) -> str:

        """

        Reads the given seisen file and returns the value of the given column in the given line.
        
        Parameters:
        seisen_file_path (str) : The path to the seisen file.
        target_line (int) : The line number of the seisen file.
        column (int) : The column we are reading.

        Returns:
        file_details[column-1] : The value of the given column.

        """

        i,ii = 0,0
        build_string = ""
        file_details = []

        with open(seisen_file_path, "r", encoding="utf-8") as file:
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

        file_details = [str(detail).replace("'COMMALITERAL'",",") for detail in file_details]
            
        return file_details[column-1]

##-------------------start-of-delete_seisen_line()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def delete_seisen_line(seisen_file_path:str, target_line:int) -> None:

        """

        Deletes the specified line from the given seisen file.

        Parameters:
        seisen_file_path (str) : The path to the seisen file.
        target_line (int) : The line number to be deleted.

        """

        with open(seisen_file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        with open(seisen_file_path, "w", encoding="utf-8") as file:
            for i, line in enumerate(lines, 1):
                if(i != target_line):
                    file.write(line)

##-------------------start-of-find_seisen_line()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def find_seisen_line(seisen_file_path:str, column_index:int, target_value:typing.Any) -> int:

        """

        Finds the line number of the given value in the given column of the given seisen file.

        Parameters:
        seisen_file_path (str) : The path to the seisen file.
        column_index (int) : The column to search.
        target_value (str) : The value to search for.

        Returns:
        i + 1 (int) : The line number of the value.

        Throws:
        ValueError : If the value is not found.

        """

        with open(seisen_file_path, 'r', encoding='utf-8') as file:
            for i, line in enumerate(file):

                line_value = FileHandler.read_seisen_line(seisen_file_path, i + 1, column_index)

                if(line_value == str(target_value)):
                    return i + 1  

        raise ValueError(f"Could not find {target_value} in {seisen_file_path} at column {column_index}.")

##-------------------start-of-extract_seisen_line_values()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def extract_seisen_line_values(line:str) -> typing.List[str]:

        """

        Extracts the values from a given seisen line.

        Parameters:
        line (str) : The line to extract the values from.

        Returns:
        values (list - str) : The values extracted from the line.

        """

        values = line.strip().split(',')

        values = [str(value).replace("'COMMALITERAL'",",") for value in values]

        if(values[-1] == ''): 
            return values[:-1]

        else:
            raise ValueError("The given line is not a valid seisen line.")  

##--------------------start-of-delete_all_occurrences_of_id()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def delete_all_occurrences_of_id(file_path:str, id_index:int, target_id:int) -> None:

        """
        
        Delete all lines that match a given ID.

        Parameters:
        file_path (str) : The path to the file to search.
        id_index (int) : The index of where the ID should be.
        target_id (str) : The ID to look for.

        """

        i = 0

        with open(file_path, 'r', encoding="utf-8") as file:
            lines = file.readlines()

        line_count = len(lines)

        while(i < line_count):

            if(int(FileHandler.read_seisen_line(file_path, i + 1, id_index)) == target_id):
                FileHandler.delete_seisen_line(file_path, i + 1)
                line_count -= 1
                
            else:
                i += 1

            if(i >= line_count):
                break

##--------------------start-of-get_new_id()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_new_id(id_list:typing.List[int]) -> int:

        """

        Generates a new ID.

        Parameters:
        id_list (list - int) : A list of already active ids.

        Returns:
        new_id (int) : A new ID that is not in the list.

        """

        id_list = [ID for ID in id_list]

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
    
##-------------------start-of-string_to_bool()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def string_to_bool(string:str) -> bool:

        """

        Converts a string to a boolean.

        Parameters:
        string (str) : The string to be converted.

        Returns:
        (bool) : The converted boolean.

        """

        return string.lower() in ['true', '1', 'yes', 'y', 't']