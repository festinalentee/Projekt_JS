from settings import ROW_SIZE, COLUMN_SIZE
from board import Board


class Minesweeper:
    """ Gra Saper """

    def __init__(self):
        self.board = Board()
        self.game_over = False
        self.win = False

    @staticmethod
    def get_user_choice():
        """ Wczytywanie danych od użytkownika. """
        while True:
            print("Podaj 2 liczby (oddzielone spacją):", end="")
            index_y, index_x = map(int, input().split())
            index = (index_y - 1) * ROW_SIZE + index_x
            if index in range(1, (ROW_SIZE * COLUMN_SIZE + 1)):
                return index - 1
            else:
                print("{} Wejście jest niepoprawne. Spróbuj jeszcze raz!".format(index_y, index_x))

    def make_move(self, index):
        status = self.board.check_cell(index)
        if status['is_bomb']:
            return True
        elif not status['is_covered']:
            print("Ta komórka jest juz odkryta. Spróbuj ponownie!")
            return False
        if status['is_board_empty']:
            self.win = True
            return True

    def display_game(self):
        self.board.display_board()

    def game(self):
        self.board.display_bombs()
        self.board.display_number_of_adjacent_bombs()
        while not self.game_over:
            self.display_game()
            index = self.get_user_choice()
            self.game_over = self.make_move(index)

        if self.win:
            print("Wygrałeś, gratulacje!")
        else:
            print("Przegrałeś!")

    def run(self):
        self.game()
