import random
import time
import threading

# 카드 생성. 그림도 각 객체에 들아가도록 함
class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value
        card_picture = 0
        if color == "Green":
            if value == 1:
                card_picture = ''
            elif value == 2:
                card_picture = ''
            elif value == 3:
                card_picture = ''
            elif value == 4:
                card_picture = ''
            elif value == 5:
                card_picture = ''
            elif value == 6:
                card_picture = ''
            elif value == 7:
                card_picture = ''
            elif value == 8:
                card_picture = ''
            elif value == 9:
                card_picture = ''
            elif value == "Skip":
                card_picture = ''
            elif value == "Draw2":
                card_picture = ''
            elif value == "Reverse":
                card_picture = ''
            elif value == "Wild":
                card_picture = ''
        elif color == "Red":
            if value == 1:
                card_picture = ''
            elif value == 2:
                card_picture = ''
            elif value == 3:
                card_picture = ''
            elif value == 4:
                card_picture = ''
            elif value == 5:
                card_picture = ''
            elif value == 6:
                card_picture = ''
            elif value == 7:
                card_picture = ''
            elif value == 8:
                card_picture = ''
            elif value == 9:
                card_picture = ''
            elif value == "Skip":
                card_picture = ''
            elif value == "Draw2":
                card_picture = ''
            elif value == "Reverse":
                card_picture = ''
            elif value == "Wild":
                card_picture = ''
        elif color == "Blue":
            if value == 1:
                card_picture = ''
            elif value == 2:
                card_picture = ''
            elif value == 3:
                card_picture = ''
            elif value == 4:
                card_picture = ''
            elif value == 5:
                card_picture = ''
            elif value == 6:
                card_picture = ''
            elif value == 7:
                card_picture = ''
            elif value == 8:
                card_picture = ''
            elif value == 9:
                card_picture = ''
            elif value == "Skip":
                card_picture = ''
            elif value == "Draw2":
                card_picture = ''
            elif value == "Reverse":
                card_picture = ''
            elif value == "Wild":
                card_picture = ''
        elif color == "Yellow":
            if value == 1:
                card_picture = ''
            elif value == 2:
                card_picture = ''
            elif value == 3:
                card_picture = ''
            elif value == 4:
                card_picture = ''
            elif value == 5:
                card_picture = ''
            elif value == 6:
                card_picture = ''
            elif value == 7:
                card_picture = ''
            elif value == 8:
                card_picture = ''
            elif value == 9:
                card_picture = ''
            elif value == "Skip":
                card_picture = ''
            elif value == "Draw2":
                card_picture = ''
            elif value == "Reverse":
                card_picture = ''
            elif value == "Wild":
                card_picture = ''
        elif color == "Wild":
            if value == "Wild":
                card_picture = ''
            elif value == "Draw1":
                card_picture = ''
            elif value == "One_more":
                card_picture = ''
        self.card_picture = card_picture

# 덱 생성 덱 섞는것과  카드 드로우 하는 함수 생성
class DrawPile:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for color in ["Red", "Green", "Blue", "Yellow"]:
            for value in range(1, 10):
                self.cards.append(Card(color, value))
                self.cards.append(Card(color, value))
            for action in ["Skip", "Draw2", "Reverse", "Wild"]:
                self.cards.append(Card(color, action))
                self.cards.append(Card(color, action))
        for action in ["Wild", "Draw1", "One_more"]:
            self.cards.append(Card("Wild", action))
            self.cards.append(Card("Wild", action))

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()

# 플래이어 객체
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
    # hand는 손패이고 deck 은 Deck()의 객체임.
    def draw(self, deck, num):
        for i in range(num):
            self.hand.append(deck.draw_card())
    
    # 카드 제출
    def play_card(self, card):
        self.hand.remove(card)
    # 카드패 확인하는 함수
    def get_hand(self):
        return self.hand

# 게임 시작시 활성화
class Game:
    def __init__(self, first_player):
        players = [Player(first_player)]
        Player_turn = 0
        if first_player == "CPU":
            Player_turn = 1
            players.append(Player("Player"))
        else:
            players.append(Player("CPU"))
        self.Player_turn = Player_turn
        self.players = players
        self.draw_pile = DrawPile()
        self.draw_pile.shuffle()
        self.play_pile = []
        self.direction = 1
        self.current_player = 0
        self.winner = None
        self.timer = 0


    def play(self):
        print("Game started!")
        self.deal_cards()
        self.play_pile.append(self.draw_pile.draw_card())
        self.print_status()
        while not self.winner:
            self.next_turn()
        print(f"{self.winner.name} has won the game!")

    def deal_cards(self):
        for i in range(7):
            for player in self.players:
                player.draw(self.draw_pile, 1)

    def next_turn(self):
            player = self.players[self.current_player]
            print(f"It is {player.name}'s turn!")
            print(f"The top card is {self.play_pile[-1].color} {self.play_pile[-1].value}")
            playable_cards = self.get_playable_cards(player)
            if playable_cards:
                card_submit = None

                if self.Player_turn == self.current_player:
                    print("Playable cards:")
                    for i, card in enumerate(playable_cards):
                        print(f"{i}: {card.color} {card.value}")
                    self.timer = time.time()
                    choice = self.input_with_timeout("Which card do you want to play?", 30)

                    if choice == "Draw":
                        card_submit = choice
                    elif choice == None:
                        pass
                    else:
                        choice = int(choice)
                        card_submit = playable_cards[choice]

                else:
                    card_submit = playable_cards[self.cpu_player_card(playable_cards)]
                    time.sleep(5)

                if card_submit == "Draw":
                    player.draw(self.draw_pile, 1)
                elif card_submit == None:
                    pass
                else:
                    self.play_pile.append(card_submit)
                    player.play_card(card_submit)
                    self.card_actions(card_submit, player)

                if self.uno_button_able(player.get_hand()):
                    self.timer = time.time()
                    uno_button = self.input_with_timeout("", 10)
                    if uno_button == "Uno":
                        if self.Player_turn != self.current_player:
                            player.draw(self.draw_pile, 1)
                    else:
                        if self.Player_turn == self.current_player:
                            player.draw(self.draw_pile, 1)

                if not player.hand:
                    self.winner = player
            else:
                if self.Player_turn == self.current_player:
                    choice = None
                    while choice == None:
                        self.timer = time.time()
                        choice = self.input_with_timeout("Which card do you want to play?", 10)
                        if choice != "Draw" and choice != None:
                            print("제출 가능한 카드가 없습니다.")
                            choice = -1
                        if choice == "Draw":
                            player.draw(self.draw_pile, 1)
                else:
                    player.draw(self.draw_pile, 1)
            self.current_player = (self.current_player + self.direction) % len(self.players)



    def get_playable_cards(self, player):
        playable_cards = []
        for card in player.hand:
            if card.color == self.play_pile[-1].color or card.value == self.play_pile[-1].value or card.color == "Wild":
                playable_cards.append(card)
            elif self.play_pile[-1].color == "Wild": # 첫 카드가 Wild 일 경우
                playable_cards.append(card)
        return playable_cards

    def print_status(self):
        print("Top card: ", self.play_pile[-1].color, self.play_pile[-1].value)
        for player in self.players:
            print(player.name, "hand: ", end="")
            for card in player.get_hand():
                print(card.color, card.value, end=" ")
            print("")

    def card_actions(self, card, player):
        if card.value == "Wild":
            if self.Player_turn == self.current_player:
                self.timer = time.time()
                select_color = self.input_with_timeout("", 10)
                if select_color:
                    self.play_pile[-1] = Card(select_color, card.value)
                else:
                    self.play_pile[-1] = Card("Wild", card.value)

            else:
                select_color=self.cpu_player_skill()
                self.play_pile[-1] = Card(select_color, card.value)
        elif card.value == "Draw1":
            if self.Player_turn == self.current_player:
                self.timer = time.time()
                select_color = self.input_with_timeout("", 10)
                if select_color:
                    self.play_pile[-1] = Card(select_color, card.value)
                else:
                    self.play_pile[-1] = Card("Wild", card.value)
            else:
                select_color = self.cpu_player_skill()
                self.play_pile[-1] = Card(select_color, card.value)
            player.draw(self.draw_pile, 1)
        elif card.value == "One_more":
            if self.Player_turn == self.current_player:
                self.timer = time.time()
                select_color = self.input_with_timeout("", 10)
                if select_color:
                    self.play_pile[-1] = Card(select_color, card.value)
                else:
                    self.play_pile[-1] = Card("Wild", card.value)
            else:
                select_color = self.cpu_player_skill()
                self.play_pile[-1] = Card(select_color, card.value)
            self.current_player = (self.current_player - self.direction) % len(self.players)
        elif card.value == "Skip":
            self.current_player = (self.current_player + self.direction) % len(self.players)
        elif card.value == "Draw2":
            player.draw(self.draw_pile, 2)
        elif card.value == "Reverse":
            self.direction = self.direction*(-1)

    def cpu_player_card(self, playable_cards):
        return random.randrange(len(playable_cards))

    def cpu_player_skill(self):
        color = ["Red", "Green", "Blue", "Yellow"]
        return color[random.randrange(len(color))]

    def uno_button_able(self,player):
        if len(player)==1:
            return True
        else:
            return False

    def input_with_timeout(self,prompt, timeout):
        print(prompt)
        user_input = [None]  # 입력값을 리스트로 저장하기 위해 사용

        def get_input():
            user_input[0] = input()

        input_thread = threading.Thread(target=get_input,daemon="True")
        input_thread.start()
        input_thread.join(timeout)
        return user_input[0]

if __name__ == "__main__":
    who_first = input() # Player 이나 CPU 입력
    game = Game(who_first)
    game.play()