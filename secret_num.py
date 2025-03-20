from tkinter import *
import random

class SecretNumberGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Secret Number Game")
        self.root.geometry("700x400")
        self.root.configure(bg="lightgray")

        self.secret_number = None
        self.score = 0
        self.level = 1
        self.button_list = []
        self.button_frame = None
        self.timer_label = None
        self.timer = 15
        self.timer_running = False
        self.single_move = False

        self.start_frame = Frame(root, bg="lightgray")
        self.game_frame = Frame(root, bg="lightgray")
        self.end_frame = Frame(root, bg="lightgray")

        self.build_start_page()
        self.build_game_page()
        self.build_end_game()

        self.show_frame(self.start_frame)

    def build_start_page(self):
        title_label = Label(self.start_frame,text="welcome to secret number game!",font=("Helvetica", 18, "bold"),bg="lightgray",pady=20)
        start_button = Button(self.start_frame,text="start game",font=("Helvetica", 14),bg="green",fg="white",padx=20,pady=10,command=lambda: self.show_frame(self.game_frame))
        quit_button = Button(self.start_frame, text="Quit", font=("Helvetica",14), bg="red", fg="white", padx=20, pady=10, command=self.root.quit)
        title_label.pack(pady=50)
        start_button.pack(pady=20)
        quit_button.pack(pady=10)

    def build_game_page(self):
        self.title_label = Label(self.game_frame, text="guess the secret number", font=("Helvetica", 14,"bold"),pady=8,bg="lightgray")
        self.score_label = Label(self.game_frame, text="score:0", font=("Helvetica", 14), fg="white",bg="blue", pady=5)
        self.level_label = Label(self.game_frame, text="Level:1", font=("Helvetica", 14), fg="white",bg="green", pady=5)
        self.answer_label = Label(self.game_frame, text="Answer",font=("Helvetica", 15), pady=13, fg="purple",bg="lightgray")
        self.timer_label = Label(self.game_frame, text="", font=("Helvetica", 14,"bold"),bg="lightgray", fg="red")
        
        self.title_label.grid(row=1, column=1, columnspan=3)
        self.score_label.grid(row=2, column=1)
        self.level_label.grid(row=2, column=2)
        self.timer_label.grid(row=2, column=3)
        self.answer_label.grid(row=4, column=1, columnspan=3)
        quit_button = Button(self.game_frame, text="Quit", font=("helvetica", 14),bg="red", fg="white", padx=20, pady=10, command=self.root.quit)
        quit_button.grid(rows=5, column=2, pady=10)

        self.StartGame()

    def build_end_game(self):
        self.end_message = Label(self.end_frame, text="Game over", font=("Helvetica", 18, "bold"), bg="lightgray",fg="red",pady=20)
        self.restart_button = Button(self.end_frame, text="restart", font=("Helvetica",14), bg="green", fg="white", padx=20, pady=10, command=self.restart_game)
        self.end_message.pack(pady=50)
        self.restart_button.pack(pady=20)
        quit_button = Button(self.end_frame, text="Quit", font=("Helvetica", 14), bg="red", fg="white", padx=20, pady=10,command=self.root.quit)
        quit_button.pack(pady=10)

    def StartGame(self):
        if self.button_frame:
            self.button_frame.destroy()

        self.button_frame = Frame(self.game_frame, bg="lightgray")
        self.button_frame.grid(row=3,column=1,columnspan=3)
        
        self.timer_running = False
        self.timer_label.config(text="")
        self.timer = 15
        if self.level >= 5:
            self.start_timer()
        
        if self.level >= 11:
            self.single_move = True
        else:
            self.single_move = False

         
        if self.level == 1:
            rows = 1
        elif self.level <= 3:
            rows = 2
        elif self.level <= 5:
            rows = 3
        elif self.level <=7:
            rows = 4
        else:
            rows = 5
        level_button_counts = {
            1:3,
            2:4,
            3:6,
            4:8,
            5:10,
            6:12,
            7:14,
            8:16,
            9:18,
            10:20
        }
        button_count = level_button_counts.get(self.level,10)
        number_range = 99
        self.button_list = []

        buttons_per_row = (button_count + rows - 1)//rows
        for row in range(rows):
            row_frame = Frame(self.button_frame, bg="lightgray")
            row_frame.pack(pady=5)
        
            for _ in range(min(buttons_per_row,button_count)):
                button = Button(row_frame,text="00",font=("Helvetica", 15), width=8, pady=10,bg="skyblue",relief="ridge",borderwidth=3)
                self.button_list.append(button)
                button.pack(side=LEFT,pady=5)

                button_count -= 1
                if button_count == 0:
                    break
        
        for button in self.button_list:
            button.config(text=str(random.randint(0,number_range)))

        random_button = random.choice(self.button_list)
        self.secret_number = random_button.cget("text")
        print("secret number is:", self.secret_number)

        for button in self.button_list:
            button.bind("<Button-1>",self.OnClick)


    
    def OnClick(self,event):
        if self.secret_number is None:
            self.answer_label.config(text="game is not started yet!", fg="red")
            return
        if self.single_move:
            for button in self.button_list:
                button.unbind("<Button-1>")


        btn = event.widget
        buttonText = btn.cget("text")

        if self.secret_number == buttonText:
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            self.answer_label.config(text=f"yes it was {self.secret_number}!", fg="green")
            btn.config(bg="lightgreen")
        
            if self.score %3 ==0:
                self.level += 1
                self.level_label.config(text=f"Level:{self.level}")
            self.root.after(500, self.StartGame)

    
        else:
            self.answer_label.config(text="no,try again!", fg="red")
            btn.config(bg="lightcoral")
            self.root.after(500, lambda: btn.config(bg="skyblue"))

    def start_timer(self):
        self.timer_running = True
        self.update_timer()
    
    def update_timer(self):
        if self.timer > 0:
            self.timer_label.config(text=f"Time Left: {self.timer}s")
            self.timer -= 1
            self.root.after(1000, self.update_timer)
        else:
            self.timer_running = False
            self.show_frame(self.end_frame)

    def restart_game(self):
        self.level = 1
        self.score = 0
        self.secret_number = None
        self.score_label.config(text="Score: 0")
        self.level_label.config(text="Level: 1")
        self.answer_label.config(text="Answer", fg="purple")
        self.show_frame(self.game_frame)
        self.StartGame()
    
    def show_frame(self,frame):
        self.start_frame.pack_forget()
        self.game_frame.pack_forget()
        self.end_frame.pack_forget()
        frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    root = Tk()
    app = SecretNumberGame(root)
    root.mainloop()
