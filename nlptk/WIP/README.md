# Readme


## Plan for how to compare data & jsonresume

### Purpose
- compute a coverage measure for how good good the jsonresume is compared to ground truth data 


### Procedure

PREP
Extract data
- Get data and jsonresume from response
```
jsonresume = response["jsonresume"]
data = response["data"]
```

Run normalization
- get rid of "value"
- normalize both (in case the schema versions are incompatible / diff versions) 
```
from nlptk.jsonresume.converter import Converter
conv = Converter()
data = conv.normalize_camel_case(data)
jsonresume = conv.normalize_camel_case(jsonresume)
```

Validate schema
- Run jsonresume schema validation to confirm they are both valid jsonresume
```
from nlptk.jrprocessor.jr_validation import JRValidate
valid = JRValidate()
valid.is_valid_json_resume(data)
valid.is_valid_json_resume(jsonresume)
```

Walk through dict
- use recursive function to walk through dicts
- for each leaf node compute Levenshtein similarity

Result
- same schema as data/jsonresume
- but instead of string values use floats for the similarity 

After walking the dict to compute the above
- roll up the individual similarity scores for each sub-section
- then do the same for each section
- then do the same for the whole dict overall


Something like this:
```
{ ...
    "work": {
        "similarity": 0.75,
        "items_similarity": [0.5, 1.0]
        "items: [
          {
          "name": 1.0,
          "summary": 0.6,
          "location": 0.98,
          "position": 1.0,
          "startdate": 0.5,
          "enddate": 0.5,
          "highlights": [1.0, 1.0, 0.5],
          "description": 0.7
          }
        ]  
    }
}
```

Caveats
- I am re-formatting dates, so will be hard to exactly compare.










