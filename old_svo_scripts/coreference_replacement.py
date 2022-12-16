"""
This script uses co-reference resolution to replace pronouns with there main reference
Takes two commandline args, arg1 is input txt file, arg2 is output text file
"""
#What are the input texts going to look like ?

import spacy
import json
import neuralcoref
import os
import time
import sys


input = sys.argv[1]
output = sys.argv[2]
nlp = spacy.load("en_core_web_lg")
neuralcoref.add_to_pipe(nlp)
with open(input,) as f:
    text = f.read()
    
doc = nlp(text)
resolved = nlp(doc._.coref_resolved)

print(resolved)

with open(output, 'w') as f:
    f.write(resolved.text)
    f.close()