# Durak - a card game with 2-6 players using 36 cards
import random
                                                    # Classes


# Class, responsible for running the game
class Game(object):
    def __init__(self, players):
        SUITS = ['Hearts', 'Spades', 'Clubs', 'Diamonds']
        VALUES = [6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']

        self.players = players
        self.gameover = False
        self.firstturn = None
        self.all_cards = []
        self.turns_num = 0
        self.rating = 1
        self.winners = []
        self.VALUE_LIST = ['J', 'Q', 'K', 'A']
        self.ran_ind_player = random.randrange(len(self.players))

        # Making up all 36 combinations of suits and values
        for suit in SUITS:
            for value in VALUES:
                card = value, suit
                self.all_cards.append(card)

    # Returns a random card
    def give_rand_card(self):
        random_card = self.all_cards[random.randrange(len(self.all_cards))]
        return random_card

    # Returns a random card and deletes it
    def give_rand_card_with_del(self):
        if len(self.all_cards) != 0:
            random_card = self.all_cards[random.randrange(len(self.all_cards))]
            for card_to_del in self.all_cards:
                if card_to_del[0] == random_card[0] and card_to_del[1] == random_card[1]:
                    card_to_del_ind = self.all_cards.index(card_to_del)
                    del self.all_cards[card_to_del_ind]
            return random_card
        else:
            return None

    # Responsible for handing cards to player
    def hand_cards(self, cards, player):
        if cards:
            for card in cards:
                player.hand.append(card)
            print(len(self.all_cards))
            return player.hand
        else:
            print(len(self.all_cards))
            if len(self.all_cards) == 0:
                print("There are no more cards in deck!\n")
            return player.hand

    # Exception check
    def player_ind_exception_check(self):
        if self.ran_ind_player + 1 <= len(self.players) - self.rating:
            self.ran_ind_player += 1
        else:
            self.ran_ind_player = 0
        return self.ran_ind_player

    def player_ind_check(self):
        if self.ran_ind_player > len(self.players) - 1:
            self.ran_ind_player = 0
        return self.ran_ind_player

    # Responsible for giving out the cards
    def card_giveout(self):
        cards_to_give_count = 0
        for person in self.players:
            if len(self.all_cards) != 0:
                for _ in range(6 - person.get_num_of_cards()):
                    cards_to_give_count += 1

        equal = True

        len_hand = len(self.players[0].hand)
        for player in self.players:
            if len(player.hand) != len_hand:
                equal = False

        if cards_to_give_count <= len(self.all_cards):
            for person in self.players:
                cards_to_give = []
                if len(self.all_cards) != 0:
                    for _ in range(6 - person.get_num_of_cards()):
                        card = game.give_rand_card_with_del()
                        if card != None:
                            cards_to_give.append(card)
                    self.hand_cards(cards_to_give, person)

        else:
            if equal:
                if len(self.all_cards) % len(self.players) == 0:
                    card_num_per_player = len(self.all_cards) // len(self.players)
                    for player in self.players:
                        for card_ind in range(card_num_per_player):
                            player.hand.append(self.all_cards[card_ind])
                            self.all_cards.remove(self.all_cards[card_ind])
                    if len(self.all_cards) != 0:
                        for player in self.players:
                            for card_ind in range(len(self.all_cards)):
                                player.hand.append(self.all_cards[card_ind])
                                self.all_cards.remove(self.all_cards[card_ind])
            else:
                for person in self.players:
                    cards_to_give = []
                    if len(self.all_cards) != 0:
                        for _ in range(6 - person.get_num_of_cards()):
                            card = game.give_rand_card_with_del()
                            if card != None:
                                cards_to_give.append(card)
                        self.hand_cards(cards_to_give, person)

    def JQKA_check(self, card):
        if isinstance(card[0], int):
            value_def = int(card[0])
        else:
            value_def = self.VALUE_LIST.index(card[0]) + 11
        return value_def

    # Processing the round / checking if the value of card is J, Q, K, A
    def turn_processing(self, attack_card, defend_card, defender, status):
        value_def = self.JQKA_check(defend_card)
        value_att = self.JQKA_check(attack_card)

        # Case with trumps
        if attack_card[1] == TRUMP and defend_card[1] == TRUMP:
            if value_def > value_att:
                winner = "D"
            else:
                winner = "A"

        else:
            # Case with defender trump only
            if defend_card[1] == TRUMP and attack_card[1] != TRUMP:
                winner = "D"

            # Case with attacker trump only
            elif defend_card[1] != TRUMP and attack_card[1] == TRUMP:
                winner = "A"

            # Case with both not trumps
            else:
                if defend_card[1] == attack_card[1]:
                    if value_def > value_att:
                        winner = "D"
                    else:
                        winner = "A"
                else:
                    winner = "A"


        # Exception check
        if status == "A":
            if winner == "A":
                print("Attacker have won the turn")
                defender.hand.append(attack_card)
                defender.hand.append(defend_card)
                defender.lose_turn = True
                self.ran_ind_player = self.player_ind_exception_check()
            elif winner == "D":
                print("Defender have won the turn")

        elif status == "S":
            if winner == "A":
                if not defender.lose_turn:
                    print("Attackers have won the turn")
                    defender.lose_turn = True
                    self.ran_ind_player = self.player_ind_exception_check()
                    defender.hand += self.cards_used_this_turn
                if defender.lose_turn:
                    print("Attackers have won the turn")
            else:
                print("Defender have won the turn")


    # Responsible for starting a new round
    def round(self):
        self.cards_used_this_turn = []
        num_cards_used_to_att = 0
        self.card_giveout()

        # Player 1 attack turn
        current_player = self.players[self.player_ind_check()]
        attack_card = current_player.attack_turn()
        self.cards_used_this_turn.append(attack_card)
        current_player.use_cards(attack_card)
        num_cards_used_to_att += 1

        # Changing the index
        self.ran_ind_player = self.player_ind_exception_check()

        # Player 2 defend turn
        current_player = defender = self.players[self.player_ind_check()]
        defend_card = current_player.defend_turn()
        self.cards_used_this_turn.append(defend_card)
        current_player.use_cards(defend_card)

        # Processing
        self.turn_processing(attack_card, defend_card, defender, 'A')

        # Searching for other players with the same value cards
        for player in self.players:
            cards_with_same_value = []
            if player.get_status() != 'D':
                for card in player.hand:
                    if attack_card[0] == card[0] or defend_card[0] == card[0]:
                        cards_with_same_value.append(card)

                # Printing all the accessible support cards
                if len(cards_with_same_value) != 0:
                    print('\t\t', player.name.title())
                    for card_num in range(len(cards_with_same_value)):
                        print('\t' + str(card_num + 1), cards_with_same_value[card_num])

                decision = ''
                while (decision.lower() != 'n') and (len(cards_with_same_value) != 0) and (num_cards_used_to_att < 6) and len(self.players[self.ran_ind_player].hand) != 0:
                    decision = player.ask_yes_no("Do you want to use the card?").lower()

                    # Exception check
                    if (decision == 'n') or (len(cards_with_same_value) == 0) or (num_cards_used_to_att >= 6):
                        if current_player.lose_turn:
                            self.ran_ind_player += 1
                        if decision == 'n':
                            print("You ended your turn.")
                            break
                        if len(cards_with_same_value) == 0:
                            print("You have no cards left")
                            break
                        if num_cards_used_to_att >= 5:
                            print("The max possible amount of cards is reached")
                            break
                        if len(self.players[self.ran_ind_player].hand) != 0:
                            print("There are no more cards in defender's hand")
                            break


                    elif decision == 'y':
                        # Support turn
                        for card_num in range(len(cards_with_same_value)):
                            print('\t' + str(card_num + 1), cards_with_same_value[card_num])
                        current_player = player
                        attack_card = current_player.support_turn(cards_with_same_value)
                        del cards_with_same_value[cards_with_same_value.index(attack_card)]
                        current_player.use_cards(attack_card)
                        self.cards_used_this_turn.append(attack_card)
                        print(len(cards_with_same_value), "cards remaining for support")
                        num_cards_used_to_att += 1

                        # Defence turn
                        if not defender.lose_turn:
                            defend_card = defender.defend_turn()
                            self.cards_used_this_turn.append(defend_card)
                            defender.use_cards(defend_card)
                            # Turn processing
                            self.turn_processing(attack_card, defend_card, defender, 'S')
                        else:
                            defender.hand.append(attack_card)

        # Check if anybody won the game in this round
        for player in self.players:
            player.lose_turn = False
            if player.get_winner():
                self.winners += player, self.rating
                self.rating += 1
                print("Winner is", player.name + "!!!")

        # Counting turn number
        self.turns_num += 1

    # Responsible for ending a game session
    def end_game(self):
        if self.rating == len(self.players):
            self.gameover = True
        return self.gameover


class Player(object):
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.winner = False
        self.first_order = False
        self.status = None
        self.lose_turn = False

    # Responsible for returning the answer to the question
    def ask_yes_no(self, message):
        ans = input(str(message) + "(y/n): ")
        return ans

    # Responsible for tracking the use of cards by a player
    def use_cards(self, card):
        del self.hand[self.hand.index(card)]

    def get_status(self):
        return self.status

    # Responsible for getting a status of the player
    def get_winner(self):
        if len(self.hand) == 0 and len(game.all_cards) == 0:
            self.winner = True
        return self.winner

    # Responsible for getting the number of cards
    def get_num_of_cards(self):
        return len(self.hand)

    def reveal_cards(self):
        print("\tThe PRIME value is: ", TRUMP.upper())
        for i in range(len(self.hand)):
            print(str(i + 1), self.hand[i])

    # Responsible for the attack turn
    def attack_turn(self):
        self.status = 'A'
        print("Now is the turn of player %s" % self.name.title())
        self.reveal_cards()
        curr_card_ind = int(input("\nType in the position of the card that you have chosen for attack(1-" + str(len(self.hand)) + "): "))
        current_card = self.hand[curr_card_ind - 1]
        print("Player", self.name.title(), "have chosen the card \t\"" + str(current_card[0]), str(current_card[1]).upper() + "\".")
        return current_card

    # Responsible for the defence turn
    def defend_turn(self):
        self.status = 'D'
        print("Now is the defence of player %s" % self.name.title())
        self.reveal_cards()
        curr_card_ind = int(input("\nType in the position of the card that you have chosen for defence(1-" + str(len(self.hand)) + "): "))
        current_card = self.hand[curr_card_ind - 1]
        print("Player", self.name.title(), "have chosen the card \t\"" + str(current_card[0]), str(current_card[1]).upper() + "\".")
        return current_card

    # Responsible for the support turn
    def support_turn(self, cards):
        self.status = 'S'
        print("Now is the support turn of player %s" % self.name.title())
        curr_card_ind = int(input("Enter the number of the card, you choose: ")) - 1
        current_card = cards[curr_card_ind]
        print("Player", self.name.title(), "have chosen the card \t\"" + str(current_card[0]), str(current_card[1]).upper() + "\".")
        return current_card


                            # Main
# Main part to run the process
ans = ''

while ans.lower() != 'n':
    ans = input("Are you going to start a new game(y/n): ")

    if ans.lower() == 'n':
        print("You ended your session, see ya!")

    elif ans.lower() == 'y':
        players = []
        pl_num = int(input("How many players?(2-6): "))
        for player_num in range(pl_num):
            name = input("Enter the name of player #" + str(player_num + 1) + ": ")
            new_player = Player(name)
            players.append(new_player)
        print("\t\tHere is the list of players: ", end="\n")
        for player in players:
            print(player.name.title())
        game = Game(players)

        # Selecting trump value
        TRUMP = game.give_rand_card()[1]

        # Starting the game
        #while not game.end_game():
        while len(game.winners) == 0:
            game.round()