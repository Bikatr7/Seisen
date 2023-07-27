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

from modules import util

##--------------------start-of-reset_storage()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def reset_storage(local_handler:localHandler, remote_handler:remoteHandler) -> typing.Tuple[localHandler, remoteHandler]:
        
        """"
        
        Resets storage, either local with remote or remote with local.\n
        Will do nothing if no database connection is available.\n

        Parameters:\n
        local_handler (object - localHandler) : the local handler.\n
        remote_handler (object - remoteHandler) : the remote handler.\n

        Returns:\n
        local_handler (object - localHandler) : the altered local handler.\n
        remote_handler (object - remoteHandler) : the altered remote handler.\n


        """

        util.clear_console()

        reset_message = "How are you resetting storage?\n\n1.Reset Local With Remote\n2.Reset Remote with Local\n3.Reset Local & Remote to Default\n"

        print(reset_message)

        type_reset = util.input_check(4, str(msvcrt.getch().decode()), 3, reset_message)

        if(type_reset == "1"):
        
            with open(remote_handler.last_local_remote_backup_accurate_path, 'r', encoding="utf-8") as file:
                last_backup_date = str(file.read().strip()).strip('\x00').strip()

            if(input("Warning, remote storage has not been updated since " + last_backup_date + ", all changes made to local storage after this will be lost. Are you sure you wish to continue? (1 for yes 2 for no) ") == "1"):
                remote_handler.reset_local_storage()
                local_handler.load_words_from_local_storage()
            else:
                pass

        elif(type_reset == "2"):

            remote_handler.reset_remote_storage()
        
        elif(type_reset == "3"):
            
            shutil.rmtree(local_handler.fileEnsurer.kana_dir)
            shutil.rmtree(local_handler.fileEnsurer.vocab_dir)

            local_handler.fileEnsurer.ensure_files(local_handler.logger)

            remote_handler.reset_remote_storage()

            local_handler.load_words_from_local_storage()

        return local_handler, remote_handler

##--------------------start-of-print_score_ratings()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def print_score_ratings(word_rater:scoreRate, local_handler:localHandler) -> None:
        
        """
        
        Prints score ratings for either kana or vocab.\n

        Parameters:\n
        word_rater (object - scoreRate) : the scoreRate object.\n
        local_handler (object - localHandler) : the localHandler object.\n

        Returns:\n
        None.\n
        
        """
        
        util.clear_console()

        score_message = "1.Kana\n2.Vocab\n"

        print(score_message)

        type_print = util.input_check(4, str(msvcrt.getch().decode()), 2, score_message)

        if(type_print == "1"):
            kana_to_test, display_list = word_rater.get_kana_to_test(local_handler.kana)
        elif(type_print == "2"):
            vocab_to_test, display_list = word_rater.get_vocab_to_test(local_handler.vocab)
        else:
            return
        
        for item in display_list:
            print(item)

        util.pause_console()

##--------------------start-of-set_up_new_database()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def set_up_new_database(remote_handler:remoteHandler) -> remoteHandler:

    """
    
    Unlinks the current database and causes the remote handler to prompt for a new database.\n

    Para

    """

    ## causes the remoteHandler to attempt a database connection upon next startup
    remote_handler.start_marked_succeeded_database_connection()
    
    ## clears the credentials file
    remote_handler.clear_credentials_file()

    ## creates a new handler
    new_handler = remoteHandler(remote_handler.fileEnsurer, remote_handler.logger)

    new_handler.logger.log_action("Remote Handler has been reset...")

    return new_handler

##--------------------start-of-restore_backup()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def restore_backup(local_handler:localHandler, remote_handler:remoteHandler) -> typing.Tuple[localHandler, remoteHandler]:
            
    """

    Restores a local or remote backup.\n

    Parameters:\n
    local_handler (object - localHandler) : the local handler object.\n
    remote_handler (object - remoteHandler) : the remote handler object.\n

    Returns:\n
    local_handler (object - localHandler) : the altered local handler object.\n
    remote_handler (object - remoteHandler) : the altered remote handler object.\n
    
    """  

    util.clear_console()

    backup_message = "Which backup do you wish to restore?\n\n1.Local\n2.Remote\n"

    print(backup_message)

    type_backup = util.input_check(4, str(msvcrt.getch().decode()), 2, backup_message)

    if(type_backup == "1"):

        local_handler.restore_local_backup()
        local_handler.fileEnsurer.ensure_files(local_handler.logger)
        local_handler.load_words_from_local_storage()

    elif(type_backup == "2"):

        remote_handler.restore_remote_backup()
        local_handler.fileEnsurer.ensure_files(local_handler.logger)
        local_handler.load_words_from_local_storage()

    return local_handler, remote_handler

##--------------------start-of-vocab_settings()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def vocab_settings(local_handler:localHandler) -> localHandler:

    """

    Controls the pathing for all vocab settings as they can get very long and crowded if shoved into one function.\n

    Parameters:\n
    local_handler (object- localHandler) : the local handler.\n

    Returns:\n
    local_handler (object - localHandler) : the altered local handler.\n

    """ 

    vocab_message = "What are you trying to do?\n\n1.Add Vocab\n2.Add CSEP/Answer to Vocab\n"

    print(vocab_message)

    type_setting = util.input_check(4, str(msvcrt.getch().decode()), 2, vocab_message)

    if(type_setting == "1"):
        local_handler = add_vocab(local_handler)
    elif(type_setting == "2"):
        local_handler = add_csep(local_handler)

    return local_handler

##--------------------start-of-add_vocab()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def add_vocab(local_handler:localHandler) -> localHandler:
     
    """
    
    Adds a user entered vocab to the local handler.\n

    Parameters:\n
    local_handler (object - localHandler) : the local handler.\n

    Returns:\n
    local_handler (object - localHandler) : the altered local handler.n

    """

    new_vocab_id = util.get_new_id(local_handler.get_list_of_all_ids(5))
    new_csep_id = util.get_new_id(local_handler.get_list_of_all_ids(6))

    csep_value_list = []
    csep_actual_list_write = []
    csep_actual_list_handler = []

    furigana = "0"
    isKanji = False

    try:
        testing_material = util.user_confirm("Please enter a vocab term")
        romaji = util.user_confirm("Please enter " + testing_material + "'s romaji/pronunciation")
        definition = util.user_confirm("Please enter " + testing_material + "'s definition/main answer")

        csep_value_list.append(definition)

        while(input("Enter 1 if " + testing_material + " has any additional answers :\n") == "1"):
            util.clear_stream()
            csep_value_list.append(util.user_confirm("Please enter " + testing_material + "'s additional answers"))

        for character in testing_material:
            if(character not in local_handler.kana):
                local_handler.logger.log_action(character + " is kanji")
                furigana = util.user_confirm("Please enter " + testing_material + "'s furigana/kana spelling")
                isKanji = True
                break
    
    except:
        return local_handler


    for csep_value in csep_value_list:
        csep_insert_values = [new_vocab_id, new_csep_id, csep_value, local_handler.VOCAB_WORD_TYPE]
        
        csep_actual_list_handler.append(csep_blueprint(new_vocab_id, new_csep_id, csep_value, local_handler.VOCAB_WORD_TYPE))

        util.write_sei_line(local_handler.vocab_csep_path, csep_insert_values)

        new_csep_id = util.get_new_id(local_handler.get_list_of_all_ids(6))

    vocab_insert_values = [new_vocab_id, testing_material, romaji, definition, furigana, 0, 0, isKanji]
    local_handler.vocab.append(vocab_blueprint(new_vocab_id, testing_material, romaji, definition, csep_actual_list_handler, furigana, 0, 0, isKanji))

    util.write_sei_line(local_handler.vocab_path, vocab_insert_values)

    return local_handler

##--------------------start-of-add_csep()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def add_csep(local_handler:localHandler) -> localHandler:

    """
    
    Adds a user entered csep to an existing vocab in the local handler.\n

    Parameters:\n
    local_handler (object - localHandler) : the local handler.\n

    Returns:\n
    local_handler (object - localHandler) : the altered local handler.n

    """

    vocab_term = ""
    vocab_id = 0

    target_index = 0

    new_csep_id = util.get_new_id(local_handler.get_list_of_all_ids(6))

    try:
        vocab_term_or_id = util.user_confirm("Please enter the vocab or vocab id that you want to add a csep/answer to.")

    except:
        return local_handler
    
    if(vocab_term_or_id.isdigit() == True):
        vocab_id = int(vocab_term_or_id)
        vocab_term = local_handler.searcher.get_term_from_id(local_handler, vocab_id) 
    else:
        vocab_term = vocab_term_or_id
        vocab_id = local_handler.searcher.get_id_from_term(local_handler, vocab_term)

    try:

        print(vocab_term)
        print(vocab_id)

        util.pause_console()

        assert vocab_term != "-1"
        assert vocab_id != -1

        csep_value = util.user_confirm("Please enter the csep/answer for " + vocab_term + " you would like to add.")

    except AssertionError:
        local_handler.logger.log_action("Invalid id or term.")
        print("invalid id or term\n")
        time.sleep(1)
        return local_handler
    
    except util.UserCancelError:
        return local_handler
    
    for i, vocab in enumerate(local_handler.vocab):
        if(vocab.word_id == vocab_id):
            target_index = i

    csep_insert_values = [vocab_id, new_csep_id, csep_value, local_handler.VOCAB_WORD_TYPE]
    util.write_sei_line(local_handler.vocab_csep_path, csep_insert_values)
    
    new_csep = csep_blueprint(int(vocab_id), new_csep_id, csep_value, local_handler.VOCAB_WORD_TYPE)
    local_handler.vocab[target_index].testing_material_answer_all.append(new_csep)

    return local_handler