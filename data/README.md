# Evaluation text

* `ko.txt` is the Korean text used for the "PPL KO" numbers (3.29 MB, 1.46 M characters).
  It is the first 300 articles of the Korean Wikipedia dump `wikimedia/wikipedia`, config `20231101.ko`,
  keeping articles longer than 1500 characters. `python3 scripts/make_ko.py data/ko.txt` rebuilds it byte for byte.
  Source: Korean Wikipedia (https://ko.wikipedia.org), text by Wikipedia contributors (authors listed in each article's
  page history), licensed CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/) and GFDL. Redistributed here under CC BY-SA 4.0.
* WikiText-2 (English) is not stored here; download it with the command in the top-level README (CC BY-SA 3.0).
