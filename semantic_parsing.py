
import re as reg
import sys
import string
from nltk import tokenize
from allennlp_models.pretrained import load_predictor




ARGM_LIST = ['ARGM-MOD', 'ARGM-ADV', 'ARGM-LVB', 'ARGM-PRD']
ARGS = ['ARG0', 'ARG1', 'ARG2', 'ARG3', 'ARG4']
subject_set = set()      
subjects = dict(phrases = {}, objects = {}) 
object_set = set()
objects = dict(phrases = {})



# def write_to_file():           
#     if output is not None:
#         with open(output, 'w') as f:
#             for i, sentence in enumerate(sentences['verbs']):
#                 f.write(str(sentences['words'][i]) + '\n')
#                 for clause in sentence:
#                     f.write(str(clause) + '\n')
            
#             f.close()        
                
# output = None
# input = sys.argv[1]
# if (len(sys.argv)) > 2:
#     output = sys.argv[2]
# print(len(sys.argv))

    
    
# with open(input) as f:
#     file = f.read()
#     f.close()




def create_text(coreferenced_text):
    text = coreferenced_text.text.replace('\\', '')
    sentencized_text = tokenize.sent_tokenize(text)
    return sentencized_text
    
    
#Converts the internal string of the prediction json into a dictionary, with only the key arguments     
def internal_string_to_dict(sentencized_text):
    global ARGM_LIST, ARGS, subject_set, subjects, object_set, objects
    predictor = load_predictor('structured-prediction-srl-bert')
    sentences_dict = dict(verbs = [], sentences = [])
    for sentence in sentencized_text:
        # print(sentence)
        clauses = []
        split_sentence = sentence.split()
        print(sentence)
        print(split_sentence)
        print("--")

        result = predictor.predict_json({"sentence": sentence})
        for verb_phrase in result['verbs']:
            clause = reg.findall(r"\[(.*?)\]", verb_phrase['description']) 
            keys = []
            values = []
            for p in clause:
                start, middle, value = p.partition(":") 
                value = tokenize.word_tokenize(value.strip())#string to list
                final = []
                i = 0
                #This loop fixes the dictionary values that were split by the allen model
                while (i < len(value)):
                    matches = []
                    for w in split_sentence:
                        if value[i] in w:
                            matches.append(w)
                    converted = value[i]
                    next_i = i+1
                    while(next_i < len(value)):
                        temp_matches = []
                        temp_word = converted + value[next_i]
                        for match in matches:
                            if temp_word in match:
                                temp_matches.append(match)
                        if len(temp_matches) == 0:
                            break
                        else:
                            matches = temp_matches
                            i = next_i
                            converted = converted + value[next_i]
                            next_i += 1  
                    i+=1
                    final.append(converted)
                
                end = " ".join(final)
                keys.append(start) 
                values.append(end)
            
            # print(values)
            clause = dict(ARG0 = None, V = None, ARG1 = None)
            clause = dict(zip(keys,values))
            clauses.append(clause)
        sentences_dict['sentences'].append(result['words'])
        sentences_dict['verbs'].append(clauses)
    return sentences_dict
    

    
#Loops through output of the model and squishes lone verbs onto the next sentence   
def verb_replacement(sentences_dict):  
    global ARGM_LIST, ARGS, subject_set, subjects, object_set, objects
    for i, sentence in enumerate(sentences_dict['verbs']):
        for j, clause in enumerate(sentence):
            found_arg = None
            if len(clause) == 1:
                #IF in argm-list and not included in the argm, add to argm
                if len(sentence) > j + 1:
                    for arg in ARGM_LIST:
                        if arg in sentence[j+1].keys():
                            found_arg = arg;
                    if found_arg != None:    
                        if clause['V'] in sentence[j+1][found_arg]:
                            continue
                        else:
                            sentence[j+1][found_arg] = clause['V'] + sentence[j+1][found_arg]
                            continue
                    else:
                        if "V" in sentence[j+1].keys():
                            continue
    return sentences_dict

def add_subject_to_dict(entities, arg, clause, i):
    current_subject = clause[arg]
    add_to_dict(subjects, subject_set, arg, clause, i)  
    if current_subject not in entities.keys():
        entities[current_subject] = dict()
    return current_subject

def add_to_dict(dic, set, arg, clause, index):
    global ARGM_LIST, ARGS, subject_set, subjects, object_set, objects
    clause['index'] = index
    if clause[arg] in set:
        dic[clause[arg]].append(clause)
    else:
        dic[clause[arg]] = []
        dic[clause[arg]].append(clause)
        set.add(clause[arg]) 

#def add_obj_to_subj(subj_d, obj_d, sub, obj):
def increment_entity_object(entities, current_subject, current_object):
    if current_object in entities[current_subject].keys():
        entities[current_subject][current_object] += 1
    else:
        entities[current_subject][current_object] = 1
    return entities


def add_new_object_to_entity(entities,arg, clause, current_subject, i):
    current_object = clause[arg]
    add_to_dict(objects, object_set, arg, clause, i) 
    if current_subject != None:
        entities = increment_entity_object(entities, current_subject, current_object)
        
        
        
#Removes Sentences that do not include a subject or object and adds them according to subject / object
def extract_subject_object(sentences_dict):
    global ARGM_LIST, ARGS, subject_set, subjects, object_set, objects
    entities = {}



    for i, sentence in enumerate(sentences_dict['verbs']):
        #print(sentences_dict['words'][i])
        for j, clause in enumerate(sentence):
            current_subject = None
            if ARGS[0] in clause.keys():
                current_subject = add_subject_to_dict(entities, ARGS[0],clause, i)
            if ARGS[1] in clause.keys():
                if ARGS[0] in clause.keys():
                    add_new_object_to_entity(entities, ARGS[1], clause, current_subject, i)
                else:
                    current_subject = add_subject_to_dict(entities, ARGS[1],clause, i)
            if ARGS[2] in clause.keys():
                add_new_object_to_entity(entities, ARGS[2], clause, current_subject, i)
                
            if ARGS[3] in clause.keys():
                add_new_object_to_entity(entities, ARGS[3], clause, current_subject, i)
            if ARGS[4] in clause.keys():
                add_new_object_to_entity(entities, ARGS[4], clause, current_subject, i)
            else:
                sentences_dict['verbs'][i].remove(sentence[j])
    sentences_dict['subjects'] = subjects   
    sentences_dict['objects'] = objects   
    # print("---") 
    # print(entities)
    return sentences_dict, entities


'''
Method which takes coreferenced text and returns a dictionary containing the original tokenized sentences;
the verb clauses
subjects 
objects
second dictionary of entities which contains the subjects of sentences/ objects which link to those subjects and the number of occurences they
appear together based on sentences
TODO
paragraphs
chapters

'''
def parse(coreferenced_text):
    #global ARGM_LIST, ARGS
    global ARGM_LIST, ARGS, subject_set, subjects, object_set, objects
    sentencized_text = create_text(coreferenced_text)
    sentences_dict = internal_string_to_dict(sentencized_text)
    sentences_dict = verb_replacement(sentences_dict)
    sentences_dict, entities = extract_subject_object(sentences_dict)
    return sentences_dict, entities;

    




  
