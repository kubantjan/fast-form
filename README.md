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

## Retrain model
We are using preparsed emnist
https://www.kaggle.com/crawford/emnist

### Example form configuration - JSON

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


