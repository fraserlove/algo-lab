from treebanks import train_corpus, test_corpus, conllu_corpus, treebank
from naive import Naive
from viterbi import Viterbi
from forwardbackward import ForwardBackward

# Header.
print(f"{'Algorithm':<18} {'Corpus':<10} {'Language':<10} {'Sentence Accuracy':<20} {'Word Accuracy':<20}")

for lang in treebank.keys():
    # Load the training and test data for the language.
    train_sents = conllu_corpus(train_corpus(lang))
    test_sents = conllu_corpus(test_corpus(lang))

    # Create the HMM algorithms.
    algorithms = {
        'Naive': Naive(train_sents, test_sents),
        'Viterbi': Viterbi(train_sents, test_sents),
        'Forward-Backward': ForwardBackward(train_sents, test_sents),
    }

    corpora = {
        'Train': train_corpus(lang),
        'Test': test_corpus(lang)
    }
    
    # Evaluate the algorithms on the test data.
    for algo_name, algo in algorithms.items():
        for corp_name, corpus in corpora.items():
            sents_acc, words_acc = algo.evaluate(conllu_corpus(corpus))
            print(f"{algo_name:<18} {corp_name:<10} {lang:<10} {sents_acc:<20.2%} {words_acc:<20.2%}")
