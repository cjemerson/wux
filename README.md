# wux
Web Crawling Exercise in Python

## Intro
The script `wux.py` uses a "config.txt" to determine and record the latest Web Novel Chapter. The Web Novel's HTML address may have a book, chapter and part but must have a numerical address. (The HTML address cannot have the chapter's title in it or anything which differs per chapter.) The name wux comes from WuxiaWorld, one of my favorite Web Novel sites.

## Config
The "config.txt" must have a formatted address with '@' for book number, '%' for chapter number, and '!' for part number. Since the script also records the latest book, chapter, and part, include 1's separated by space for each book, chapter, and/or part. Any line with a '#' will be ignored and regarded as a comment.

## Author Notes
The script uses an exponential stride at first to quickly traverse any Web Novels which have a large number of chapters. The stride increases by a factor of 2 upon successful access of an existing chapter. After an unsuccessful access the stride is halved and halved again upon success in the next iteration.

## Known Bugs
This script ignores the possibility of a Chapter 0.
