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
and then run `field_recognizer/emnist-neural-network.ipynb` in jupyter notebook.

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
 * /DONE/ retrain model on capital letters only
 * /DONE/ enrich emnist dataset by different letter positioning
 * enrich emnist dataset by different letter thickness
 * Add model for numbers
 * Solve czech characters, either
   * find different dataset with czech diacritics
   * enrich emnist dataset by letters with diacritics 
   * Add second clasifier, that would recognize diacritics  / accute(') / carron(ˇ) / none  / 
   
#### Refactoring
 * Restructure repository to separate code from data
 * consider refactoring to original emnist dataset structure instead of this csv data

#### Preprocessing
 * smarter threasholding
 * smarter corner classification
 


