## built-in modules
import typing
import time

## custom modules
from handlers.local_handler import LocalHandler
from handlers.remote_handler import RemoteHandler
from handlers.file_handler import FileHandler

from modules.searcher import Searcher
from modules.toolkit import Toolkit
from modules.logger import Logger
from modules.file_ensurer import FileEnsurer

from entities.vocab import Vocab as vocab_blueprint 
from entities.testing_material import TestingMaterial as testing_material_blueprint
from entities.synonym import Synonym as synonym_blueprint
from entities.reading import Reading as reading_blueprint
from entities.typo import Typo as typo_blueprint
from entities.incorrect_typo import IncorrectTypo as incorrect_typo_blueprint

from entities.vocab import Vocab
from entities.synonym import Synonym
from entities.reading import Reading
from entities.typo import Typo
from entities.incorrect_typo import IncorrectTypo
from entities.testing_material import TestingMaterial

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

        vocab_message = "What are you trying to do?\n\n1.Add Entity\n2.Edit Entity\n3.Delete Entity\n4.Search Entity\n"

        print(vocab_message)

        type_setting = Toolkit.input_check(4, Toolkit.get_single_key(), 4, vocab_message)

        if(type_setting == "1"):
            VocabSettingsHandler.add_entity()

        elif(type_setting == "2"):
            VocabSettingsHandler.edit_entity()

        elif(type_setting == "3"):
            VocabSettingsHandler.delete_entity()

        elif(type_setting == "4"):
            VocabSettingsHandler.search_entity()

##--------------------start-of-add_entity()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
    @staticmethod
    def add_entity() -> None:

        """

        Adds a vocab entity to the database.

        """ 

        Logger.log_action("User is adding a vocab entity.")

        entity_message = "What type of entity are you trying to add?\n\n1.Add Vocab\n2.Add Synonym to Existing Vocab\n3.Add TestingMaterial to Existing Vocab\n4.Add Reading to Existing Vocab\n5.Add Typo to Existing Vocab\n6.Add IncorrectTypo to Existing Vocab\n"

        print(entity_message)

        type_setting = Toolkit.input_check(4, Toolkit.get_single_key(), 6, entity_message)

        if(type_setting == "1"):
            VocabSettingsHandler.add_vocab()

        elif(type_setting == "2"):
            VocabSettingsHandler.add_synonym_to_existing_vocab()

        elif(type_setting == "3"):
            VocabSettingsHandler.add_testing_material_to_existing_vocab()

        elif(type_setting == "4"):
            VocabSettingsHandler.add_reading_to_existing_vocab()

        elif(type_setting == "5"):
            VocabSettingsHandler.add_typo_to_existing_vocab()

        elif(type_setting == "6"):
            VocabSettingsHandler.add_incorrect_typo_to_existing_vocab()

##--------------------start-of-edit_entity()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
    @staticmethod
    def edit_entity() -> None:

        """

        Edits a vocab entity in the database.

        """ 

        Logger.log_action("User is editing a vocab entity.")

        entity_message = "What type of entity are you trying to edit?\n\n1.Edit Vocab\n2.Edit Synonym of Existing Vocab\n3.Edit TestingMaterial of Existing Vocab\n4.Edit Reading of Existing Vocab\n5.Edit Typo of Existing Vocab\n6.Edit IncorrectTypo of Existing Vocab\n"

        print(entity_message)

        type_setting = Toolkit.input_check(2, Toolkit.get_single_key(), 6, entity_message)

        if(type_setting == "1"):
            VocabSettingsHandler.edit_vocab()

        elif(type_setting == "2"):
            VocabSettingsHandler.edit_synonym()

        elif(type_setting == "3"):
            VocabSettingsHandler.edit_testing_material()

        elif(type_setting == "4"):
            VocabSettingsHandler.edit_reading()

        elif(type_setting == "5"):
            VocabSettingsHandler.edit_typo()

        elif(type_setting == "6"):
            VocabSettingsHandler.edit_incorrect_typo()

##--------------------start-of-delete_entity()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
    @staticmethod
    def delete_entity() -> None:

        """

        Deletes a vocab entity from the database.

        """ 

        Logger.log_action("User is deleting a vocab entity.")

        entity_message = "What type of entity are you trying to delete?\n\n1.Delete Vocab\n2.Delete Synonym of Existing Vocab\n3.Delete TestingMaterial of Existing Vocab\n4.Delete Reading of Existing Vocab\n5.Delete Typo of Existing Vocab\n6.Delete IncorrectTypo of Existing Vocab\n"

        print(entity_message)

        type_setting = Toolkit.input_check(2, Toolkit.get_single_key(), 6, entity_message)

        if(type_setting == "1"):
            VocabSettingsHandler.delete_vocab()

        elif(type_setting == "2"):
            VocabSettingsHandler.delete_synonym()

        elif(type_setting == "3"):
            VocabSettingsHandler.delete_testing_material()

        elif(type_setting == "4"):
            VocabSettingsHandler.delete_reading()

        elif(type_setting == "5"):
            VocabSettingsHandler.delete_typo()

        elif(type_setting == "6"):
            VocabSettingsHandler.delete_incorrect_typo()

##--------------------start-of-search_entity()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def search_entity() -> None:

        """

        Searches for a vocab entity in the database.

        """ 

        pass

##--------------------start-of-add_vocab()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def add_vocab() -> None:

        """

        Adds a vocab entity to the database.

        """ 

        ## gets new vocab id
        new_vocab_id = FileHandler.get_new_id(LocalHandler.get_list_of_all_ids(6))

        ## raw strings
        raw_testing_material:typing.List[str] = []
        raw_romaji:typing.List[str] = []
        raw_furigana:typing.List[str] = []
        raw_synonyms:typing.List[str] = []

        ## actual objects
        testing_material:typing.List[TestingMaterial] = []
        readings:typing.List[Reading] = []
        synonyms:typing.List[Synonym] = []

        ## get vocab components
        try:

            ## testing material
            curr_raw_testing_material = Toolkit.user_confirm("Please enter your vocab's main testing material (testing material are kanji/kana that are used as the material to be tested on).")
            raw_testing_material.append(curr_raw_testing_material)

            while(input(f"Enter 1 if {curr_raw_testing_material} has any additional testing material, otherwise enter 2 (testing material are kanji/kana that are used as the material to be tested on).\n") == "1"):
                Toolkit.clear_stream()
                raw_testing_material.append(Toolkit.user_confirm("Please enter your vocab's additional testing material (testing material are kanji/kana that are used as the material to be tested on)."))

            ## romaji and furigana (reading)
            curr_raw_romaji = Toolkit.user_confirm(f"Please enter {curr_raw_testing_material}'s main romaji (romaji are the pronunciation of the testing material, your main romaji should match the main testing material).")
            curr_raw_furigana = Toolkit.user_confirm(f"Please enter {curr_raw_romaji}'s furigana (furigana is the kana spelling of {curr_raw_romaji}).") 

            raw_romaji.append(curr_raw_romaji)
            raw_furigana.append(curr_raw_furigana)

            while(input(f"Enter 1 if {raw_testing_material} has any additional romaji, otherwise enter 2 (romaji are the pronunciation of the testing material).\n") == "1"):
                Toolkit.clear_stream()
                raw_romaji.append(Toolkit.user_confirm(f"Please enter {raw_testing_material}'s additional romaji (romaji are the pronunciation of the testing material. Additional Romaji can match any)."))
                raw_furigana.append(Toolkit.user_confirm(f"Please enter {raw_romaji[-1]}'s furigana (furigana is the kana spelling of {raw_romaji[-1]})."))

            ## synonyms
            raw_synonyms.append(Toolkit.user_confirm(f"Please enter {curr_raw_testing_material}'s main synonym (Synonyms are the definition of the testing material. Your main synonym should match the main testing material)."))

            while(input(f"Enter 1 if {raw_testing_material} has any additional synonyms, otherwise enter 2 (Synonyms are the definition of the testing material).\n") == "1"):
                Toolkit.clear_stream()
                raw_synonyms.append(Toolkit.user_confirm(f"Please enter {raw_testing_material}'s additional synonym (Synonyms are the definition of the testing material. Additional synonyms can match any)."))

        except Toolkit.UserCancelError:
            print("\nCancelled.\n")
            time.sleep(Toolkit.sleep_constant)
            return

        ## assemble actual objects and assign ids
        for i in range(len(raw_testing_material)):
            new_testing_material_id = FileHandler.get_new_id(LocalHandler.get_list_of_all_ids(12))
            testing_material.append(testing_material_blueprint(new_vocab_id, new_testing_material_id, raw_testing_material[i]))

            stuff_to_write = [new_vocab_id, new_testing_material_id, raw_testing_material[i]]
            FileHandler.write_seisen_line(FileEnsurer.vocab_testing_material_path, stuff_to_write)

        for i in range(len(raw_romaji)):
            new_reading_id = FileHandler.get_new_id(LocalHandler.get_list_of_all_ids(10))
            readings.append(reading_blueprint(new_vocab_id, new_reading_id, raw_furigana[i], raw_romaji[i]))

            stuff_to_write = [new_vocab_id, new_reading_id, raw_furigana[i], raw_romaji[i]]
            FileHandler.write_seisen_line(FileEnsurer.vocab_readings_path, stuff_to_write)

        for i in range(len(raw_synonyms)):
            new_synonym_id = FileHandler.get_new_id(LocalHandler.get_list_of_all_ids(8))
            synonyms.append(synonym_blueprint(new_vocab_id, new_synonym_id, raw_synonyms[i]))

            stuff_to_write = [new_vocab_id, new_synonym_id, raw_synonyms[i]]
            FileHandler.write_seisen_line(FileEnsurer.vocab_synonyms_path, stuff_to_write)

        ## assemble vocab object
        new_vocab = vocab_blueprint(new_vocab_id, testing_material, synonyms[0], synonyms, readings, incoming_incorrect_count=0, incoming_correct_count=0)

        ## write to file
        stuff_to_write = [new_vocab_id, new_vocab.incorrect_count, new_vocab.correct_count]
        FileHandler.write_seisen_line(FileEnsurer.vocab_path, stuff_to_write)

        ## add to current session
        LocalHandler.vocab.append(new_vocab)

##--------------------start-of-add_synonym_to_existing_vocab()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def add_synonym_to_existing_vocab() -> None:

        """

        Adds a synonym entity to an existing vocab entity in the database.

        """ 

        ## raw strings and actual objects
        raw_synonyms:typing.List[str] = []
        synonyms:typing.List[Synonym] = []

        ## gets synonym components
        try:
            target_vocab_id = int(Toolkit.user_confirm("Please enter the vocab id that you want to add a Synonym to."))

            print(target_vocab_id)

            Toolkit.pause_console()

            ## get target vocab
            try:
                target_vocab = Searcher.get_vocab_from_id(target_vocab_id)

                print(target_vocab.word_id)

                Toolkit.pause_console()

            except Searcher.IDNotFoundError:
                print("Vocab not found.\n")
                time.sleep(Toolkit.sleep_constant)
                return
        
            raw_synonyms.append(Toolkit.user_confirm("Please enter the Synonym/Answer for " + target_vocab.testing_material_main.testing_material_value + " you would like to add. (Synonyms are the definition of the testing material)."))

            while(input(f"Enter 1 if you'd like to add more synonyms for {target_vocab.testing_material_main.testing_material_value}, otherwise enter 2.\n") == "1"):
                Toolkit.clear_stream()
                raw_synonyms.append(Toolkit.user_confirm(f"Please enter the Synonym/Answer for {target_vocab.testing_material_main.testing_material_value} you would like to add. (Synonyms are the definition of the testing material)."))
        
        except Toolkit.UserCancelError:
            print("\nCancelled.\n")
            time.sleep(Toolkit.sleep_constant)
            return
        
        ## assemble actual objects, assign ids, and write to persistent storage
        for i in range(len(raw_synonyms)):
            new_synonym_id = FileHandler.get_new_id(LocalHandler.get_list_of_all_ids(8))
            synonyms.append(synonym_blueprint(target_vocab_id, new_synonym_id, raw_synonyms[i]))

            stuff_to_write = [target_vocab_id, new_synonym_id, raw_synonyms[i]]
            FileHandler.write_seisen_line(FileEnsurer.vocab_synonyms_path, stuff_to_write)

        ## add to current session
        for i in range(len(synonyms)):
            target_vocab.testing_material_answer_all.append(synonyms[i])

##--------------------start-of-add_testing_material_to_existing_vocab()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def add_testing_material_to_existing_vocab() -> None:

        """

        Adds a testing material entity to an existing vocab entity in the database.

        """ 

        ## raw strings and actual objects
        raw_testing_material:typing.List[str] = []
        testing_material:typing.List[TestingMaterial] = []

        ## gets testing material components
        try:
            target_vocab_id = int(Toolkit.user_confirm("Please enter the vocab id that you want to add a Testing Material to."))

            ## get target vocab
            try:
                target_vocab = Searcher.get_vocab_from_id(target_vocab_id)

            except Searcher.IDNotFoundError:
                print("Vocab not found.\n")
                time.sleep(Toolkit.sleep_constant)
                return
        
            raw_testing_material.append(Toolkit.user_confirm("Please enter the Testing Material for " + target_vocab.testing_material_main.testing_material_value + " you would like to add. (testing material are kanji/kana that are used as the material to be tested on)."))

            while(input(f"Enter 1 if you'd like to add more Testing Material for {target_vocab.testing_material_main.testing_material_value}, otherwise enter 2.\n") == "1"):
                Toolkit.clear_stream()
                raw_testing_material.append(Toolkit.user_confirm(f"Please enter the Testing Material for {target_vocab.testing_material_main.testing_material_value} you would like to add. (testing material are kanji/kana that are used as the material to be tested on)."))
        
        except Toolkit.UserCancelError:
            print("\nCancelled.\n")
            time.sleep(Toolkit.sleep_constant)
            return
        
        ## assemble actual objects, assign ids, and write to persistent storage
        for i in range(len(raw_testing_material)):
            new_testing_material_id = FileHandler.get_new_id(LocalHandler.get_list_of_all_ids(12))
            testing_material.append(testing_material_blueprint(target_vocab_id, new_testing_material_id, raw_testing_material[i]))

            stuff_to_write = [target_vocab_id, new_testing_material_id, raw_testing_material[i]]
            FileHandler.write_seisen_line(FileEnsurer.vocab_testing_material_path, stuff_to_write)

        ## add to current session
        for i in range(len(testing_material)):
            target_vocab.testing_material_all.append(testing_material[i])

##--------------------start-of-add_reading_to_existing_vocab()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def add_reading_to_existing_vocab() -> None:

        """

        Adds a reading entity to an existing vocab entity in the database.

        """ 

        ## raw strings and actual objects
        raw_romaji:typing.List[str] = []
        raw_furigana:typing.List[str] = []
        readings:typing.List[Reading] = []

        ## gets reading components
        try:
            target_vocab_id = int(Toolkit.user_confirm("Please enter the vocab id that you want to add a Reading to."))

            ## get target vocab
            try:
                target_vocab = Searcher.get_vocab_from_id(target_vocab_id)

            except Searcher.IDNotFoundError:
                print("Vocab not found.\n")
                time.sleep(Toolkit.sleep_constant)
                return
        
            curr_raw_romaji = Toolkit.user_confirm(f"Please enter a romaji for {target_vocab.testing_material_main.testing_material_value} you would like to add. (romaji are the pronunciation of the testing material).")
            curr_raw_furigana = Toolkit.user_confirm(f"Please enter {curr_raw_romaji}'s furigana (furigana is the kana spelling of {curr_raw_romaji}).") 

            raw_romaji.append(curr_raw_romaji)
            raw_furigana.append(curr_raw_furigana)

            while(input(f"Enter 1 if {target_vocab.testing_material_main.testing_material_value} has any additional romaji, otherwise enter 2 (romaji are the pronunciation of the testing material).\n") == "1"):
                Toolkit.clear_stream()
                raw_romaji.append(Toolkit.user_confirm(f"Please enter {target_vocab.testing_material_main.testing_material_value}'s additional romaji (romaji are the pronunciation of the testing material)."))
                raw_furigana.append(Toolkit.user_confirm(f"Please enter {raw_romaji[-1]}'s furigana (furigana is the kana spelling of {raw_romaji[-1]})."))

        except Toolkit.UserCancelError:
            print("\nCancelled.\n")
            time.sleep(Toolkit.sleep_constant)
            return
        
        ## assemble actual objects, assign ids, and write to persistent storage
        for i in range(len(raw_romaji)):
            new_reading_id = FileHandler.get_new_id(LocalHandler.get_list_of_all_ids(10))
            readings.append(reading_blueprint(target_vocab_id, new_reading_id, raw_furigana[i], raw_romaji[i]))

            stuff_to_write = [target_vocab_id, new_reading_id, raw_furigana[i], raw_romaji[i]]
            FileHandler.write_seisen_line(FileEnsurer.vocab_readings_path, stuff_to_write)

        ## add to current session
        for i in range(len(readings)):
            target_vocab.readings.append(readings[i])

##--------------------start-of-add_typo_to_existing_vocab()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            
    @staticmethod
    def add_typo_to_existing_vocab() -> None:

        """

        Adds a typo entity to an existing vocab entity in the database.

        """ 

        ## raw strings and actual objects
        raw_typo:typing.List[str] = []
        typos:typing.List[Typo] = []

        ## gets typo components
        try:
            target_vocab_id = int(Toolkit.user_confirm("Please enter the vocab id that you want to add a Typo to."))

            ## get target vocab
            try:
                target_vocab = Searcher.get_vocab_from_id(target_vocab_id)

            except Searcher.IDNotFoundError:
                print("Vocab not found.\n")
                time.sleep(Toolkit.sleep_constant)
                return
        
            raw_typo.append(Toolkit.user_confirm(f"Please enter a typo for {target_vocab.testing_material_main.testing_material_value} you would like to add. (typos are the incorrect spelling of the testing material) These \"typos\" automatically count as correct answers."))

            while(input(f"Enter 1 if {target_vocab.testing_material_main.testing_material_value} has any additional typos, otherwise enter 2 (typos are the incorrect spelling of the testing material, These \"typos\" automatically count as correct answers).\n") == "1"):
                Toolkit.clear_stream()
                raw_typo.append(Toolkit.user_confirm(f"Please enter a typo for {target_vocab.testing_material_main.testing_material_value} you would like to add. (typos are the incorrect spelling of the testing material).\n"))
        
        except Toolkit.UserCancelError:
            print("\nCancelled.\n")
            time.sleep(Toolkit.sleep_constant)
            return
        
        ## assemble actual objects, assign ids, and write to persistent storage
        for i in range(len(raw_typo)):
            new_typo_id = FileHandler.get_new_id(LocalHandler.get_list_of_all_ids(3))
            typos.append(typo_blueprint(target_vocab_id, new_typo_id, raw_typo[i]))

            stuff_to_write = [target_vocab_id, new_typo_id, raw_typo[i]]
            FileHandler.write_seisen_line(FileEnsurer.vocab_typos_path, stuff_to_write)

        ## add to current session
        for i in range(len(typos)):
            target_vocab.typos.append(typos[i])

##--------------------start-of-add_incorrect_typo_to_existing_vocab()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            
    @staticmethod
    def add_incorrect_typo_to_existing_vocab() -> None:

        """

        Adds an incorrect typo entity to an existing vocab entity in the database.

        """ 

        ## raw strings and actual objects
        raw_incorrect_typo:typing.List[str] = []
        incorrect_typos:typing.List[IncorrectTypo] = []

        ## gets incorrect typo components
        try:
            target_vocab_id = int(Toolkit.user_confirm("Please enter the vocab id that you want to add an Incorrect Typo to."))

            ## get target vocab
            try:
                target_vocab = Searcher.get_vocab_from_id(target_vocab_id)

            except Searcher.IDNotFoundError:
                print("Vocab not found.\n")
                time.sleep(Toolkit.sleep_constant)
                return
        
            raw_incorrect_typo.append(Toolkit.user_confirm(f"Please enter an incorrect typo for {target_vocab.testing_material_main.testing_material_value} you would like to add. (incorrect typos are the incorrect spelling of the testing material that are counted as incorrect answers)."))

            while(input(f"Enter 1 if {target_vocab.testing_material_main.testing_material_value} has any additional incorrect typos, otherwise enter 2 (incorrect typos are the incorrect spelling of the testing material that are counted as incorrect answers).\n") == "1"):
                Toolkit.clear_stream()
                raw_incorrect_typo.append(Toolkit.user_confirm(f"Please enter an incorrect typo for {target_vocab.testing_material_main.testing_material_value} you would like to add. (incorrect typos are the incorrect spelling of the testing material that are counted as incorrect answers).\n"))
        
        except Toolkit.UserCancelError:
            print("\nCancelled.\n")
            time.sleep(Toolkit.sleep_constant)
            return
        
        ## assemble actual objects, assign ids, and write to persistent storage
        for i in range(len(raw_incorrect_typo)):
            new_incorrect_typo_id = FileHandler.get_new_id(LocalHandler.get_list_of_all_ids(4))
            incorrect_typos.append(incorrect_typo_blueprint(target_vocab_id, new_incorrect_typo_id, raw_incorrect_typo[i]))

            stuff_to_write = [target_vocab_id, new_incorrect_typo_id, raw_incorrect_typo[i]]
            FileHandler.write_seisen_line(FileEnsurer.vocab_incorrect_typos_path, stuff_to_write)

        ## add to current session
        for i in range(len(incorrect_typos)):
            target_vocab.incorrect_typos.append(incorrect_typos[i])

##--------------------start-of-edit_vocab()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            
    @staticmethod
    def edit_vocab() -> None:

        """

        Edits a vocab entity in the database.

        """ 

        ## gets target vocab
        try:
            target_vocab_id = int(Toolkit.user_confirm("Please enter the id of the vocab you want to edit."))

            ## get target vocab
            try:
                target_vocab = Searcher.get_vocab_from_id(target_vocab_id)

            except Searcher.IDNotFoundError:
                print("Vocab not found.\n")
                time.sleep(Toolkit.sleep_constant)
                return
            
            ## get value to edit
            edit_message = "What would you like to edit?\n\n1. Incorrect Count\n2. Correct Count\nID cannot be edited, please use other settings to edit associated entities (testing material, synonyms, etc.)\n"

            print(edit_message)

            type_setting = Toolkit.input_check(2, Toolkit.get_single_key(), 2, edit_message)

            if(type_setting == "1"):
                value_to_edit = target_vocab.incorrect_count
                message_to_print = "Please enter the new incorrect count for " + target_vocab.testing_material_main.testing_material_value + ". (Incorrect count is the number of times the user has gotten the vocab wrong. Currently: " + str(value_to_edit) + ")"

            else:
                value_to_edit = target_vocab.correct_count
                message_to_print = "Please enter the new correct count for " + target_vocab.testing_material_main.testing_material_value + ". (Correct count is the number of times the user has gotten the vocab right. Currently: " + str(value_to_edit) + ")"

            new_value = int(Toolkit.user_confirm(message_to_print))

            ## edit value in current session
            if(type_setting == "1"):
                target_vocab.incorrect_count = new_value
                index = 2

            else:
                target_vocab.correct_count = new_value
                index = 3

            ## edit value in persistent storage
            target_vocab_line = FileHandler.find_seisen_line(FileEnsurer.vocab_path, column_index=1, target_value=target_vocab_id)
            FileHandler.edit_seisen_line(FileEnsurer.vocab_path, target_vocab_line, index, new_value)

        except Toolkit.UserCancelError:
            print("\nCancelled.\n")
            time.sleep(Toolkit.sleep_constant)
            return
        
##--------------------start-of-edit_synonym()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
    @staticmethod
    def edit_synonym() -> None:

        """

        Edits a synonym entity in the database.

        """ 

        ## gets target synonym
        try:
            target_synonym_id = int(Toolkit.user_confirm("Please enter the id of the synonym you want to edit."))

            ## get target synonym
            try:
                target_synonym = Searcher.get_synonym_from_id(target_synonym_id)

            except Searcher.IDNotFoundError:
                print("Synonym not found.\n")
                time.sleep(Toolkit.sleep_constant)
                return
            
            message_to_print = "Please enter the new synonym for " + target_synonym.synonym_value + ". (Synonym is the definition of the testing material)."

            new_value = Toolkit.user_confirm(message_to_print)

            ## edit value in current session
            target_synonym.synonym_value = new_value

            ## edit value in persistent storage
            target_synonym_line = FileHandler.find_seisen_line(FileEnsurer.vocab_synonyms_path, column_index=2, target_value=target_synonym_id)
            FileHandler.edit_seisen_line(FileEnsurer.vocab_synonyms_path, target_synonym_line, column_number=3, value_to_replace_to=new_value)

        except Toolkit.UserCancelError:
            print("\nCancelled.\n")
            time.sleep(Toolkit.sleep_constant)
            return
        
##--------------------start-of-edit_testing_material()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
    @staticmethod
    def edit_testing_material() -> None:

        """

        Edits a testing material entity in the database.

        """ 

        ## gets target testing material
        try:
            target_testing_material_id = int(Toolkit.user_confirm("Please enter the id of the testing material you want to edit."))

            ## get target testing material
            try:
                target_testing_material = Searcher.get_testing_material_from_id(target_testing_material_id)

            except Searcher.IDNotFoundError:
                print("Testing Material not found.\n")
                time.sleep(Toolkit.sleep_constant)
                return
            
            message_to_print = "Please enter the new testing material for " + target_testing_material.testing_material_value + ". (Testing Material is the kanji/kana that are used as the material to be tested on)."

            new_value = Toolkit.user_confirm(message_to_print)

            ## edit value in current session
            target_testing_material.testing_material_value = new_value

            ## edit value in persistent storage
            target_testing_material_line = FileHandler.find_seisen_line(FileEnsurer.vocab_testing_material_path, column_index=2, target_value=target_testing_material_id)
            FileHandler.edit_seisen_line(FileEnsurer.vocab_testing_material_path, target_testing_material_line, column_number=3, value_to_replace_to=new_value)

        except Toolkit.UserCancelError:
            print("\nCancelled.\n")
            time.sleep(Toolkit.sleep_constant)
            return
        
##--------------------start-of-edit_reading()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
    @staticmethod
    def edit_reading() -> None:

        """

        Edits a reading entity in the database.

        """ 

        ## gets target reading
        try:
            target_reading_id = int(Toolkit.user_confirm("Please enter the id of the reading you want to edit."))

            ## get target reading
            try:
                target_reading = Searcher.get_reading_from_id(target_reading_id)

            except Searcher.IDNotFoundError:
                print("Reading not found.\n")
                time.sleep(Toolkit.sleep_constant)
                return
            
            message_to_print = "Please enter the new romaji for " + target_reading.romaji_value + ". (Romaji is the pronunciation of the testing material)."

            new_romaji = Toolkit.user_confirm(message_to_print)

            message_to_print = "Please enter the new furigana for " + target_reading.furigana_value + ". (Furigana is the kana spelling of the romaji)."

            new_furigana = Toolkit.user_confirm(message_to_print)            

            ## edit value in current session
            target_reading.romaji_value = new_romaji
            target_reading.furigana_value = new_furigana

            ## edit value in persistent storage
            target_reading_line = FileHandler.find_seisen_line(FileEnsurer.vocab_readings_path, column_index=2, target_value=target_reading_id)
            FileHandler.edit_seisen_line(FileEnsurer.vocab_readings_path, target_reading_line, column_number=3, value_to_replace_to=new_furigana)
            FileHandler.edit_seisen_line(FileEnsurer.vocab_readings_path, target_reading_line, column_number=4, value_to_replace_to=new_romaji)

        except Toolkit.UserCancelError:
            print("\nCancelled.\n")
            time.sleep(Toolkit.sleep_constant)
            return
        
##--------------------start-of-edit_typo()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
    @staticmethod
    def edit_typo() -> None:

        """

        Edits a typo entity in the database.

        """ 

        ## gets target typo
        try:
            target_typo_id = int(Toolkit.user_confirm("Please enter the id of the typo you want to edit."))

            ## get target typo
            try:
                target_typo = Searcher.get_typo_from_id(target_typo_id)

            except Searcher.IDNotFoundError:
                print("Typo not found.\n")
                time.sleep(Toolkit.sleep_constant)
                return
            
            message_to_print = "Please enter the new typo for " + target_typo.typo_value + ". (Typo is the incorrect spelling of the testing material)."

            new_value = Toolkit.user_confirm(message_to_print)

            ## edit value in current session
            target_typo.typo_value = new_value

            ## edit value in persistent storage
            target_typo_line = FileHandler.find_seisen_line(FileEnsurer.vocab_typos_path, column_index=2, target_value=target_typo_id)
            FileHandler.edit_seisen_line(FileEnsurer.vocab_typos_path, target_typo_line, column_number=3, value_to_replace_to=new_value)

        except Toolkit.UserCancelError:
            print("\nCancelled.\n")
            time.sleep(Toolkit.sleep_constant)
            return
        
##--------------------start-of-edit_incorrect_typo()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
    @staticmethod
    def edit_incorrect_typo() -> None:

        """

        Edits an incorrect typo entity in the database.

        """ 

        ## gets target incorrect typo
        try:
            target_incorrect_typo_id = int(Toolkit.user_confirm("Please enter the id of the incorrect typo you want to edit."))

            ## get target incorrect typo
            try:
                target_incorrect_typo = Searcher.get_incorrect_typo_from_id(target_incorrect_typo_id)

            except Searcher.IDNotFoundError:
                print("Incorrect Typo not found.\n")
                time.sleep(Toolkit.sleep_constant)
                return
            
            message_to_print = "Please enter the new incorrect typo for " + target_incorrect_typo.incorrect_typo_value + ". (Incorrect Typo is the incorrect spelling of the testing material that is counted as incorrect)."

            new_value = Toolkit.user_confirm(message_to_print)

            ## edit value in current session
            target_incorrect_typo.incorrect_typo_value = new_value

            ## edit value in persistent storage
            target_incorrect_typo_line = FileHandler.find_seisen_line(FileEnsurer.vocab_incorrect_typos_path, column_index=2, target_value=target_incorrect_typo_id)
            FileHandler.edit_seisen_line(FileEnsurer.vocab_incorrect_typos_path, target_incorrect_typo_line, column_number=3, value_to_replace_to=new_value)

        except Toolkit.UserCancelError:
            print("\nCancelled.\n")
            time.sleep(Toolkit.sleep_constant)
            return
        
##--------------------start-of-delete_vocab()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
    @staticmethod
    def delete_vocab() -> None:

        """

        Deletes a vocab entity from the database.

        """ 

        ## gets target vocab
        try:
            target_vocab_id = int(Toolkit.user_confirm("Please enter the id of the vocab you want to delete."))

            ## get target vocab
            try:
                target_vocab = Searcher.get_vocab_from_id(target_vocab_id)

            except Searcher.IDNotFoundError:
                print("Vocab not found.\n")
                time.sleep(Toolkit.sleep_constant)
                return
            
            print_item = Searcher.get_vocab_print_item_from_id(target_vocab_id)

            print(print_item)

            if(input("\nEnter 1 if you are sure you want to delete, otherwise enter 2.\n") == "1"):
                pass
            
            else:
                print("\nCancelled.\n")
                time.sleep(Toolkit.sleep_constant)
                return

            ## delete vocab from current session
            LocalHandler.vocab.remove(target_vocab)

            ## delete vocab from persistent storage
            FileHandler.delete_all_occurrences_of_id(FileEnsurer.vocab_path, id_index=1, target_id=target_vocab_id)
            FileHandler.delete_all_occurrences_of_id(FileEnsurer.vocab_testing_material_path, id_index=1, target_id=target_vocab_id)
            FileHandler.delete_all_occurrences_of_id(FileEnsurer.vocab_synonyms_path, id_index=1, target_id=target_vocab_id)
            FileHandler.delete_all_occurrences_of_id(FileEnsurer.vocab_readings_path, id_index=1, target_id=target_vocab_id)
            FileHandler.delete_all_occurrences_of_id(FileEnsurer.vocab_typos_path, id_index=1, target_id=target_vocab_id)
            FileHandler.delete_all_occurrences_of_id(FileEnsurer.vocab_incorrect_typos_path, id_index=1, target_id=target_vocab_id)
            
        except Toolkit.UserCancelError:
            print("\nCancelled.\n")
            time.sleep(Toolkit.sleep_constant)
            return
        
##--------------------start-of-delete_synonym()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
    @staticmethod
    def delete_synonym() -> None:

        """

        Deletes a synonym entity from the database.

        """ 

        ## gets target synonym
        try:
            target_synonym_id = int(Toolkit.user_confirm("Please enter the id of the synonym you want to delete."))

            ## get target synonym
            try:
                target_synonym = Searcher.get_synonym_from_id(target_synonym_id)

            except Searcher.IDNotFoundError:
                print("Synonym not found.\n")
                time.sleep(Toolkit.sleep_constant)
                return
            
            print_item = Searcher.get_synonym_print_item_from_id(target_synonym_id)

            print(print_item)

            if(input("\nEnter 1 if you are sure you want to delete, otherwise enter 2.\n") == "1"):
                pass
            
            else:
                print("\nCancelled.\n")
                time.sleep(Toolkit.sleep_constant)
                return
            
            ## obtain vocab that contains synonym
            target_vocab = Searcher.get_overlying_vocab_from_synonym_id(target_synonym_id)

            ### check to ensure that the user is not deleting the only synonym for a vocab
            if(len(target_vocab.testing_material_answer_all) == 1):
                print("You cannot delete the only synonym for a vocab.\n")
                Toolkit.pause_console()
                return
            
            ## check to ensure that the user is not deleting the main synonym for a vocab, if so, change the main synonym to the next synonym
            if(target_vocab.testing_material_answer_main.synonym_id == target_synonym_id):
                target_vocab.testing_material_answer_main = target_vocab.testing_material_answer_all[1]

            ## delete synonym from current session
            target_vocab.testing_material_answer_all.remove(target_synonym)

            ## delete synonym from persistent storage
            FileHandler.delete_all_occurrences_of_id(FileEnsurer.vocab_synonyms_path, id_index=2, target_id=target_synonym_id)
            
        except Toolkit.UserCancelError:
            print("\nCancelled.\n")
            time.sleep(Toolkit.sleep_constant)
            return