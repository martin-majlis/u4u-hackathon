# U4U Hackathon

https://ufal.mff.cuni.cz/ufal-ukraine

## Ukrainer.net

- https://ukrainer.net/
- contains texts in Czech and Ukrainian.

### Approach

1. Download pages 3 levels deep from the Czech version - https://ukrainer.net/cs/
   - Initial attempt - `wget --header='Accept-Language: cs' --execute="robots = off" -r -N -l 3 --no-remove-listing --convert-links --wait=1 -R png,jpg,jpeg,css,js,webp https://ukrainer.net/cs/`
   - Try to start from themes and skip pages that has language suffix - `wget --header='Accept-Language: cs' --execute="robots = off" -r -N -l 4 --no-remove-listing --convert-links --wait=1 -R png,jpg,jpeg,css,js,webp,-de,-ja,-fr,-es,feed,wp-json, https://ukrainer.net/temata/`
2. Articles have drop downs with links to the articles in different languages.
   - `(cs) Čeština`
   - `(ua) Українська`
3. We can find pages written in both languages with the following command:
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
7. Install Hunalign - https://github.com/danielvarga/hunalign
   - Commands:
     ```
     wget 'ftp://ftp.mokk.bme.hu/Hunglish/src/hunalign/latest/hunalign-1.1.tgz'
     tar -xzf hunalign-1.1.tgz
     cd hunalign-1.1/src/hunalign
     make
     ```
8. Run alignment:
   - Combine Sentences:
     ```
     make combine-sentences
     ```
     or
     ```
     find data/ukrainer-processed/ -name 'cs_sentences.txt' -exec cat {} \; > data/cs_sentences.txt
     find data/ukrainer-processed/ -name 'ua_sentences.txt' -exec cat {} \; > data/ua_sentences.txt
     ```
   - Alignment:
     ```
     make run-hunalign
     ```
     or
     ```
     hunalign-1.1/src/hunalign/hunalign hunalign-1.1/data/null.dic data/cs_sentences.txt data/ua_sentences.txt -text > data/cs-ua-aligned_sentences.txt
     ```

### Helper Commands

#### Figure out the number of sentences

Text content:

```
make stats-sentences-extracted
```

or

```
wc data/*_sentences.txt
```

Current Stats:

```
  14621  344796 3303363 data/cs-ua-hunaligned_sentences.txt
  14841  165444 1171383 data/cs_sentences.txt
  14734  163399 2002770 data/ua_sentences.txt
  44196  673639 6477516 total
```
