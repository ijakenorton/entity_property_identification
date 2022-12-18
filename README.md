To setup allennlp-models environment run 
```
conda env create -f allen.yml
conda activate allen
conda install -c conda-forge jsonnet
pip install -r requirements.txt && pip install allennlp-models
pip install ./neuralcoref
pip install spacy==2.3.5
python -m spacy download en_core_web_lg
python -m spacy download en_core_web_sm

```

