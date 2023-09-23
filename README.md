---------------------------------------------------------------------------------------------------------------------------------------------------
**Table of Contents**

- [Notes](#notes)
- [Dependencies](#dependencies)
- [Quick Start](#quickstart)
- [Settings Menu](#settings)
- [Vocab Settings](#vocab-settings)
- [Storage Settings](#storage-settings)
- [Setting Up A MySQL Database](#SUAMSD)
- [License](#license)
- [Contact](#contact)

---------------------------------------------------------------------------------------------------------------------------------------------------

## DEVELOPMENT IS PAUSED UNTIL OCTOBER 2023 (Outside of critical bug fixes)

---------------------------------------------------------------------------------------------------------------------------------------------------
**Notes**<a name="notes"></a>

Built for Windows, Should work on Linux/MacOS but is untested.

Python Version: 3.8+

Tests the user on Japanese Kana and Vocabulary.

---------------------------------------------------------------------------------------------------------------------------------------------------
**Dependencies**<a name="dependencies"></a>

mysql.connector-python

requests

or see requirements.txt

---------------------------------------------------------------------------------------------------------------------------------------------------
**Quick Start**<a name="quickstart"></a>

Run seisen.py

Upon opening the file, you will be prompted to enter database credentials, if you have these go ahead and enter these, otherwise enter z to skip.

Once at the main menu, press 1 and begin to quiz yourself on kana or 2 to quiz yourself on vocab.

All Japanese Kana and 7 Vocab words are included by default. You can add more vocab in the settings menu.

---------------------------------------------------------------------------------------------------------------------------------------------------
**Settings Menu**<a name="settings"></a>

pressing 3 will enter the settings menu. The settings are as follows:

1. Vocab Settings - Enters vocab settings
2. Storage Settings - Enters storage settings
3. See Score Ratings - this will print the likelihood of each kana/vocab being tested.
4. Set Up New Database - - this will cause Seisen to prompt for a new database.
   
---------------------------------------------------------------------------------------------------------------------------------------------------
**Vocab Settings**<a name="vocab-settings"></a>

Vocab Settings are as follows:

1. Add Vocab - Adds a custom vocab to the testing deck
2. Add CSEP/Answer to Vocab - Adds a answer (CSEP) to an existing vocab
3. Replace Vocab Value - Edits a vocab value
4. Replace CSEP/Answer - Edits a CSEP/Answer
5. Delete Vocab Value - Deletes a vocab value
6. Delete CSEP/Answer - Deletes a CSEP/Answer from a vocab
7. Search Vocab - Searches for a vocab, given a term (can be numeric, alphabetic, or japanese)

---------------------------------------------------------------------------------------------------------------------------------------------------
**Storage Settings**<a name="storage-settings"></a>

1. Reset Local with Remote - Resets Local Storage with the Database (will do nothing if no connection)
2. Reset Remote with Local - Resets Remote Storage with the Local Storage (will do nothing if no connection)
3. Reset Local & Remote to Default - Resets all storage to default settings (remote will be unaffected if no connection)
4. Restore Backup - Prompts the user to restore either a local or remote backup
5. Export Vocab Deck - Exports the vocab deck to a .seisen file that can be imported by another user or yourself later
6. Import Vocab Deck - Imports a .seisen file that was exported by Seisen into the current deck (replaces current deck)

---------------------------------------------------------------------------------------------------------------------------------------------------
**Setting Up A MySQL Database**<a name="SUAMSD"></a>

Seisen uses a backup data method using MySQL, once Seisen is opened for the first time it will prompt for A database name and password, if you have these already feel free to enter these and Seisen will take care of the rest.

If not, you can always set this up latter in settings by typing 3 and then press 4.

---------------------------------------------------------------------------------------------------------------------------------------------------
**License**<a name="license"></a>

This project (Seisen) is licensed under the GNU General Public License (GPL). You can find the full text of the license in the [LICENSE](License.md) file.

The GPL is a copyleft license that promotes the principles of open-source software. It ensures that any derivative works based on this project must also be distributed under the same GPL license. This license grants you the freedom to use, modify, and distribute the software.

Please note that this information is a brief summary of the GPL. For a detailed understanding of your rights and obligations under this license, please refer to the full license text.

---------------------------------------------------------------------------------------------------------------------------------------------------
**Contact**<a name="contact"></a>

If you have any questions, comments, or concerns, please feel free to contact me at [Tetralon07@gmail.com](mailto:Tetralon07@gmail.com).

For any bugs or suggestions please use this issues tab [here](https://github.com/Bikatr7/Seisen/issues).

---------------------------------------------------------------------------------------------------------------------------------------------------
