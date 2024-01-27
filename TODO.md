Add permission error handling to all file operations

Refactor number choice words to have literals instead of numbers cause that's fucking stupid

User_confirm needs to be refactored as well to lesson the confusion for instructions

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
