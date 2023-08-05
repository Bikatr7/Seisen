## built-in modules
import typing
import msvcrt
import shutil
import time

## custom modules
from modules.localHandler import localHandler
from modules.remoteHandler import remoteHandler

from modules.scoreRate import scoreRate

from modules.vocab import vocab as vocab_blueprint 

from modules.csep import csep as csep_blueprint

from modules.logger import logger
from modules.fileEnsurer import fileEnsurer
from modules.toolkit import toolkit

class vocabSettingsHandler():

    """
    
    The handler that handles all of Seisen's vocab settings
    
    """
##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self) -> None:

        """
        
        Initializes the vocabSettingsHandler class.\n

        Parameters:\n
        self (object - vocabSettingsHandler) : The handler object.\n
        file_ensurer (object - fileEnsurer) : The fileEnsurer object.\n
        logger (object - logger) : The logger object.\n
        toolkit (object - toolkit) : The toolkit object.\n

        Returns:\n
        None.\n

        """

        ##----------------------------------------------------------------objects----------------------------------------------------------------


##--------------------start-of-vocab_settings()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def change_vocab_settings(self, local_handler:localHandler) -> localHandler:

        """

        Controls the pathing for all vocab settings.\n

        Parameters:\n
        local_handler (object- localHandler) : the local handler.\n

        Returns:\n
        local_handler (object - localHandler) : the altered local handler.\n

        """ 

        local_handler.logger.log_action("User is changing vocab settings")

        vocab_message = "What are you trying to do?\n\n1.Add Vocab\n2.Add CSEP/Answer to Vocab\n3.Replace Vocab Value\n4.Delete Vocab Value\n"

        print(vocab_message)

        type_setting = local_handler.toolkit.input_check(4, str(msvcrt.getch().decode()), 4, vocab_message)

        if(type_setting == "1"):
            local_handler = self.add_vocab(local_handler)
        elif(type_setting == "2"):
            local_handler = self.add_csep(local_handler)
        elif(type_setting == "3"):
            local_handler = self.replace_vocab_value(local_handler)
        elif(type_setting == "4"):
            local_handler = self.delete_vocab_value(local_handler)

        return local_handler
    
##--------------------start-of-add_vocab()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def add_vocab(self, local_handler:localHandler) -> localHandler:
        
        """
        
        Adds a user entered vocab to the local handler.\n

        Parameters:\n
        local_handler (object - localHandler) : the local handler.\n

        Returns:\n
        local_handler (object - localHandler) : the altered local handler.n

        """

        new_vocab_id = local_handler.fileEnsurer.file_handler.get_new_id(local_handler.get_list_of_all_ids(5))
        new_csep_id = local_handler.fileEnsurer.file_handler.get_new_id(local_handler.get_list_of_all_ids(6))

        csep_value_list = []
        csep_actual_list_handler = []

        furigana = "0"
        isKanji = False

        try:
            testing_material = local_handler.toolkit.user_confirm("Please enter a vocab term")
            romaji = local_handler.toolkit.user_confirm("Please enter " + testing_material + "'s romaji/pronunciation")
            definition = local_handler.toolkit.user_confirm("Please enter " + testing_material + "'s definition/main answer")

            csep_value_list.append(definition)

            while(input("Enter 1 if " + testing_material + " has any additional answers :\n") == "1"):
                local_handler.toolkit.clear_stream()
                csep_value_list.append(local_handler.toolkit.user_confirm("Please enter " + testing_material + "'s additional answers"))

            kana = [value.testing_material for value in local_handler.kana]

            for character in testing_material:
                if(character not in kana):
                    local_handler.logger.log_action(character + " is kanji")
                    furigana = local_handler.toolkit.user_confirm("Please enter " + testing_material + "'s furigana/kana spelling")
                    isKanji = True
                    break
        
        except:
            return local_handler

        for csep_value in csep_value_list:
            csep_insert_values = [new_vocab_id, new_csep_id, csep_value, local_handler.VOCAB_WORD_TYPE]
            
            csep_actual_list_handler.append(csep_blueprint(new_vocab_id, new_csep_id, csep_value, local_handler.VOCAB_WORD_TYPE))

            local_handler.fileEnsurer.file_handler.write_sei_line(local_handler.vocab_csep_path, csep_insert_values)

            new_csep_id = local_handler.fileEnsurer.file_handler.get_new_id(local_handler.get_list_of_all_ids(6))

        vocab_insert_values = [new_vocab_id, testing_material, romaji, definition, furigana, 0, 0]
        local_handler.vocab.append(vocab_blueprint(new_vocab_id, testing_material, romaji, definition, csep_actual_list_handler, furigana, 0, 0, isKanji))

        local_handler.fileEnsurer.file_handler.write_sei_line(local_handler.vocab_path, vocab_insert_values)

        return local_handler
    
##--------------------start-of-add_csep()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def add_csep(self, local_handler:localHandler) -> localHandler:

        """
        
        Adds a user entered csep to an existing vocab in the local handler.\n

        Parameters:\n
        local_handler (object - localHandler) : the local handler.\n

        Returns:\n
        local_handler (object - localHandler) : the altered local handler.\n

        """

        vocab_term = ""
        vocab_id = 0

        target_index = 0

        new_csep_id = local_handler.fileEnsurer.file_handler.get_new_id(local_handler.get_list_of_all_ids(6))

        try:
            vocab_term_or_id = local_handler.toolkit.user_confirm("Please enter the vocab or vocab id that you want to add a csep/answer to.")

        except:
            return local_handler
        
        if(vocab_term_or_id.isdigit() == True):
            vocab_id = int(vocab_term_or_id)
            vocab_term = local_handler.searcher.get_term_from_id(local_handler, vocab_id) 
        else:
            vocab_term = vocab_term_or_id
            vocab_id = local_handler.searcher.get_id_from_term(local_handler, vocab_term)

        try:

            assert vocab_term != "-1"
            assert vocab_id != -1

            csep_value = local_handler.toolkit.user_confirm("Please enter the csep/answer for " + vocab_term + " you would like to add.")

        except AssertionError:
            local_handler.logger.log_action("Invalid id or term.")
            print("invalid id or term\n")
            time.sleep(1)
            return local_handler
        
        except local_handler.toolkit.UserCancelError:
            return local_handler
        
        target_index = next((i for i, vocab in enumerate(local_handler.vocab) if vocab.word_id == vocab_id))

        csep_insert_values = [vocab_id, new_csep_id, csep_value, local_handler.VOCAB_WORD_TYPE]
        local_handler.fileEnsurer.file_handler.write_sei_line(local_handler.vocab_csep_path, csep_insert_values)
        
        new_csep = csep_blueprint(int(vocab_id), new_csep_id, csep_value, local_handler.VOCAB_WORD_TYPE)
        local_handler.vocab[target_index].testing_material_answer_all.append(new_csep)

        return local_handler

##--------------------start-of-replace_vocab_value()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def replace_vocab_value(self, local_handler:localHandler) -> localHandler:

        """
        
        Replaces a value within a vocab.\n

        Parameters:\n
        local_handler (object - localHandler) : the local handler.\n

        Returns:\n
        local_handler (object - localHandler) : the altered local handler.\n

        """

        value_to_replace = 0
        index_to_replace = 0

        target_vocab_line = 0
        target_csep_line = 0

        target_index = 0

        csep_id = 0

        ATTRIBUTE_TESTING_MATERIAL = 2
        ATTRIBUTE_ROMAJI = 3
        ATTRIBUTE_FURIGANA = 5
        ATTRIBUTE_TESTING_MATERIAL_ANSWER_MAIN = 4
        ATTRIBUTE_INCORRECT_COUNT = 6
        ATTRIBUTE_CORRECT_COUNT = 7

        try:
            vocab_term_or_id = local_handler.toolkit.user_confirm("Please enter the vocab or vocab id that you want to replace a value in.")

        except:
            return local_handler
        
        if(vocab_term_or_id.isdigit() == True):
            vocab_id = int(vocab_term_or_id)
            vocab_term = local_handler.searcher.get_term_from_id(local_handler, vocab_id) 
        else:
            vocab_term = vocab_term_or_id
            vocab_id = local_handler.searcher.get_id_from_term(local_handler, vocab_term)

        try:

            assert vocab_term != "-1"
            assert vocab_id != -1

        except AssertionError:
            local_handler.logger.log_action("Invalid id or term.")
            print("invalid id or term\n")
            time.sleep(1)
            return local_handler
        
        except local_handler.toolkit.UserCancelError:
            return local_handler
        
        target_index = next((i for i, vocab in enumerate(local_handler.vocab) if vocab.word_id == vocab_id), -1)

        target_vocab = local_handler.vocab[target_index]

        type_replacement_message = local_handler.searcher.get_print_item_from_id(local_handler, vocab_id)

        type_replacement_message += "\n\nWhat value would you like to replace? (1-6) (select index)"

        print(type_replacement_message)

        type_value = local_handler.toolkit.input_check(4, str(msvcrt.getch().decode()), 6, type_replacement_message)

        attributes_map = {
            "1": (target_vocab.testing_material, ATTRIBUTE_TESTING_MATERIAL),
            "2": (target_vocab.romaji, ATTRIBUTE_ROMAJI),
            "3": (target_vocab.furigana, ATTRIBUTE_FURIGANA),
            "4": (target_vocab.testing_material_answer_main, ATTRIBUTE_TESTING_MATERIAL_ANSWER_MAIN),
            "5": (target_vocab.incorrect_count, ATTRIBUTE_INCORRECT_COUNT),
            "6": (target_vocab.correct_count, ATTRIBUTE_CORRECT_COUNT)
        }

        value_to_replace, index_to_replace = attributes_map[type_value]

        try:
            replacement_value = local_handler.toolkit.user_confirm("What are you replacing " + str(value_to_replace) + " with?")

        except:
            return local_handler
        
        ## if the user is changing the main definition, we also need to adjust the csep for it
        if(type_value == "4"):

            csep_id = next((csep.csep_id for csep in target_vocab.testing_material_answer_all if csep.csep_value == value_to_replace))

            target_csep_line = next((i + 1 for i, line in enumerate(local_handler.vocab_csep_path) if int(local_handler.fileEnsurer.file_handler.read_sei_file(local_handler.vocab_csep_path, i + 1, 2)) == csep_id))

            local_handler.fileEnsurer.file_handler.edit_sei_line(local_handler.vocab_csep_path, target_csep_line, 3, str(replacement_value))
        
        else:
            pass

        target_vocab_line = next((i + 1 for i, line in enumerate(local_handler.vocab_path) if int(local_handler.fileEnsurer.file_handler.read_sei_file(local_handler.vocab_path, i + 1, 1)) == vocab_id))

        ## edits the vocab word
        local_handler.fileEnsurer.file_handler.edit_sei_line(local_handler.vocab_path, target_vocab_line, index_to_replace, str(replacement_value))
            
        ## it's easier to just reload everything than for me to figure out how to juggle csep values in the handler if the user wants to fuck with definitions or answers
        local_handler.load_words_from_local_storage()

        return local_handler

##--------------------start-of-delete_vocab_value()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def delete_vocab_value(self, local_handler:localHandler) -> localHandler:

        """
        
        Deletes a vocab value.\n

        Parameters:\n
        local_handler (object - localHandler) : the local handler.\n

        Returns:\n
        local_handler (object - localHandler) : the altered local handler.\n

        """

        try:
            vocab_term_or_id = local_handler.toolkit.user_confirm("Please enter the vocab or vocab id that you want to delete.")

        except:
            return local_handler
        
        if(vocab_term_or_id.isdigit() == True):
            vocab_id = int(vocab_term_or_id)
            vocab_term = local_handler.searcher.get_term_from_id(local_handler, vocab_id) 
        else:
            vocab_term = vocab_term_or_id
            vocab_id = local_handler.searcher.get_id_from_term(local_handler, vocab_term)

        try:

            assert vocab_term != "-1"
            assert vocab_id != -1

        except AssertionError:
            local_handler.logger.log_action("Invalid id or term.")
            print("invalid id or term\n")
            time.sleep(1)
            return local_handler
        
        except local_handler.toolkit.UserCancelError:
            return local_handler

        target_vocab_index = next((i for i, vocab in enumerate(local_handler.vocab) if vocab.word_id == vocab_id))

        target_vocab_line = next((i + 1 for i, line in enumerate(local_handler.vocab_path) if int(local_handler.fileEnsurer.file_handler.read_sei_file(local_handler.vocab_path, i + 1, 1)) == vocab_id))

        ## deletes the vocab itself
        local_handler.fileEnsurer.file_handler.delete_sei_line(local_handler.vocab_path, target_vocab_line)
        local_handler.vocab.pop(target_vocab_index)

        ## deletes the cseps
        local_handler.fileEnsurer.file_handler.delete_all_occurrences_of_id(local_handler.vocab_csep_path, 1, vocab_id)

        ## deletes the typos
        local_handler.fileEnsurer.file_handler.delete_all_occurrences_of_id(local_handler.vocab_incorrect_typos_path, 1, vocab_id)
        local_handler.fileEnsurer.file_handler.delete_all_occurrences_of_id(local_handler.vocab_typos_path, 1, vocab_id)

        return local_handler