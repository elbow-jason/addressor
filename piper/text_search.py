from piper.strings import similarity

class TextSearch(object):

    @staticmethod
    def count_scores(all_words):
        """
        Accepts a list of sets of strings
        """
        scored = {}
        for wordset in all_words:
            for word in wordset:
                score = scored.setdefault(word, 0)
                scored[word] += 1
        return scored

    @staticmethod
    def score_with_similarity(scores_list, word):
        return [(item, score, similarity(word, item)) for (item, score) in scores_list]

    @staticmethod
    def shingle_count(word):
        return len(TextSearch.shinglize(word))

    @staticmethod
    def shinglize(word):
        if len(word) < 3:
            return [word]
        shingles = []
        for i in range(len(word)+3):
            shingle = word[_zero_min(i-3):i]
            if len(shingle) >= 2:
                shingles.append(shingle)
        return shingles

    def __init__(self):
        self._shingles_dict = dict() #shingles to word hashes sets
        self._words_dict = dict() # hashes to words sets

    def has_word(self, word):
        found = self._words_dict.get(hash(word), set())
        return word in found

    def search(self, word, limit=None):
        found = []
        for shingle in TextSearch.shinglize(word):
            shingle_set = self._shingles_dict.get(shingle, set())
            found.append(shingle_set)
        all_words = []
        for word_hashes in found:
            for word_hash in word_hashes:
                all_words.append(self._words_dict[word_hash])
        scores_dict = TextSearch.count_scores(all_words)
        scores_list = ((item, score) for (item, score) in scores_dict.items())
        scores_list = sorted(scores_list, key=lambda item: 0-item[1])
        scores_list = TextSearch.score_with_similarity(scores_list, word)
        if limit:
            return scores_list[:limit]
        else:
            return scores_list


    def add_word(self, word):
        word_hash = hash(word)
        shingles = TextSearch.shinglize(word)
        words_set = self._words_dict.setdefault(word_hash, set())
        words_set.add(word)
        for s in shingles:
            self._add_shingle(s, word_hash)

    def _add_shingle(self, shingle, word_hash):
        the_set = self._shingles_dict.setdefault(shingle, set())
        the_set.add(word_hash)

def _zero_min(i):
    if i < 0:
        return 0
    return i