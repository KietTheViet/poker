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

# ---- HAND STRENGTH FUNCTIONS ---- #
# All return "cardList" object or 0 #
# if specified hand isn't found.    #
# --------------------------------- #

def getPair(h):
    card_list = sorted(h.cards, key=lambda x: x.rank, reverse=True)
    for i in range(len(card_list)-1):
        if card_list[i+1].rank == card_list[i].rank:
            return cardList([card_list[i], card_list[i+1]])
    return 0

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
    # Create list of cards with no duplicate rankings
    card_list = []
    rank_list = []
    for c in sorted(h.cards, key=lambda x: x.rank, reverse=True):
        if c.rank not in rank_list:
            card_list.append(c)
            rank_list.append(c.rank)

    # Find highest straight
    for i in range(len(card_list)-4):
        if all(False for j in range(0,4) if card_list[i+j].rank != card_list[i+j+1].rank + 1):
            return cardList(card_list[i:i + 5])

    # If an ace is present, check for 5-high straight
    if card_list[0].rank == 14:
        # make sure there are five or more cards, then check ranks of the 4 lowest
        if len(card_list) >= 5 and all(False for i in range(1,5) if card_list[-i].rank != i+1):
            return cardList([card_list[-4], card_list[-3], card_list[-2], card_list[-1], card_list[0]])

    return 0

def getFlush(h):
    card_list = sorted(h.cards, key=lambda x: x.rank, reverse=True)

    # split hand list into sub-lists based on suits
    spades   = [c for c in card_list if c.suit == 's']
    clubs    = [c for c in card_list if c.suit == 'c']
    hearts   = [c for c in card_list if c.suit == 'h']
    diamonds = [c for c in card_list if c.suit == 'd']

    # return highest-ranking flush or 0 if none are found
    result = 0
    for suit in [spades, clubs, hearts, diamonds]:
        if len(suit) >= 5:
            if result == 0:
                result = cardList(suit[0:5])
            else:
                i = 0
                outranked = False
                while not outranked and i < 5:
                    if suit[i].rank > result.cards[i].rank:
                        result = cardList(suit[0:5])
                        outranked = True
                    elif suit[i].rank < result.cards[i].rank:
                        outranked = True
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
    hand = h
    flush = getFlush(h)
    removed_aces = []
    # While there exists a flush in the hand...
    while flush:
        # Check if the flush is also a straight
        if getStraight(flush):
            # NOTE: Must return "getStraight(flush)" instead
            # of simply "flush" because if the straight flush
            # is 5-high we have to make sure the 5 is at the
            # 0th index. Returning "flush" in this case would
            # cause the hand to appear as "Ax5x4x3x2x".
            return getStraight(flush)
        # Not a straight flush. Remove highest flush card and look again.
        if flush.cards[0].rank == 14:
            removed_aces.append(flush.cards[0])

        hand = hand.removeCards([flush.cards[0]])
        flush = getFlush(hand)

    # Check for 5-high straight (need to do
    # this because the above code removes
    # aces from the card list if they don't
    # make a royal flush).
    for ace in removed_aces:
        # Add ace back into the current hand
        hand.cards.append(ace)
        if getStraight(getFlush(hand)):
            return getStraight(getFlush(hand))
            # Note: This should always work fine. It is
            # implied that if an ace was removed, then
            # it had made a flush earlier. It is also
            # implied that if a flush was made, then
            # there should be at least one "four to a
            # flush" once we exit the previous while
            # loop. However, we could make this code
            # safer by asserting that the hand still
            # makes a flush when the ace is added back
            # (it always should) so that we don't
            # accidentally call getStraight() on the
            # value 0.
    return 0

def getRoyalFlush(h):
    straight_flush = getStraightFlush(h)
    if straight_flush and straight_flush.cards[0].rank == 14:
        return straight_flush
    return 0

# return strongest 5-card hand from "h"
def get5CardHand(h):
    if getFlush(h):
        if getStraightFlush(h):
            if getRoyalFlush(h):
                return getRoyalFlush(h)
            return getStraightFlush(h)
        if getFourOfAKind(h):
            # Note: Quads AND a flush should
            # not be possible in the same hand
            # in NLH. The function is written
            # this way to allow for portability
            # and use in other variants of poker.
            card_list = sorted(h.removeCards(getFourOfAKind(h).cards).cards, key=lambda x: x.rank, reverse=True)
            return cardList(getFourOfAKind(h).cards + card_list[0:1])
        if getFullHouse(h):
            # [See above note] The same applies
            # for full houses and flushes.
            return getFullHouse(h)
        return getFlush(h)

    if getStraight(h):
        if getFourOfAKind(h):
            # Same note applies.
            card_list = sorted(h.removeCards(getFourOfAKind(h).cards).cards, key=lambda x: x.rank, reverse=True)
            return cardList(getFourOfAKind(h).cards + card_list[0:1])
        if getFullHouse(h):
            return getFullHouse(h)
        return getStraight(h)

    if getPair(h):
        if getThreeOfAKind(h):
            if getFourOfAKind(h):
                card_list = sorted(h.removeCards(getFourOfAKind(h).cards).cards, key=lambda x: x.rank, reverse=True)
                return cardList(getFourOfAKind(h).cards + card_list[0:1])
            card_list = sorted(h.removeCards(getThreeOfAKind(h).cards).cards, key=lambda x: x.rank, reverse=True)
            return cardList(getThreeOfAKind(h).cards + card_list[0:2])
        if getTwoPair(h):
            card_list = sorted(h.removeCards(getTwoPair(h).cards).cards, key=lambda x: x.rank, reverse=True)
            return cardList(getTwoPair(h).cards + card_list[0:1])
        card_list = sorted(h.removeCards(getPair(h).cards).cards, key=lambda x: x.rank, reverse=True)
        return cardList(getPair(h).cards + card_list[0:3])

    return cardList(h.cards[0:5]) # order by rank, also out of bounds?


# MAIN FUNCTION
def main():
    # Create deck
    deck = []
    for suit in ['s', 'c', 'h', 'd']:
        for rank in range(2, 15):
            deck.insert(0, card(rank, suit))

    test_hand = cardList([deck[35], deck[1], deck[40], deck[0], deck[38], deck[30], deck[14], deck[13], deck[24], deck[23], deck[22], deck[25], deck[27]])
    print(test_hand)

    print("Pair:", getPair(test_hand))
    print("Two Pair:", getTwoPair(test_hand))
    print("Trips:", getThreeOfAKind(test_hand))
    print("Straight:", getStraight(test_hand))
    print("Flush:", getFlush(test_hand))
    print("Full House:", getFullHouse(test_hand))
    print("Quads:", getFourOfAKind(test_hand))
    print("Straight Flush:", getStraightFlush(test_hand))
    print("Royal Flush:", getRoyalFlush(test_hand))
    print("Best Hand:", get5CardHand(test_hand))

if __name__ == '__main__':
    main()

# REMINDERS:
# Two pair returns even when there's a full house
# Trips returns when there are quads and full houses.
# Flush may return highest flush instead of straight flush
