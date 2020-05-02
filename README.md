# fast-form
project from UniHack hackathon, helps to extract data from forms

## Example configuration JSON

```
{
  "fields": [
    {
      "name": "Example",
      "type": "string",//possible types: string, numbers, boxes 
      "topLeft": {
        "x": 10,
        "y": 20
      },
      "numberOfBoxes": 10,
      "boxWidth": 3,
      "boxHeight": 2,
      "spaceBetweenBoxes": 1
    }
  ]
}
```
