class TerminalAttempt:
    def __init__(self, word_list):
        word_list = [word.upper() for word in word_list]
        word_lengths = [len(word) for word in word_list]
        lengths_agree = [length == word_lengths[0] for length in word_lengths[1:]]

        if all(lengths_agree):
            self.word_list = word_list
            self.candidates = word_list
        else:
            disagreements = [
                word
                for word, agreement in zip(word_list[1:], word_lengths)
                if not agreement
            ]

            error_str = f"Word lengths disagree\n{word_list[0]}:{disagreements}"
            raise ValueError(error_str)
        
        self.calculate_similarities()

    @staticmethod
    def word_similarity(word_1, word_2):
        similarity_score = sum([l_1 == l_2 for l_1, l_2 in zip(word_1, word_2)])
        return similarity_score

    def calculate_similarities(self):
        similarity_dict = {
            word_1: {
                word_2: (
                    TerminalAttempt.word_similarity(word_1, word_2)
                    if word_1 != word_2
                    else len(word_1)
                )
                for word_2 in self.word_list
            }
            for word_1 in self.word_list
        }
        self.similarity_dict = similarity_dict

    def get_viable_candidates(self, actual_similarity):
        """
        eg: true_scoredict = {"stop": 1, "shop": 2, "swap": 1, "wasp": 2, "womp": None}
        """
        valid_candidates = [
            candidate_word
            for candidate_word in self.word_list
            if all(
                [
                    self.similarity_dict[candidate_word][word] == score
                    for word, score in actual_similarity.items()
                    if score
                ]
            )
        ]

        return valid_candidates


if __name__ == "__main__":
    candidates = ["STOP", "SHOT", "SWAP", "WOMP", "SHOP"]
    attempt = TerminalAttempt(candidates)
    attempt.calculate_similarities()
    # print(attempt.similarity_dict)
    # lets pretend the actual word is SHOP
    # actual_similarity = {'STOP': 3, 'SHOT': 3, 'SWAP': 2, 'WOMP': 1, 'SHOP': 4}
    actual_similarity = {
        "STOP": None,
        "SHOT": None,
        "SWAP": 2,
        "WOMP": None,
        "SHOP": None,
    }
    viable_candidates = attempt.get_viable_candidates(actual_similarity)
    print(viable_candidates)
