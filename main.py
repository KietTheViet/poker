cardChar = {10: "T", 11: "J", 12: "Q", 13: "K", 14: "A"}

class card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        if self.rank in cardChar:
            return cardChar[self.rank] + str(self.suit)
        return str(self.rank) + str(self.suit)

def toChar(num):
    if num > 9:
        return cardChar[num]
    return num

# "CHECK HAND STRENGTH" FUNCTIONS
# returns rank of top pair or 0
def getPair(h):
    hand = sorted(h, key=lambda x: x.rank, reverse=True)
    for i in range(len(hand)-1):
        if hand[i+1].rank == hand[i].rank:
            return hand[i].rank
    return 0

# returns tuple (topRank, secondRank) or 0 if one or fewer pairs found
def getTwoPair(h):
    top_rank = 0
    hand = sorted(h, key=lambda x: x.rank, reverse=True)

    i = 0
    while i < len(hand)-1:
        if hand[i+1].rank == hand[i].rank:
            if not top_rank:
                top_rank = hand[i].rank
                i += 1
            else:
                return top_rank, hand[i].rank
        i += 1
            # QUADS MAY BE SEEN AS TWO OF THE SAME PAIR
    return 0

def getThreeOfAKind(h):
    hand = sorted(h, key=lambda x: x.rank, reverse=True)
    for i in range(len(hand)-2):
        if hand[i+2].rank == hand[i+1].rank == hand[i].rank:
            return hand[i].rank
    return 0

def getStraight(h):
    hand = sorted(h, key=lambda x: x.rank, reverse=True)

    # remove duplicate ranks
    # CODE HERE

    for i in range(len(hand)-4):
        straight = True
        for j in range(hand[i].rank, i-5):
            if hand[j].rank != hand[j+1].rank + 1:
                straight = False
        if straight:
            return hand[i].rank
        # DUPLICATE RANKS CAUSE PROBLEMS

    # Check for 5-high straight (ace is considered low)
    if hand[0].rank == 14 and hand[-1].rank == 2:
        straight = True
        for i in range(-4, -1):
            if hand[j].rank != hand[j + 1].rank + 1:
                straight = False
            if straight:
                return 5

    return 0

def getFlush(h):
    print("FLUSH:")
    hand = sorted(h, key=lambda x: x.suit)
    for card in hand:
        print(card)
    return 0
    # INCOMPLETE

def getFullHouse(h):
    top_rank = 0
    hand = sorted(h, key=lambda x: x.rank, reverse=True)
    top_rank = getThreeOfAKind(hand)
    # INCOMPLETE

def getFourOfAKind(h):
    hand = sorted(h, key=lambda x: x.rank, reverse=True)
    for i in range(len(hand)-3):
        if hand[i+3].rank == hand[i+2].rank == hand[i+1].rank == hand[i].rank:
            return hand[i].rank
    return 0

def getStraightFlush(h):
    pass

def getRoyalFlush(h):
    pass

def getHandStrength():
    pass

# MAIN FUNCTION
def main():
    # Create deck
    deck = []
    for suit in ['s', 'c', 'h', 'd']:
        for rank in range(2, 15):
            deck.insert(0, card(rank, suit))

    test_hand = [deck[0], deck[11], deck[10], deck[12], deck[9], deck[8], deck[22], deck[33], deck[44]]
    hand = sorted(test_hand, key=lambda x: x.rank, reverse=True)

    hand_str = ""
    for c in test_hand:
        hand_str += str(c) + " "
    print("Hand:", hand_str + "\n")d

    print("Pair:", getPair(hand))
    print("Two Pair:", getTwoPair(hand))
    print("Trips:", getThreeOfAKind(hand))
    print("Quads:", getFourOfAKind(hand))
    print("Straight:", getStraight(hand))
    print("Flush:", getFlush(hand))

if __name__ == '__main__':
    main()

# REMINDERS:
# May need to return multiple values in funcs in case of ties (ex. if same one pair, need to check kicker)