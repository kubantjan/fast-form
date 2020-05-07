# fast-form
project from UniHack hackathon, helps to extract data from forms

## Installing dependencies

first run 

```
pip install pip-tools
pip-sync
```

adding dependencies:

add line to requirements.in and then run
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

``` json
{
  "fields": [
    {
      "name": "Example",
      "type": "letters",
      "topLeft": {
        "x": 10,
        "y": 20
      },
      "numberOfBoxes": 10,
      "boxWidth": 3,
      "boxHeight": 2,
      "spaceBetweenBoxes": 1,
      "orientation": "horizontal"
    },
    {
      "name": "Example2",
      "type": "boxes",
      "topLeft": {
        "x": 10,
        "y": 60
      },
      "numberOfBoxes": 10,
      "boxWidth": 3,
      "boxHeight": 2,
      "spaceBetweenBoxes": 1,
      "orientation": "vertical"
    }
  ],
  "size": {
    "width": 740,
    "height": 1049
  }
}
```
there are 3 possible types "letter", "numbers", "boxes"

## Road map

#### Character Recognition
 * [x] retrain model on capital letters only
 * [x] enrich emnist dataset by different letter positioning
 * [ ] use this notebook to improve the model https://www.kaggle.com/tarunkr/digit-recognition-tutorial-cnn-99-67-accuracy
 * [ ] enrich emnist dataset by different letter thickness
 * [ ] Add model for numbers
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
 * [ ] smarter thresholding
 * [ ] smarter corner classification
 * [ ] completely drop corners, orient page based on the original file provided (fitting text on text)

 
#### Configuration
 * [ ] location of text via top left corner, bottom right corner plus number of letters
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
