import random
import re
import time

#win/lose bet amounts

wincond = 0
#1: playerlose , 2: playerbj , 3: player win, 4: tie
#defining 52 cards

number=[]
for n in range(52):
    number.append(str(n))
#print(number)

spades=[]
clubs=[]
hearts=[]
diamonds=[]
cards=[]
suits=[spades,clubs,diamonds,hearts]
special=[0,12,11,10]
specialnames=['Ace','King','Queen','Jack']
def addcard(suitname,b):
    if suit==suitname:
        for i in range(13):
            if i in special:
                suitname.append(str(specialnames[special.index(i)]+' of '+str(b)))
            else:
                suitname.append(str(i+1)+' of '+str(b))
for suit in suits:
    addcard(spades,'Spades')
    addcard(clubs,'Clubs')
    addcard(hearts,'Hearts')
    addcard(diamonds,'Diamonds')
def totalcards(totalsuit):
    for item in totalsuit:
        cards.append(item)
totalcards(spades)
totalcards(clubs)
del hearts[13:]
totalcards(hearts)
totalcards(diamonds)

#print(cards)
#print('Total cards: ', len(cards))

#Draw cards

availcards = random.sample(cards, 52)

dealer = []
player = []

#print(availcards)

def draw(owner):
    owner.append(availcards[0])
    availcards.remove(availcards[0])

#Starting hand

draw(dealer)
draw(player)
draw(dealer)
draw(player)

#debug:
#player = ['Ace of','Jack']
#dealer = ['Ace','Queen']

print("\n----------- Dealer's hand: ", dealer[0], '----------------------')
#print('dealers hand:',dealer)
print("----------- Your cards: ", player[0],', ', player[1], '-----------\n')

#debug:
#print("****dealer's hand: ", dealer)
#print(len(availcards))

# instant blackjack conditions

def blackjack(person):
    if person[0][0] == 'A':
        if person[1][0] == 'J' or person[1][0] == 'Q' or person[1][0] == 'K' or person[1][0] == '1':
            return True
    elif person[1][0] == 'A':
        if person[0][0] == 'J' or person[0][0] == 'Q' or person[0][0] == 'K' or person[0][0] == '1':
            return True
    else:
        return False

#print('Dealer blackjack: ', blackjack(dealer)) ## DEBUG:

if blackjack(dealer) == True:
    if blackjack(player) == True:
        print('Tie: Both hands are blackjacks.')
        wincond = 4
    else:
        print('Dealer blackjack! You lose the hand.')
        print(""" Dealer's hand:""")
        wincond = 1
        for i in dealer:
            print(i)
else:
    if blackjack(player) == True:
        print('Blackjack! You win the hand.')
        wincond = 2

#Card scoring system
def score(card):
    if card[0] == '1' or card[0] == 'J' or card[0] == 'Q' or card[0] == 'K' :
        return 10
    elif card[0] == 'A':
        return 11
    elif int(card[0]) >= 2 and  int(card[0]) <= 9:
        return int(card[0])

playerscore = score(player[0]) + score(player[1])
dealerscore = score(dealer[0]) + score(dealer[1])

#print('Your score: ',playerscore)

#Player's options

if blackjack(player) == False and blackjack(dealer) == False:
    print('''
--------------------------------------------------------------
                F: Hit
                C: Stand
                W: Double Down
                Q: Split
--------------------------------------------------------------
''') #display options

#test acecount:
#player = ['A', '7' ]
#playerscore = score(player[0]) + score(player[1])
#availcards = ['A','1']

acecount = 0
for i in player:
    if i[0] == 'A':
        acecount = acecount+ 1
dacecount = 0
for i in dealer:
    if i[0] == 'A':
        dacecount = dacecount + 1

while True:
    if blackjack(dealer) == True or blackjack(player) == True:
        break
    choice = input().strip().upper()
    if choice == 'F':

        draw(player)
        playerscore = playerscore + score(player[-1])
        print('You drew the ',player[-1])
        #print('your cards:',player) ## DEBUG:
        #print('acecount: ', acecount)
        #print('score: ',playerscore)

        #player.append('A')

        #print(playerscore)
        if player[-1][0] == 'A':
            acecount = acecount+1

        if playerscore > 21:
            if acecount >=1:
                playerscore = playerscore - 10
                if playerscore >21:
                    print('You have gone bust!')
                    wincond = 1
                    break
                acecount = acecount - 1
                #print( 'Ace detected, score - 10 ')## DEBUG:
                #print('acecount', acecount)
                #print('playerscore: ' ,playerscore)
                #print(player) ## DEBUG:
            else:
                print('You have gone bust!')
                wincond = 1
                #print('playerscore: ', playerscore)
                break

    if choice == 'C':
        print('You have chosen to stand.')
        #print('playerscore = ',playerscore)
        print("\nDealer's hand: \n ")
        for i in range(2):
            print(dealer[i-1])
        break

#Dealer's  draw
while dealerscore < 17 :
    time.sleep(1)
    draw(dealer)
    print(dealer[-1])

    if dealer[-1][0] == 'A':
        dacecount = dacecount+1
    #print('dealer drew the ',dealer[-1])
    dealerscore = dealerscore + score(dealer[-1])
    #print('dealerscore:',dealerscore)
    if dealerscore > 21:
        if dacecount >=1:
            dealerscore = dealerscore - 10
            if dealerscore >21:
                time.sleep(1)
                print('Dealer has gone bust, you win!')
                wincond = 3
            dacecount = dacecount - 1
            #print( 'Ace detected in dealers hand, dealerscore - 10 ')## DEBUG:
            #print('dacecount', dacecount)
            #print('dealerscore: ' ,dealerscore)
            #print(dealer) ## DEBUG:
        else:
            time.sleep(1)
            print('Dealer has gone bust, you win!')
            wincond = 3
            #print('dealerscore: ', dealerscore)
            break

if dealerscore >= 17 and dealerscore <22:
    if dealerscore > playerscore and blackjack(player) == False:
        wincond = 1
        print("""--------------------------------------------------------------
        Dealer wins.
-------------------------------------------------------------- """ )

#    if blackjack(dealer) == False:
#        print("Dealer's hand:")
#        for i in dealer:
#            print(i)

    if dealerscore < playerscore and playerscore < 22:
        print('You win!')
        wincond = 3
    if dealerscore == playerscore:
        print('Tie.')
        wincond = 4
