import random

cardChar = {10: "T", 11: "J", 12: "Q", 13: "K", 14: "A"}
cardRank = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}

def toChar(num):
    if num > 9:
        return cardChar[num]
    return num

class cardList:
    def __init__(self, cards):
        self.cards = cards
    def removeCards(self, toRemove):
        result = cardList(self.cards.copy())
        for c in toRemove:
            result.cards.remove(c)
        return result
    def __add__(self, other):
        return cardList(self.cards + other.cards)
    def __str__(self):
        result = "|"
        for c in self.cards:
            result += str(c) + "|"
        return result

class card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    def __str__(self):
        if self.rank in cardChar:
            return cardChar[self.rank] + str(self.suit)
        return str(self.rank) + str(self.suit)
    def __eq__(self, other):
        if self.rank == other.rank and self.suit == other.suit:
            return True
        return False

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
    # Create list of cards with no unique rankings
    card_list = []
    rank_list = []
    for c in sorted(h.cards, key=lambda x: x.rank, reverse=True):
        if c.rank not in rank_list:
            card_list.append(c)
            rank_list.append(c.rank)

    # Search for straight
    for i in range(len(card_list)-4):
        if all(False for j in range(0,4) if card_list[i+j].rank != card_list[i+j+1].rank + 1):
            return cardList(card_list[i:i + 5])

    # No straight found. If an ace is
    # present, check for 5-high straight
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
                    i += 1
    return result

def getFullHouse(h):
    # Check for trips
    if not getThreeOfAKind(h):
        return 0
    trips = getThreeOfAKind(h).cards

    # Remove trips from hand being checked
    hand = h.removeCards(trips)

    # Check for pair
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

# return strongest possible 5-card hand from cardList
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
            if getFullHouse(h):
                return getFullHouse(h)
            card_list = sorted(h.removeCards(getThreeOfAKind(h).cards).cards, key=lambda x: x.rank, reverse=True)
            return cardList(getThreeOfAKind(h).cards + card_list[0:2])
        if getTwoPair(h):
            card_list = sorted(h.removeCards(getTwoPair(h).cards).cards, key=lambda x: x.rank, reverse=True)
            return cardList(getTwoPair(h).cards + card_list[0:1])
        card_list = sorted(h.removeCards(getPair(h).cards).cards, key=lambda x: x.rank, reverse=True)
        return cardList(getPair(h).cards + card_list[0:3])

    return cardList(sorted(h.cards, key=lambda x: x.rank, reverse=True)[0:5])

def getHandRank(h):
    if getFlush(h):
        if getStraightFlush(h):
            if getRoyalFlush(h):
                return 9
            return 8
        if getFourOfAKind(h):
            return 7
        if getFullHouse(h):
            return 6
        return 5

    if getStraight(h):
        if getFourOfAKind(h):
            return 7
        if getFullHouse(h):
            return 6
        return 4

    if getPair(h):
        if getThreeOfAKind(h):
            if getFourOfAKind(h):
                return 7
            if getFullHouse(h):
                return 6
            return 3
        if getTwoPair(h):
            return 2
        return 1

    return 0

def getWinningHands(cardLists):
    winning_hands = []
    for hand in cardLists:
        if len(winning_hands) == 0:
            winning_hands.append(get5CardHand(hand))
        elif getHandRank(hand) > getHandRank(winning_hands[0]):
            winning_hands = [get5CardHand(hand)]
        elif getHandRank(hand) == getHandRank(winning_hands[0]):
            # Hand ranks are the same. Check individual card ranks.
            i = 0
            beaten = False
            while not beaten and i < 5:
                if get5CardHand(hand).cards[i].rank != winning_hands[0].cards[i].rank:
                    beaten = True
                else: # <-- else is needed to preserve i's value for the following "if beaten" statement
                    i += 1
            if beaten:
                # Check if the current hand beat the previous winning hand(s)
                if get5CardHand(hand).cards[i].rank > winning_hands[0].cards[i].rank:
                    winning_hands = [get5CardHand(hand)]
            else:
                # Tie. Add current hand to winning_hands.
                winning_hands.append(get5CardHand(hand))
    return winning_hands

# Deck handling functions

def shuffle(deck):
    result = []
    while len(deck) > 0:
        result.insert(random.randint(0,len(result)), deck.pop())
    return result

def main():
    # Create deck
    deck = []
    for suit in ['s', 'c', 'h', 'd']:
        for rank in range(2, 15):
            deck.insert(0, card(rank, suit))

    welcome_msg = ("=========================================\n"
                   "Welcome to the Poker Hand Evaluator!\n"
                   "This program takes a deck of any number\n"
                   "of cards from 1 to 52 and determines the\n"
                   "best 5-card poker hand that can be made\n"
                   "using those cards.\n"
                   "=========================================")

    cmd_msg = ("Commands:\n"
               "help:   List commands\n"
               "test:   Evaluate a random deck of a given\n"
               "        length\n"
               "custom: Create a custom deck to evaluate\n"
               "hand:   Simulate a poker hand between two\n"
               "        players and determine the winner\n"
               "score:  See total results of all simulated\n"
               "        hands so far\n"
               "exit:   End program\n"
               "or press ENTER to quickly test a deck of\n"
               "random length.\n"
               "=========================================")

    print(welcome_msg)
    input("Press ENTER to begin")
    print(cmd_msg)

    hands = 0
    hero_wins = 0
    villain_wins = 0
    num_ties = 0

    while 1:
        cmd = input("Enter a command: ")
        if cmd == 'help':
            print(cmd_msg)
        elif cmd == 'test':
            num_cards = None
            # get number of cards to include in the deck
            while type(num_cards) != int or num_cards not in range(1,53):
                try:
                    num_cards = int(input("Enter number of cards (1-52): "))
                    if num_cards < 1 or num_cards > 52:
                        print("Invalid number")
                except:
                    print("Invalid input")
            deck = shuffle(deck)
            test_hand = cardList(deck[0:num_cards])
            print("Test Hand:", test_hand)
            print("Best Hand:", get5CardHand(test_hand))
        elif cmd == "custom":
            card_insert_msg = ("Enter \"deck\" to see the current deck, \"done\"\n"
                               "if finished, or the name of a card to insert\n"
                               "(ex. \"Th\", \"Ac\", etc.): ")
            card_list = []
            test_hand = cardList(card_list)
            card_name = ""
            # get cards to include in deck
            while card_name != "done" or len(card_list) == 0:
                card_name = input(card_insert_msg)
                if card_name == "done" and len(card_list) == 0:
                    print("You must add at least 1 card.")
                elif card_name == "deck":
                    print("Current deck:", test_hand)
                elif len(card_name) == 2:
                    try:
                        if card_name[1] in ['s', 'c', 'h', 'd']:
                            if card_name[0] in cardRank:
                                new_card = card(cardRank[card_name[0]], card_name[1])
                                if new_card not in card_list:
                                    card_list.append(new_card)
                                    test_hand = cardList(card_list)
                                    print("Inserted", new_card)
                                else:
                                    print("Duplicate card entered")
                            else:
                                new_card = card(int(card_name[0]), card_name[1])
                                if new_card not in card_list:
                                    card_list.append(new_card)
                                    test_hand = cardList(card_list)
                                    print("Inserted", new_card)
                                else:
                                    print("Duplicate card entered")
                        else:
                            print("Invalid card")
                    except:
                        print("Invalid card")
                else:
                    print("Invalid card")
            print("Test Hand:", test_hand)
            print("Best Hand:", get5CardHand(test_hand))
        elif cmd == 'hand':
            deck = shuffle(deck)
            hero = cardList(deck[0:2])
            villain = cardList(deck[2:4])
            board = cardList(deck[4:9])
            print("Hero:   ", hero)
            print("Villain:", villain)
            print("Board:  ", board)
            winning_hands = getWinningHands([hero + board, villain + board])
            hands += 1
            if len(winning_hands) == 1:
                if winning_hands[0].cards == get5CardHand(hero + board).cards:
                    message = "Hero wins with "
                    hero_wins += 1
                else:
                    message = "Villain wins with "
                    villain_wins += 1
            else:
                message = "Tie between:"
                num_ties += 1
            for h in winning_hands:
                message += " " + str(h)
            print(message)
        elif cmd == 'score':
            if hands == 0:
                print("No hands have been simulated.\n"
                      "Use command \"hand\" to simulate.")
            else:
                print("Hero:   ", hero_wins, "(" + str(round(float(hero_wins) / float(hands) * 100, 2)) + "%)")
                print("Villain:", villain_wins, "(" + str(round(float(villain_wins) / float(hands) * 100, 2)) + "%)")
                print("Ties:   ", num_ties, "(" + str(round(float(num_ties) / float(hands) * 100, 2)) + "%)")
        elif cmd == "":
            deck = shuffle(deck)
            test_hand = cardList(deck[0:random.randint(1,52)])
            print("Test Hand:", test_hand)
            print("Best Hand:", get5CardHand(test_hand))
        elif cmd == "exit":
            break
        else:
            print("Invalid command")

    input("\nThanks for using the poker hand evaluator!\n"
          "Press ENTER to quit")

    # print("Pair:", getPair(test_hand))
    # print("Two Pair:", getTwoPair(test_hand))
    # print("Trips:", getThreeOfAKind(test_hand))
    # print("Straight:", getStraight(test_hand))
    # print("Flush:", getFlush(test_hand))
    # print("Full House:", getFullHouse(test_hand))
    # print("Quads:", getFourOfAKind(test_hand))
    # print("Straight Flush:", getStraightFlush(test_hand))
    # print("Royal Flush:", getRoyalFlush(test_hand))
    # print("Best Hand:", get5CardHand(test_hand), "Rank:", getHandRank(test_hand))

if __name__ == '__main__':
    main()

# Notes:
# Certain hand functions may return higher ranking
# hands if found. For example, getThreeOfAKind can
# return a hand identical to getFourOfAKind because
# of the nature of the poker hands. This does not
# affect the correctness of the final 5-card hand
# returned by get5CardHand because the higher
# ranking hand will always be chosen in the end.
