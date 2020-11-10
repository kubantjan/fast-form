# fast-form
project from UniHack hackathon, helps to extract data from forms

## Setting up
create conda environment with python 3.7.9 and poppler:
```
conda env create -f conda.yml -y
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

priorities till 15.11.2020 


#### Character Recognition
 * [x] retrain model on capital letters only
 * [x] enrich emnist dataset by different letter positioning
 * [x] use this notebook to improve the model https://www.kaggle.com/tarunkr/digit-recognition-tutorial-cnn-99-67-accuracy
 * [x] Add model for numbers
 * [ ] Solve czech characters, either
   * find different dataset with czech diacritics
   * enrich emnist dataset by letters with diacritics 
   * Add second clasifier, that would recognize diacritics  / accute(') / carron(ˇ) / none  / 
   * Create our own, small dataset (maybe adding the diacritics to current dataset)
    and use methods here: https://arxiv.org/pdf/1904.08095.pdf
 * [ ] (depends on something in section Model results processing) Create a model distinguishing X or filled circle or nothing or anomaly.
  Improve true/false computation for boxes

#### Refactoring
 * [x] Restructure repository to separate code from data
 * [ ] Refactor to original emnist dataset structure instead of preparsed csv data from kaggle

#### Preprocessing
 * [x] smarter thresholding
 * [x] smarter corner classification
 * [x] completely drop corners, orient page based on the original file provided (fitting text on text)
 * [x] Improve just config so it centers boxes better and reponse 159 in PID1 is correctly parsed
 * [x] ***Change code to handle multiple pages somehow***
 * [ ] Better noise cancellation on the whole file
 * [ ] Better noise cancellation on the level of the cropped boxes (important to do before cropping to the symbol area as it is broken by noise at the moment sometimes)
  many options how to approach, choose any
 * [ ] Possibly (but maybe hard to do): remove bounding lines from figures.
 * [ ] Speedup: the current matching teplate logic is simly tooo slow. Think what to do
 - use other feature extraction method than SIFT (I have tried ORB which did not work well enough, but maybe after some tuning it would. it is way faster)
 - do whathever else
 * [ ] Saving of templates -> pickle is not working, but can be made working by 
 https://stackoverflow.com/questions/10045363/pickling-cv2-keypoint-causes-picklingerror

#### Model results processing

 * [x] ***Implement logic around single choice forms return only single choice if there is only 1 true choice found, otherwise -1 (if no question answered) or -2 (if more than one question answered).***
 * [ ] Add to single choice logic also logic for filled in and anomaly circles. 


#### Specific Questionnaire processing
 * [ ] Prepare empty template that will have only header and some repeating thigs for PID, test how it works, potentially alter
 PID a bit, so it works for such empty template
* [x] ***Prepare at the top of the first page space where one can fill in the patient code and add this to config as only number field***
 
#### Configuration
 * [x] location of text via top left corner, bottom right corner plus number of letters
 * [ ] Create a tool for config file creation
    
#### Packaging, proper output
* [x] prepare for pdf with multiple questionnaires
* [x] create config for the current questionnaire we are working on
* [ ] ***For the name of the patient use the name from questionnaire of question called patient_id. In case such question is not present, use the name of the pdf (as it is done now)***
* [ ] ***Prepare python script that will process the scanned pdfs:***

The program should get the following parameters from config file that will have to be existing in the folder:

    - folder with scanned files (how should be new questionnaire recongized? new file for each?
    - path to template document as pdf or jpg or something
    - config file with location of answers in the template document via coordinates in pixels (see configuration above)

And it should output:

    - excel file with the answers and their accuracies and also the parts of the original scan that were used for the recognition. 
    
* [ ] ***Prepare python script that will process the excel document with all the answers into an excel sheet. One questionnaire per line.*** 
params:
    - path to the excel with answers
    - path to the excel to put it in (if none, create new)
    - name of the sheet (if none create new)
if the sheet is non empty put the data below the data already there 

* [ ] ***Write a nice readme ale let someone test on mac***