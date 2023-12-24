import tkinter as tk
import os

class GameModeFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.titleLabel = tk.Label(self, text="Chọn chế độ chơi", font=("consolas", 40))
        self.titleLabel.pack(pady=10)

        self.play1Button = tk.Button(self, text="Chơi 1 người", font=("consolas", 20) ,command=self.play1_player)
        self.play1Button.pack(pady=10)

        self.play2Button = tk.Button(self, text="Chơi 2 người",font=("consolas", 20) , command=self.play2_players)
        self.play2Button.pack(pady=10)

    def play1_player(self):
        # Đóng cửa sổ hiện tại
        self.master.destroy()
        # Chạy file tictac1p.py
        os.system("python tictac1p.py")

    def play2_players(self):
        # Đóng cửa sổ hiện tại
        self.master.destroy()
        # Chạy file tictac2p.py
        os.system("python tictac2p.py")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Game Tic Tac Toe")
    app = GameModeFrame(master=root)
    app.mainloop()
