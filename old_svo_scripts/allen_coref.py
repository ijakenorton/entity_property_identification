from typing import List, Dict


from spacy.tokens import Doc
import numpy

from allennlp.common.util import JsonDict
from allennlp.common.util import get_spacy_model
from allennlp.data import DatasetReader, Instance
from allennlp.data.fields import ListField, SequenceLabelField
from allennlp.models import Model
from allennlp.predictors.predictor import Predictor
from allennlp_models.pretrained import load_predictor

with open ('../text_files/plain_text/drac1.txt', 'r') as file:
    drac_chp1 = file.read()

#archive = load_archive(FIXTURES_ROOT / "coref" / "serialization" / "model.tar.gz")
predictor = load_predictor("coreference_resolution")

result = predictor.predict_json(drac_chp1)
print(result)