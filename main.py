cardChar = {10: "T", 11: "J", 12: "Q", 13: "K", 14: "A"}

def toChar(num):
    if num > 9:
        return cardChar[num]
    return num

# exists to print hands more easily
class cardList:
    def __init__(self, cards):
        self.cards = cards
    def removeCards(self, toRemove):
        result = cardList(self.cards.copy())
        for c in toRemove:
            result.cards.remove(c)
        return result
    def __str__(self):
        result = "|"
        for c in self.cards:
            result += str(c) + "|"
        return result

# exists to print cards more easily :) (as opposed to using dicts)
class card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        if self.rank in cardChar:
            return cardChar[self.rank] + str(self.suit)
        return str(self.rank) + str(self.suit)

# HAND STRENGTH FUNCTIONS
# returns cardList or 0 if pair not found
def getPair(h):
    card_list = sorted(h.cards, key=lambda x: x.rank, reverse=True)
    for i in range(len(card_list)-1):
        if card_list[i+1].rank == card_list[i].rank:
            return cardList([card_list[i], card_list[i+1]])
    return 0

# returns cardList or 0 if pair not found
def getTwoPair(h):
    # Check for first pair and save cards
    if not getPair(h):
        return 0
    first_pair = getPair(h).cards

    # Remove first pair from hand being checked
    hand = h.removeCards(first_pair)

    # Check for second pair with different rank from first pair
    while getPair(hand) and getPair(hand).cards[0].rank == first_pair[0].rank:
        hand = hand.removeCards(getPair(hand).cards)
    if not getPair(hand):
        return 0
    second_pair = getPair(hand).cards

    return cardList(first_pair + second_pair)

def getThreeOfAKind(h):
    card_list = sorted(h.cards, key=lambda x: x.rank, reverse=True)
    for i in range(len(card_list)-2):
        if card_list[i+2].rank == card_list[i+1].rank == card_list[i].rank:
            return cardList(card_list[i:i+3])
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
    card_list = sorted(h.cards, key=lambda x: x.rank, reverse=True)

    # split hand list into sub-lists based on suits
    spades   = [c for c in card_list if c.suit == 's']
    clubs    = [c for c in card_list if c.suit == 'c']
    hearts   = [c for c in card_list if c.suit == 'h']
    diamonds = [c for c in card_list if c.suit == 'd']

    # return highest-ranking flush or 0 if none are found
    high_rank = 0
    result = 0
    for suit in [spades, clubs, hearts, diamonds]:
        if len(suit) >= 5 and suit[0].rank > high_rank:
            high_rank = suit[0].rank
            result = cardList(suit[0:5])
    return result

def getFullHouse(h):
    # Check for trips and save cards
    if not getThreeOfAKind(h):
        return 0
    trips = getThreeOfAKind(h).cards

    # Remove trips from hand being checked
    hand = h.removeCards(trips)

    # Check for pair and save cards
    if not getPair(hand):
        return 0
    pair = getPair(hand).cards

    return cardList(trips + pair)

def getFourOfAKind(h):
    card_list = sorted(h.cards, key=lambda x: x.rank, reverse=True)
    for i in range(len(card_list)-3):
        if card_list[i+3].rank == card_list[i+2].rank == card_list[i+1].rank == card_list[i].rank:
            return cardList(card_list[i:i+4])
    return 0

def getStraightFlush(h):
    pass

def getRoyalFlush(h):
    pass


# MAIN FUNCTION
def main():
    # Create deck
    deck = []
    for suit in ['s', 'c', 'h', 'd']:
        for rank in range(2, 15):
            deck.insert(0, card(rank, suit))

    test_hand = cardList([deck[0], deck[15], deck[3], deck[14], deck[2], deck[16], deck[41], deck[20], deck[25], deck[24], deck[6], deck[7]])
    print(test_hand)

    print("Pair:", getPair(test_hand))
    print("Two Pair:", getTwoPair(test_hand))
    print("Trips:", getThreeOfAKind(test_hand))
    print("Quads:", getFourOfAKind(test_hand))
    # print("Straight:", getStraight(hand))
    print("Flush:", getFlush(test_hand))
    print("Full House:", getFullHouse(test_hand))

if __name__ == '__main__':
    main()

# REMINDERS:
# May need to return multiple values in funcs in case of ties (ex. if same one pair, need to check kicker)
# Two pair returns even when there's a full house
# Trips returns when there are quads and full houses.
# Flush may return highest flush instead of straight flush
