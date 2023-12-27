## built-in modules
import time

## custom modules
from handlers.local_handler import LocalHandler
from handlers.file_handler import FileHandler

from modules.searcher import Searcher
from modules.toolkit import Toolkit
from modules.logger import Logger
from modules.file_ensurer import FileEnsurer

from entities.vocab import vocab as vocab_blueprint 
from entities.csep import csep as csep_blueprint

class VocabSettingsHandler():

    """
    
    The handler that handles all of Seisen's vocab settings.
    
    """
##--------------------start-of-change_vocab_settings()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def change_vocab_settings() -> None:

        """

        Controls the pathing for all vocab settings.\n

        Parameters:\n
        VocabSettingsHandler (object - vocabSettingsHandler) : The vocab settings handler object.\n

        Returns:\n
        None.\n

        """ 

        Logger.log_action("User is changing vocab settings")

        vocab_message = "What are you trying to do?\n\n1.Add Vocab\n2.Add CSEP/Answer to Vocab\n3.Replace Vocab Value\n4.Replace CSEP/Answer Value\n5.Delete Vocab Value\n6.Delete CSEP/Answer from Vocab\n7.Search Vocab\n"

        print(vocab_message)

        type_setting = Toolkit.input_check(4, Toolkit.get_single_key(), 7, vocab_message)

        if(type_setting == "1"):
            VocabSettingsHandler.add_vocab()
        elif(type_setting == "2"):
            VocabSettingsHandler.add_csep()
        elif(type_setting == "3"):
            VocabSettingsHandler.replace_vocab_value()
        elif(type_setting == "4"):
            VocabSettingsHandler.replace_csep_value()
        elif(type_setting == "5"):
            VocabSettingsHandler.delete_vocab_value()
        elif(type_setting == "6"):
            VocabSettingsHandler.delete_csep_value()
        elif(type_setting == "7"):
            VocabSettingsHandler.search_vocab() 
    
##--------------------start-of-add_vocab()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def add_vocab() -> None:
        
        """
        
        Adds a user entered vocab to the local handler.

        """ 

        ## gets new ids
        new_vocab_id = FileHandler.get_new_id(LocalHandler.get_list_of_all_ids(6))
        new_csep_id = FileHandler.get_new_id(LocalHandler.get_list_of_all_ids(8))

        csep_value_list = []
        csep_actual_list_handler = []

        furigana = "0"
        isKanji = False

        ## gets vocab and csep details
        try:
            testing_material = Toolkit.user_confirm("Please enter a vocab term")
            romaji = Toolkit.user_confirm("Please enter " + testing_material + "'s romaji/pronunciation")
            definition = Toolkit.user_confirm("Please enter " + testing_material + "'s definition/main answer")

            csep_value_list.append(definition)

            while(input("Enter 1 if " + testing_material + " has any additional answers :\n") == "1"):
                Toolkit.clear_stream()
                csep_value_list.append(Toolkit.user_confirm("Please enter " + testing_material + "'s additional answers"))

            kana = [value.testing_material for value in LocalHandler.kana]

            for character in testing_material:
                if(character not in kana):
                    Logger.log_action(character + " is kanji")
                    furigana = Toolkit.user_confirm("Please enter " + testing_material + "'s furigana/kana spelling")
                    isKanji = True
                    break
        
        except:
            return
        
        ## checks if inc vocab is a duplicate
        for vocab in LocalHandler.vocab:
            
            if(vocab.testing_material == testing_material and vocab.romaji == romaji and vocab.furigana == furigana):

                Toolkit.clear_console()

                print(testing_material + " is in vocab already.\n")
                time.sleep(1)
                
                return

        ## inserts cseps first
        for csep_value in csep_value_list:

            csep_insert_values = [new_vocab_id, new_csep_id, csep_value, LocalHandler.VOCAB_WORD_TYPE]
            
            ## adds csep to local handler
            csep_actual_list_handler.append(csep_blueprint(new_vocab_id, new_csep_id, csep_value, LocalHandler.VOCAB_WORD_TYPE))

            ## writes csep to local
            FileHandler.write_sei_line(FileEnsurer.vocab_csep_actual_path, csep_insert_values)

            new_csep_id = FileHandler.get_new_id(LocalHandler.get_list_of_all_ids(8))

        ## writes vocab to local
        vocab_insert_values = [new_vocab_id, testing_material, romaji, definition, furigana, 0, 0]
        FileHandler.write_sei_line(FileEnsurer.vocab_actual_path, vocab_insert_values)

        ## updates local handler with new vocab
        LocalHandler.vocab.append(vocab_blueprint(new_vocab_id, testing_material, romaji, definition, csep_actual_list_handler, furigana, 0, 0, isKanji))
    
##--------------------start-of-add_csep()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def add_csep() -> None:

        """
        
        Adds a user entered csep to an existing vocab in the local handler.

        """ 

        vocab_term = ""
        vocab_id = 0

        target_index = 0

        ## gets new id
        new_csep_id = FileHandler.get_new_id(LocalHandler.get_list_of_all_ids(8))

        try:
            vocab_term_or_id = Toolkit.user_confirm("Please enter the vocab or vocab id that you want to add a csep/answer to.")

        except:
            return
        
        if(vocab_term_or_id.isdigit() == True):
            vocab_id = int(vocab_term_or_id)
            vocab_term = Searcher.get_vocab_term_from_id(vocab_id) 
        else:
            vocab_term = vocab_term_or_id
            vocab_id = Searcher.get_id_from_vocab_term(vocab_term)

        try:

            assert vocab_term != "-1"
            assert vocab_id != -1

            csep_value = Toolkit.user_confirm("Please enter the csep/answer for " + vocab_term + " you would like to add.")

        except AssertionError:
            print("invalid id or term\n")
            time.sleep(1)
            return
        
        except Toolkit.UserCancelError:
            return
        
        ## gets index of vocab in local handler
        target_index = next((i for i, vocab in enumerate(LocalHandler.vocab) if vocab.word_id == vocab_id))

        ## adds csep to local storage
        csep_insert_values = [vocab_id, new_csep_id, csep_value, LocalHandler.VOCAB_WORD_TYPE]
        FileHandler.write_sei_line(FileEnsurer.vocab_csep_actual_path, csep_insert_values)
        
        ## adds csep to local handler/current session
        new_csep = csep_blueprint(int(vocab_id), new_csep_id, csep_value, LocalHandler.VOCAB_WORD_TYPE)
        LocalHandler.vocab[target_index].testing_material_answer_all.append(new_csep)

##--------------------start-of-replace_vocab_value()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def replace_vocab_value() -> None:

        """
        
        Replaces a value within a vocab.

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
            vocab_term_or_id = Toolkit.user_confirm("Please enter the vocab or vocab id that you want to replace a value in.")

        except:
            return
        
        if(vocab_term_or_id.isdigit() == True):
            vocab_id = int(vocab_term_or_id)
            vocab_term = Searcher.get_vocab_term_from_id(vocab_id) 
        else:
            vocab_term = vocab_term_or_id
            vocab_id = Searcher.get_id_from_vocab_term(vocab_term)

        try:

            assert vocab_term != "-1"
            assert vocab_id != -1

        except AssertionError:
            print("invalid id or term\n")
            time.sleep(1)
            return 
        
        except Toolkit.UserCancelError:
            return
        
        ## gets index of target vocab in local handler
        target_index = next((i for i, vocab in enumerate(LocalHandler.vocab) if vocab.word_id == vocab_id))

        target_vocab = LocalHandler.vocab[target_index]

        type_replacement_message = Searcher.get_vocab_print_item_from_id(vocab_id)

        type_replacement_message += "\n\nWhat value would you like to replace? (1-6) (select index)"

        print(type_replacement_message)

        type_value = Toolkit.input_check(4, Toolkit.get_single_key(), 6, type_replacement_message)

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
            replacement_value = Toolkit.user_confirm("What are you replacing " + str(value_to_replace) + " with?")

        except:
            return 
        
        ## if the user is changing the main definition, we also need to adjust the csep for it
        if(type_value == "4"):

            csep_id = next((csep.csep_id for csep in target_vocab.testing_material_answer_all if csep.csep_value == value_to_replace))

            target_csep_line = next((i + 1 for i, line in enumerate(FileEnsurer.vocab_csep_actual_path) if int(FileHandler.read_sei_file(FileEnsurer.vocab_csep_actual_path, i + 1, 2)) == csep_id))

            FileHandler.edit_sei_line(FileEnsurer.vocab_csep_actual_path, target_csep_line, 3, str(replacement_value))
        
        else:
            pass

        target_vocab_line = next((i + 1 for i, line in enumerate(FileEnsurer.vocab_actual_path) if int(FileHandler.read_sei_file(FileEnsurer.vocab_actual_path, i + 1, 1)) == vocab_id))

        ## edits the vocab word
        FileHandler.edit_sei_line(FileEnsurer.vocab_actual_path, target_vocab_line, index_to_replace, str(replacement_value))
            
        ## it's easier to just reload everything than for me to figure out how to juggle csep values in the handler if the user wants to fuck with definitions or answers
        LocalHandler.load_words_from_local_storage()

##--------------------start-of-replace_csep_value()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def replace_csep_value() -> None:

        """
        
        Replaces a value within a csep.

        """

        CSEP_VALUE_COLUMN_NUMBER = 3

        try:
            vocab_term_or_id = Toolkit.user_confirm("Please enter the vocab or vocab id that contains the csep you want to edit.")

        except:
            return
        
        if(vocab_term_or_id.isdigit() == True):
            vocab_id = int(vocab_term_or_id)
            vocab_term = Searcher.get_vocab_term_from_id(vocab_id) 
        else:
            vocab_term = vocab_term_or_id
            vocab_id = Searcher.get_id_from_vocab_term(vocab_term)

        try:

            assert vocab_term != "-1"
            assert vocab_id != -1

        except AssertionError:
            Logger.log_action("Invalid id or term.")
            print("invalid id or term\n")
            time.sleep(1)
            return 
        
        except Toolkit.UserCancelError:
            return
        
        ## gets target vocab from local handler directly
        target_index = next((i for i, vocab in enumerate(LocalHandler.vocab) if vocab.word_id == vocab_id))
        target_vocab = LocalHandler.vocab[target_index]

        ## gets csep print items
        valid_cseps = Searcher.get_csep_print_items_from_vocab_id(vocab_id)

        for csep_item in valid_cseps:
            print(csep_item)

        target_csep_id = int(input("\nPlease enter the CSEP ID for the csep you would like to edit:\n")) 

        ## gets the csep to edit, will do nothing if id is invalid or incorrect
        for i, csep in enumerate(target_vocab.testing_material_answer_all):
            
            if(csep.csep_id == target_csep_id):
                try:
                    replace_value = Toolkit.user_confirm("What are you replacing " + csep.csep_value + " with?")

                    csep.csep_value = replace_value

                    target_csep_line = next((i + 1 for i, line in enumerate(FileEnsurer.vocab_csep_actual_path) if int(FileHandler.read_sei_file(FileEnsurer.vocab_csep_actual_path, i + 1, 2)) == csep.csep_id))

                    FileHandler.edit_sei_line(FileEnsurer.vocab_csep_actual_path, target_csep_line, CSEP_VALUE_COLUMN_NUMBER, replace_value)

                    ## if the csep is the main answer, we also need to change the vocab definition
                    if(csep.csep_value == target_vocab.testing_material_answer_main):

                        target_vocab_line = next((i + 1 for i, line in enumerate(FileEnsurer.vocab_actual_path) if int(FileHandler.read_sei_file(FileEnsurer.vocab_actual_path, i + 1, 1)) == vocab_id))

                        FileHandler.edit_sei_line(FileEnsurer.vocab_actual_path, target_vocab_line, 4, replace_value)

                    break

                except:
                    return

##--------------------start-of-delete_vocab_value()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def delete_vocab_value() -> None:

        """
        
        Deletes a vocab value.

        """ 

        try:
            vocab_term_or_id = Toolkit.user_confirm("Please enter the vocab or vocab id that you want to delete.")

        except:
            return
        
        if(vocab_term_or_id.isdigit() == True):
            vocab_id = int(vocab_term_or_id)
            vocab_term = Searcher.get_vocab_term_from_id(vocab_id) 
        else:
            vocab_term = vocab_term_or_id
            vocab_id = Searcher.get_id_from_vocab_term(vocab_term)

        try:

            assert vocab_term != "-1"
            assert vocab_id != -1

        except AssertionError:
            Logger.log_action("Invalid id or term.")
            print("invalid id or term\n")
            time.sleep(1)
            return
        
        except Toolkit.UserCancelError:
            return

        target_vocab_index = next((i for i, vocab in enumerate(LocalHandler.vocab) if vocab.word_id == vocab_id))

        target_vocab_line = next((i + 1 for i, line in enumerate(FileEnsurer.vocab_actual_path) if int(FileHandler.read_sei_file(FileEnsurer.vocab_actual_path, i + 1, 1)) == vocab_id))

        ## deletes the vocab itself
        FileHandler.delete_sei_line(FileEnsurer.vocab_actual_path, target_vocab_line)
        LocalHandler.vocab.pop(target_vocab_index)

        ## deletes the cseps
        FileHandler.delete_all_occurrences_of_id(FileEnsurer.vocab_csep_actual_path, 1, vocab_id)

        ## deletes the typos
        FileHandler.delete_all_occurrences_of_id(FileEnsurer.vocab_incorrect_typos_path, 1, vocab_id)
        FileHandler.delete_all_occurrences_of_id(FileEnsurer.vocab_typos_path, 1, vocab_id)

##--------------------start-of-delete_csep_value()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def delete_csep_value():

        """
        
        Deletes a csep value.

        """ 

        try:
            vocab_term_or_id = Toolkit.user_confirm("Please enter the vocab or vocab id that you want to delete a csep from.")

        except:
            return
        
        if(vocab_term_or_id.isdigit() == True):
            vocab_id = int(vocab_term_or_id)
            vocab_term = Searcher.get_vocab_term_from_id(vocab_id) 
        else:
            vocab_term = vocab_term_or_id
            vocab_id = Searcher.get_id_from_vocab_term(vocab_term)

        try:

            assert vocab_term != "-1"
            assert vocab_id != -1

        except AssertionError:
            Logger.log_action("Invalid id or term.")
            print("invalid id or term\n")
            time.sleep(1)
            return 
        
        except Toolkit.UserCancelError:
            return
        
        ## gets target vocab from local handler directly
        target_index = next((i for i, vocab in enumerate(LocalHandler.vocab) if vocab.word_id == vocab_id))
        target_vocab = LocalHandler.vocab[target_index]

        ## gets csep print items
        valid_cseps = Searcher.get_csep_print_items_from_vocab_id(vocab_id)

        for csep_item in valid_cseps:
            print(csep_item)

        target_csep_id = int(input("\nPlease enter the CSEP ID for the csep you would like to delete:\n"))

        ## pops the matching csep in the handler if exists, will do nothing if id is invalid or incorrect
        for i, csep in enumerate(target_vocab.testing_material_answer_all):

            
            if(csep.csep_id == target_csep_id):

                ## if it's the only csep, decline to delete
                if(len(target_vocab.testing_material_answer_all) == 1):
                    print("Cannot delete the only csep.\n")
                    time.sleep(1)
                    return
                
                ## if it's the main csep, change the main csep to the next one
                elif(csep.csep_value == target_vocab.testing_material_answer_main):
                        
                        target_vocab.testing_material_answer_main = target_vocab.testing_material_answer_all[1].csep_value
    
                        target_vocab_line = next((i + 1 for i, line in enumerate(FileEnsurer.vocab_actual_path) if int(FileHandler.read_sei_file(FileEnsurer.vocab_actual_path, i + 1, 1)) == vocab_id))
    
                        FileHandler.edit_sei_line(FileEnsurer.vocab_actual_path, target_vocab_line, 4, target_vocab.testing_material_answer_main)
                
                target_vocab.testing_material_answer_all.pop(i)

        ## same thing but for the file
        FileHandler.delete_all_occurrences_of_id(FileEnsurer.vocab_csep_actual_path, id_index=2, id_value=target_csep_id)

##--------------------start-of-search_vocab()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def search_vocab() -> None:

        """
        
        Searches throughout all of vocab for a search term.
        """

        matching_vocab_ids = []
        matching_csep_ids = []

        csep_search_result = ""

        vocab_match_msg = ""
        csep_match_msg = ""

        match_found_vocab = False
        match_found_csep = False

        try:
            search_term = Toolkit.user_confirm("Please enter search term.")

        except:
            return
        
        ## if search term is an id
        if(search_term.isnumeric()):

            matching_vocab_ids.append(int(search_term))
            matching_csep_ids.append(int(search_term))

            vocab_match_msg = "Vocab with the id of " + str(search_term) + ':\n'
            csep_match_msg = "CSEP with the id of " + str(search_term) + ':\n\n'

        ## if search term is not an id/number and not japanese
        elif(all(ord(char) < 128 for char in search_term)):
            
            matching_vocab_ids, matching_csep_ids = Searcher.get_ids_from_alpha_term(search_term)

            vocab_match_msg = "Vocab that contain " + str(search_term) + ':\n'
            csep_match_msg = "CSEP that contain " + str(search_term) + ':\n\n'

        ## if search term is japanese
        else:
            matching_vocab_ids = Searcher.get_ids_from_japanese(search_term)

            vocab_match_msg = "Vocab that contain " + str(search_term) + ':\n'

        ## print vocab matches as they are found
        for id in matching_vocab_ids:

            try:
                print_item = Searcher.get_vocab_print_item_from_id(id)

                print(vocab_match_msg)

                print(print_item)

                match_found_vocab = True

            except Searcher.IDNotFoundError:
                pass

        ## cseps have to be handled differently, determine if they exist before doing anything with them
        for id in matching_csep_ids:

            try:
                print_item = Searcher.get_csep_print_item_from_id(id)

                csep_search_result += csep_match_msg

                csep_search_result += print_item

                match_found_csep = True

            except Searcher.IDNotFoundError:
                pass

        ## no need to pause if no vocab results were found
        if(match_found_vocab and match_found_csep):  
            Toolkit.pause_console("Press any key to see matching CSEP results")
            Toolkit.clear_console()

        ## print cseps if exist or vocab exist otherwise no matches
        print(csep_search_result if(csep_search_result or match_found_vocab) else "No Matches\n")

        Toolkit.pause_console()