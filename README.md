# fast-form
[![PyPI Latest Release](https://img.shields.io/pypi/v/fast-form.svg)](https://pypi.org/project/fast-form/)


Project from UniHack hackathon, helps to extract data from forms. 


## Installation

To use fast-form first install [Anaconda](https://www.anaconda.com/) on your computer from:
https://www.anaconda.com/products/individual#Downloads
you can keep default options for all the configurations of Installation wizard.

then open *Anaconda Prompt* and run these commands one by one:
```
conda create -n fast-form python=3.7.10
conda activate fast-form
pip install fast-form
```
Installing dependencies will take couple of minuts.


If the installation was successful, you can test if the CLI works correctly, by running:

```bash
fast-form --version
```
Now you can start using the tool.

## Test Run
To run fast-form, first, initialize data folder:
```bash
fast-form init
```
This will create a folder `fast-form-data` containing test data and all the config files in your current working path.

You will want to customize these files later on, for the test run, leave them as they are and run:
```bash
fast-form extract
```
This will create `validation_excel.xlsx`, which you can open in office suite and manually fix all the results that were not recognized correctly. 

 * -1 is used for answers that were recognized as having multiple fields crossed
 * -2 in case no crossed field was recognized
 
 You can replace those, in case picture recognition did a poor job.

Once you are happy with the result, save the validation excel and run

```bash
fast-form finalize
```
This will compile validated data in to format "one questionnaire per line" and append it in to excel configured in `final_excel_path` in `path_config.json`.


## Using fast-form
`fast-form init` created following directory structure
```
fast-form-data
│   path_config.json
│   config.json    
│   template.pdf
└───documents
    │   document.jpg
    │   ...

```
To configure fast-form for your custom questionnaire, you will have to replace/reconfigure these files
#### path_config.json
Provides paths to all files and folders necessary for the script to run.
You can either let it as is and change the filenames, or change this configuration using any plain text processor (e.g. Notepad).
```json
{
    "template_path": "/pathtotemplate/template.jpg",
    "form_structure_path": "/pathtoconfig/config.json",
    "folder_with_documents_path": "/pathtodocumentfolder/documents",
    "final_excel_path": "/pathtofinalexcel/final_excel.xlsx"
}
```

#### config.json
Contains description of all the fields in the questionnaire and their exact position on the page.
Those configs have to be created manually using the template and there is no visual tool to do it. We have a [ jupyter notebook](https://github.com/kubantjan/fast-form/blob/master/notebooks/create_config.ipynb) for this task, but workflow is far from smooth at this point.

#### template.pdf
Is clear, empty questionnaire, used as a template to correctly scale and rotate scanned files.
You can use pdf version of the file, that is used to print the questionnaires.

#### documents
Simply a folder where you put all the scanned questionnaires to be processed.
Once files have been processed, it might be good idea to archive them.

#### final_excel.xlsx
If you want the results to be appended to your existing excel document, provide path to this file, otherwise fast-form will create new excel document.

___________________

Once you provided all the configuration files, you can process the files using following loop
 1. Fill batch of scans in to documents folder.
 2. run
```bash
fast-form extract
```
3. validate results in table processor (such as Microsoft Excel)
4. Finalize validated results with command:
```bash
fast-form finalize
```




## Development

Before development please run
`
make setup
`
Installing new dependencies added on remote

```
pip-sync
```

### Adding dependencies:

add line to `requirements.in` and then run
```
pip-compile
```

### Retrain model
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
* [x] ***For the name of the patient use the name from questionnaire of question called patient_id. In case such question is not present, use the name of the pdf (as it is done now)***
* [x] ***Prepare python script that will process the scanned pdfs:***

The program should get the following parameters from config file that will have to be existing in the folder:

    - folder with scanned files (how should be new questionnaire recongized? new file for each?
    - path to template document as pdf or jpg or something
    - config file with location of answers in the template document via coordinates in pixels (see configuration above)

And it should output:

    - excel file with the answers and their accuracies and also the parts of the original scan that were used for the recognition. 
    
* [x] ***Prepare python script that will process the excel document with all the answers into an excel sheet. One questionnaire per line.*** 
params:
    - path to the excel with answers
    - path to the excel to put it in (if none, create new)
    - name of the sheet (if none create new)
if the sheet is non empty put the data below the data already there 

* [x] ***Write readme***
* [ ] ***Write nicer readme***
* [ ] ***Create from this a package on pypi***
* [ ] ***Test and especially let someone test on mac***
