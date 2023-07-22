## built-in modules
import typing
import msvcrt

## custom modules
from modules.localHandler import localHandler
from modules.remoteHandler import remoteHandler

from modules.scoreRate import scoreRate

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

        reset_message = "How are you resetting storage?\n\n1.Reset Local With Remote\n2.Reset Remote with Local\n"

        print(reset_message)

        type_reset = util.input_check(4, str(msvcrt.getch().decode()), 2, reset_message)

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