import itertools
import numpy as np

class PokerHand:
    def __init__(self,hand):
        self.check_size(hand) #Validation of the size of the poker hand
        self.check_hand(hand) # validation of the right format of the card
        self.transform_to_numeric(hand) #Transform the string into card values 
        
    def check_size(self,hand):
        #Method to check the size of the card hand
        if(len(hand.split())!=5):
            raise Exception("Incorrect number's cars: %s, expected 5 cards" % len(hand.split()))
    
    def check_card(self,card):  
        return card[0] in self.one and card[1] in self.two      
    
    def check_hand(self,hand):
        #Method to detect if the value and symbol of the card are correct
        self.one  = [str(i) for i in range(2,10)]+['T','J','Q','K','A']
        self.two = ['S','H','D','C']
        for card in hand.split():
            if(not self.check_card(card)):
                raise Exception(' Incorrect format of car : %s' % (card))
                
    def transform_to_numeric(self,hand):
        #Method to transform the poker hand into numeric and simbols values
        value_dict = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        value_dict.update((str(x), x) for x in range(2,10))
        self.hand=hand.split()
        self.hand=sorted([(value_dict[r],s) for r,s in self.hand],reverse=True)
        self.values = sorted([c[0] for c in self.hand], reverse=True)  
    
    def get_rank(self):
        #Method to get the rank of the hand      
        #Get the symbols of the poker hand
        suits = [c[1] for c in self.hand]
        #Evalute Flush,straight and  Straight Flush
        flush = len(set(suits)) == 1
        #Considering the case A,2,3,4,5 as possible straight Flush
        straight = (((max(self.values )-min(self.values ))==4) or  self.values == [14, 5, 4, 3, 2]) and len(set(self.values))==5
        # Straight and fLush
        if straight and flush:
            return [(8,[max(self.values )],self.values )if (self.values !=[14, 5, 4, 3, 2] ) else (8,5,self.values)][0]
        elif flush: return (5,[max(self.values)],self.values) #Flush
        elif straight: return (4,[max(self.values)],self.values) #Straight
        trips = []
        pairs = []
        for v, group in itertools.groupby(self.values):
            count = sum(1 for _ in group)
            if count == 4: 
                return (7, [v], self.values) #Four of a kind
            elif count == 3: trips.append(v)
            elif count == 2: pairs.append(v)
        if trips:
            if pairs:
                return(6,[max(trips)],self.values) #Full house
            else:
                return(3,[max(trips)],self.values) # Three of a kind
        elif len(pairs)==1:
            return(len(pairs),[max(pairs)],self.values) #One pair
        elif len(pairs)==2:
            return(len(pairs),pairs,self.values) #Two pairs
        else:
            return(0,[max(self.values)],self.values) #High card
    def max_vector(self,a,b):
        #Method for detect the wich vector of cards is the greatest
        a=np.array(sorted(a,reverse=True))
        b=np.array(sorted(b,reverse=True))
        c=a-b
        for i in c:
            if i>0:
                return 'WIN'
            elif i<0:
                return 'LOSS'
        return 'NONE'
    
    def compare_with(self,hand2):
        #Method for comparing the two poker hands
        a=self.get_rank()
        b=hand2.get_rank()
        if a[0]!=b[0]:
            return ['WIN' if (a[0]>b[0]) else 'LOSS'][0]
        elif a[0]!=2:
            if a[1]!=b[1]:
                return ['WIN' if (a[1]>b[1]) else 'LOSS'][0]
            else:
                set_val_a=list(set(a[2])-set(a[1]))
                set_val_b=list(set(b[2])-set(b[1]))
                return self.max_vector(set_val_a,set_val_b)
        else:
            #a[0]==2,(len(pairs),pairs,values) 
            if self.max_vector(a[1],b[1])=='NONE':
                one_a=list(set(a[2])-set(a[1]))[0]
                one_b=list(set(b[2])-set(b[1]))[0]
                return ['WIN' if one_a>one_b else 'LOSS'][0]
            else: 
                return self.max_vector(a[1],b[1])