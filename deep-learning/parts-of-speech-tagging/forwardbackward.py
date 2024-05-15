from math import log, exp
from hmm import HMM

min_log_prob = float('-inf') # log(0)

# Adding a list of probabilities represented as log probabilities.
def logsumexp(vals):
    if len(vals) == 0:
        return min_log_prob
    m = max(vals)
    if m == min_log_prob:
        return min_log_prob
    else:
        return m + log(sum([exp(val - m) for val in vals]))

class ForwardBackward(HMM):

    def __init__(self, train_sents, test_sents):
        super().__init__(train_sents, test_sents)

    def forward(self, sent):
        """ Calculate the forward probabilities for a given sentence. """
        # Initialise the forward matrix with a size for each word.
        forward = [{} for _ in range(len(sent))]
        # Initialise forward probabilities from '<s>' to the first word.
        forward[0] = {tag: self.transitions['<s>'].logprob(tag) + self.emissions[tag].logprob(sent[0]) for tag in self.tags}

        # Build the forward matrix for the rest of the sentence.
        for t, word in enumerate(sent[1:], start=1):
            for tag in self.tags:
                # Calculate the probability for the current tag from all previous tags.
                forward[t][tag] = logsumexp([
                    forward[t - 1][prev_tag] + self.transitions[prev_tag].logprob(tag) + self.emissions[tag].logprob(word)
                    for prev_tag in self.tags
                ])

        forward[-1]['</s>'] = logsumexp([forward[-1][tag] + self.transitions[tag].logprob('</s>') for tag in self.tags])
        forward.insert(0, {'<s>': 0}) # Log probability of the start state '<s>' is 0.
        return forward

    def backward(self, sent):
        """ Calculate the backward probabilities for a given sentence. """
        # Initialise backward matrix with a size for each word plus start '<s>' and end '</s>' states.
        backward = [{} for _ in range(len(sent) + 2)]
        # Initialise backward probabilities from the last word to '</s>'.
        backward[-2] = {tag: self.transitions[tag].logprob('</s>') for tag in self.tags}

        # Build the backward matrix for the rest of the sentence, moving backwards.
        for t in range(len(sent) - 1, -1, -1):
            word = sent[t]
            for tag in self.tags:
                backward[t][tag] = logsumexp([
                    backward[t + 1][next_tag] + self.transitions[tag].logprob(next_tag) + self.emissions[next_tag].logprob(word)
                    for next_tag in self.tags
                ])

        # Compute the backward probability for the start state '<s>'.
        backward[0]['<s>'] = logsumexp([
            backward[1][tag] + self.transitions['<s>'].logprob(tag) + self.emissions[tag].logprob(sent[0])
            for tag in self.tags
        ])
        return backward

    def predict(self, sent):
        """ Predict the most likely tags for each word in a sentence using forward and backward probabilities. """
        forward = self.forward(sent)
        backward = self.backward(sent)
        predicted_tags = [
            max(self.tags, key=lambda tag: forward[t + 1][tag] + backward[t + 1][tag])
            for t in range(len(sent))
        ]
        return predicted_tags