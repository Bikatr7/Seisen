## built-in libraries
import os
import typing

## custom modules
from modules.logger import Logger
from modules.toolkit import permission_error_decorator

class FileHandler():

    """
    
    The FileHandler class contains methods for handling files. As well as ID generation and deletion.

    """

##--------------------start-of-standard_create_directory()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    @permission_error_decorator()
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
    @permission_error_decorator()
    def modified_create_directory(directory_path:str, path_to_check:str) -> None:

        """

        Creates a directory if it doesn't exist or if the path provided is blank or empty, as well as logs what was created.
        path_to_check can be a path to a file or a directory.

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
    @permission_error_decorator()
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
    @permission_error_decorator()
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
    @permission_error_decorator()
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

##--------------------start-of-standard_delete_file()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    @permission_error_decorator()
    def standard_delete_file(file_path:str) -> None:

        """

        Deletes a file, as well as logs what was deleted.

        Parameters:
        file_path (str) : Path to the file to be deleted.

        """

        if(os.path.exists(file_path)):
            os.remove(file_path)
            Logger.log_action(file_path + " was deleted.")

##--------------------start-of-clear_file()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    @permission_error_decorator()
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
    @permission_error_decorator()
    def standard_read_file(file_path:str) -> str:

        """

        Reads a file and returns its content.

        Parameters:
        file_path (str) : Path to the file to be read.

        Returns:
        content (str) : The content of the file.

        """

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read().strip()

        return content

##--------------------start-of-write_seisen_line()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    @permission_error_decorator()
    def write_seisen_line(seisen_file_path:str, items_to_write:typing.List[typing.Any]) -> None:

        """
        
        Writes the given items to the given seisen file.

        Parameters:
        seisen_file_path (str) : The path to the seisen file.
        items_to_write (list - Any) : The items to be written to the seisen file.

        """

        line = ",".join(str(item).replace(",", "'COMMALITERAL'") for item in items_to_write)
        
        with open(seisen_file_path, "a+", encoding="utf-8") as file:
            file.write(line + ",\n")

##--------------------start-of-write_seisen_lines()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    @permission_error_decorator()
    def write_seisen_lines(seisen_file_path:str, items_to_write:typing.List[typing.List[typing.Any]]) -> None:

        """
        
        Writes the given items to the given seisen file.

        Parameters:
        seisen_file_path (str) : The path to the seisen file.
        items_to_write (list - list - Any) : The items to be written to the seisen file. Each inner list is a line.

        """

        lines = []

        for items in items_to_write:
            line = ",".join(str(item).replace(",", "'COMMALITERAL'") for item in items)
            lines.append(line)

        with open(seisen_file_path, "a+", encoding="utf-8") as file:
            file.write(",\n".join(lines) + ",\n")

##-------------------start-of-edit_sei_file()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    @permission_error_decorator()
    def edit_seisen_line(file_path:str, target_line:int, column_number:int, value_to_replace_to:typing.Any) -> None:
        
        """

        Edits the given line in the given file.

        Parameters:
        file_path (str) : The file being edited.
        target_line (int) : The line number we are editing.
        column_number (int) : The column number we are editing.
        value_to_replace_to (Any) : The value to replace the current value with.

        """

        value_to_replace_to = str(value_to_replace_to).replace(",","'COMMALITERAL'")
        temp_file_path = file_path + '.tmp'

        with open(file_path, 'r', encoding='utf8') as read_file, open(temp_file_path, 'w', encoding='utf8') as write_file:
            for current_line_number, line in enumerate(read_file, start=1):
                if(current_line_number == target_line):
                    items = line.split(",")
                    items[column_number - 1] = value_to_replace_to
                    line = ",".join(items)

                write_file.write(line)

        os.replace(temp_file_path, file_path)

##-------------------start-of-read_seisen_line()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    @permission_error_decorator()
    def read_seisen_line(seisen_file_path:str, target_line:int, column:int) -> str:

        """

        Reads the given seisen file and returns the value of the given column in the given line.
        
        Parameters:
        seisen_file_path (str) : The path to the seisen file.
        target_line (int) : The line number of the seisen file.
        column (int) : The column we are reading.

        Returns:
        file_details[column-1] : The value of the given column.

        Raises:
        ValueError : If the target line is not found.

        """

        with open(seisen_file_path, "r", encoding="utf-8") as file:
            for current_line_number, line in enumerate(file, start=1):
                if(current_line_number == target_line):
                    file_details = line.split(",")
                    file_details = [str(detail).replace("COMMALITERAL",",") for detail in file_details]
                    return file_details[column-1]
                
        raise ValueError(f"Could not find {target_line} in {seisen_file_path}.")

##-------------------start-of-delete_seisen_line()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    @permission_error_decorator()
    def delete_seisen_line(seisen_file_path:str, target_line:int) -> None:

        """

        Deletes the specified line from the given seisen file.

        Parameters:
        seisen_file_path (str) : The path to the seisen file.
        target_line (int) : The line number to be deleted.

        """

        temp_file_path = seisen_file_path + '.tmp'

        with open(seisen_file_path, 'r', encoding='utf8') as read_file, open(temp_file_path, 'w', encoding='utf8') as write_file:
            for current_line_number, line in enumerate(read_file, start=1):
                if(current_line_number != target_line):
                    write_file.write(line)

        os.replace(temp_file_path, seisen_file_path)

##-------------------start-of-find_seisen_line()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    @permission_error_decorator()
    def find_seisen_line(seisen_file_path:str, column_index:int, target_value:typing.Any) -> int:

        """

        Finds the line number of the given value in the given column of the given seisen file.

        Parameters:
        seisen_file_path (str) : The path to the seisen file.
        column_index (int) : The column to search.
        target_value (Any) : The value to search for.

        Returns:
        i + 1 (int) : The line number of the value.

        Raises:
        ValueError : If the value is not found.

        """

        with open(seisen_file_path, 'r', encoding='utf-8') as file:
            for i, line in enumerate(file):
                line_values = line.split(",")
                line_values = [str(value).replace("COMMALITERAL",",") for value in line_values]

                if(line_values[column_index - 1] == str(target_value)):
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

        Raises:
        ValueError : If the given line is not a valid seisen line.

        """

        values = line.strip().split(',')

        if(values[-1] == ''):
            values = values[:-1]
        else:
            raise ValueError("The given line is not a valid seisen line.")

        values = [str(value).replace("COMMALITERAL", ",") for value in values]

        return values
        
##-------------------start-of-is_file_damaged()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    @permission_error_decorator()
    def is_file_damaged(file_path:str) -> bool:

        """

        Checks if a file is damaged.

        File is considered damaged if it doesn't exist or if it is empty.

        Parameters:
        file_path (str) : The path to the file to check.

        Returns:
        (bool) : Whether the file is damaged.

        """

        return not os.path.exists(file_path) or os.path.getsize(file_path) == 0

##--------------------start-of-delete_all_occurrences_of_id()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    @permission_error_decorator()
    def delete_all_occurrences_of_id(file_path:str, id_index:int, target_id:int) -> None:

        """
        
        Delete all lines that match a given ID.

        Parameters:
        file_path (str) : The path to the file to search.
        id_index (int) : The index of where the ID should be.
        target_id (int) : The ID to search for.

        """

        temp_file_path = file_path + '.tmp'

        with open(file_path, 'r', encoding="utf-8") as read_file, open(temp_file_path, 'w', encoding="utf-8") as write_file:
            for line in read_file:
                line_values = line.split(",")
                line_values = [str(value).replace("COMMALITERAL",",") for value in line_values]

                if(int(line_values[id_index - 1]) != target_id):
                    write_file.write(line)

        os.replace(temp_file_path, file_path)

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

        id_set = set(id_list)
        new_id = 1

        while new_id in id_set:
            new_id += 1

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