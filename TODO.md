## Things to after the above branch
Refactor searcher and vocab_settings_handler to fit with new architecture

Add a auto replace for when user is searching characters that have "- in it to replace to the japanese one "ー"

Need to add a way to allow user to see additional readings and testing material, likely via a keybind

implement 'b' functionality for kana testing

-----------------------------------------------------------------------------------------------------------------
Tasks above are to be implemented in (full-refactor of searcher and vocab_settings_handler) branch
-----------------------------------------------------------------------------------------------------------------

## Things to look into
Getting rid of the requests requirement? Could be easy just to handle it myself.

Properly test what happens if mysql.connector-python isn't installed, and add countermeasures to ensure Seisen can function without it.

## Backlog
Redo All Documentation

Add confirmations to a lot of core decisions, something old me liked to do was not tell you what was happening???

Make logging better

REFACTOR ALL CODE, LIKE LITERALLY EVERYTHING

## Things I'd like to add eventually
Look into using spacy to get root verbs and force things into it, could add a conjugation mode

Add a phrase class, for phrases that the user can add to the deck

Look into building a jisho query option into it

Look into gradio implementation

Look into using OpenAi to generate sentences for the user to translate
