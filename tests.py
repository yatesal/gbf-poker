import unittest

from poker import *

class TestCard(unittest.TestCase):

    def test_instantiate_card(self):
        """Tests that Card can be instantiated"""
        eight_of_hearts = Card('8', "hearts", (50, 50, 25, 25))
        self.assertEqual(str(eight_of_hearts), '8 of hearts')
        

    def test_receive_just_Joker_as_arg(self):
        """Tests that a Joker card returns just its name, no suit"""
        joker_card = Card('Joker', "", (0,0,50, 100))
        self.assertEqual(str(joker_card), 'Joker')
      
class TestChips(unittest.TestCase):        
    
    def test_instantiate_chips(self):
        """Tests that Chips can be instantiated"""
        chip_counter = Chips()
        self.assertEqual((chip_counter.total, chip_counter.wager), (0, 1000))

    def test_bet_reduces_total(self):
        """Tests that bet() reduces total"""
        chip_counter = Chips()
        chip_counter.bet()
        self.assertEqual(chip_counter.total, -1000)
    
    def test_win_with_royal_straight_flush(self):
        """Multiplies wager by 250"""
        chip_counter = Chips()
        chip_counter.win('Royal Straight Flush')
        self.assertEqual(chip_counter.wager, 250000)
        
    def test_win_with_five_of_a_kind(self):
        """Multiplies wager by 60"""
        chip_counter = Chips()
        chip_counter.win('Five of a Kind')
        self.assertEqual(chip_counter.wager, 60000)

    def test_win_with_straight_flush(self):
        """Multiplies wager by 25"""
        chip_counter = Chips()
        chip_counter.win('Straight Flush')
        self.assertEqual(chip_counter.wager, 25000)

    def test_win_with_four_of_a_kind(self):
        """Multiplies wager by 20"""
        chip_counter = Chips()
        chip_counter.win('Four of a Kind')
        self.assertEqual(chip_counter.wager, 20000)

    def test_win_with_full_house(self):
        """Multiplies wager by 10"""
        chip_counter = Chips()
        chip_counter.win('Full House')
        self.assertEqual(chip_counter.wager, 10000)

    def test_win_with_flush(self):
        """Multiplies wager by 4"""
        chip_counter = Chips()
        chip_counter.win('Flush')
        self.assertEqual(chip_counter.wager, 4000)

    def test_win_with_straight(self):
        """Multiplies wager by 3"""
        chip_counter = Chips()
        chip_counter.win('Straight')
        self.assertEqual(chip_counter.wager, 3000)

    def test_win_with_three_of_a_kind(self):
        """Multiplies wager by 1"""
        chip_counter = Chips()
        chip_counter.win('Three of a Kind')
        self.assertEqual(chip_counter.wager, 1000)

    def test_win_with_two_pair(self):
        """Multiplies wager by 1"""
        chip_counter = Chips()
        chip_counter.win('Two Pairs')
        self.assertEqual(chip_counter.wager, 1000)
    
    def test_double_increases_wager(self):
        """Tests that bet() reduces total"""
        chip_counter = Chips()
        chip_counter.double()
        self.assertEqual(chip_counter.wager, 2000)
    
    def test_cash_out_increases_total(self):
        """Tests that cashing out adds wager to total"""
        chip_counter = Chips()
        chip_counter.cash_out()
        self.assertEqual(chip_counter.total, 1000)

    def test_reset_wager_to_1000(self):
        """Tests that bet() reduces total"""
        chip_counter = Chips()
        chip_counter.wager = 5000
        chip_counter.reset_wager()
        self.assertEqual(chip_counter.wager, 1000)
        
class TestSelect(unittest.TestCase):

    """Tests that mouse position moves within given region"""
    def test_select_within_region(self):
        select((200, 300, 20, 30))
        position = pyautogui.position()
        self.assertTrue(200 <= position[0] <= 200+20)
        self.assertTrue(300 <= position[1] <= 300+30)
        
class TestLimitReached(unittest.TestCase):
    
    def test_limit_reached(self):
        """Tests that wager is doubled and added to total"""
        chip_counter = Chips()
        limit_reached(chip_counter)
        self.assertEqual(chip_counter.total, 2000)

class TestRank(unittest.TestCase):
    
    def test_returns_pair(self):
        """Finds pair in hand and returns 'Pair'"""
        hand = [Card('2', 'hearts', (0,0,0,0)), Card('5', 'hearts', (0,0,0,0)),
                Card('5', 'spades', (0,0,0,0)), Card('9', 'clubs', (0,0,0,0)),
                Card('10', 'hearts', (0,0,0,0))]
                
        self.assertEqual(rank(hand), ('Pair', [hand[1], hand[2]]))
        
    def test_return_no_cards(self):
        """Sees no winning hand and returns an empty list"""
        hand = [Card('2', 'hearts', (0,0,0,0)), Card('4', 'hearts', (0,0,0,0)),
                Card('5', 'spades', (0,0,0,0)), Card('9', 'clubs', (0,0,0,0)),
                Card('10', 'hearts', (0,0,0,0))]
        
        self.assertEqual(rank(hand), ('No cards to keep', []))
        
class TestRoyalStraightFlush(unittest.TestCase):

    def test_returns_royal_straight_flush(self):
        """Returns royal straight flush"""
        hand = [Card('10', 'hearts', (0,0,0,0)), Card('Jack', 'hearts', (0,0,0,0)),
                Card('Queen', 'hearts', (0,0,0,0)), Card('King', 'hearts', (0,0,0,0)),
                Card('Ace', 'hearts', (0,0,0,0))]
                
        self.assertEqual(is_royal_straight_flush(hand), hand)
        
    def test_returns_royal_straight_flush_with_Joker(self):
        """Returns royal straight flush with Joker"""
        hand = [Card('Jack', 'hearts', (0,0,0,0)), Card('Queen', 'hearts', (0,0,0,0)),
                Card('King', 'hearts', (0,0,0,0)), Card('Ace', 'hearts', (0,0,0,0)),
                Card('Joker', 'hearts', (0,0,0,0))]
                
        self.assertEqual(is_royal_straight_flush(hand), hand)

    def test_does_not_return_royal_straight_flush(self):
        """Returns None for royal straight flush"""
        hand = [Card('10', 'hearts', (0,0,0,0)), Card('Jack', 'hearts', (0,0,0,0)),
                Card('King', 'spade', (0,0,0,0)), Card('King', 'hearts', (0,0,0,0)),
                Card('Ace', 'hearts', (0,0,0,0))]
                
        self.assertEqual(is_royal_straight_flush(hand), None)

        
class TestFiveofaKind(unittest.TestCase):

    def test_returns_five_of_a_kind(self):
        """Returns five of a kind"""
        hand = [Card('10', 'hearts', (0,0,0,0)), Card('10', 'spades', (0,0,0,0)),
                Card('10', 'clubs', (0,0,0,0)), Card('10', 'diamonds', (0,0,0,0)),
                Card('Joker', '', (0,0,0,0))]
                
        self.assertEqual(is_five_of_a_kind(hand), hand)
        
    def test_does_not_return_five_of_a_kind(self):
        """Returns None for five of a kind"""
        hand = [Card('Jack', 'hearts', (0,0,0,0)), Card('Queen', 'hearts', (0,0,0,0)),
                Card('King', 'hearts', (0,0,0,0)), Card('Ace', 'hearts', (0,0,0,0)),
                Card('Joker', 'hearts', (0,0,0,0))]
                
        self.assertEqual(is_five_of_a_kind(hand), None)

class TestStraightFlush(unittest.TestCase):

    def test_returns_straight_flush(self):
        """Returns straight flush"""
        hand = [Card('4', 'hearts', (0,0,0,0)), Card('5', 'hearts', (0,0,0,0)),
                Card('6', 'hearts', (0,0,0,0)), Card('7', 'hearts', (0,0,0,0)),
                Card('8', 'hearts', (0,0,0,0))]
                
        self.assertEqual(is_straight_flush(hand), hand)
        
    def test_returns_straight_flush_with_Joker(self):
        """Returns straight flush with Joker"""
        hand = [Card('4', 'hearts', (0,0,0,0)), Card('5', 'hearts', (0,0,0,0)),
                Card('6', 'hearts', (0,0,0,0)), Card('8', 'hearts', (0,0,0,0)),
                Card('Joker', '', (0,0,0,0))]
                
        self.assertEqual(is_straight_flush(hand), hand)

    def test_does_not_return_straight_flush(self):
        """Returns None for straight flush"""
        hand = [Card('4', 'hearts', (0,0,0,0)), Card('5', 'hearts', (0,0,0,0)),
                Card('8', 'spade', (0,0,0,0)), Card('9', 'hearts', (0,0,0,0)),
                Card('Joker', '', (0,0,0,0))]
                
        self.assertEqual(is_straight_flush(hand), None)
        
class TestFourofaKind(unittest.TestCase):

    def test_returns_four_of_a_kind(self):
        """Returns four of a kind"""
        hand = [Card('10', 'hearts', (0,0,0,0)), Card('10', 'spades', (0,0,0,0)),
                Card('10', 'clubs', (0,0,0,0)), Card('10', 'diamonds', (0,0,0,0)),
                Card('Jack', 'clubs', (0,0,0,0))]
                
        self.assertEqual(is_four_of_a_kind(hand), (hand[0], hand[1], hand[2], hand[3]))
        
    def test_returns_four_of_a_kind_with_Joker(self):
        """Returns four of a kind with Joker"""
        hand = [Card('10', 'hearts', (0,0,0,0)), Card('10', 'spades', (0,0,0,0)),
                Card('10', 'clubs', (0,0,0,0)), Card('Jack', 'diamonds', (0,0,0,0)),
                Card('Joker', '', (0,0,0,0))]
                
        self.assertEqual(is_four_of_a_kind(hand), (hand[0], hand[1], hand[2], hand[4]))
        
    def test_does_not_return_four_of_a_kind(self):
        """Returns None for four of a kind"""
        hand = [Card('10', 'hearts', (0,0,0,0)), Card('10', 'spades', (0,0,0,0)),
                Card('10', 'clubs', (0,0,0,0)), Card('Queen', 'hearts', (0,0,0,0)),
                Card('King', 'hearts', (0,0,0,0))]
                
        self.assertEqual(is_four_of_a_kind(hand), None)

class TestFullHouse(unittest.TestCase):

    def test_returns_full_house(self):
        """Returns full house"""
        hand = [Card('2', 'hearts', (0,0,0,0)), Card('2', 'spades', (0,0,0,0)),
                Card('2', 'clubs', (0,0,0,0)), Card('3', 'diamonds', (0,0,0,0)),
                Card('3', 'clubs', (0,0,0,0))]
                
        self.assertEqual(is_full_house(hand), hand)
        
    def test_returns_full_house_with_Joker(self):
        """Returns full house with Joker"""
        hand = [Card('2', 'hearts', (0,0,0,0)), Card('3', 'spades', (0,0,0,0)),
                Card('3', 'clubs', (0,0,0,0)), Card('3', 'diamonds', (0,0,0,0)),
                Card('Joker', '', (0,0,0,0))]
                
        self.assertEqual(is_full_house(hand), hand)
        
    def test_does_not_return_full_house(self):
        """Returns None for full house"""
        hand = [Card('2', 'hearts', (0,0,0,0)), Card('2', 'spades', (0,0,0,0)),
                Card('3', 'clubs', (0,0,0,0)), Card('3', 'hearts', (0,0,0,0)),
                Card('King', 'hearts', (0,0,0,0))]
                
        self.assertEqual(is_full_house(hand), None)
        
class TestFlush(unittest.TestCase):

    def test_returns_flush(self):
        """Returns flush"""
        hand = [Card('2', 'hearts', (0,0,0,0)), Card('3', 'hearts', (0,0,0,0)),
                Card('4', 'hearts', (0,0,0,0)), Card('5', 'hearts', (0,0,0,0)),
                Card('6', 'hearts', (0,0,0,0))]
                
        self.assertEqual(is_flush(hand), hand)
        
    def test_returns_flush_with_Joker(self):
        """Returns flush with Joker"""
        hand = [Card('2', 'spades', (0,0,0,0)), Card('3', 'spades', (0,0,0,0)),
                Card('4', 'spades', (0,0,0,0)), Card('5', 'spades', (0,0,0,0)),
                Card('Joker', '', (0,0,0,0))]
                
        self.assertEqual(is_flush(hand), hand)
        
    def test_does_not_return_flush(self):
        """Returns None for flush"""
        hand = [Card('2', 'hearts', (0,0,0,0)), Card('2', 'hearts', (0,0,0,0)),
                Card('3', 'hearts', (0,0,0,0)), Card('3', 'spades', (0,0,0,0)),
                Card('King', 'hearts', (0,0,0,0))]
                
        self.assertEqual(is_flush(hand), None)
        
class TestStraight(unittest.TestCase):

    def test_returns_straight(self):
        """Returns straight"""
        hand = [Card('4', 'clubs', (0,0,0,0)), Card('5', 'hearts', (0,0,0,0)),
                Card('6', 'hearts', (0,0,0,0)), Card('7', 'spades', (0,0,0,0)),
                Card('8', 'hearts', (0,0,0,0))]
                
        self.assertEqual(is_straight(hand), hand)
        
    def test_returns_straight_with_Joker(self):
        """Returns straight with Joker"""
        hand = [Card('4', 'clubs', (0,0,0,0)), Card('6', 'hearts', (0,0,0,0)),
                Card('7', 'spades', (0,0,0,0)), Card('8', 'hearts', (0,0,0,0)),
                Card('Joker', '', (0,0,0,0))]
                
        self.assertEqual(is_straight(hand), hand)

    def test_does_not_return_straight(self):
        """Returns None for straight"""
        hand = [Card('4', 'hearts', (0,0,0,0)), Card('5', 'hearts', (0,0,0,0)),
                Card('6', 'spade', (0,0,0,0)), Card('9', 'hearts', (0,0,0,0)),
                Card('10', 'spade', (0,0,0,0))]
                
        self.assertEqual(is_straight(hand), None)
        
class TestThreeofaKind(unittest.TestCase):

    def test_returns_three_of_a_kind(self):
        """Returns three of a kind"""
        hand = [Card('10', 'hearts', (0,0,0,0)), Card('10', 'spades', (0,0,0,0)),
                Card('10', 'clubs', (0,0,0,0)), Card('Jack', 'diamonds', (0,0,0,0)),
                Card('Queen', 'clubs', (0,0,0,0))]
                
        self.assertEqual(is_three_of_a_kind(hand), [hand[0], hand[1], hand[2]])
        
    def test_returns_three_of_a_kind_with_Joker(self):
        """Returns three_of_a_kind_with_Joker"""
        hand = [Card('10', 'hearts', (0,0,0,0)), Card('10', 'spades', (0,0,0,0)),
                Card('Jack', 'clubs', (0,0,0,0)), Card('Queen', 'diamonds', (0,0,0,0)),
                Card('Joker', '', (0,0,0,0))]
                
        self.assertEqual(is_three_of_a_kind(hand), [hand[0], hand[1], hand[4]])
        
    def test_does_not_return_three_of_a_kind(self):
        """Returns None for three of a kind"""
        hand = [Card('10', 'hearts', (0,0,0,0)), Card('Jack', 'spades', (0,0,0,0)),
                Card('Jack', 'clubs', (0,0,0,0)), Card('Queen', 'hearts', (0,0,0,0)),
                Card('King', 'hearts', (0,0,0,0))]
                
        self.assertEqual(is_three_of_a_kind(hand), None)
        
class TestTwoPairs(unittest.TestCase):

    def test_returns_two_pairs(self):
        """Returns two pairs"""
        hand = [Card('10', 'hearts', (0,0,0,0)), Card('10', 'spades', (0,0,0,0)),
                Card('Jack', 'clubs', (0,0,0,0)), Card('Jack', 'diamonds', (0,0,0,0)),
                Card('Queen', 'clubs', (0,0,0,0))]
                
        self.assertEqual(is_two_pairs(hand), [hand[0], hand[1], hand[2], hand[3]])
        
    def test_returns_two_pairs_with_Joker(self):
        """Returns two pairs with Joker"""
        hand = [Card('10', 'hearts', (0,0,0,0)), Card('Jack', 'spades', (0,0,0,0)),
                Card('Jack', 'clubs', (0,0,0,0)), Card('Queen', 'diamonds', (0,0,0,0)),
                Card('Joker', '', (0,0,0,0))]
                
        self.assertEqual(is_two_pairs(hand), [hand[1], hand[2], hand[4], hand[0]])
        
    def test_does_not_return_two_pairs(self):
        """Returns None for two pairs"""
        hand = [Card('10', 'hearts', (0,0,0,0)), Card('Jack', 'spades', (0,0,0,0)),
                Card('Jack', 'clubs', (0,0,0,0)), Card('Queen', 'hearts', (0,0,0,0)),
                Card('King', 'hearts', (0,0,0,0))]
                
        self.assertEqual(is_two_pairs(hand), None)

class TestAlmostStraight(unittest.TestCase):

    def test_returns_almost_straight(self):
        """Returns almost straight"""
        hand = [Card('4', 'clubs', (0,0,0,0)), Card('5', 'hearts', (0,0,0,0)),
                Card('7', 'hearts', (0,0,0,0)), Card('8', 'spades', (0,0,0,0)),
                Card('9', 'hearts', (0,0,0,0))]
                
        self.assertEqual(is_almost_straight(hand), [hand[0], hand[1], hand[2], hand[3]])
        
    def test_returns_almost_straight_with_Joker(self):
        """Returns almost straight with Joker"""
        hand = [Card('4', 'clubs', (0,0,0,0)), Card('6', 'hearts', (0,0,0,0)),
                Card('7', 'spades', (0,0,0,0)), Card('10', 'hearts', (0,0,0,0)),
                Card('Joker', '', (0,0,0,0))]
                
        self.assertEqual(is_almost_straight(hand), [hand[4], hand[0], hand[1], hand[2]])

    def test_does_not_return_almost_straight(self):
        """Returns None for almost straight"""
        hand = [Card('4', 'hearts', (0,0,0,0)), Card('5', 'hearts', (0,0,0,0)),
                Card('6', 'spade', (0,0,0,0)), Card('9', 'hearts', (0,0,0,0)),
                Card('10', 'spade', (0,0,0,0))]
                
        self.assertEqual(is_almost_straight(hand), None)
        
class TestAlmostFlush(unittest.TestCase):

    def test_returns_almost_flush(self):
        """Returns almost flush"""
        hand = [Card('4', 'clubs', (0,0,0,0)), Card('5', 'clubs', (0,0,0,0)),
                Card('6', 'spades', (0,0,0,0)), Card('7', 'clubs', (0,0,0,0)),
                Card('8', 'clubs', (0,0,0,0))]
                
        self.assertEqual(is_almost_flush(hand), [hand[0], hand[1], hand[3], hand[4]])
        
    def test_returns_almost_flush_with_Joker(self):
        """Returns almost flush with Joker"""
        hand = [Card('4', 'hearts', (0,0,0,0)), Card('6', 'hearts', (0,0,0,0)),
                Card('7', 'hearts', (0,0,0,0)), Card('8', 'clubs', (0,0,0,0)),
                Card('Joker', '', (0,0,0,0))]
                
        self.assertEqual(is_almost_flush(hand), [hand[4], hand[0], hand[1], hand[2]])

    def test_does_not_return_almost_flush(self):
        """Returns None for almost flush"""
        hand = [Card('4', 'hearts', (0,0,0,0)), Card('5', 'hearts', (0,0,0,0)),
                Card('6', 'spade', (0,0,0,0)), Card('9', 'clubs', (0,0,0,0)),
                Card('10', 'spade', (0,0,0,0))]
                
        self.assertEqual(is_almost_flush(hand), None)

class TestIsPair(unittest.TestCase):
    
    def test_returns_pair(self):
        """Returns a pair"""
        hand = [Card('4', 'clubs', (0,0,0,0)), Card('5', 'diamonds', (0,0,0,0)),
                Card('6', 'spades', (0,0,0,0)), Card('6', 'clubs', (0,0,0,0)),
                Card('8', 'clubs', (0,0,0,0))]   

        self.assertEqual(is_pair(hand), [hand[2], hand[3]])
         
    def test_does_not_return_pair(self):
        """Returns None instead of pair"""
        hand = [Card('4', 'clubs', (0,0,0,0)), Card('5', 'diamonds', (0,0,0,0)),
                Card('8', 'spades', (0,0,0,0)), Card('10', 'clubs', (0,0,0,0)),
                Card('Jack', 'clubs', (0,0,0,0))]   

        self.assertEqual(is_pair(hand), None)
         
class TestHasJoker(unittest.TestCase):

    def test_returns_joker(self):
        """Returns joker"""
        hand = [Card('4', 'clubs', (0,0,0,0)), Card('6', 'diamonds', (0,0,0,0)),
                Card('8', 'spades', (0,0,0,0)), Card('10', 'clubs', (0,0,0,0)),
                Card('Joker', '', (0,0,0,0))]   

        self.assertEqual(has_joker(hand), hand[4])
         
    def test_does_not_return_joker(self):
        """Returns joker"""
        hand = [Card('4', 'clubs', (0,0,0,0)), Card('6', 'diamonds', (0,0,0,0)),
                Card('8', 'spades', (0,0,0,0)), Card('10', 'clubs', (0,0,0,0)),
                Card('King', '', (0,0,0,0))]   

        self.assertEqual(has_joker(hand), None)
        

        
if __name__ == '__main__':
    unittest.main()
