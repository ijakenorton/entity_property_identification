import semantic_parsing
import spacy
import json
import neuralcoref
import os
import time
import sys
import string
nlp = None

from spacy import displacy

with open ('./text_files/plain_text/drac2-4.txt', 'r') as file:
    drac_chp1 = file.read()


#ARG0 : Always SUBJECT.
#ARG1 : Object unless there is an ARG0, otherwise subject.
#ARG2 : OBJ
#ARG3 : OBJ
def instantiate_nlp():
    global nlp
    nlp = spacy.load("en_core_web_lg")
    neuralcoref.add_to_pipe(nlp)
    
def resolve(doc):
    return nlp(doc._.coref_resolved)


    
    
    
def get_entity_types(doc, entities):
    persons = set()
    orgs = set()
    gpes = set()
    locs = set()

    tempset = set()

    for ent in doc.ents:

        if ent._.coref_cluster != None:
            tempset.add(ent._.coref_cluster)

        if(ent.label_ == "PERSON"):
            persons.add(ent.text)
            # if ent._.coref_cluster != None:
            #     for mention in ent._.coref_cluster.mentions:
            #         if mention.text.lower() in ['he', 'him','his', "himself"]:
            #             print("man")
            #         if mention.text.lower() in ['she', 'her', 'hers', 'herself']:
            #             print("woman")

        elif(ent.label_ == "ORG"):
            orgs.add(ent.text)
        elif(ent.label_ == "GPE"):
            gpes.add(ent.text)
        elif(ent.label_ == "LOC"):
            locs.add(ent.text)

    # for each in tempset:
    #     print(each)
    return persons, orgs, gpes, locs


def main():
    global nlp
    instantiate_nlp()
    doc = nlp(drac_chp1)
    parsed, entities = semantic_parsing.parse(resolve(doc))
    persons, orgs, gpes, locs = get_entity_types(doc, entities)
    # verbs = parsed['verbs'] 
    # subjects = parsed['subjects']
    # objects = parsed['objects']
    for key in entities:
        print('Subject:', key)
        for object_key in entities[key]:
            print('\t','object >> ',object_key,' >>> count:', entities[key][object_key])

    
    # subjects = parsed['subjects']
    # for each in subjects:
    #     #print(each, ":", subjects[each])
    #     print("*****",each,"*****")
    #     for clause in subjects[each]:
    #         print(clause)




if __name__ == '__main__':
    main()








