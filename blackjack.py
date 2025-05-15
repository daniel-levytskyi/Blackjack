import customtkinter as ctk
from PIL import Image
import random
import os


class Startup(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Blackjack")
        self.geometry("1280x720")
        self._set_appearance_mode("system")

        self.button_style = {
            "fg_color": "#8B0000",    
            "hover_color": "#FFD700",  
            "text_color": "#F8F8FF"
        }

        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color="#0B3D2E")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.content_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#145A32")
        self.content_frame.pack(side="left", expand=True, fill="both")

        self.create_widgets()
        self.load_cards()
        self.money = 1000

    def load_cards(self):
        self.card_images={}
        suits = ['clubs','diamonds','hearts','spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
        for suit in suits:
            for rank in ranks:
                name = f"{rank}_of_{suit}"
                path = os.path.join("/home/levytskyi/Documents/Python/Tkinter/Blackjack/cards/", f"{name}.png")
                if os.path.exists(path):
                    pil_img = Image.open(path)
                    img = ctk.CTkImage(light_image=pil_img, size=(160, 200))
                    self.card_images[(rank, suit)] = img
        back_path = os.path.join("/home/levytskyi/Documents/Python/Tkinter/Blackjack/cards/", "back.png")
        if os.path.exists(back_path):
            pil_back = Image.open(back_path)
            back_img = ctk.CTkImage(light_image=pil_back, size=(160, 200))
            self.card_images["back"] = back_img

    def create_widgets(self):
        self.play_button = ctk.CTkButton(self.sidebar, text="Play", command=self.load_bets, width=200, height=60, font=("Arial", 30), **self.button_style)
        self.play_button.pack(pady=20, padx=10, side="top")

        self.exit_button = ctk.CTkButton(self.sidebar, text="Exit", command=self.destroy, width=200, height=60, font=("Arial", 30), **self.button_style)
        self.exit_button.pack(pady=20, padx=10, side="bottom")

        self.blackjack_label = ctk.CTkLabel(self.content_frame, text="Levytskyi's Blackjack", font=("Helvetica", 70, "bold"), text_color="#D4AF37")
        self.blackjack_label.pack(expand=True)

    def open_loss_window(self):
        window = ctk.CTkToplevel(self)
        window.geometry("300x100")
        window.title("You have lost...")
        loss_window = ctk.CTkFrame(window, corner_radius=0, fg_color="#145A32")
        loss_window.pack(fill="both", expand=True)
        loss_message = ctk.CTkLabel(loss_window, text="The House always wins.", font=("Arial", 20, "bold"), text_color="#D4AF37")
        loss_message.pack(expand=True)
        loss_message2 = ctk.CTkLabel(loss_window, text="You have been reset.", font=("Arial", 20, "bold"), text_color="#D4AF37")
        loss_message2.pack(expand=True)
        continue_button = ctk.CTkButton(loss_window, text="Continue", command=window.destroy, **self.button_style)
        continue_button.pack(expand=True)

    def load_bets(self):
        if self.money <= 0:
            self.open_loss_window()
            print("The house always wins.")
            print("You have been reset.")
            self.money = 1000
            for widget in self.content_frame.winfo_children():
                widget.destroy()
            for option in self.sidebar.winfo_children():
                option.destroy()
            self.create_widgets()
        else:
            for widget in self.content_frame.winfo_children():
                widget.destroy()
            self.bet_text = ctk.CTkLabel(self.content_frame, text="Place your bet:", text_color="#F8F8FF", font=("Arial", 50, "bold"))
            self.bet_box = ctk.CTkEntry(self.content_frame)
            self.complete_bet = ctk.CTkButton(self.content_frame, text="Done", command=self.check_bets, **self.button_style)
            self.invalid_text = ctk.CTkLabel(self.content_frame, text="", text_color="#D4AF37")
            self.money_text = ctk.CTkLabel(self.content_frame, text=f"Current money: ${self.money}", font=("Helvetica", 50), text_color="#D4AF37")
            self.bet_text.pack(pady=10, padx=10)
            self.bet_box.pack(pady=10, padx=10)
            self.complete_bet.pack(pady=10, padx=10)
            self.invalid_text.pack(pady=10, padx=10)
            self.money_text.pack(side="bottom", expand=True)

    def deal_card(self, hand, frame, hide=False):
        card = self.deck.pop()
        hand.append((card, hide))
        if hide:
            image = self.card_images["back"]
        else:
            image = self.card_images[card]
        label = ctk.CTkLabel(frame, image=image, text="", text_color="#D4AF37")
        label.pack(side="left", padx=5)
        return label

    def check_bets(self):
        try:
            bet=int(self.bet_box.get())
            if bet<=0:
                self.invalid_text.configure(text="Bet must be over $0", text_color="#D4AF37")
            elif bet>self.money:
                self.invalid_text.configure(text="You do not have enough money.", text_color="#D4AF37")
            else:
                self.money -= bet
                self.money_text.configure(text=f"Current money: ${self.money}", text_color="#D4AF37")
                self.bet_amount = bet
                self.invalid_text.configure(text=f"Bet of ${bet} accepted", text_color="#D4AF37")
                root.after(1000, self.load_blackjack)
        except ValueError:
            self.invalid_text.configure(text="Invalid input. Enter a number", text_color="#D4AF37")

    def amount_calc(self, hand):
        value = 0
        ace_count = 0
        for card, hide in hand:
            rank = card[0]
            if hide:
                continue
            if rank in ['jack','queen','king']:
                value += 10
            elif rank == "ace":
                value += 11
                ace_count += 1
            else:
                value += int(rank)

        while value > 21 and ace_count > 0:
            value -= 10
            ace_count -= 1

        return value

    def restart(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.load_bets()

    def dealer_moves(self):
        card, _ = self.dealer_hand[1]
        self.dealer_hand[1] = (self.dealer_hand[1][0], False)
        self.dealer_card_count.configure(text=f"{self.amount_calc(self.dealer_hand)}", text_color="#D4AF37")
        self.hidden_dealer.configure(image=self.card_images[card])
        def draw_next():
            if self.amount_calc(self.dealer_hand) < 17:
                self.deal_card(self.dealer_hand, self.dealer_frame)
                self.dealer_card_count.configure(text=f"{self.amount_calc(self.dealer_hand)}", text_color="#D4AF37")
                self.after(500, draw_next)
            else:
                if self.amount_calc(self.dealer_hand) <= 21:
                    self.win_message.configure(text="The Dealer Wins. You Lose", text_color="#D4AF37")
                    self.after(3000, self.restart)
                else:
                    self.win_message.configure(text="The dealer busts. It's a draw.", text_color="#D4AF37")
                    self.money += self.bet_amount
                    self.money_count.configure(text=f"Bank: ${self.money}", text_color="#D4AF37")
                    self.after(3000, self.restart)

        self.after(500, draw_next)   

    def stand_handling(self):
        card, _ = self.dealer_hand[1]
        self.dealer_hand[1] = (self.dealer_hand[1][0], False)
        self.dealer_card_count.configure(text=f"{self.amount_calc(self.dealer_hand)}", text_color="#D4AF37")
        self.hidden_dealer.configure(image=self.card_images[card])
        def draw_next():
            if self.amount_calc(self.dealer_hand) < 17:
                self.deal_card(self.dealer_hand, self.dealer_frame)
                self.dealer_card_count.configure(text=f"{self.amount_calc(self.dealer_hand)}", text_color="#D4AF37")
                self.after(500, draw_next)
            else:
                if self.amount_calc(self.dealer_hand) <= 21 and self.amount_calc(self.dealer_hand) > self.amount_calc(self.player_hand):
                    self.win_message.configure(text="The Dealer Wins. You Lose.", text_color="#D4AF37")
                    self.after(3000, self.restart)
                elif self.amount_calc(self.dealer_hand) == self.amount_calc(self.player_hand):
                    self.win_message.configure(text="Same Quantity. It's a draw.", text_color="#D4AF37")
                    self.money += self.bet_amount
                    self.money_count.configure(text=f"Bank: ${self.money}", text_color="#D4AF37")
                    self.after(3000, self.restart)
                else:
                    self.win_message.configure(text="The Dealer Busts. You Win!", text_color="#D4AF37")
                    self.money += (self.bet_amount*2)
                    self.money_count.configure(text=f"Bank: ${self.money}", text_color="#D4AF37")
                    self.after(3000, self.restart)
        self.after(500, draw_next)  

    def hit_handling(self):
        self.deal_card(self.player_hand, self.player_frame)
        self.player_card_count.configure(text=f"{self.amount_calc(self.player_hand)}", text_color="#D4AF37")
        if self.amount_calc(self.player_hand) > 21:
            for widget in self.button_frame.winfo_children():
                widget.destroy()     
            self.dealer_moves()

    def load_blackjack(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.deck = list(self.card_images.keys())
        self.deck.remove("back")
        random.shuffle(self.deck)

        self.player_hand = []
        self.dealer_hand = []

        self.dealer_frame = ctk.CTkFrame(self.content_frame, height=220, fg_color="#2e4d3e")
        self.dealer_frame.pack(pady=10, padx=200, side="top", anchor="ne", fill="x")
        self.dealer_frame.pack_propagate(False)

        self.center_frame = ctk.CTkFrame(self.content_frame, fg_color="#145A32")
        self.center_frame.pack(fill="both", expand=True)

        self.win_message = ctk.CTkLabel(self.center_frame, text="", text_color="#D4AF37")
        self.win_message.pack(anchor="center")

        #HIT AND STAY BUTTONS
        self.button_frame = ctk.CTkFrame(self.center_frame, fg_color="#145A32")
        self.button_frame.pack(side="bottom", pady=20)

        self.hit_button = ctk.CTkButton(self.button_frame, text="Hit", command=self.hit_handling, width=200, height=60, font=("Arial", 30), **self.button_style)
        self.hit_button.pack(side="left", padx=10)

        self.stand_button = ctk.CTkButton(self.button_frame, text="Stand", command=self.stand_handling, width=200, height=60, font=("Arial", 30), **self.button_style)
        self.stand_button.pack(side="left",padx=10)
        
        #PLAYER FRAME
        self.player_frame = ctk.CTkFrame(self.content_frame, height=220, fg_color="#2e4d3e")
        self.player_frame.pack(pady=10, padx=200, side="bottom", anchor="se", fill="x")
        self.player_frame.pack_propagate(False)

        self.money_count = ctk.CTkLabel(self.content_frame, text=f"Bank: ${self.money}", font=("Arial", 25, "bold"), text_color="#D4AF37")
        self.money_count.place(relx=0.01, rely=0.95, anchor="sw")

        self.deal_card(self.player_hand, self.player_frame)
        self.deal_card(self.player_hand, self.player_frame)
        self.deal_card(self.dealer_hand, self.dealer_frame)
        self.hidden_dealer = self.deal_card(self.dealer_hand, self.dealer_frame, hide=True)

        self.player_card_count = ctk.CTkLabel(self.player_frame, text=f"{self.amount_calc(self.player_hand)}", font=("Arial", 40), text_color="#D4AF37")
        self.player_card_count.pack(side="right", padx=20)

        self.dealer_card_count = ctk.CTkLabel(self.dealer_frame, text=f"{self.amount_calc(self.dealer_hand)}", font=("Arial", 40), text_color="#D4AF37")
        self.dealer_card_count.pack(side="right", padx=20)    

if __name__ == "__main__":
    root = Startup()
    root.mainloop()
