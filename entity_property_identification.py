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
            #santized = ent.text.translate(str.maketrans('', '', string.punctuation))
            #stripped = "'".join(santized.split())
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
    # for key in entities.keys():
    #     print("Subject:",key)
        # for object_key in entities[key].keys():
        #     print('\t','object >> ',object_key,' >>> count:', entities[key][object_key])
            
            
    #print("oh yeah, btw:", entities)

    # for subject_key in parsed['subjects'].keys():
    #     subject_relations[subject_key] = {}
    #     current_index_set = set()
    #     for clause in parsed['subjects'][subject_key]: ##values of subject keys. (loop through a list of clauses)      
    #         for object_key in parsed['objects'].keys(): #loop through object keys
    #             for object_clause in parsed['objects'][object_key]: #for each obj key, loop over its values( list of clauses)   
    #                 if clause['index'] == object_clause['index']:
    #                     if clause['index'] not in current_index_set:
    #                         continue
    #                     else:
    #                         current_index_set.add(clause['index'])
    #                     # print('sub_clause>>',clause)
    #                     # print('object_clause>>',object_clause)
    #                     # print('object key', object_key)
    #                     # print('subject_relations[subject_key].keys()>>>>', subject_relations[subject_key].keys())
    #                     if object_key in subject_relations[subject_key].keys():
    #                         subject_relations[subject_key][object_key] += 1
    #                     else:
    #                         subject_relations[subject_key][object_key] = 1
    
    # for subject_key in subject_relations.keys():
    #     print('subject key >>>',subject_key)
    #     for object_key in subject_relations[subject_key].keys():
    #         print(object_key,'>>>',subject_relations[subject_key][object_key])
    #     print("---- New SUB ------")
                        
    # for verb in parsed['verbs']:
    #     for clause in verb:
    #         print(clause)                    
                        
    
    # subjects = parsed['subjects']
    # for each in subjects:
    #     #print(each, ":", subjects[each])
    #     print("*****",each,"*****")
    #     for clause in subjects[each]:
    #         print(clause)




if __name__ == '__main__':
    main()




#resolved_chp1 = resolve(doc)


# parsed_chp1  = semantic_parsing.parse(resolved_chp1)


# sents = parsed_chp1['words']  #words is actullly a  sentence, cheers jake.
# verbs = parsed_chp1['verbs'] 
# subjects = parsed_chp1['subjects']
# objects = parsed_chp1['objects']\

# for each in subjects:
#     #print(each, ":", subjects[each])
#     print("*****",each,"*****")
#     for clause in subjects[each]:
#         print(clause)



