## Important
Likely to grow and expand overtime.

## Immediate
Ensurer functionality of all current features, do not worry about new features. If old architecture is preventing functionality, move to backlog.

## Soon
Database sanitization has been practically solved by using parameterized queries, but we still need to deal with .seisen files having commas written to them, which would be like super bad. So we need to sanitize the input of the .seisen files, should be fine just to do commas and replace them to a literal or so, perhaps literally just "comma" or something. 

## Something I know I need to do but like nowhere near there yet
Break core word definitions into multiple classes, due to the way Japanese is absolute bullshit, we need to account for multiple different kanji, romaji, and furigana readings.
So like with how Alternative answers, and typos are built into Synonyms, and Typo classes respectively, we need to do the same with the core word definitions.
Likely being
> testing_material (basically the kanji writing): If it has multiple kanji, we need to account for this and have a class for it, will likely be structured the same way synonyms are.

> romaji: Same as above, need to account for multiple romaji readings

> furigana: Same as above, need to account for multiple furigana readings

This was necessitate three new classes and three new file collections, which while doesn't seem a lot, is a LOT of fucking work and I'll have to redo all of remote again (and fucking with sql is annoying).

With the new word class basically just being
> word_id

> testing_material_answer_main

> incorrect_count

> correct_count

> likelihood

if you exclude the other classes we need (can throw on is_kanji for vocab class)


## Architecture
word_type needs to be fucking removed and extinguished. It's a vestigial part of the codebase that I somehow let remain back when i wanted to put everything into one file (lmao no)

## New features I'd like to add eventually
A way to force kana reading to show if another vocab with the same kanji reading is in the deck (Likely gonna be annoying as hell once we add different readings)

## Backlog
Redo All Documentation

Add confirmations to a lot of core decisions, something old me liked to do was not tell you what was happening???

REFACTOR ALL CODE, LIKE LITERALLY EVERYTHING

## After done
Make a deck converter to whatever the new decks end up looking like, cause I have thousands of words that I am *not* redoing lol.
