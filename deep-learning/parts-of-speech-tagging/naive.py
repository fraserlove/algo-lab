from hmm import HMM

class Naive(HMM):

    def __init__(self, train_sents, test_sents):
        super().__init__(train_sents, test_sents)

    def predict(self, sent):
        """ Predict the most likely sequence of POS tags for a given sentence using the Naive algorithm. """
        predicted_tags = ['<s>']
        
        for word in sent:
            tag_probs = {} # Store the probability of each tag for the word.

            # Calculate the probability for each possible tag based on transition and emission probabilities.
            for tag in self.tags:
                tag_probs[tag] = self.transitions[predicted_tags[-1]].prob(tag) * self.emissions[tag].prob(word)
            
            # Predict the tag with the highest probability for the word.
            predicted_tags.append(max(tag_probs, key=tag_probs.get))

        return predicted_tags[1:]