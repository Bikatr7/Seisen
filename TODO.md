## Important
Likely to grow and expand overtime.

## Next (Breakdown of word/vocab classes and large architecture changes)
~~Break core word definitions into multiple classes, due to the way Japanese is absolute bullshit, we need to account for multiple different kanji, romaji, and furigana readings.~~
~~So like with how Alternative answers, and typos are built into Synonyms, and Typo classes respectively, we need to do the same with the core word definitions.~~
~~Likely being:~~
> ~~testing_material (basically the kanji writing): If it has multiple kanji, we need to account for this and have a class for it, will likely be structured the same way synonyms are.~~

> ~~romaji: Same as above, need to account for multiple romaji readings~~

> ~~furigana: Same as above, need to account for multiple furigana readings~~

~~They have to exist independently of each other cause the number of testing_material, romaji, and furigana readings for a vocab/word will not always be the same, and we need to account for this.~~

~~This will necessitate two new classes and two new file collections, which while doesn't seem a lot, is a LOT of fucking work and I'll have to redo all of remote again (and fucking with sql is annoying).~~

~~Gonna combine furigana and romaji into one class called reading~~

~~With the new word class basically just being~~
> ~~word_id~~

> ~~testing_material_answer_main~~

> ~~incorrect_count~~

> ~~correct_count~~

> ~~likelihood~~


## Architecture
~~word_type needs to be fucking removed and extinguished. It's a vestigial part of the codebase that I somehow let remain back when i wanted to put everything into one file (lmao no)~~

~~Need to update file architecture to fit with new entity architecture~~

~~Change an absent furigana value to no longer exist, all kana/vocab will have a furigana and we can just filter these out later by comparing if the furigana matches the testing material itself~~

~~since spaces and other shit keep getting added to the timestamp files, we can just start deleting them instead lol~~

Add a default testing_material, likely just the first index of all testing material

Need to add a way to allow user to see additional readings and testing material, likely via a keybind

implement 'b' functionality for kana testing

remote archive creation seems broken

need to make kana/vocab testing work properly

-----------------------------------------------------------------------------------------------------------------
Tasks above are to be implemented in Breakdown-of-word/vocab-classes-and-large-architecture-changes
-----------------------------------------------------------------------------------------------------------------

## Things to after the above branch
vocab settings need to be redone
Refactor searcher and vocab_settings_handler to fit with new architecture
add a auto replace for when user is searching characters that have "- in it to replace to the japanese one "ー"

## Things to look into
Getting rid of the requests requirement? Could be easy just to handle it myself.
Properly test what happens if mysql.connector-python isn't installed, and add countermeasures to ensure Seisen can function without it.

## Backlog
Redo All Documentation

Add confirmations to a lot of core decisions, something old me liked to do was not tell you what was happening???

Make logging better

REFACTOR ALL CODE, LIKE LITERALLY EVERYTHING

## After done
Make a deck converter to whatever the new decks end up looking like, cause I have thousands of words that I am *not* redoing lol.

## New features I'd like to add eventually
A way to force kana reading to show if another vocab with the same kanji reading is in the deck (Likely gonna be annoying as hell once we add different readings)
Look into using spacy to get root verbs and force things into it
Add a phrase class, for phrases that the user can add to the deck
Look into building a jisho query option into it
Look into gradio implementation
Look into using OpenAi to generate sentences for the user to translate