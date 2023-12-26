## built-in modules
from __future__ import annotations ## used for cheating the circular import issue that occurs when i need to type check some things

import typing

## custom modules
from entities.typos import typo as typo_blueprint
from entities.typos import incorrectTypo as incorrect_typo_blueprint

from entities.csep import csep as csep

from entities import words

if(typing.TYPE_CHECKING): ## used for cheating the circular import issue that occurs when i need to type check some things
    from handlers.local_handler import localHandler

class vocab(words.word):

    """
    
    The vocab class is for testing material that is longer than a single kana. Inherits the word class.\n

    """

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, incoming_id:int, incoming_testing_material:str, incoming_romaji:str, incoming_testing_material_answer_main:str, incoming_testing_material_answer_main_all:typing.List[csep], incoming_furigana:str, incoming_incorrect_count:int,incoming_correct_count:int, incoming_kanji_flag:bool):

        """
        
        Initializes the vocab class\n

        Parameters:\n
        incoming_id (int) : the id of the vocab.\n
        incoming_testing_material (str) : the testing material of the vocab.\n
        incoming_romaji (str) : the romaji of the vocab.\n
        incoming_testing_material_answer_main (str) : the main answer of the testing material.\n
        incoming_testing_material_answer_main_all (list - str) : the list of all answers to the testing material of the vocab.\n
        incoming_furigana (str) : the furigana of the vocab.\n
        incoming_incorrect_count (int) : the number of incorrect guesses of the vocab.\n
        incoming_correct_count (int) : the number of correct guesses of the vocab.\n
        incoming_kanji_flag (bool) : if the vocab contains kanji or not.\n

        Returns:\n
        None.\n

        """
        
        super().__init__(incoming_id, incoming_testing_material, incoming_testing_material_answer_main, incoming_testing_material_answer_main_all, incoming_incorrect_count, incoming_correct_count)

        self.romaji = incoming_romaji

        self.furigana = incoming_furigana

        self.isKanji = incoming_kanji_flag

        self.word_type = "3"

##--------------------start-of-log_correct_answer()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def log_correct_answer(self, local_handler:localHandler) -> None:

        """

        Logs a correct answer to the vocab.\n

        Parameters:\n
        self (object - vocab) : the vocab being tested.\n
        local_handler (object - localHandler) : the local handler object.\n

        Returns:\n
        None.\n
        
        """

        ## where the correct count index is in the
        CORRECT_ANSWER_COUNT_FILE_INDEX_LOCATION = 7
        VOCAB_ID_FILE_INDEX_LOCATION = 1

        vocab_ids = []

        line_to_write_to = 0

        self.correct_count += 1

        with open(local_handler.vocab_path, 'r', encoding="utf-8") as file:
            vocab_lines = file.readlines()

        for i, line in enumerate(vocab_lines):
            vocab_ids.append(local_handler.file_ensurer.file_handler.read_sei_file(local_handler.vocab_path, i+1, VOCAB_ID_FILE_INDEX_LOCATION))
                            
        ## line returned needs to be incremented by one to match file
        line_to_write_to = vocab_ids.index(str(self.word_id)) + 1

        local_handler.file_ensurer.file_handler.edit_sei_line(local_handler.vocab_path, line_to_write_to, CORRECT_ANSWER_COUNT_FILE_INDEX_LOCATION , str(self.correct_count))

        local_handler.file_ensurer.logger.log_action("Logged a correct answer for " + self.testing_material + ", id : " + str(self.word_id))

##--------------------start-of-log_incorrect_answer()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def log_incorrect_answer(self, local_handler:localHandler) -> None:

        """

        Logs an incorrect answer to the vocab.\n

        Parameters:\n
        self (object - vocab) : the vocab being tested.\n
        local_handler (object - localHandler) : the local handler object.\n

        Returns:\n
        None.\n
        
        """

        ## where the correct count index is in the
        INCORRECT_ANSWER_COUNT_FILE_INDEX_LOCATION = 6
        VOCAB_ID_FILE_INDEX_LOCATION = 1

        vocab_ids = []

        line_to_write_to = 0

        self.incorrect_count += 1

        with open(local_handler.vocab_path, 'r', encoding="utf-8") as file:
            vocab_lines = file.readlines()

        for i, line in enumerate(vocab_lines):
            vocab_ids.append(local_handler.file_ensurer.file_handler.read_sei_file(local_handler.vocab_path, i+1, VOCAB_ID_FILE_INDEX_LOCATION))
                            
        ## line returned needs to be incremented by one to match file
        line_to_write_to = vocab_ids.index(str(self.word_id)) + 1

        local_handler.file_ensurer.file_handler.edit_sei_line(local_handler.vocab_path, line_to_write_to, INCORRECT_ANSWER_COUNT_FILE_INDEX_LOCATION , str(self.incorrect_count))

        local_handler.file_ensurer.logger.log_action("Logged an incorrect answer for " + self.testing_material + ", id : " + str(self.word_id))

##--------------------start-of-log_new_typo()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def log_new_typo(self, typo:str, local_handler:localHandler) -> None:

        """

        Logs a new typo to the vocab.\n

        Parameters:\n
        self (object - vocab) : the vocab being tested\n
        typo (str) : the typo to be logged.\n
        local_handler (object - localHandler) : the localHandler object.\n

        Returns:\n
        None.\n
        
        """

        ## gets a new id for the typo
        new_typo_id = local_handler.file_ensurer.file_handler.get_new_id(local_handler.get_list_of_all_ids(3))

        new_typo = typo_blueprint(self.word_id, new_typo_id, typo, self.word_type)

        ## updates local storage so the typo will be saved
        local_handler.file_ensurer.file_handler.write_sei_line(local_handler.vocab_typos_path, [str(self.word_id), str(new_typo_id), str(new_typo.typo_value), str(new_typo.word_type)])

        ## updates the current session with the typo
        self.typos.append(new_typo)

        local_handler.file_ensurer.logger.log_action("Logged a typo : " + typo + " for " + self.testing_material + ", id : " + str(self.word_id))


##--------------------start-of-log_new_incorrect_typo()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def log_new_incorrect_typo(self, incorrect_typo:str, local_handler:localHandler) -> None:

        """
        
        Logs a new incorrect typo to the vocab.\n

        Parameters:\n
        self (object - vocab) : the object being tested.\n
        incorrect_typo (str) : the incorrect_typo to be logged.\n
        local_handler (object - localHandler) : the localHandler object.\n
        
        """

        ## gets a new id for the incorrect typo
        new_incorrect_typo_id = local_handler.file_ensurer.file_handler.get_new_id(local_handler.get_list_of_all_ids(4))

        new_incorrect_typo = incorrect_typo_blueprint(self.word_id, new_incorrect_typo_id, incorrect_typo, self.word_type)

        ## updates local storage so the incorrect typo will be saved
        local_handler.file_ensurer.file_handler.write_sei_line(local_handler.vocab_incorrect_typos_path, [str(self.word_id), str(new_incorrect_typo_id), str(new_incorrect_typo.incorrect_typo_value), str(new_incorrect_typo.word_type)])

        ## updates the current session with the incorrect typo
        self.incorrect_typos.append(new_incorrect_typo)

        local_handler.file_ensurer.logger.log_action("Logged an incorrect typo : " + incorrect_typo + " for " + self.testing_material + ", id : " + str(self.word_id))

