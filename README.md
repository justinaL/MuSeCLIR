# MuSeCLIR: A Multiple Senses and Cross-lingual Information Retrieval dataset

Wing Yan Li, Julie Weeds, David Weir. *MuSeCLIR: A Multiple Senses and Cross-lingual Information Retrieval dataset.* COLING 2022 (short).

Paper at: [https://aclanthology.org/2022.coling-1.96/](https://aclanthology.org/2022.coling-1.96/)

If you use MuSeCLIR fr your work, please cite as: 
```
@inproceedings{li-etal-2022-museclir,
    title = "{M}u{S}e{CLIR}: A Multiple Senses and Cross-lingual Information Retrieval Dataset",
    author = "Li, Wing Yan  and Weeds, Julie  and Weir, David",
    booktitle = "Proceedings of the 29th International Conference on Computational Linguistics",
    month = oct,
    year = "2022",
    address = "Gyeongju, Republic of Korea",
    publisher = "International Committee on Computational Linguistics",
    url = "https://aclanthology.org/2022.coling-1.96",
    pages = "1128--1135"
}
```


This repository is for reproducing MuSeCLIR. Ground-truth bilingual dictionaries are cloned from the original [MUSE](https://github.com/facebookresearch/MUSE) repository.


### Requirements

- v0.5.4 [Wikipedia-API](https://github.com/martin-majlis/Wikipedia-API/)
- v3.2.0 spacy
- v1.1.1.post1 [OpenCC](https://github.com/BYVoid/OpenCC/)


### How to use
Download the ground-truth bilingual dictionaries with:
```sh
cd data/
./get_evaluation.sh
```
By changing the [language code](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) of the `target_lang` argument, users can re-produce MuSeCLIR in other language pairs. 
```sh
python main.py --target_lang zh
```