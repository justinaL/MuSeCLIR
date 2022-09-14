# MuSeCLIR: A Multiple Senses and Cross-lingual Information Retrieval dataset

Wing Yan Li, Julie Weeds, David Weir. *MuSeCLIR: A Multiple Senses and Cross-lingual Information Retrieval dataset.* COLING 2022 (short).

This repository is for reproducing MuSeCLIR. Ground-truth bilingual dictionaries are cloned from the original [MUSE](https://github.com/facebookresearch/MUSE) repository.


### Requirements

- v0.5.4 [Wikipedia-API](https://github.com/martin-majlis/Wikipedia-API/)
- v3.2.0 spacy
- v1.1.1.post1 [OpenCC](https://github.com/BYVoid/OpenCC/)


### How to use
By changing the [language code](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) of the `target_lang` argument, users can re-produce MuSeCLIR in other language pairs. 
```sh
$ python main.py --target_lang zh
```