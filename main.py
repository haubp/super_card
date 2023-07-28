import random
import arcade


class Card:
    def __init__(self, n, s):
        self.num = n
        self.suit = s


class Cards:
    def __init__(self):
        self.cards = []
        for n in range(1, 14):
            for s in ["heart", "diamond", "club", "spade"]:
                self.cards.append(Card(n, s))

    def shuffle(self):
        for i in range(50):
            start = random.randrange(1, 51)
            end = random.randrange(start + 1, 53)
            t = self.cards[end - 1]
            tt = self.cards[start]
            for j in range(start, end - 1):
                temp = self.cards[j + 1]
                self.cards[j + 1] = tt
                tt = temp
            self.cards[start] = t


class Player:
    def __init__(self):
        self.cards = []


class Blackjack:
    def __int__(self):
        self.cards = Cards()
        self.cards.shuffle()



def main():
    b = Blackjack()

    p1 = Player()
    p2 = Player()



if __name__ == "__main__":
    main()
