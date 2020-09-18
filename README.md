# fast-form
project from UniHack hackathon, helps to extract data from forms

## Setting up
create clean environment python 3.8:
```
conda create -n fast-form python=3.7 -y
conda activate fast-form
```

Then set it up

```
make setup
```
### Installing new dependencies added on remote

```
pip-sync
```

### Adding dependencies:

add line to `requirements.in` and then run
```
pip-compile
```

## Run
```bash
python3 main.py -c config/config.json
``` 

## Retrain model
We are using preparsed emnist dataset.
https://www.kaggle.com/crawford/emnist

To retrain the model, you need to download it to training_data folder 
```text
fast-form
 - training_data
    - emnist-balanced-mapping.txt
    - emnist-balanced-train.csv
    - emnist-balanced-test.csv
    ...
 ...
```

and then first run `field_recognizer/enrich_dataset.ipynb` in jupyter notebook and after that use
 `field_recognizer/emnist-neural-network.ipynb` twice, once for type numbers, once for type letters 
 (see inside of notebook )

## Example form configuration - JSON
```
tests/form_for_test/config.json
```

## Road map

#### Character Recognition
 * [x] retrain model on capital letters only
 * [x] enrich emnist dataset by different letter positioning
 * [x] use this notebook to improve the model https://www.kaggle.com/tarunkr/digit-recognition-tutorial-cnn-99-67-accuracy
 * [ ] enrich emnist dataset by different letter thickness
 * [x] Add model for numbers
 * [ ] Solve czech characters, either
   * find different dataset with czech diacritics
   * enrich emnist dataset by letters with diacritics 
   * Add second clasifier, that would recognize diacritics  / accute(') / carron(ˇ) / none  / 
   * Create our own, small dataset (maybe adding the diacritics to current dataset)
    and use methods here: https://arxiv.org/pdf/1904.08095.pdf
   
#### Refactoring
 * [ ] Restructure repository to separate code from data
 * [ ] consider refactoring to original emnist dataset structure instead of this csv data

#### Preprocessing
 * [x] smarter thresholding
 * [x] smarter corner classification
 * [x] completely drop corners, orient page based on the original file provided (fitting text on text)

 
#### Configuration
 * [x] location of text via top left corner, bottom right corner plus number of letters
 * [ ] create a tool for config file creation
 
#### Packaging, proper output
* [ ] package it:

The program should get the following parameters:

    - folder with scanned files
    - path to original document
    - config file with location of answers in the original document via coordinates in pixels

And it should output:

    - excel file and csv file (or make it a parameter) with the answers and their accuracies and somehow also the 
    parts of the original scan that were used for the recognition. Maybe in separate folder, properly named.
