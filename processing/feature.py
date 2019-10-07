import os

## Merge helper function
def dict_merger(dict1, dict2): 
    res = {**dict1, **dict2} 
    return res