## Important
Likely to grow and expand overtime.

## Next (Breakdown of word/vocab classes and large architecture changes)
Break core word definitions into multiple classes, due to the way Japanese is absolute bullshit, we need to account for multiple different kanji, romaji, and furigana readings.
So like with how Alternative answers, and typos are built into Synonyms, and Typo classes respectively, we need to do the same with the core word definitions.
Likely being
> testing_material (basically the kanji writing): If it has multiple kanji, we need to account for this and have a class for it, will likely be structured the same way synonyms are.

> romaji: Same as above, need to account for multiple romaji readings

> furigana: Same as above, need to account for multiple furigana readings

They have to exist independently of each other cause the number of testing_material, romaji, and furigana readings for a vocab/word will not always be the same, and we need to account for this.

This will necessitate three new classes and three new file collections, which while doesn't seem a lot, is a LOT of fucking work and I'll have to redo all of remote again (and fucking with sql is annoying).

With the new word class basically just being
> word_id

> testing_material_answer_main

> incorrect_count

> correct_count

> likelihood

if you exclude the other classes we need (can throw on is_kanji for vocab class)


## Architecture
word_type needs to be fucking removed and extinguished. It's a vestigial part of the codebase that I somehow let remain back when i wanted to put everything into one file (lmao no)
since spaces and other shit keep getting added to the timestamp files, we can just start deleting them instead lol

## Things to look into
Searcher refactor? Not really liking how it's implemented currently
Getting rid of the requests requirement? Could be easy just to handle it myself.
Properly test what happens if mysql.connector-python isn't installed, and add countermeasures to ensure Seisen can function without it.

## New features I'd like to add eventually
A way to force kana reading to show if another vocab with the same kanji reading is in the deck (Likely gonna be annoying as hell once we add different readings)
Look into bundling a JMdict/EDICT with Seisen to allow easy force to root verb
Look into building a jisho query option into it

## Backlog
Redo All Documentation

Add confirmations to a lot of core decisions, something old me liked to do was not tell you what was happening???

Make logging better

REFACTOR ALL CODE, LIKE LITERALLY EVERYTHING

## After done
Make a deck converter to whatever the new decks end up looking like, cause I have thousands of words that I am *not* redoing lol.
