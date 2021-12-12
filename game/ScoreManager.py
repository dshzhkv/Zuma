class ScoreManager:
    def __init__(self):
        self.score = 0
        self.lives = 2
        self.is_win = False
        self.is_lose = False

    def add_score(self, score):
        self.add_lives(score)
        self.score += score

    def add_lives(self, score):
        for i in range(self.score + 1, self.score + score + 1):
            if i % 500 == 0:
                self.lives += 1

    def win(self):
        self.is_win = True

    def lose(self):
        self.is_lose = True
