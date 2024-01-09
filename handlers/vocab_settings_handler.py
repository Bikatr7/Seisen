## built-in modules
import time

## custom modules
from handlers.local_handler import LocalHandler
from handlers.file_handler import FileHandler

from modules.searcher import Searcher
from modules.toolkit import Toolkit
from modules.logger import Logger
from modules.file_ensurer import FileEnsurer

from entities.vocab import Vocab as vocab_blueprint 
from entities.synonym import Synonym as synonym_blueprint

class VocabSettingsHandler():

    """
    
    The handler that handles all of Seisen's vocab settings.
    
    """
##--------------------start-of-change_vocab_settings()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def change_vocab_settings() -> None:

        """

        Controls the pathing for all vocab settings.

        """ 

        Logger.log_action("User is changing vocab settings.")

        vocab_message = "What are you trying to do?\n\n1.Add Vocab\n2.Add Synonym/Answer to Vocab\n3.Replace Vocab Value\n4.Replace Synonym/Answer Value\n5.Delete Vocab Value\n6.Delete Synonym/Answer from Vocab\n7.Search Vocab\n"

        print(vocab_message)

        type_setting = Toolkit.input_check(4, Toolkit.get_single_key(), 7, vocab_message)

        if(type_setting == "1"):
            VocabSettingsHandler.add_vocab()
        elif(type_setting == "2"):
            VocabSettingsHandler.add_synonym()
        elif(type_setting == "3"):
            VocabSettingsHandler.replace_vocab_value()
        elif(type_setting == "4"):
            VocabSettingsHandler.replace_synonym_value()
        elif(type_setting == "5"):
            VocabSettingsHandler.delete_vocab_value()
        elif(type_setting == "6"):
            VocabSettingsHandler.delete_synonym_value()
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
        new_synonym_id = FileHandler.get_new_id(LocalHandler.get_list_of_all_ids(8))

        synonym_value_list = []
        synonym_actual_list_handler = []

        furigana = "0"
        is_kanji = False

        ## gets vocab and Synonym details
        try:
            testing_material = Toolkit.user_confirm("Please enter a vocab term.").strip()
            romaji = Toolkit.user_confirm("Please enter " + testing_material + "'s romaji/pronunciation.").strip()
            definition = Toolkit.user_confirm("Please enter " + testing_material + "'s definition/main answer.").strip()

            synonym_value_list.append(definition)

        except Toolkit.UserCancelError:
            print("\nCancelled.\n")
            time.sleep(Toolkit.sleep_constant)
            return
        
        ## checks if inc vocab is a duplicate
        for vocab in LocalHandler.vocab:
            
            if(vocab.testing_material == testing_material and vocab.romaji == romaji and vocab.furigana == furigana):

                Toolkit.clear_console()

                ## find the line where
                target_vocab_line = FileHandler.find_seisen_line(FileEnsurer.vocab_path, 1, vocab.word_id)

                print(testing_material + " is in vocab already. See line " + str(target_vocab_line) + " in vocab.seisen.\n")
                Toolkit.pause_console()
                return
            
        try:

            while(input("Enter 1 if " + testing_material + " has any additional answers :\n") == "1"):
                Toolkit.clear_stream()
                synonym_value_list.append(Toolkit.user_confirm("Please enter " + testing_material + "'s additional answers.").strip())

            for character in testing_material:
                if(character not in FileEnsurer.kana_filter):
                    Logger.log_action(character + " is kanji")
                    furigana = Toolkit.user_confirm("Please enter " + testing_material + "'s furigana/kana spelling.").strip()
                    is_kanji = True
                    break

        except Toolkit.UserCancelError:
            print("\nCancelled.\n")
            time.sleep(Toolkit.sleep_constant)
            return

        ## inserts synonyms first
        for synonym_value in synonym_value_list:

            synonym_insert_values = [new_vocab_id, new_synonym_id, synonym_value, LocalHandler.VOCAB_WORD_TYPE]
            
            ## adds synonym to local handler
            synonym_actual_list_handler.append(synonym_blueprint(new_vocab_id, new_synonym_id, synonym_value, LocalHandler.VOCAB_WORD_TYPE))

            ## writes synonym to local
            FileHandler.write_seisen_line(FileEnsurer.vocab_synonyms_path, synonym_insert_values)

            new_synonym_id = FileHandler.get_new_id(LocalHandler.get_list_of_all_ids(8))

        ## writes vocab to local
        vocab_insert_values = [new_vocab_id, testing_material, romaji, definition, furigana, 0, 0]
        FileHandler.write_seisen_line(FileEnsurer.vocab_path, vocab_insert_values)

        ## updates local handler with new vocab
        LocalHandler.vocab.append(vocab_blueprint(new_vocab_id, testing_material, romaji, definition, synonym_actual_list_handler, furigana, 0, 0, is_kanji))
    
##--------------------start-of-add_synonym()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def add_synonym() -> None:

        """
        
        Adds a user entered Synonym to an existing vocab in the local handler.

        """ 

        vocab_term = ""
        vocab_id = 0

        target_index = 0

        ## gets new id
        new_synonym_id = FileHandler.get_new_id(LocalHandler.get_list_of_all_ids(8))

        try:
            vocab_term_or_id = Toolkit.user_confirm("Please enter the vocab or vocab id that you want to add a Synonym/Answer to.").strip()

        except Toolkit.UserCancelError:
            print("Cancelled.\n")
            time.sleep(Toolkit.sleep_constant)
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

            synonym_value = Toolkit.user_confirm("Please enter the Synonym/Answer for " + vocab_term + " you would like to add.").strip()

        except AssertionError:
            print("Invalid id or term.\n")
            time.sleep(Toolkit.sleep_constant)
            return
        
        except Toolkit.UserCancelError:
            print("\nCancelled.\n")
            time.sleep(Toolkit.sleep_constant)
            return
        
        ## gets index of vocab in local handler
        target_index = next((i for i, vocab in enumerate(LocalHandler.vocab) if vocab.word_id == vocab_id))

        ## adds Synonym to local storage
        synonym_insert_values = [vocab_id, new_synonym_id, synonym_value, LocalHandler.VOCAB_WORD_TYPE]
        FileHandler.write_seisen_line(FileEnsurer.vocab_synonyms_path, synonym_insert_values)
        
        ## adds Synonym to local handler/current session
        new_synonym = synonym_blueprint(int(vocab_id), new_synonym_id, synonym_value, LocalHandler.VOCAB_WORD_TYPE)
        LocalHandler.vocab[target_index].testing_material_answer_all.append(new_synonym)

##--------------------start-of-replace_vocab_value()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def replace_vocab_value() -> None:

        """
        
        Replaces a value within a vocab.

        """ 

        value_to_replace = 0
        index_to_replace = 0

        target_vocab_line = 0

        target_index = 0

        synonym_id = 0

        ATTRIBUTE_TESTING_MATERIAL = 2
        ATTRIBUTE_ROMAJI = 3
        ATTRIBUTE_FURIGANA = 5
        ATTRIBUTE_TESTING_MATERIAL_ANSWER_MAIN = 4
        ATTRIBUTE_INCORRECT_COUNT = 6
        ATTRIBUTE_CORRECT_COUNT = 7

        try:
            vocab_term_or_id = Toolkit.user_confirm("Please enter the vocab or vocab id that you want to replace a value in.").strip()

        except Toolkit.UserCancelError:
            print("Cancelled.\n")
            time.sleep(Toolkit.sleep_constant)
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
            print("Invalid id or term.\n")
            time.sleep(Toolkit.sleep_constant)
            return 
        
        ## gets index of target vocab in local handler
        target_index = next((i for i, vocab in enumerate(LocalHandler.vocab) if vocab.word_id == vocab_id))

        target_vocab = LocalHandler.vocab[target_index]

        attribute_names = ["testing_material", "romaji", "furigana", "testing_material_answer_main", "incorrect_count", "correct_count"]

        attributes_map = {
            attribute_names[0]: (target_vocab.testing_material, ATTRIBUTE_TESTING_MATERIAL),
            attribute_names[1]: (target_vocab.romaji, ATTRIBUTE_ROMAJI),
            attribute_names[2]: (target_vocab.furigana, ATTRIBUTE_FURIGANA),
            attribute_names[3]: (target_vocab.testing_material_answer_main, ATTRIBUTE_TESTING_MATERIAL_ANSWER_MAIN),
            attribute_names[4]: (target_vocab.incorrect_count, ATTRIBUTE_INCORRECT_COUNT),
            attribute_names[5]: (target_vocab.correct_count, ATTRIBUTE_CORRECT_COUNT)
        }

        type_replacement_message = Searcher.get_vocab_print_item_from_id(vocab_id)

        readable_attributes_map = "\n".join(f"{i+1}: {value[0]}" for i, (key, value) in enumerate(attributes_map.items()))
        type_replacement_message += "\n" + readable_attributes_map

        type_replacement_message += "\n\nWhat value would you like to replace? (1-6) (select index):"

        print(type_replacement_message)

        type_value = Toolkit.input_check(4, Toolkit.get_single_key(), 6, type_replacement_message)
        attribute_name = list(attributes_map.keys())[int(type_value) - 1]

        value_to_replace, index_to_replace = attributes_map[attribute_name]

        try:
            replacement_value = Toolkit.user_confirm("What are you replacing " + str(value_to_replace) + " with?").strip()

        except Toolkit.UserCancelError:
            print("\nCancelled.\n")
            time.sleep(Toolkit.sleep_constant)
            return 
        
        ## if the user is changing the main definition, we also need to adjust the Synonym for it
        if(type_value == "4"):

            synonym_id = next((synonym.synonym_id for synonym in target_vocab.testing_material_answer_all if synonym.synonym_value == value_to_replace))

            target_synonym = next((synonym for synonym in target_vocab.testing_material_answer_all if synonym.synonym_value == value_to_replace))
            target_synonym_line = FileHandler.find_seisen_line(FileEnsurer.vocab_synonyms_path, 2, synonym_id)

            ## local handler change
            target_synonym.synonym_value = replacement_value

            ## edits the Synonym in the file
            FileHandler.edit_seisen_line(FileEnsurer.vocab_synonyms_path, target_synonym_line, 3, str(replacement_value))
        
        else:
            pass

        target_vocab_line = FileHandler.find_seisen_line(FileEnsurer.vocab_path, 1, vocab_id)

        ## edits the vocab word in the file directly
        FileHandler.edit_seisen_line(FileEnsurer.vocab_path, target_vocab_line, index_to_replace, str(replacement_value))

        if(attribute_name in ["incorrect_count", "correct_count"]):
            replacement_value = int(replacement_value)

        ## Updates the value in the local handler directly
        target_vocab.__dict__[attribute_name] = replacement_value

##--------------------start-of-replace_synonym_value()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def replace_synonym_value() -> None:

        """
        
        Replaces a value within a Synonym.

        """

        SYNONYM_VALUE_COLUMN_NUMBER = 3

        try:
            vocab_term_or_id = Toolkit.user_confirm("Please enter the vocab or vocab id that contains the Synonym you want to edit.").strip()

        except Toolkit.UserCancelError:
            print("\nCancelled.\n")
            time.sleep(Toolkit.sleep_constant)
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
            print("Invalid id or term.\n")
            time.sleep(Toolkit.sleep_constant)
            return 
        
        ## gets target vocab from local handler directly
        target_index = next((i for i, vocab in enumerate(LocalHandler.vocab) if vocab.word_id == vocab_id))
        target_vocab = LocalHandler.vocab[target_index]

        ## gets Synonym print items
        valid_synonyms = Searcher.get_synonym_print_items_from_vocab_id(vocab_id)

        for synonym_item in valid_synonyms:
            print(synonym_item)

        try:
            target_synonym_id = int(input("Please enter the Synonym ID for the Synonym you would like to edit:\n")) 

        except:
            target_synonym_id = -1

        if(target_synonym_id not in [synonym.synonym_id for synonym in target_vocab.testing_material_answer_all]):
            print("\nInvalid Synonym ID.\n")
            time.sleep(Toolkit.sleep_constant)
            return

        ## gets the Synonym to edit, will do nothing if id is invalid or incorrect
        for i, Synonym in enumerate(target_vocab.testing_material_answer_all):
            
            if(Synonym.synonym_id == target_synonym_id):

                try:

                    replace_value = Toolkit.user_confirm("What are you replacing " + Synonym.synonym_value + " with?")
                    target_synonym_line = FileHandler.find_seisen_line(FileEnsurer.vocab_synonyms_path, 2, Synonym.synonym_id)

                    ## if the Synonym is the main answer, we also need to change the vocab definition
                    if(Synonym.synonym_value == target_vocab.testing_material_answer_main):

                        target_vocab_line = FileHandler.find_seisen_line(FileEnsurer.vocab_path, 1, vocab_id)

                        ## local handler change
                        target_vocab.testing_material_answer_main = replace_value

                        ## edits the vocab word in the file directly
                        FileHandler.edit_seisen_line(FileEnsurer.vocab_path, target_vocab_line, 4, replace_value)

                    ## local handler change
                    Synonym.synonym_value = replace_value

                    ## edits the Synonym in the file
                    FileHandler.edit_seisen_line(FileEnsurer.vocab_synonyms_path, target_synonym_line, SYNONYM_VALUE_COLUMN_NUMBER, replace_value)

                    break

                except Toolkit.UserCancelError:
                    print("\nCancelled.\n")
                    time.sleep(Toolkit.sleep_constant)
                    return

##--------------------start-of-delete_vocab_value()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def delete_vocab_value() -> None:

        """
        
        Deletes a vocab value.

        """ 

        try:
            vocab_term_or_id = Toolkit.user_confirm("Please enter the vocab or vocab id that you want to delete.").strip()

        except Toolkit.UserCancelError:
            print("\nCancelled.\n")
            time.sleep(Toolkit.sleep_constant)
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
            print("Invalid id or term.\n")
            time.sleep(Toolkit.sleep_constant)
            return
        
        target_vocab_index = next((i for i, vocab in enumerate(LocalHandler.vocab) if vocab.word_id == vocab_id))

        target_vocab_line = FileHandler.find_seisen_line(FileEnsurer.vocab_path, 1, vocab_id)

        Toolkit.clear_console()

        if(input("Are you sure you want to delete this vocab? (1 for yes, 2 for no) \n\n" + Searcher.get_vocab_print_item_from_id(int(vocab_id)) + "\n") == "1"):
            pass

        else:
            print("\nCancelled.\n")
            time.sleep(Toolkit.sleep_constant)
            return

        ## deletes the vocab itself
        FileHandler.delete_seisen_line(FileEnsurer.vocab_path, target_vocab_line)
        LocalHandler.vocab.pop(target_vocab_index)

        ## deletes the synonyms
        FileHandler.delete_all_occurrences_of_id(FileEnsurer.vocab_synonyms_path, 1, vocab_id)

        ## deletes the typos
        FileHandler.delete_all_occurrences_of_id(FileEnsurer.vocab_incorrect_typos_path, 1, vocab_id)
        FileHandler.delete_all_occurrences_of_id(FileEnsurer.vocab_typos_path, 1, vocab_id)

##--------------------start-of-delete_synonym_value()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def delete_synonym_value():

        """
        
        Deletes a Synonym value.

        """ 

        print_string = ""

        try:
            vocab_term_or_id = Toolkit.user_confirm("Please enter the vocab or vocab id that you want to delete a Synonym from.").strip()

        except Toolkit.UserCancelError:
            print("\nCancelled.\n")
            time.sleep(Toolkit.sleep_constant)
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
            print("Invalid id or term.\n")
            time.sleep(Toolkit.sleep_constant)
            return 
    
        ## gets target vocab from local handler directly
        target_index = next((i for i, vocab in enumerate(LocalHandler.vocab) if vocab.word_id == vocab_id))
        target_vocab = LocalHandler.vocab[target_index]

        ## gets Synonym print items
        valid_synonyms = Searcher.get_synonym_print_items_from_vocab_id(vocab_id)

        ## if it's the only Synonym, decline to delete
        if(len(target_vocab.testing_material_answer_all) <= 1):
            print("Cannot delete the only Synonym.\n")
            Toolkit.pause_console()
            return
            
        for synonym_item in valid_synonyms:
            print_string += synonym_item

        try:

            print_string += "\nPlease enter the Synonym ID for the Synonym you would like to delete:\n"

            target_synonym_id = Toolkit.user_confirm(print_string)

        except Toolkit.UserCancelError:
            print("\nCancelled.\n")
            time.sleep(Toolkit.sleep_constant)
            return
        
        Toolkit.clear_console()

        if(input("Are you sure you want to delete this Synonym? (1 for yes, 2 for no) \n\n" + Searcher.get_synonym_print_item_from_id(int(target_synonym_id)) + "\n") == "1"):
            pass

        else:
            print("\nCancelled.\n")
            time.sleep(Toolkit.sleep_constant)
            return

        Toolkit.pause_console()
        
        try:
            target_synonym_id = int(target_synonym_id)

        except:
            target_synonym_id = -1

        if(target_synonym_id not in [synonym.synonym_id for synonym in target_vocab.testing_material_answer_all]):
            print("\nInvalid Synonym ID.\n")
            time.sleep(Toolkit.sleep_constant)
            return

        ## pops the matching Synonym in the handler if exists, will do nothing if id is invalid or incorrect
        for i, Synonym in enumerate(target_vocab.testing_material_answer_all):

            if(Synonym.synonym_id == target_synonym_id):

                ## if it's the main Synonym, change the main Synonym to the next one
                if(Synonym.synonym_value == target_vocab.testing_material_answer_main):
                        
                        target_vocab.testing_material_answer_main = target_vocab.testing_material_answer_all[1].synonym_value
    
                        target_vocab_line = FileHandler.find_seisen_line(FileEnsurer.vocab_path, 1, vocab_id)
    
                        FileHandler.edit_seisen_line(FileEnsurer.vocab_path, target_vocab_line, 4, target_vocab.testing_material_answer_main)
                
                ## deletes the Synonym itself
                target_vocab.testing_material_answer_all.pop(i)

        ## same thing but for the file
        FileHandler.delete_all_occurrences_of_id(FileEnsurer.vocab_synonyms_path, id_index=2, target_id=int(target_synonym_id))

##--------------------start-of-search_vocab()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def search_vocab() -> None:

        """
        
        Searches throughout all of vocab for a search term.
        """

        matching_vocab_ids = []
        matching_synonym_ids = []

        synonym_search_result = ""

        vocab_match_msg = ""
        synonym_match_msg = ""

        match_found_vocab = False
        match_found_synonym = False

        try:
            search_term = Toolkit.user_confirm("Please enter search term.").strip()

        except Toolkit.UserCancelError:
            print("\nCancelled.\n")
            time.sleep(Toolkit.sleep_constant)
            return
        
        ## if search term is an id
        if(search_term.isnumeric()):

            matching_vocab_ids.append(int(search_term))
            matching_synonym_ids.append(int(search_term))

            vocab_match_msg = "Vocab with the id of " + str(search_term) + ':\n'
            synonym_match_msg = "Synonym with the id of " + str(search_term) + ':\n\n'

        ## if search term is not an id/number and not japanese
        elif(all(ord(char) < 128 for char in search_term)):
            
            matching_vocab_ids, matching_synonym_ids = Searcher.get_ids_from_alpha_term(search_term)

            vocab_match_msg = "Vocab that contain " + str(search_term) + ':\n'
            synonym_match_msg = "Synonym that contain " + str(search_term) + ':\n\n'

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

        ## synonyms have to be handled differently, determine if they exist before doing anything with them
        for id in matching_synonym_ids:

            try:
                print_item = Searcher.get_synonym_print_item_from_id(id)

                synonym_search_result += synonym_match_msg

                synonym_search_result += print_item         
                match_found_synonym = True

            except Searcher.IDNotFoundError:
                pass

        ## no need to pause if no vocab results were found
        if(match_found_vocab and match_found_synonym):  
            Toolkit.pause_console("Press any key to see matching Synonym results")
            Toolkit.clear_console()

        ## print synonym if exist or vocab exist otherwise no matches
        print(synonym_search_result if(synonym_search_result or match_found_vocab) else "No Matches\n")

        Toolkit.pause_console()