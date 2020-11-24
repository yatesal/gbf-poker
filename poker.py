import pyautogui, logging, os.path, random, time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)-4.5s] %(message)s",
    datefmt='%H:%M:%S',
    handlers=[
        logging.StreamHandler()
    ])

CARD_SUITS = ['hearts', 'diamonds', 'clubs', 'spades', 'None']
CARD_VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10',
               'Jack', 'Queen', 'King', 'Ace', 'Joker']

GAME_REGION = None
HI_LO_REGION = None
MID_BUTTON = None
LEFT_BUTTON = None
RIGHT_BUTTON = None

class Card():
    """Contains info regarding the value/suit/and coordinates of card"""
    def __init__(self, value, suit, region):
        self.value = value
        if suit != "":
            self.suit = " of " + suit
        else:
            self.suit = suit
        self.region = region
        
    def __repr__(self):
        return self.value + self.suit

class Chips():
    """The Chips object determines how many chips the player has won"""
    def __init__(self):
        self.total = 0
        self.wager = 1000
        
    def bet(self):
        """Reduces total number of chips won by wager amount (1000)"""  
        self.total = self.total - self.wager
        logging.info('Current total of chips won: ' + str(self.total))
        
    def win(self, hand_type):
        """Multiplies wager based on winning hand_type"""
        if hand_type == 'Royal Straight Flush':
            self.wager = self.wager * 250
        elif hand_type == 'Five of a Kind':
            self.wager = self.wager * 60
        elif hand_type == 'Straight Flush':
            self.wager = self.wager * 25
        elif hand_type == 'Four of a Kind':
            self.wager = self.wager * 20
        elif hand_type == 'Full House':
            self.wager = self.wager * 10
        elif hand_type == 'Flush':
            self.wager = self.wager * 4
        elif hand_type == 'Straight':
            self.wager = self.wager * 3
        elif hand_type == 'Three of a Kind' or hand_type == 'Two Pairs':
            self.wager = self.wager * 1
        
    def double(self):
        """Doubles wager amount after winning round of high-or-low"""
        self.wager = self.wager * 2
        
    def cash_out(self):
        """Cashes out number of chips won and resets wager amount"""
        self.total = self.total + self.wager
        logging.info('Amount of chips won: ' + str(self.wager))
        
    def reset_wager(self):
        """Resets wager amount to 1000 chips"""
        self.wager = 1000        

def main():
    """Runs the program"""
    find_board()
    set_up_game()
    play()
    
def find_board():
    """Locates gameboard or returns error"""
    logging.info("Please ensure the gameboard is on the screen")
    for i in range(10):
        try:
            region = pyautogui.onScreen(os.path.join('images', 'board', 'gameboard.png'))
        except TypeError:
            logging.error('Trying again')
            time.sleep(3)
        else:
            break
    else:
        logging.error("Error: unable to find gameboard. Exiting program.")
        quit()
        
def set_up_game():
    """Sets up game region and button coordinates"""
    global GAME_REGION, HI_LO_REGION, MID_BUTTON, LEFT_BUTTON, RIGHT_BUTTON
    
    region = find('board', 'gameboard')
    
    GAME_REGION = (region[0], region[1], region[2], 600)
    HI_LO_REGION = (region[0] + 300, region[1], region[2], 600)
    
    logging.info('game region is: ' + str(GAME_REGION))
    logging.info('high low region is: ' + str(HI_LO_REGION))
    
    MID_BUTTON = (GAME_REGION[0]+234, GAME_REGION[1]+522, 130, 38)
    LEFT_BUTTON = (MID_BUTTON[0]-100, MID_BUTTON[1], MID_BUTTON[2]-20, MID_BUTTON[3])
    RIGHT_BUTTON = (MID_BUTTON[0]+100, MID_BUTTON[1], MID_BUTTON[2]-20, MID_BUTTON[3])

    logging.info('deal/ok button region is: ' + str(MID_BUTTON))
    logging.info('no/high button region is: ' + str(LEFT_BUTTON))
    logging.info('yes/low button region is: ' + str(RIGHT_BUTTON))
    
def find(dir, file, coordinates=None, all=False):
    """Locates image on screen"""
    if coordinates == None:
        return(pyautogui.locateOnScreen(os.path.join('images', dir, file + '.png'),
                                       grayscale=True, confidence=0.97))
    elif all is not True:
        return(pyautogui.locateOnScreen(os.path.join('images', dir, file + '.png'),
                                    grayscale=True, confidence=0.97, region=coordinates))
    else:
        return(pyautogui.locateAllOnScreen(os.path.join('images', dir, file + '.png'),
                                    grayscale=True, confidence=0.97, region=coordinates))    

def play():
    """Loops through game until time runs out or user enters Ctrl+c"""
    chip_counter = Chips()    
    
    try:
        while time.time() < time.time() + 60*30:
            logging.info('Selecting DEAL button')
            select(MID_BUTTON)
            chip_counter.bet()
            time.sleep(3)        
            
            keep_cards()
            
            if find('board', 'win', GAME_REGION) is not None:
                logging.info('Success')                
                hand = rank(identify_hand())
                
                logging.info('Final Hand Rank: ' + hand[0])
                logging.info('Winning Cards: ' + str(hand[1]))
                                
                chip_counter.win(str(hand[0]))                                
                play_hi_lo(chip_counter)
                chip_counter.reset_wager()
            else:
                logging.info('Failure')
                pass                        
    except KeyboardInterrupt:
        logging.info('Ctrl-C entered. Game ended prematurely')
    finally:
        logging.info('Total amount of chips won: ' + str(chip_counter.total))
        logging.info('Ending program')
            
def select(region):
    """Takes region as an argument and moves the mouse to a random location within and clicks"""
    rand_x = random.randint(region[0], region[0]+region[2])
    rand_y = random.randint(region[1], region[1]+region[3])
    pyautogui.moveTo(rand_x, rand_y, 0.5)
    pyautogui.click(rand_x, rand_y)


def keep_cards():
    """Selects which cards should be kept based on hand rank"""
    keep = rank(identify_hand())

    logging.info('Preliminary Hand Rank: ' + keep[0])
    logging.info('Keeping cards: ' + str(keep[1]))

    for i in range(len(keep[1])):
        select(keep[1][i].region) 
        
    logging.info('Selecting OK button')
    select(MID_BUTTON)
    time.sleep(4)    
        
def identify_hand():
    """Identifies cards in hand and returns them as a list"""
    cards = []
    
    for card_value in enumerate(CARD_VALUES, 2):
        card_gen = find('value', card_value[1], GAME_REGION, all=True)
        for card_obj in card_gen:
            suit_region = (card_obj[0], card_obj[1], 80, 80)
            
            if card_value[1] == 'Joker':
                logging.info('Locating card')
                cards.append(Card(card_value[1], "", suit_region))
                break
                
            for card_suit in enumerate(CARD_SUITS):
                if card_value[0] > 10 and card_value[0] < 14:
                    find_suit = find('big_suit', card_suit[1], suit_region)
                else:
                    find_suit = find('suit', card_suit[1], suit_region)
                if find_suit is not None:
                    logging.info('Locating card')
                    cards.append(Card(card_value[1], card_suit[1], suit_region))
                    break
                    
    logging.info('Hand: ' + str(cards))
        
    return cards
                
def rank(hand):
    """Tests hand in order of highest ranking possible hands"""
    if is_royal_straight_flush(hand):
        return('Royal Straight Flush', is_royal_straight_flush(hand))
    elif is_five_of_a_kind(hand):
        return('Five of a Kind', is_five_of_a_kind(hand))
    elif is_straight_flush(hand):
        return('Straight Flush', is_straight_flush(hand))
    elif is_four_of_a_kind(hand):
        return('Four of a Kind', is_four_of_a_kind(hand))
    elif is_full_house(hand):
        return('Full House', is_full_house(hand))
    elif is_flush(hand):
        return('Flush', is_flush(hand))
    elif is_straight(hand):
        return('Straight', is_straight(hand))
    elif is_three_of_a_kind(hand):
        return('Three of a Kind', is_three_of_a_kind(hand))
    elif is_two_pairs(hand):
        return ('Two Pairs', is_two_pairs(hand))
    elif is_almost_flush(hand):
        return('Almost Flush', is_almost_flush(hand))
    elif is_almost_straight(hand):
        return('Almost Straight', is_almost_straight(hand))
    elif is_pair(hand):
        return('Pair', is_pair(hand))
    elif has_joker(hand):
        return ('Has Joker', [has_joker(hand)])
    else:    
        return('No cards to keep', []) 

def is_royal_straight_flush(hand):
    """Returns hand if cards are of incrementing value, share a suit, and cover values 10 - Ace"""
    if hand[0].value == '10' or hand[4].value == 'Joker' and hand[0].value == 'Jack':
        if is_straight_flush(hand):
            return hand

def is_five_of_a_kind(hand):
    """Returns hand if all cards share a value and a Joker exists"""
    if hand[0].value == hand[3].value:
        if hand[0].value == hand[4].value or hand[4].value == "Joker":
            return hand

def is_straight_flush(hand):
    """Returns hand if cards are of incrementing value and share a suit"""   
    if is_straight(hand) and is_flush(hand):
        return hand

def is_four_of_a_kind(hand):
    """Returns four cards from the hand if they have a matching value"""
    for i in range(len(hand)-3):
        if hand[i].value == hand[i+2].value:
            if hand[i].value == hand[i+3].value:
                return hand[i], hand[i+1], hand[i+2], hand[i+3]
            elif hand[4].value == 'Joker':
                return hand[i], hand[i+1], hand[i+2], hand[4]
                
def is_full_house(hand):
    """Returns hand if it contains a pair of matching values and a three of a kind"""
    if hand[0].value == hand[2].value:
        if hand[3].value == hand[4].value:
            return hand
    elif hand[0].value == hand[1].value:
        if hand[2].value == hand[4].value:
            return hand
        elif hand[2].value == hand[3].value and hand[4].value == 'Joker':
            return hand
    elif hand[1].value == hand[3].value and hand[4].value == 'Joker':
        return hand

def is_flush(hand):
    """Returns hand if all cards share a suit"""
    for i in range(len(hand)-1):
        if hand[i].suit != hand[i+1].suit and hand[i+1].value != "Joker":
            return

    return hand

def is_straight(hand):
    """Returns hand if cards are of incrementing value"""
    order = dict((key, value) for value, key in enumerate(CARD_VALUES))
        
    space_for_joker = 1    
        
    for i in range(len(hand)-1):
        if order[hand[i].value] != order[hand[i+1].value]-1 and hand[i+1].value != 'Joker':
            if hand[4].value == 'Joker' and space_for_joker > 0:
                space_for_joker = 0
            else:
                return
    
    return hand

def is_three_of_a_kind(hand):
    """Returns 3 cards of matching value if they exist in the hand"""
    for i in range(len(hand)-2):
        if hand[i].value == hand[i+1].value:
            if hand[i].value == hand[i+2].value:
                return [hand[i], hand[i+1], hand[i+2]]
            elif hand[4].value == 'Joker':
                return [hand[i], hand[i+1], hand[4]]
            
def is_two_pairs(hand):
    """Returns two pairs of cards if they exist in the hand"""
    keep = []
    for i in range(len(hand)-1):
        if hand[i].value == hand[i+1].value:
            keep.append(hand[i])
            keep.append(hand[i+1])
    if hand[4].value == 'Joker':
        keep.append(hand[4])
        for i in range(len(hand)-1):
            if hand[i] not in keep:
                keep.append(hand[i])
                break
    if len(keep) == 4:
        return keep
 
def is_almost_straight(hand):
    """Returns 4 cards from the hand if they're one card short of a straight."""   
    order = dict((key, value) for value, key in enumerate(CARD_VALUES))   
    keep = []
    
    for j in range(2):
        del keep[:]        
        
        if order[hand[4].value] == 13:
            keep.append(hand[4])
            spare_card = 2
        else:
            spare_card = 1
            
        keep.append(hand[j])
                
        for i in range(j, len(hand)-1):
            if order[hand[i].value] == order[hand[i+1].value]-1:
                keep.append(hand[i+1])
            elif order[hand[i].value] == order[hand[i+1].value]-2:
                keep.append(hand[i+1])
                spare_card = spare_card - 1
            elif order[hand[i].value] == order[hand[i+1].value]-3 and order[hand[4].value] == 13:
                keep.append(hand[i+1])
                spare_card = spare_card - 2
            else:
                break
            if len(keep) == 4 and spare_card > -1:
                return keep
            
def is_almost_flush(hand):
    """Returns 4 cards of the same suit if they exist in the hand"""   
    sorted_hand = sorted(hand, key= lambda x: x.suit, reverse=False)
    
    if sorted_hand[0].value == 'Joker':
        if sorted_hand[1].suit == sorted_hand[3].suit:
            return [sorted_hand[0], sorted_hand[1], sorted_hand[2], sorted_hand[3]]
        elif sorted_hand[2].suit == sorted_hand[4].suit:
            return [sorted_hand[0], sorted_hand[2], sorted_hand[3], sorted_hand[4]]
        else:
            return
    else:
        if sorted_hand[0].suit == sorted_hand[3].suit:
            return [sorted_hand[0], sorted_hand[1], sorted_hand[2], sorted_hand[3]]
        elif sorted_hand[1].suit == sorted_hand[4].suit:
            return [sorted_hand[1], sorted_hand[2], sorted_hand[3], sorted_hand[4]]
        else:
            return    
    
def is_pair(hand):
    """Returns a pair of cards if one exists in the hand"""    
    for i in range(len(hand)-1):
        if hand[i].value == hand[i+1].value:
            return [hand[i], hand[i+1]]

def has_joker(hand):
    """Returns a Joker if one exists in the hand"""   
    if hand[4].value == 'Joker':
        return hand[4]

def play_hi_lo(chip_counter):
    """Plays game of hi-or-low"""   
    logging.info('Starting game of high-or-low')
    select(RIGHT_BUTTON)
    time.sleep(3)
    
    while find('board', 'highlow', GAME_REGION)is not None:
        logging.info('Current wager amount: ' + str(chip_counter.wager))
        
        for left_card in enumerate(CARD_VALUES, 2):
            card = find('big_value', left_card[1], GAME_REGION)
            if card is not None:
                decide_hi_or_lo(left_card)
                break
        time.sleep(3)
        
        
        if pyautogui.locateOnScreen(os.path.join('images', 'board', 'highlowwin.png')) is not None:
            for right_card in enumerate(CARD_VALUES, 2):
                card = find('big_value', right_card[1], HI_LO_REGION)
                if card is not None:
                    logging.info('Right card value: ' + str(right_card[1]))
                    if quit_hi_or_lo(left_card, right_card, chip_counter) is True:                  
                        return
                    break                          
            if find('board', 'limit', GAME_REGION) is not None:
                limit_reached(chip_counter)
                return
            else:
                replay_hi_or_lo(left_card, right_card, chip_counter)
                
        else:
            logging.info('Lost game of high-or-low.')
            return
                        
def decide_hi_or_lo(left_card):
    """If card value is less than 8, goes high, otherwise goes low"""    
    logging.info('Left card value: ' + str(left_card[1]))
    if left_card[0] < 8:
        logging.info('Going high')
        select(LEFT_BUTTON)
    else:
        logging.info('Going low')
        select(RIGHT_BUTTON)
        
def quit_hi_or_lo(left_card, right_card, chip_counter):
    """Cash out if right card value is 7/8/9"""
    if right_card[0] > 6 and right_card[0] < 10:
        logging.info('Too risky. Ending game of high-or-low')
        if left_card[0] != right_card[0]:
            chip_counter.double()
        chip_counter.cash_out()
        select(LEFT_BUTTON)
        time.sleep(3)
        return True

def limit_reached(chip_counter):
    """Upon chip limit being reached, double wager and cash out"""
    logging.info('Limit reached. Ending game of high-or-low')
    chip_counter.double()
    chip_counter.cash_out()
    time.sleep(3)

def replay_hi_or_lo(left_card, right_card, chip_counter):
    """Double the wager amount if high-or-low doesn't end in draw and replay high-or-low"""
    logging.info('Continuing game of high-or-low')
    if left_card[0] != right_card[0]:
        chip_counter.double()
    select(RIGHT_BUTTON)
    time.sleep(3)

if __name__ == '__main__':
    main()
