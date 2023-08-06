## built-in modules
import msvcrt
import time

## custom modules
from modules.localHandler import localHandler
from modules.remoteHandler import remoteHandler

from modules.vocab import vocab as vocab_blueprint 

from modules.csep import csep as csep_blueprint

class vocabSettingsHandler():

    """
    
    The handler that handles all of Seisen's vocab settings
    
    """
##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, local_handler:localHandler, remote_handler:remoteHandler) -> None:

        """
        
        Initializes the vocabSettingsHandler class.\n

        Parameters:\n
        self (object - vocabSettingsHandler) : The vocab settings handler object.\n
        local_handler (object - localHandler) : The local handler object.\n
        remote_handler (object - remoteHandler) : The remote handler object.\n

        Returns:\n
        None.\n

        """

        ##----------------------------------------------------------------objects----------------------------------------------------------------

        self.local_handler = local_handler

        self.remote_handler = remote_handler

##--------------------start-of-change_vocab_settings()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def change_vocab_settings(self) -> None:

        """

        Controls the pathing for all vocab settings.\n

        Parameters:\n
        self (object - vocabSettingsHandler) : The vocab settings handler object.\n

        Returns:\n
        None.\n

        """ 

        self.local_handler.toolkit.logger.log_action("User is changing vocab settings")

        vocab_message = "What are you trying to do?\n\n1.Add Vocab\n2.Add CSEP/Answer to Vocab\n3.Replace Vocab Value\n4.Delete Vocab Value\n5.Delete CSEP/Answer to Vocab\n"

        print(vocab_message)

        type_setting = self.local_handler.toolkit.input_check(4, str(msvcrt.getch().decode()), 5, vocab_message)

        if(type_setting == "1"):
            self.add_vocab()
        elif(type_setting == "2"):
            self.add_csep()
        elif(type_setting == "3"):
            self.replace_vocab_value()
        elif(type_setting == "4"):
            self.delete_vocab_value()
        elif(type_setting == "5"):
            self.delete_csep_value()
    
##--------------------start-of-add_vocab()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def add_vocab(self) -> None:
        
        """
        
        Adds a user entered vocab to the local handler.\n

        Parameters:\n
        self (object - vocabSettingsHandler) : The vocab settings handler object.\n

        Returns:\n
        None.\n

        """ 

        new_vocab_id = self.local_handler.fileEnsurer.file_handler.get_new_id(self.local_handler.get_list_of_all_ids(5))
        new_csep_id = self.local_handler.fileEnsurer.file_handler.get_new_id(self.local_handler.get_list_of_all_ids(6))

        csep_value_list = []
        csep_actual_list_handler = []

        furigana = "0"
        isKanji = False

        try:
            testing_material = self.local_handler.toolkit.user_confirm("Please enter a vocab term")
            romaji = self.local_handler.toolkit.user_confirm("Please enter " + testing_material + "'s romaji/pronunciation")
            definition = self.local_handler.toolkit.user_confirm("Please enter " + testing_material + "'s definition/main answer")

            csep_value_list.append(definition)

            while(input("Enter 1 if " + testing_material + " has any additional answers :\n") == "1"):
                self.local_handler.toolkit.clear_stream()
                csep_value_list.append(self.local_handler.toolkit.user_confirm("Please enter " + testing_material + "'s additional answers"))

            kana = [value.testing_material for value in self.local_handler.kana]

            for character in testing_material:
                if(character not in kana):
                    self.local_handler.toolkit.logger.log_action(character + " is kanji")
                    furigana = self.local_handler.toolkit.user_confirm("Please enter " + testing_material + "'s furigana/kana spelling")
                    isKanji = True
                    break
        
        except:
            return

        for csep_value in csep_value_list:
            csep_insert_values = [new_vocab_id, new_csep_id, csep_value, self.local_handler.VOCAB_WORD_TYPE]
            
            csep_actual_list_handler.append(csep_blueprint(new_vocab_id, new_csep_id, csep_value, self.local_handler.VOCAB_WORD_TYPE))

            self.local_handler.fileEnsurer.file_handler.write_sei_line(self.local_handler.vocab_csep_path, csep_insert_values)

            new_csep_id = self.local_handler.fileEnsurer.file_handler.get_new_id(self.local_handler.get_list_of_all_ids(6))

        vocab_insert_values = [new_vocab_id, testing_material, romaji, definition, furigana, 0, 0]
        self.local_handler.vocab.append(vocab_blueprint(new_vocab_id, testing_material, romaji, definition, csep_actual_list_handler, furigana, 0, 0, isKanji))

        self.local_handler.fileEnsurer.file_handler.write_sei_line(self.local_handler.vocab_path, vocab_insert_values)
    
##--------------------start-of-add_csep()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def add_csep(self) -> None:

        """
        
        Adds a user entered csep to an existing vocab in the local handler.\n

        Parameters:\n
        self (object - vocabSettingsHandler) : The vocab settings handler object.\n

        Returns:\n
        None.\n

        """ 

        vocab_term = ""
        vocab_id = 0

        target_index = 0

        new_csep_id = self.local_handler.fileEnsurer.file_handler.get_new_id(self.local_handler.get_list_of_all_ids(6))

        try:
            vocab_term_or_id = self.local_handler.toolkit.user_confirm("Please enter the vocab or vocab id that you want to add a csep/answer to.")

        except:
            return
        
        if(vocab_term_or_id.isdigit() == True):
            vocab_id = int(vocab_term_or_id)
            vocab_term = self.local_handler.searcher.get_term_from_id(self.local_handler, vocab_id) 
        else:
            vocab_term = vocab_term_or_id
            vocab_id = self.local_handler.searcher.get_id_from_term(self.local_handler, vocab_term)

        try:

            assert vocab_term != "-1"
            assert vocab_id != -1

            csep_value = self.local_handler.toolkit.user_confirm("Please enter the csep/answer for " + vocab_term + " you would like to add.")

        except AssertionError:
            self.local_handler.toolkit.logger.log_action("Invalid id or term.")
            print("invalid id or term\n")
            time.sleep(1)
            return
        
        except self.local_handler.toolkit.UserCancelError:
            return
        
        target_index = next((i for i, vocab in enumerate(self.local_handler.vocab) if vocab.word_id == vocab_id))

        csep_insert_values = [vocab_id, new_csep_id, csep_value, self.local_handler.VOCAB_WORD_TYPE]
        self.local_handler.fileEnsurer.file_handler.write_sei_line(self.local_handler.vocab_csep_path, csep_insert_values)
        
        new_csep = csep_blueprint(int(vocab_id), new_csep_id, csep_value, self.local_handler.VOCAB_WORD_TYPE)
        self.local_handler.vocab[target_index].testing_material_answer_all.append(new_csep)

##--------------------start-of-replace_vocab_value()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def replace_vocab_value(self) -> None:

        """
        
        Replaces a value within a vocab.\n

        Parameters:\n
        self (object - vocabSettingsHandler) : The vocab settings handler object.\n

        Returns:\n
        None.\n

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
            vocab_term_or_id = self.local_handler.toolkit.user_confirm("Please enter the vocab or vocab id that you want to replace a value in.")

        except:
            return
        
        if(vocab_term_or_id.isdigit() == True):
            vocab_id = int(vocab_term_or_id)
            vocab_term = self.local_handler.searcher.get_term_from_id(self.local_handler, vocab_id) 
        else:
            vocab_term = vocab_term_or_id
            vocab_id = self.local_handler.searcher.get_id_from_term(self.local_handler, vocab_term)

        try:

            assert vocab_term != "-1"
            assert vocab_id != -1

        except AssertionError:
            self.local_handler.toolkit.logger.log_action("Invalid id or term.")
            print("invalid id or term\n")
            time.sleep(1)
            return 
        
        except self.local_handler.toolkit.UserCancelError:
            return
        
        target_index = next((i for i, vocab in enumerate(self.local_handler.vocab) if vocab.word_id == vocab_id))

        target_vocab = self.local_handler.vocab[target_index]

        type_replacement_message = self.local_handler.searcher.get_vocab_print_item_from_id(self.local_handler, vocab_id)

        type_replacement_message += "\n\nWhat value would you like to replace? (1-6) (select index)"

        print(type_replacement_message)

        type_value = self.local_handler.toolkit.input_check(4, str(msvcrt.getch().decode()), 6, type_replacement_message)

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
            replacement_value = self.local_handler.toolkit.user_confirm("What are you replacing " + str(value_to_replace) + " with?")

        except:
            return 
        
        ## if the user is changing the main definition, we also need to adjust the csep for it
        if(type_value == "4"):

            csep_id = next((csep.csep_id for csep in target_vocab.testing_material_answer_all if csep.csep_value == value_to_replace))

            target_csep_line = next((i + 1 for i, line in enumerate(self.local_handler.vocab_csep_path) if int(self.local_handler.fileEnsurer.file_handler.read_sei_file(self.local_handler.vocab_csep_path, i + 1, 2)) == csep_id))

            self.local_handler.fileEnsurer.file_handler.edit_sei_line(self.local_handler.vocab_csep_path, target_csep_line, 3, str(replacement_value))
        
        else:
            pass

        target_vocab_line = next((i + 1 for i, line in enumerate(self.local_handler.vocab_path) if int(self.local_handler.fileEnsurer.file_handler.read_sei_file(self.local_handler.vocab_path, i + 1, 1)) == vocab_id))

        ## edits the vocab word
        self.local_handler.fileEnsurer.file_handler.edit_sei_line(self.local_handler.vocab_path, target_vocab_line, index_to_replace, str(replacement_value))
            
        ## it's easier to just reload everything than for me to figure out how to juggle csep values in the handler if the user wants to fuck with definitions or answers
        self.local_handler.load_words_from_local_storage()

##--------------------start-of-delete_vocab_value()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def delete_vocab_value(self) -> None:

        """
        
        Deletes a vocab value.\n

        Parameters:\n
        self (object - vocabSettingsHandler) : The vocab settings handler object.\n

        Returns:\n
        None.\n

        """ 

        try:
            vocab_term_or_id = self.local_handler.toolkit.user_confirm("Please enter the vocab or vocab id that you want to delete.")

        except:
            return
        
        if(vocab_term_or_id.isdigit() == True):
            vocab_id = int(vocab_term_or_id)
            vocab_term = self.local_handler.searcher.get_term_from_id(self.local_handler, vocab_id) 
        else:
            vocab_term = vocab_term_or_id
            vocab_id = self.local_handler.searcher.get_id_from_term(self.local_handler, vocab_term)

        try:

            assert vocab_term != "-1"
            assert vocab_id != -1

        except AssertionError:
            self.local_handler.toolkit.logger.log_action("Invalid id or term.")
            print("invalid id or term\n")
            time.sleep(1)
            return
        
        except self.local_handler.toolkit.UserCancelError:
            return

        target_vocab_index = next((i for i, vocab in enumerate(self.local_handler.vocab) if vocab.word_id == vocab_id))

        target_vocab_line = next((i + 1 for i, line in enumerate(self.local_handler.vocab_path) if int(self.local_handler.fileEnsurer.file_handler.read_sei_file(self.local_handler.vocab_path, i + 1, 1)) == vocab_id))

        ## deletes the vocab itself
        self.local_handler.fileEnsurer.file_handler.delete_sei_line(self.local_handler.vocab_path, target_vocab_line)
        self.local_handler.vocab.pop(target_vocab_index)

        ## deletes the cseps
        self.local_handler.fileEnsurer.file_handler.delete_all_occurrences_of_id(self.local_handler.vocab_csep_path, 1, vocab_id)

        ## deletes the typos
        self.local_handler.fileEnsurer.file_handler.delete_all_occurrences_of_id(self.local_handler.vocab_incorrect_typos_path, 1, vocab_id)
        self.local_handler.fileEnsurer.file_handler.delete_all_occurrences_of_id(self.local_handler.vocab_typos_path, 1, vocab_id)

##--------------------start-of-delete_csep_value()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def delete_csep_value(self):

        """
        
        Deletes a csep value.\n

        Parameters:\n
        self (object - vocabSettingsHandler) : The vocab settings handler object.\n

        Returns:\n
        None.\n

        """ 

        try:
            vocab_term_or_id = self.local_handler.toolkit.user_confirm("Please enter the vocab or vocab id that you want to delete a csep from.")

        except:
            return
        
        if(vocab_term_or_id.isdigit() == True):
            vocab_id = int(vocab_term_or_id)
            vocab_term = self.local_handler.searcher.get_term_from_id(self.local_handler, vocab_id) 
        else:
            vocab_term = vocab_term_or_id
            vocab_id = self.local_handler.searcher.get_id_from_term(self.local_handler, vocab_term)

        try:

            assert vocab_term != "-1"
            assert vocab_id != -1

        except AssertionError:
            self.local_handler.toolkit.logger.log_action("Invalid id or term.")
            print("invalid id or term\n")
            time.sleep(1)
            return 
        
        except self.local_handler.toolkit.UserCancelError:
            return
        
        ## gets target vocab from local handler directly
        target_index = next((i for i, vocab in enumerate(self.local_handler.vocab) if vocab.word_id == vocab_id))
        target_vocab = self.local_handler.vocab[target_index]

        ## gets csep print items
        valid_cseps = self.local_handler.searcher.get_csep_print_items_from_id(self.local_handler, vocab_id)

        for csep_item in valid_cseps:
            print(csep_item)

        target_csep_id = int(input("\nPlease enter the CSEP ID for the csep you would like to delete:\n"))

        ## pops the matching csep in the handler if exists, will do nothing if id is invalid or incorrect
        for i, csep in enumerate(target_vocab.testing_material_answer_all):
            
            if(csep.csep_id == target_csep_id):
                target_vocab.testing_material_answer_all.pop(i)

        ## same thing but for the file
        self.local_handler.fileEnsurer.file_handler.delete_all_occurrences_of_id(self.local_handler.vocab_csep_path, id_index=2, id_value=target_csep_id)