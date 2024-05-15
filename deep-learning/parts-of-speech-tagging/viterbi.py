from hmm import HMM

class Viterbi(HMM):

    def __init__(self, train_sents, test_sents):
        super().__init__(train_sents, test_sents)

    def predict(self, sent):
        """ Predict the most likely sequence of POS tags for a given sentence using the Viterbi algorithm. """
         # Initialise the Viterbi matrix with a size for each word.
        viterbi = [{} for _ in range(len(sent))]
         # Initialise probabilities from '<s>' to the first word.
        viterbi[0] = {tag: (self.transitions['<s>'].logprob(tag) + self.emissions[tag].logprob(sent[0]), ['<s>', tag]) for tag in self.tags}
        
        # Build the Viterbi matrix for the rest of the sentence.
        for t, word in enumerate(sent[1:], start=1):
            for tag in self.tags:
                # Calculate the max log probability for the current tag from all previous tags and the best path.
                viterbi[t][tag] = max(
                    (viterbi[t-1][prev_tag][0] + self.transitions[prev_tag].logprob(tag) + self.emissions[tag].logprob(word), viterbi[t-1][prev_tag][1] + [tag])
                    for prev_tag in self.tags
                )

        # Identify the ending tag with the highest probability and retrieve the best path.
        _, predicted_tags = max((viterbi[-1][tag][0] + self.transitions[tag].logprob('</s>'), viterbi[-1][tag][1]) for tag in self.tags)
    
        return predicted_tags[1:]  # Exclude the initial '<s>' tag from the returned path.