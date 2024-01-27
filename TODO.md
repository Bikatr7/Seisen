~~Vocab Setting Design (searcher to be refactored alongside):~~
~~Likely Going to need to structure into Add/Edit/Delete due to constraint of 9 options per prompt:~~

~~So:~~

~~first menu would be~~

1. ~~Add Entity~~
2. ~~Edit Entity~~
3. ~~Delete Entity~~
4. ~~Search Entity~~

For add we'd need:
1. ~~Add Vocab~~
2. ~~Add Synonym To Vocab~~
3. ~~Add TestingMaterial To Vocab~~
4. ~~Add Reading To Vocab~~
5. ~~Add Typo To Vocab~~
6. ~~Add IncorrectTypo To Vocab~~

For Edit we'd need:
1. ~~Edit Vocab~~
2. ~~Edit Synonym For Vocab~~
3. ~~Edit TestingMaterial For Vocab~~
4. ~~Edit Reading For Vocab~~
5. ~~Edit Typo For Vocab~~
6. ~~Edit IncorrectTypo For Vocab~~

For Delete we'd need:
1. ~~Delete Vocab~~
2. ~~Delete Synonym From Vocab~~
3. ~~Delete TestingMaterial From Vocab~~
4. ~~Delete Reading From Vocab~~
5. ~~Delete Typo From Vocab~~
6. ~~Delete IncorrectTypo From Vocab~~

Constraints:
1. ~~Vocab must have at least one reading, one testing material, and one synonym at creation.~~
2. ~~When you delete a vocab, you must delete all readings, testing materials, synonyms, typos, and incorrect typos associated with it.~~
3. ~~You cannot delete a reading, testing material, or synonym if it is the only one associated with a vocab.~~
4. ~~If deleting the main something (vocab, reading, testing material, synonym) you must select a new main something to replace it with.~~

~~for get_underlying_vocab_from_synonym_id, change it to be more generic, and have it provide a literal of what type of id we are using to find the underlying vocab.~~

~~Then we can just have a search function.~~

~~For the search function we'd need:~~
~~an auto replace for when user is searching characters that have "- in it to replace to the japanese one "ー"~~
~~Need to auto correct hyphens to the japanese one "ー" for japanese entries but correct japanese one to hyphen for english entries~~

~~Searcher needs to be refactored to not require each search to have an assert, and incorporate more exception throwing.~~

~~Have a new entity class and have all entities inherit it, should just have an id. Then we can unify all that buillshit~~

~~Rename entity vars since they kinda suck, also make default main values for word/vocab core classes~~

-----------------------------------------------------------------------------------------------------------------
Tasks above are to be implemented in (full-refactor of searcher and vocab_settings_handler) branch
-----------------------------------------------------------------------------------------------------------------

Need to add a way to allow user to see additional readings and testing material, likely via a keybind

implement 'b' functionality for kana testing

## Things to look into
Getting rid of the requests requirement? Could be easy just to handle it myself.

Properly test what happens if mysql.connector-python isn't installed, and add countermeasures to ensure Seisen can function without it.

## Backlog
Redo All Documentation

Add confirmations to a lot of core decisions, something old me liked to do was not tell you what was happening???

Make logging better

REFACTOR ALL CODE, LIKE LITERALLY EVERYTHING

Refactor number choice words to have literals instead of numbers cause that's fucking stupid

## Things I'd like to add eventually
Look into using spacy to get root verbs and force things into it, could add a conjugation mode

Add a phrase class, for phrases that the user can add to the deck

Look into building a jisho query option into it

Look into gradio implementation

Look into using OpenAi to generate sentences for the user to translate
