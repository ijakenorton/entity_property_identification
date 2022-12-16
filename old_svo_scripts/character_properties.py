import entitiy_property_identification.semantic_parsing as semantic_parsing
import spacy
import json
import neuralcoref
import os
import time
import sys

from spacy import displacy
from spacy.tokens import Span

nlp = spacy.load("en_core_web_lg")
neuralcoref.add_to_pipe(nlp)

drac_chp1 = """Chapter I is taken from the May 3rd and May 4th entries in Jonathan Harker's journal. Harker is on a business trip in Eastern Europe, making his way across one of the most isolated regions of Europe. He is going to meet with a noble of Transylvania, Count Dracula. The heading to his journal entry tells us that Jonathan is writing in Bistritz, in what is now Romania. Two days ago, he was in Munich. One day ago, he was in Vienna. As he has moved farther east, the country has become wilder and less modern. Jonathan Harker records his observations of the people and the countryside, their costume and customs. He has been instructed to stay at an old fashioned hotel in Bistritz before setting out for the final leg of the journey to Dracula's castle. At Bistritz, a letter from Dracula is waiting for him. Jonathan is to rest before setting out the next day for the Borgo Pass, where the Count's coach will be waiting for him. The landlord and his wife are visibly distressed by Jonathan's intentions to go to Dracula's castle. Although they cannot understand each other's languages and must communicate in German, the innkeeper passively tries to stop Jonathan by pretending not to understand his requests for a carriage to the Borgo Pass. The landlord's wife more aggressively tries to dissuade Jonathan, warning him that tomorrow is St. George's Day, and at midnight on St. George's Eve evil is at its strongest. When he insists that he must go, she gives him a crucifix, Jonathan accepts the gift, even though, as an English Protestant, he considers crucifixes idolatrous. Before Jonathan leaves, he notices that a number of the peasants are watching him with apprehension. Although he cannot understand much of their language, he can make out the words for devil, Satan, werewolf, and vampire. The peasants make motions at him to protect him from the evil eye. On the carriage ride, his fellow passengers, on learning where he is going, treat him with the same kind of concerned sympathy, giving him gifts and protecting him with charms. The ride is in wild and beautiful country. The carriage driver arrives at the Borgo Pass an hour early, and in bad German he then tries to convince Jonathan that Dracula's coachman might not come tonight, and Jonathan should come with the rest of them to Bukovina. At that moment, a fearsome-looking coachman arrives on a vehicle pulled by coal-black horses. One of the passengers whispers, "for He rebukes the carriage driver, and brings Jonathan onto the coach. The final part of the trip is terrifying. The moon is bright but is occasionally obscured by clouds, and strange blue fires and wolves appear along the way. On several occasions, the driver leaves the coach, at which point the wolves come closer and closer to the vehicle. Whenever the driver returns, the wolves fleethe final time this phenomenon occurs, it seems that the wolves flee on the driver's command. The chapter ends with Dracula's castle coming into view, its crumbling battlements cutting a jagged line against the night sky."""

#ARG0 : Always SUBJECT.
#ARG1 : Object unless there is an ARG0, otherwise subject.
#ARG2 : OBJ
#ARG3 : OBJ


def resolve(doc):
    resolved = nlp(doc._.coref_resolved)
    return resolved



doc = nlp(drac_chp1)

persons = set()
orgs = set()
gpes = set()
locs = set()

pronoun_dict = dict()

#persons2 = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
persons2 = []

person_clusters = set()

for ent in doc.ents:
    if ent.label_ == "PERSON":
        if ent._.coref_cluster != None:
            person_clusters.add(ent._.coref_cluster)

#entity = dict(gender = '', type = '', objects = dict())



# entities['Jake'] = entity
# entities['Jake']['objects'].add()



# for cluster in person_clusters:
#     for mention in cluster.mentions:
#         if mention.text.lower() in ['he', 'him','his', "himself"]:
#              gendered_entities.add(cluster.main.text)
#         if mention.text.lower() in ['she', 'her', 'hers', 'herself']:



# print(gendered_entities)



entities = dict()

# persons.add(ent.text for ent in doc.ents if ent.label_ == "PERSON")

for ent in doc.ents:
    if(ent.label_ == "PERSON"):
        persons.add(ent.text)

    elif(ent.label_ == "ORG"):
        orgs.add(ent.text)
        entities[ent.label]
    elif(ent.label_ == "GPE"):
        gpes.add(ent.text)
    elif(ent.label_ == "LOC"):
        locs.add(ent.text)



displacy.serve(doc, style="ent")

print(persons)
print(orgs)
print(gpes)
print(locs)

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



