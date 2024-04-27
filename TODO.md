## Overall cleaning
A lot of stuff needs to be refactored and trimmed down, especially seisen.py and storage_settings_handler.py

## Related to romaji
need to add it to where romaji typos can get saved
need to clean up a lot of code regarding that
for the typos, we'd need a way to differentiate synonym typos vs reading typos
make it to where if it's asking for a reading, and you answer a synonym, it'll let you try again and vice versa

## Things that will get added eventually (maybe)
Look into using spacy to get root verbs and force things into it, could add a conjugation mode

Add a phrase class, for phrases that the user can add to the deck

Look into building a jisho query option into it

Look into gradio implementation

Look into using OpenAi to generate sentences for the user to translate

## The "I can't be fucking bothered to do this anytime soon list"
Perfect Logging