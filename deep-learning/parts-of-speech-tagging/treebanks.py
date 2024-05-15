from io import open
from conllu import parse_incr

treebank = {'en': 'UD_English-LinES/en_lines'}

def train_corpus(lang):
    return treebank[lang] + '-ud-train.conllu'

def test_corpus(lang):
    return treebank[lang] + '-ud-test.conllu'

# Remove contractions such as 'isn't'.
def prune_sentence(sentence):
    return [token for token in sentence if type(token['id']) is int]

def conllu_corpus(path):
    data_file = open(path, 'r', encoding='utf-8')
    sentences = list(parse_incr(data_file))
    return [prune_sentence(sentence) for sentence in sentences]
