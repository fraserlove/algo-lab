from nltk import FreqDist, WittenBellProbDist

class HMM:

    def __init__(self, train_sents, test_sents):
        self.tags = {token['upos'] for corpus in [train_sents, test_sents] for sent in corpus for token in sent}
        self.transitions = self.transition(train_sents)
        self.emissions = self.emission(train_sents)
        
    def transition(self, sents):
        """ Compute transition probabilities between POS tags. """
        transitions = {tag: [] for tag in self.tags.union({'<s>'})} # Holds lists of tags for each POS tag.

        for sent in sents:
            transitions['<s>'].append(sent[0]['upos']) # Handle the start of sentence.
            # Handle transitions within the sentence.
            for prev_tag, curr_tag in zip(sent, sent[1:]):
                transitions[prev_tag['upos']].append(curr_tag['upos'])
            transitions[sent[-1]['upos']].append('</s>') # Handle the end of sentence.
        
        return self.smooth(transitions) # Smooth the transition probabilities.

    def emission(self, sents):
        """ Compute emission probabilities of words for each POS tag. """
        emissions = {tag: [] for tag in self.tags} # Holds lists of words for each POS tag.

        # Populate the dictionary with words for each tag.
        for sent in sents:
            for token in sent:
                emissions[token['upos']].append(token['form'])
        
        return self.smooth(emissions) # Smooth the emission probabilities.

    def smooth(self, probs):
        """ Smooth probabilities using Witten-Bell smoothing. """
        return {tag: WittenBellProbDist(FreqDist(freq), bins=1e5) for tag, freq in probs.items()}
    
    def evaluate(self, sents):
        """ Evaluate the POS tagger on a corpus of sentences. """
        acc_sents, acc_words = 0, 0
        total_words = sum(len(sent) for sent in sents)
        total_sents = len(sents)

        for sent in sents:
            # Extract the words and true tags from the sentence.
            test_sent, true_tags = zip(*[(token['form'], token['upos']) for token in sent])

            # Predict tags for the entire sentence.
            predicted_tags = self.predict(test_sent)

            # Calculate errors and check if the entire sentence is correct.
            acc_words += sum(pred == true for pred, true in zip(predicted_tags, true_tags))
            acc_sents += all(pred == true for pred, true in zip(predicted_tags, true_tags))

        # Return sentence-level and word-level accuracy.
        return acc_sents / total_sents, acc_words / total_words
    
    def predict(self, sent):
        """ Predict the most likely sequence of POS tags for a given sentence. """
        pass