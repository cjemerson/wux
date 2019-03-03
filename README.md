# wux - Web Crawling Exercise in Python
Charles "CJ" Emerson

## Intro
The script `wux.py` is intended to determine the most recent Web Novel chapter. However, the script can be easily modified to identify the most recent web post. The only real requirement is that the HTML address does not have a title or anything which differs per post.

The script uses a "config.txt" to determine and record the latest Web Novel Chapter. The name ***wux*** comes from WuxiaWorld, one of my favorite Web Novel sites.

## Config
The "config.txt" must have a formatted address with '@' for volume number, book number, chapter number, part number, etc. The '@' will be replaced from left to right as major to minor section numbers (part number cannot come before volume number). If there is only a formatted address, the script defaults to 1 for each '@'. Additionally, any line with a '#' in it will be regarded as a comment and ignored. An example "config.txt" is included in the repository.

## Author Notes
The script uses an exponential stride to quickly traverse any Web Novels which have a large number of chapters. The stride increases by a factor of 2 upon successful access of an existing chapter. After an unsuccessful access, every following stride is halved.

## Known Bugs
This script ignores the possibility of a Chapter 0 (same for book, section, part, etc.).
