import random
import time
import threading
import sys
import pygame

class Popup(pygame.sprite.Sprite):
    def __init__(self, name, position):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image = pygame.image.load('./img/'+name+'.png')
        self.position = position
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def get_name(self):
        return self.name
    def get_rect(self):
        return self.rect

# 카드 생성. 그림도 각 객체에 들아가도록 함
class Card(pygame.sprite.Sprite):
    def __init__(self, color, value):
        self.color = color
        self.value = value
        self.name = color+'_'+value
        self.image = pygame.image.load('./img/' + self.name + '.png')
        self.rect = self.image.get_rect()
    def change_position(self,x,y):
        self.rect.centerx = x
        self.rect.centery = y
    def change_imge_size(self,x,y):
        self.image = pygame.transform.scale(self.image, (x, y))

# 덱 생성 덱 섞는것과  카드 드로우 하는 함수 생성
class Deck:
    def __init__(self,player_name):
        self.cards = []
        self.player_name = player_name
        self.build()

    def build(self): # 총 113 장
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
            self.cards.append(Card("Wild", action))


    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self,mode,name):
        if mode == '1':
            random_num = random.random()
            if name != self.player_name:
                for i in range(1,len(self.cards)+1):
                    if random_num * (2*len(self.cards) + int(self.check_card())) < 3*self.check_card():
                        if random_num * (2 * len(self.cards) + int(self.check_card())) < 2*i:
                            return self.cards.pop(i - 1)
                    else:
                        if random_num * (2 * len(self.cards) + int(self.check_card())) < 3*i:
                            return self.cards.pop(i - 1)
            else:
                for i in range(1,len(self.cards)+1):
                    if random_num*len(self.cards) < i:
                        return self.cards.pop(i-1)


        elif mode == '4' and name == self.player_name:
            pop_card = len(self.cards)-1
            while (not self.cards[pop_card].value in [1,2,3,4,5,6,7,8,9]) and (pop_card >= 0):
                pop_card = pop_card - 1
            if pop_card == -1:
                return None
            else:
                return self.cards.pop(pop_card)
        else:
            return self.cards.pop()

    def check_card(self):
        num_num = 0
        for card in self.cards:
            if card.value in [1,2,3,4,5,6,7,8,9]:
                num_num += 1
        return num_num



# 플래이어 객체
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
    # hand는 손패이고 deck 은 Deck()의 객체임.
    def draw(self, deck, num):
        for i in range(num):
            if len(deck.cards) != 0:
                willdarw_card=deck.draw_card(mode, self.name)
                if willdarw_card:
                    self.hand.append(willdarw_card)


    
    # 카드 제출
    def play_card(self, card):
        self.hand.remove(card)
    # 카드패 확인하는 함수
    def get_hand(self):
        return self.hand


# 게임 시작시 활성화
class Game:
    def __init__(self, mode, player_names,player_name,first_player):
        players =[]
        for i in player_names:
            players.append(Player(i))
        self.players = players
        self.player_name = player_name
        self.deck = Deck(player_name)
        if not mode == '1':
            self.deck.shuffle()
        self.play_pile = []
        self.direction = 1
        self.current_player = first_player
        self.winner = None
        self.timer = 0
        self.mode = mode
        self.turn_num  =1
        self.uno_input = False
        self.window_size=0
        self.window_sizes = [[900, 600],[1200, 800], [1500, 1000]]
        self.window = None
        self.card_sizes = [[45,60],[60,80],[75,100]]
        self.img_deck = pygame.image.load('./img/Deck.png')

        self.speed = 5

    def play(self):
        print("Game started!")
        self.deal_cards()
        self.play_pile.append(self.deck.draw_card(mode,None))
        self.print_status()
        while not self.winner:
            self.next_turn()
            self.turn_num += 1
            if self.mode=='3' and self.turn_num % 5 == 0:
                colors = ["Red", "Green", "Blue", "Yellow"]
                self.play_pile[-1].value = random.choice(colors)

        print(f"{self.winner.name} has won the game!")

    def deal_cards(self):
        if mode == '2':
            for i in range(28):
                for player in self.players:
                    player.draw(self.deck, 1)
        else:
            for i in range(7):
                for player in self.players:
                    player.draw(self.deck, 1)


    def next_turn(self):
            player = self.players[self.current_player]
            print(f"It is {player.name}'s turn!")
            print(f"The top card is {self.play_pile[-1].color} {self.play_pile[-1].value}")
            playable_cards = self.get_playable_cards(player)
            if playable_cards:
                card_submit = None

                if 'Player'== player.name:
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
                    player.draw(self.deck, 1)
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
                        if 'Player' != player.name:
                            player.draw(self.deck, 1)
                    else:
                        if 'Player' == player.name:
                            player.draw(self.deck, 1)

                if not player.hand:
                    self.winner = player
            else:
                if 'Player' == player.name:
                    choice = None
                    while choice == None:
                        self.timer = time.time()
                        choice = self.input_with_timeout("Which card do you want to play?", 10)
                        if choice != "Draw" and choice != None:
                            print("제출 가능한 카드가 없습니다.")
                            choice = -1
                        if choice == "Draw":
                            player.draw(self.deck, 1)
                else:
                    player.draw(self.deck, 1)
            self.current_player = (self.current_player + self.direction) % len(self.players)



    def get_playable_cards(self, player):
        playable_cards = []
        for card in player.hand:
            if card.color == self.play_pile[-1].color or card.value == self.play_pile[-1].value or card.color == "Wild":
                playable_cards.append(card)
            elif self.play_pile[-1].color == "Wild": # 첫 카드가 Wild 일 경우
                playable_cards.append(card)
        return playable_cards

    def check_skill_card(self,cards):
        skill_num = len(cards)
        for card in cards:
            if card.value in [1,2,3,4,5,6,7,8,9]:
                skill_num = skill_num - 1
        return skill_num

    def print_status(self):
        print("Top card: ", self.play_pile[-1].color, self.play_pile[-1].value)
        for player in self.players:
            print(player.name, "hand: ", end="")
            for card in player.get_hand():
                print(card.color, card.value, end=" ")
            print("")

    def card_actions(self, card, player):
        if card.value == "Wild":
            if 'Player' == player.name:
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
            if 'Player' == player.name:
                self.timer = time.time()
                select_color = self.input_with_timeout("", 10)
                if select_color:
                    self.play_pile[-1] = Card(select_color, card.value)
                else:
                    self.play_pile[-1] = Card("Wild", card.value)
            else:
                select_color = self.cpu_player_skill()
                self.play_pile[-1] = Card(select_color, card.value)
            player.draw(self.deck, 1)
        elif card.value == "One_more":
            if 'Player' == player.name:
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
            player.draw(self.deck, 2)
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




    def window_make(self):
        pygame.init()

        self.window = self.window_size_change(self.window_size)

        #덱
        self.img_deck = self.card_size_change(self.img_deck,self.card_sizes[self.window_size])
        self.deck_postion = self.img_deck.get_rect()
        self.deck_postion.centerx = self.window_sizes[self.window_size][0]//2
        self.deck_postion.centery = self.window_sizes[self.window_size][1]//2

        #UNO버튼
        self.img_unobutton = self.card_size_change("./img/UNO.png",self.card_sizes[self.window_size])
        self.UNO_postion = self.img_unobutton.get_rect()
        self.UNO_postion.centerx = self.window_sizes[self.window_size][0]//2 + self.card_sizes[self.window_size][0]*2
        self.UNO_postion.centery = self.window_sizes[self.window_size][1]//2
        
        #플레이어 이름 표시
        self.printwindow_text((0,0,0))

        #현재 플레이어 표시
        self.select_player(self.current_player)

        # 현재 카드 color
        self.current_color = self.card_size_change("./img/"+self.play_pile[-1].color+".png", self.card_sizes[self.window_size])
        self.current_color_postion= self.current_color.get_rect()
        self.current_color_postion.centerx = self.window_sizes[self.window_size][0]//2 - self.card_sizes[self.window_size][0]*2
        self.current_color_postion.centery = self.window_sizes[self.window_size][1]//2

        #각 플레이어 덱 표시



    def window_size_change(self,window_size):
        x,y = self.window_sizes[window_size]
        return pygame.display.set_mode((x,y))
    def card_size_change(self,img,card_size):
        x,y =card_size
        return pygame.transform.scale(img, (x, y))
    def printwindow_text(self,color):
        if len(self.players) >= 3:
            com2_text = self.text_format(self.players[2].name, self.card_sizes[self.window_size][0]//2, color)
            self.window.blit(com2_text, (self.card_sizes[self.window_size][0]//4, self.window_sizes[self.window_sizes][1]//3+self.card_sizes[self.window_size][0]//4))
        if len(self.players) >= 4:
            com3_text = self.text_format(self.players[3].name, self.card_sizes[self.window_size][0]//2, color)
            self.window.blit(com3_text, (self.window_sizes[self.window_sizes][0]//3*2+self.card_sizes[self.window_size][0]//4, (self.window_sizes[self.window_sizes][1]//3) + self.card_sizes[self.window_size][0]//4))
        if len(self.players) >= 5:
            com4_text = self.text_format(self.players[4].name, self.card_sizes[self.window_size][0]//2, color)
            self.window.blit(com4_text, (self.card_sizes[self.window_size][0]//4, self.card_sizes[self.window_size][0]//4))
        if len(self.players) >= 6:
            com5_text = self.text_format(self.players[5].name, self.card_sizes[self.window_size][0]//2, color)
            self.window.blit(com5_text, (self.window_sizes[self.window_sizes][0]//3*2+self.card_sizes[self.window_size][0]//4, self.card_sizes[self.window_size][0]//4))

        user_text = self.text_format(self.players[0].name, self.card_sizes[self.window_size][0]//2, color)
        self.window.blit(user_text, (self.window_sizes[self.window_sizes][0]//3+self.card_sizes[self.window_size][0]//4, (self.window_sizes[self.window_sizes][1]//3)*2 + self.card_sizes[self.window_size][0]//4))
        com1_text = self.text_format(self.players[1].name, self.card_sizes[self.window_size][0]//2, color)
        self.window.blit(com1_text, (self.window_sizes[self.window_sizes][0]//3+self.card_sizes[self.window_size][0]//4, self.card_sizes[self.window_size][0]//4))

    def select_player(self, now_turn):
        color = (255,242,0)
        if now_turn == 0:
            user_text = self.text_format(self.players[0].name, self.card_sizes[self.window_size][0] // 2, color)
            self.window.blit(user_text, (
            self.window_sizes[self.window_sizes][0] // 3 + self.card_sizes[self.window_size][0] // 4,
            (self.window_sizes[self.window_sizes][1] // 3) * 2 + self.card_sizes[self.window_size][0] // 4))
        elif now_turn == 1:
            com1_text = self.text_format(self.players[1].name, self.card_sizes[self.window_size][0] // 2, color)
            self.window.blit(com1_text, (
            self.window_sizes[self.window_sizes][0] // 3 + self.card_sizes[self.window_size][0] // 4,
            self.card_sizes[self.window_size][0] // 4))
        elif now_turn == 2:
            com2_text = self.text_format(self.players[2].name, self.card_sizes[self.window_size][0] // 2, color)
            self.window.blit(com2_text, (self.card_sizes[self.window_size][0] // 4,
                                         self.window_sizes[self.window_sizes][1] // 3 +
                                         self.card_sizes[self.window_size][0] // 4))
        elif now_turn == 3:
            com3_text = self.text_format(self.players[3].name, self.card_sizes[self.window_size][0] // 2, color)
            self.window.blit(com3_text, (
            self.window_sizes[self.window_sizes][0] // 3 * 2 + self.card_sizes[self.window_size][0] // 4,
            (self.window_sizes[self.window_sizes][1] // 3) + self.card_sizes[self.window_size][0] // 4))
        elif now_turn == 4:
            com4_text = self.text_format(self.players[4].name, self.card_sizes[self.window_size][0] // 2, color)
            self.window.blit(com4_text,
                             (self.card_sizes[self.window_size][0] // 4, self.card_sizes[self.window_size][0] // 4))
        elif now_turn == 5:
            com5_text = self.text_format(self.players[5].name, self.card_sizes[self.window_size][0] // 2, color)
            self.window.blit(com5_text, (
            self.window_sizes[self.window_sizes][0] // 3 * 2 + self.card_sizes[self.window_size][0] // 4,
            self.card_sizes[self.window_size][0] // 4))
        pygame.display.update()
    
    
    #카드 사이즈 조정 필요
    def deck_print(self):

        for i in len(self.players[0].hand):
            player_hand = self.players[0].hand[i].image
            self.window.blit(player_hand,self.window_sizes[self.window_sizes][0]//3+self.card_sizes[self.window_size][0]//4+self.card_sizes[self.window_size][1]//2+(self.window_sizes[self.window_size]//3-self.card_sizes[self.window_size][1])//len(self.players[0].hand)*i, (self.window_sizes[self.window_sizes][1]//3)*2+ self.card_sizes[self.window_size][0]*4//3)

        for i in len(self.players[1].hand):
            cpu1_hand = pygame.image.load('./img/Deck.png')
            self.window.blit(cpu1_hand,(self.window_sizes[self.window_sizes][0]//3+self.card_sizes[self.window_size][0]//4+self.card_sizes[self.window_size][1]//2+(self.window_sizes[self.window_size]//3-self.card_sizes[self.window_size][1])//len(self.players[1].hand)*i, self.card_sizes[self.window_size][0]*4//3))

        if len(self.players) >= 3:
            for i in len(self.players[2].hand):
                cpu2_hand =pygame.image.load('./img/Deck.png')
                self.window.blit(cpu2_hand,(self.card_sizes[self.window_size][0]//4+self.card_sizes[self.window_size][1]//2+(self.window_sizes[self.window_size]//3-self.card_sizes[self.window_size][1])//len(self.players[2].hand)*i, self.window_sizes[self.window_sizes][1]//3+self.card_sizes[self.window_size][0]*4//3))
        if len(self.players) >= 4:
            for i in len(self.players[3].hand):
                cpu3_hand =pygame.image.load('./img/Deck.png')
                self.window.blit(cpu3_hand,(self.window_sizes[self.window_sizes][0]//3*2+self.card_sizes[self.window_size][0]//4+self.card_sizes[self.window_size][1]//2+(self.window_sizes[self.window_size]//3-self.card_sizes[self.window_size][1])//len(self.players[3].hand)*i, self.window_sizes[self.window_sizes][1]//3+self.card_sizes[self.window_size][0]*4//3))
        if len(self.players) >= 5:
            for i in len(self.players[4].hand):
                cpu4_hand =pygame.image.load('./img/Deck.png')
                self.window.blit(cpu4_hand,(self.card_sizes[self.window_size][0]//4+self.card_sizes[self.window_size][1]//2+(self.window_sizes[self.window_size]//3-self.card_sizes[self.window_size][1])//len(self.players[4].hand)*i, self.card_sizes[self.window_size][0]*4//3))

        if len(self.players) >= 6:
            for i in len(self.players[5].hand):
                cpu5_hand =pygame.image.load('./img/Deck.png')
                self.window.blit(cpu5_hand,(self.window_sizes[self.window_sizes][0]//3*2+self.card_sizes[self.window_size][0]//4+self.card_sizes[self.window_size][1]//2+(self.window_sizes[self.window_size]//3-self.card_sizes[self.window_size][1])//len(self.players[5].hand)*i, self.card_sizes[self.window_size][0]*4//3))



    #skill effect
    def skill_effect(self,card):
        skill_image = pygame.image.load('./img/'+card.value+'.png')
        self.window.blit(skill_image,(self.window_sizes[self.window_sizes][0]//3*2+self.card_sizes[self.window_size][0]//4+self.card_sizes[self.window_size][1]//2+(self.window_sizes[self.window_size]//3-self.card_sizes[self.window_size][1])//len(self.players[5].hand)*i, self.card_sizes[self.window_size][0]*8//3))


    #color change
    def pick_color(self): # 위치 조정 예정
        color_popup = Popup('pickcolor', (400, 300))
        popup_group = pygame.sprite.RenderPlain(color_popup)
        red = Popup('RED', (306, 320))
        yellow = Popup('YELLOW', (368, 320))
        green = Popup('GREEN', (432, 320))
        blue = Popup('BLUE', (494, 320))
        colors = [red, yellow, green, blue]
        color_group = pygame.sprite.RenderPlain(*colors)

        loop = True
        while loop:
            popup_group.draw(self.window)
            color_group.draw(self.window)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP: # 다음에 내야할 곳에 표시 수정 사항
                    mouse_pos = pygame.mouse.get_pos()
                    for sprite in color_group:
                        if sprite.get_rect().collidepoint(mouse_pos):
                            temp_name = sprite.get_name()
                            temp = Card(temp_name, (430, 300))
                            self.waste_card.append(temp_name)
                            self.waste_group.add(temp)
                            self.printwindow()
                            loop = False
        return 0

    def text_format(self, message, textSize, textColor):
        newFont = pygame.font.SysFont('Berlin Sans FB', textSize, True, False)
        newText = newFont.render(message, True, textColor)
        return newText
if __name__ == "__main__":
    mode = input()
    player_names = ['Player','CPU1','CPU2','CPU3','CPU4','CPU5']
    if mode == 'single':
        pass
    elif mode == '1':
        player_names = ['Player','CPU1']
    elif mode == '2':
        player_names = ['Player', 'CPU1','CPU2','CPU3']
    elif mode == '3':
        player_names = ['Player', 'CPU1','CPU2']
    elif mode == '4':
        player_names = ['Player','CPU1']
    player_name = 'Player'
    first_player = 0
    game = Game(mode,player_names,player_name,first_player)
    game.play()


# 입출력값 받아오는것 구현