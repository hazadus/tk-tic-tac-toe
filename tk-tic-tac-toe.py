import random
from tkinter import *
from tkinter.font import Font


class Player:
    def __init__(self, mark):
        self.mark = mark

    def __repr__(self):
        return self.mark

    def __eq__(self, other):
        return self.mark == other.mark if isinstance(other, Player) else False


class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.owner = None

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def set_owner(self, owner: Player):
        self.owner = owner

    def is_free(self):
        return True if self.owner is None else False


class Board:
    winning_coords = [
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],

        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],

        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)],
    ]

    def __init__(self):
        self.cells = [[Cell(x, y) for x in range(3)] for y in range(3)]
        self.players = [Player('X'), Player('O')]
        self.curr_move_player_id = random.choice([0, 1])
        self.is_game_over = False
        self.winner = None

    def get_current_player(self):
        return self.players[self.curr_move_player_id]

    def is_full(self):
        return not any([self.cells[x][y].is_free() for x in range(3) for y in range(3)])

    def make_move(self, coord: tuple):
        x, y = coord
        if self.cells[x][y].is_free():
            self.cells[x][y].set_owner(self.get_current_player())
        else:
            raise Exception(f'Клетка ({x},{y}) не свободна!')

    def check_for_win(self):
        player = self.get_current_player()
        is_winner = False
        for combo in self.winning_coords:
            if all([self.cells[x][y].owner == player for x, y in combo]):
                is_winner = True
                break
        return is_winner

    def check_game_over(self):
        is_win = self.check_for_win()

        if is_win:
            self.winner = self.get_current_player()

        self.is_game_over = is_win

        if not self.is_game_over:
            self.is_game_over = self.is_full()

        # Игра продолжается, делаем другого игрока "текущим"
        if not is_win:
            self.curr_move_player_id = 1 if self.curr_move_player_id == 0 else 0

    def is_cell_free(self, coord):
        x, y = coord
        return self.cells[x][y].is_free()


# Инициализируем игровую логику
the_board = Board()

# Функции для обновления GUI
board_buttons = list()  # список всех "игровых" кнопок в формате [[колонка1], [колонка2], [колонка3]]


def toggle_buttons_enabled(enabled: bool):
    for column in board_buttons:
        for button in column:
            button['state'] = NORMAL if enabled else DISABLED


# Функции обработки GUI
def update_gui(board: Board, info_label: Label):
    # Выводим Х / О на кнопках
    for x in range(3):
        for y in range(3):
            mark = board.cells[x][y].owner.mark if board.cells[x][y].owner is not None else ''
            if mark:
                mark = '\U00002B55' if mark == 'O' else '\U0000274C'
            board_buttons[x][y]['text'] = mark

    if not board.is_game_over:
        info_label['text'] = 'Следующий ход делает: ' + str(the_board.get_current_player())
    else:
        info_label['text'] = 'Игра закончена – ' + \
                             (f'выиграл {board.winner}!' if board.winner is not None else 'ничья!')
        toggle_buttons_enabled(False)


def btn_clicked(info_label: Label, board: Board, coord: tuple):
    if board.is_cell_free(coord):
        board.make_move(coord)
        board.check_game_over()
        update_gui(board, info_label)
    else:
        info_label['text'] = 'Нельзя ходить на эту клетку!'


def restart_clicked(info_label: Label):
    global the_board
    the_board = Board()

    toggle_buttons_enabled(True)
    update_gui(the_board, info_label)


# Инициализируем и выводим на экран GUI
root = Tk()
root.eval('tk::PlaceWindow . center')
root.title('Крестики-нолики')

# Создаем елементы GUI
font = Font(size=18)
label_info = Label(root, text='Следующий ход делает: ' + str(the_board.get_current_player()), font=font)
button_restart = Button(root, text='Заново', command=lambda: restart_clicked(label_info), font=font)
button_quit = Button(root, text='\U0000238B Выход', command=root.quit, font=font)

button1 = Button(root, text='', width=10, height=7, command=lambda: btn_clicked(label_info, the_board, (0, 0)))
button2 = Button(root, text='', width=10, height=7, command=lambda: btn_clicked(label_info, the_board, (1, 0)))
button3 = Button(root, text='', width=10, height=7, command=lambda: btn_clicked(label_info, the_board, (2, 0)))

button4 = Button(root, text='', width=10, height=7, command=lambda: btn_clicked(label_info, the_board, (0, 1)))
button5 = Button(root, text='', width=10, height=7, command=lambda: btn_clicked(label_info, the_board, (1, 1)))
button6 = Button(root, text='', width=10, height=7, command=lambda: btn_clicked(label_info, the_board, (2, 1)))

button7 = Button(root, text='', width=10, height=7, command=lambda: btn_clicked(label_info, the_board, (0, 2)))
button8 = Button(root, text='', width=10, height=7, command=lambda: btn_clicked(label_info, the_board, (1, 2)))
button9 = Button(root, text='', width=10, height=7, command=lambda: btn_clicked(label_info, the_board, (2, 2)))

board_buttons.append([button1, button4, button7])
board_buttons.append([button2, button5, button8])
board_buttons.append([button3, button6, button9])

# Размещаем элементы GUI
label_info.grid(row=0, columnspan=3)

button1.grid(row=1, column=0)
button2.grid(row=1, column=1)
button3.grid(row=1, column=2)

button4.grid(row=2, column=0)
button5.grid(row=2, column=1)
button6.grid(row=2, column=2)

button7.grid(row=3, column=0)
button8.grid(row=3, column=1)
button9.grid(row=3, column=2)

button_restart.grid(row=4, column=1)
button_quit.grid(row=4, column=2)

root.mainloop()
