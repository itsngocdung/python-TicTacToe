from tkinter import *
from tkinter import messagebox
import random
import pygame




pygame.init()
pygame.mixer.init()


def next_turn(row, column):
    global player

    if buttons[row][column]['text'] == "" and check_winner() is False:

        if player == players[0]:

            buttons[row][column]['text'] = player

            if check_winner() is True: # Da thang
                label.config(text=(players[0]+" đã thắng!!"))
            elif check_winner() is False: #Van thua
                player = players[1] #Chuyen sang bot
                label.config(text=("Lượt của " + players[1]))

                bot_move(row,column)
                if check_winner() is False:
                    label.config(text=("Lượt của " + players[0]))
                    player = players[0]

                elif check_winner() is True:
                    label.config(text=(players[1]+" đã thắng"))

            #     elif check_winner() == "Tie":
            #         label.config(text="cả 2 đã hòa!") 
            # elif check_winner() == "Tie":
            #     label.config(text="Cả 2 đã hòa!")
        
def bot_move(row, col):
    global player

    # Kiểm tra ô trống ở bên cạnh ô người chơi vừa chọn
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]  # Hướng: phải, trái, dưới, trên
    random.shuffle(directions)  # Trộn ngẫu nhiên thứ tự của các hướng

    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 10 and 0 <= new_col < 10 and buttons[new_row][new_col]['text'] == "":
            # Di chuyển bot vào ô trống ở hướng được chọn
            buttons[new_row][new_col]['text'] = players[1]  # player[1] là bot
            label.config(text=("Lượt của " + players[0]))
            return

    # Nếu không có ô trống ở bất kỳ hướng nào,   bot sẽ di chuyển ngẫu nhiên
    empty_cells = [(row, col) for row in range(10) for col in range(10) if buttons[row][col]['text'] == ""]
    
    if empty_cells:
        # Chọn một ô trống ngẫu nhiên từ danh sách ô trống
        bot_row, bot_col = random.choice(empty_cells)
        
        buttons[bot_row][bot_col]['text'] = players[1]  # player[1] là bot
        label.config(text=("Lượt của " + players[0]))
def clear_scores():
    try:
        with open("scores.txt", "w", encoding="utf-8") as file:
            file.write("")  # Ghi một chuỗi trống để xóa nội dung
    except Exception as e:
        print(f"Lỗi khi xóa điểm: {e}")

score_recorded = False
player1Score = 0
player2Score = 0

def record_score(winning_player):
    global score_recorded, player1Score, player2Score
    if not score_recorded:
        try:
            with open("scores.txt", "a", encoding="utf-8") as file:
                file.write(f"{winning_player} thắng!\n")
            score_recorded = True  # Đặt biến cờ thành True để chỉ ghi một lần
            
            # Cập nhật số lần thắng cho player1 và player2
            if winning_player == players[0]:
                player1Score += 1
            elif winning_player == players[1]:
                player2Score += 1
        except Exception as e:
            print(f"Lỗi ghi điểm: {e}")

# Modify the check_winner function



def mark_winning_cells(start_row, start_col, end_row, end_col):
    for row in range(start_row, end_row + 1):
        for col in range(start_col, end_col + 1):
            buttons[row][col].config(bg="green")
def check_winner():
    #kiểm tra theo chiến thắng ngang
    for row in range(10):
        for col in range(6):  # Kiểm tra cột từ 0 đến 5 (10 - 5 + 1)
            if all(buttons[row][col+i]['text'] == player for i in range(5)):
                mark_winning_cells(row, col, row, col + 4)
                record_score(player)
                
                win_sound = pygame.mixer.Sound("win_sound.wav")
                win_sound.play()
                return True

    #kiểm tra theo chiến thắng dọc
    for col in range(10):
        for row in range(6):  # Kiểm tra hàng từ 0 đến 5 (10 - 5 + 1)
            if all(buttons[row+i][col]['text'] == player for i in range(5)):
                mark_winning_cells(row, col, row + 4, col)
                record_score(player)
                return True

    for row in range(6):  # Kiểm tra đường chéo xuôi
        for col in range(6):
            if all(buttons[row+i][col+i]['text'] == player for i in range(5)):
                for i in range (5):
                    buttons[row+i][col+i].config(bg="green") 
                record_score(player)
                return True

    for row in range(6):  # Kiểm tra đường chéo ngược
        for col in range(9, 3, -1):
            if all(buttons[row+i][col-i]['text'] == player for i in range(5)):
                for i in range (5):
                    buttons[row+i][col-i].config(bg="green") 
                record_score(player)
                return True

    return False


def empty_spaces():
    spaces = 100

    for row in range (10):
        for column in range(10):
            if buttons[row][column]['text'] != "":
                spaces -= 1
    if spaces == 0:
        return False
    else:
        return True            

def new_game():
    global player
    global score_recorded 
    score_recorded = False
    player = players[0]

    label.config(text= "Lượt của " + player)

    if dark_mode is False:
        for row in range(10):
            for column in range(10):
                buttons[row][column].config(text="", bg="#F0F0F0")
    else:
        for row in range(10):
            for column in range(10):
                buttons[row][column].config(text="", bg="#333333")



# Thêm hai biến toàn cục để lưu số lần thắng của player1 và player2
player1Score = 0
player2Score = 0



def show_history():
    global player1Score, player2Score
    try:
        with open("scores.txt", "r", encoding="utf-8") as file:
            content = file.read()
        if content:
            # Hiển thị cửa sổ lịch sử
            history_window = Toplevel(window)
            history_window.title("Lịch sử")

            # Hiển thị lịch sử và số lần thắng của player1 và player2
            history_label = Label(history_window, text=f"{content}\n\nSố lần thắng của {players[0]}: {player1Score}\nSố lần thắng của {players[1]}: {player2Score}", font=("consolas", 14), justify=LEFT)
            history_label.pack(padx=20, pady=20)
        else:
            messagebox.showinfo("Lịch sử", "Chưa có dữ liệu.")
    except Exception as e:
        print(f"Lỗi đọc lịch sử: {e}")

# Hàm để chuyển giữa Dark Mode và Light Mode
dark_mode = False
def toggle_dark_mode():
    global dark_mode
    if dark_mode:
        window.config(bg="#F0F0F0")  # Chuyển nền của cửa sổ về màu sáng
        label.config(fg="#333333",bg="#F0F0F0" )  # Chuyển màu chữ về đen
        history_button.config(bg="#F0F0F0", fg="#333333")
        reset_button.config(bg="#F0F0F0", fg="#333333")
        dark_mode_button.config(bg="#F0F0F0", fg="#333333", text="Dark mode")
        button_frame.config(bg="#F0F0F0")
        for row in range(10):
            for column in range(10):
                buttons[row][column].config(bg="#F0F0F0", fg="#333333")
        dark_mode = False
    else:
        window.config(bg="#333333")  # Chuyển nền của cửa sổ về màu tối
        label.config(fg="white", bg="#333333")  # Chuyển màu chữ về trắng
        history_button.config(bg="#333333", fg="#F0F0F0")
        reset_button.config(bg="#333333", fg="#F0F0F0")
        dark_mode_button.config(bg="#333333", fg="#F0F0F0", text="Light mode")
        button_frame.config(bg="#333333")


        for row in range(10):
            for column in range(10):
                buttons[row][column].config(bg="#333333", fg="#F0F0F0")

        dark_mode = True


window = Tk()
window.title("10x10")



players = ["x", "Bot"]
# players = get_player_names()
player = players[0]
buttons = [[0]*10 for _ in range(10)]

label = Label(text= "Lượt của " + player, font = ("consolas", 40))
label.pack(side="top")

# Tạo Frame để chứa ba nút
button_frame = Frame(window)
button_frame.pack(side="top", pady=10)  # Đặt Frame ở trên cùng với khoảng cách 10 pixel từ top

# Tạo nút "Chơi lại" và đặt vào Frame
reset_button = Button(button_frame, text="Chơi lại", font=("consolas", 15), command=new_game)
reset_button.pack(side="left", padx=10)  # Đặt nút "Chơi lại" bên trái với khoảng cách 10 pixel

# Tạo nút "Lịch sử" và đặt vào Frame
history_button = Button(button_frame, text="Lịch sử", font=("consolas", 15), command=show_history)
history_button.pack(side="left", padx=10)  # Đặt nút "Lịch sử" bên trái với khoảng cách 10 pixel

# Tạo nút "Dark Mode" và đặt vào Frame
dark_mode_button = Button(button_frame, text="Dark Mode", font=("consolas", 15), command=toggle_dark_mode)
dark_mode_button.pack(side="left", padx=10)  # Đặt nút "Dark Mode" bên trái với khoảng cách 10 pixel



frame = Frame(window)
frame.pack()

for row in range(10):
    for column in range(10):
        buttons[row][column] = Button(frame, text="", font=("consolas", 16), width=3, height=1,
                                       command=lambda row=row, column=column: next_turn(row, column))
        buttons[row][column].grid(row=row, column=column)

clear_scores()
window.mainloop()
