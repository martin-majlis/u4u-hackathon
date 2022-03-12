# U4U Hackathon

https://ufal.mff.cuni.cz/ufal-ukraine

## Ukrainer.net

- https://ukrainer.net/
- contains texts in Czech and Ukrainian.

### Approach

1. Download pages 3 level deep from the Czech version - https://ukrainer.net/cs/
   - Initial attempt - `wget --header='Accept-Language: cs' --execute="robots = off" -r -N -l 3 --no-remove-listing --convert-links --wait=1 -R png,jpg,jpeg,css,js,webp https://ukrainer.net/cs/`
   - Try to start from themes and skip pages that has language suffix - `wget --header='Accept-Language: cs' --execute="robots = off" -r -N -l 4 --no-remove-listing --convert-links --wait=1 -R png,jpg,jpeg,css,js,webp,-de,-ja,-fr,-es https://ukrainer.net/temata/`
2. Articles has drop downs with links to the articles in different languages.
   - `(cs) Čeština`
   - `(ua) Українська`
3. We can find pages that are written in both languages with following command:
   - Command:
     ```
     while [ 1 == 1 ]; do \
     date; \
     find ukrainer.net/ -type f -exec grep -H "(ua) Українська" {} \; | sort | cut -f1 -d: > ua.txt; \
     find ukrainer.net/ -type f -exec grep -H "(cs) Čeština" {} \; | sort | cut -f1 -d: > cs.txt; \
     cat ua.txt cs.txt | sort | uniq -c | sort -nr > pages-cs-or-ua.txt; \
     wc -l pages-cs-or-ua.txt; \
     egrep '\s+2' pages-cs-or-ua.txt > pages-cs-and-ua.txt; \
     wc -l pages-cs-and-ua.txt; \
     sleep 60; \
     done;
     ```
4. Download Lindat Translation - https://github.com/ufal/lindat-translation
   - Commands:
     ```
     wget https://github.com/ufal/lindat-translation/archive/refs/heads/master.zip -O lindat_translation_master.zip
     unzip lindat_translation_master.zip
     mv lindat-translation-master lindat_translation_master
     ```
5. Install requirements - `make dep-install`
6. We can use `python ukrainer.py` to extract those texts.`
