# wux - Web Crawling Exercise in Python
Charles "CJ" Emerson

## Intro
TL;DR:
 - `wux.py` can quickly determine the highest web address that uses sequential numbering.
 - `wux_records.py` can open sequential web pages in your web browser and then store the sequence as a record.

There are two scripts, `wux.py` and `wux_records.py`. The first (as a standalone) is a script to determine the most recent Web Novel chapter since it was last run (which is stored in `config.txt`). The second uses the first as a module to act as a reading manager (which uses `wux_save.txt`).

The name ***wux*** comes from WuxiaWorld, one of my favorite Web Novel sites.

## wux.py
The script `wux.py` is intended to determine the most recent Web Novel chapter. However, the script can be easily modified to identify the most recent web post. The only real requirement is that the HTML address does not have a title or anything which differs per post. The script uses a "config.txt" to determine and record the latest Web Novel Chapter.

## wux_records.py
The script `wux_records.py` is intended to act as a reading manager. By using the script to manage your Web Novels you can quickly check to see if any of your web novels have an update.

**TO SETUP WUX_RECORDS.PY YOU NEED TO SPECIFY A BROWSER**. On my machine, Python's `webbrowser` module loaded empty. As a workaround, I had to add my web browser to the system PATH and call via the command line. You can use whatever method you want to open a web browser, simply change the very first function `openWebPage(htmlAddress)` in `wux_records.py`.

## Config
The `config.txt` must have a formatted address with '@' for volume number, book number, chapter number, part number, etc. The '@' will be replaced from left to right as major to minor section numbers (part number cannot come before volume number). If there is only a formatted address, the script defaults to 1 for each '@'. Additionally, any line with a '#' in it will be regarded as a comment and ignored. An example "config.txt" is included in the repository.

## Author Notes
The script `wux.py` uses an exponential stride to quickly traverse any Web Novels which have a large number of chapters. The stride increases by a factor of 2 upon successful access of an existing chapter. After an unsuccessful access, every following stride is halved.

## Known Bugs
This script ignores the possibility of a Chapter 0 (same for book, section, part, etc.). In some cases, this actually prevents the user from seeing the most recent chapter.

## Future Plans
It would be nice if the user could specify that a value might be zero. Future plans are to allow allow '$' in place of '@' to mean the space might be zero.
