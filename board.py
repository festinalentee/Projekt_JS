from settings import ROW_SIZE, COLUMN_SIZE, NUMBER_OF_TILES, NUMBER_OF_BOMBS

import random
import colorama


class Cell:
    """ Pojedyncza komórka planszy."""
    def __init__(self, display_character):
        self.display_character = display_character
        self.is_covered = True
        self.is_bomb = False
        self.adjacent_bombs_counter = 0


class Board:
    """ Plansza do gry Saper."""
    def __init__(self):
        self.NUMBER_OF_FREE_TILES = NUMBER_OF_TILES - NUMBER_OF_BOMBS
        self.grid = [Cell('-') for _ in range(ROW_SIZE) for _ in range(COLUMN_SIZE)]
        self.create_bombs()
        self.calculate_adjacent_bombs()

    def create_bombs(self):
        """ Umieszczanie min na losowych komórkach planszy. """
        for _ in range(NUMBER_OF_BOMBS):
            bomb_is_placed = False
            while not bomb_is_placed:
                bomb_position = random.randint(0, (NUMBER_OF_TILES - 1))
                if not self.grid[bomb_position].is_bomb:
                    self.grid[bomb_position].is_bomb = True
                    bomb_is_placed = True

    def calculate_adjacent_bombs(self):
        """ Obliczanie liczby min sąsiadujących z każdą komórką. """
        for index, cell in enumerate(self.grid):
            check_up = index > (ROW_SIZE - 1)
            check_down = index < (NUMBER_OF_TILES - ROW_SIZE)
            check_left = index % ROW_SIZE != 0
            check_right = (index + 1) % ROW_SIZE != 0

            check_up_left = check_up and check_left
            check_up_right = check_up and check_right
            check_down_left = check_down and check_left
            check_down_right = check_down and check_right

            if check_up and self.grid[index - ROW_SIZE].is_bomb:
                cell.adjacent_bombs_counter += 1
            if check_down and self.grid[index + ROW_SIZE].is_bomb:
                cell.adjacent_bombs_counter += 1
            if check_left and self.grid[index - 1].is_bomb:
                cell.adjacent_bombs_counter += 1
            if check_right and self.grid[index + 1].is_bomb:
                cell.adjacent_bombs_counter += 1
            if check_up_left and self.grid[index - ROW_SIZE - 1].is_bomb:
                cell.adjacent_bombs_counter += 1
            if check_up_right and self.grid[index - ROW_SIZE + 1].is_bomb:
                cell.adjacent_bombs_counter += 1
            if check_down_left and self.grid[index + ROW_SIZE - 1].is_bomb:
                cell.adjacent_bombs_counter += 1
            if check_down_right and self.grid[index + ROW_SIZE + 1].is_bomb:
                cell.adjacent_bombs_counter += 1

    def uncover_cell(self, index):
        """ Odkrywanie pojedynczej komórki planszy. """
        self.grid[index].display_character = str(self.grid[index].adjacent_bombs_counter)
        self.grid[index].is_covered = False
        self.NUMBER_OF_FREE_TILES -= 1

    def uncover_board(self, index):
        """ Odkrywanie wszystkich komórek sąsiadujących z daną aż do napotkania komórki z miną. """
        if not self.grid[index].is_covered:
            return None
        self.uncover_cell(index)
        if self.grid[index].adjacent_bombs_counter != 0:
            return None

        check_up = index > (ROW_SIZE - 1)
        check_down = index < (NUMBER_OF_TILES - ROW_SIZE)
        check_left = index % ROW_SIZE != 0
        check_right = (index + 1) % ROW_SIZE != 0

        if check_up:
            self.uncover_board(index - ROW_SIZE)
        if check_down:
            self.uncover_board(index + ROW_SIZE)
        if check_left:
            self.uncover_board(index - 1)
        if check_right:
            self.uncover_board(index + 1)

    def check_cell(self, index):
        """ Sprawdzanie czy komórka zawiera minę. """
        current_state = {'is_bomb': False, 'is_covered': True, 'is_board_empty': False}
        if self.grid[index].is_bomb:
            current_state['is_bomb'] = True
        if not self.grid[index].is_covered:
            current_state['is_covered'] = False
        self.uncover_board(index)
        if self.NUMBER_OF_FREE_TILES <= 0:
            current_state['is_board_empty'] = True
        return current_state

    def display_board(self):
        """ Wyświetlanie planszy do gry. """
        print()
        print(colorama.Back.BLUE + "                 S A P E R               ", colorama.Style.RESET_ALL)
        for row_size_index in range(ROW_SIZE + 1):
            print(colorama.Fore.LIGHTBLUE_EX + "%-4d" % row_size_index, end="")
        print(colorama.Style.RESET_ALL)
        row = ''
        column_size_index = 1
        for index in range(len(self.grid)):
            if column_size_index <= COLUMN_SIZE and not row:
                print(colorama.Fore.LIGHTBLUE_EX + "%-4d" % column_size_index, end="")
                print(colorama.Style.RESET_ALL, end="")
                column_size_index += 1
            row += self.grid[index].display_character + '   '
            if (index + 1) % ROW_SIZE == 0:
                print(row)
                row = ''

    def display_bombs(self):
        """ Wyświetlanie rozmieszaczenia min na planszy. """
        print(colorama.Back.BLUE + "            ROZMIESZCZENIE MIN           ", colorama.Style.RESET_ALL)
        for row_size_index in range(ROW_SIZE + 1):
            print(colorama.Fore.BLUE + "%-4d" % row_size_index, end="")
        print(colorama.Style.RESET_ALL)
        row = ""
        column_size_index = 1
        for index in range(len(self.grid)):
            if column_size_index <= COLUMN_SIZE and not row:
                print(colorama.Fore.BLUE + "%-4d" % column_size_index, end="")
                print(colorama.Style.RESET_ALL, end="")
                column_size_index += 1
            if self.grid[index].is_bomb:
                row += "*   "
            else:
                row += self.grid[index].display_character + "   "
            if (index + 1) % ROW_SIZE == 0:
                print(row)
                row = ""

    def display_number_of_adjacent_bombs(self):
        """ Wyświetlanie liczby min sąsiadujących z poszczególną komórką. """
        print()
        print(colorama.Back.BLUE + "              MINY SĄSIADUJĄCE           ", colorama.Style.RESET_ALL)
        for row_size_index in range(ROW_SIZE + 1):
            print(colorama.Fore.BLUE + "%-4d" % row_size_index, end="")
        print(colorama.Style.RESET_ALL)
        row = ""
        column_size_index = 1
        for index in range(len(self.grid)):
            if column_size_index <= COLUMN_SIZE and not row:
                print(colorama.Fore.BLUE + "%-4d" % column_size_index, end="")
                print(colorama.Style.RESET_ALL, end="")
                column_size_index += 1
            row += str(self.grid[index].adjacent_bombs_counter) + "   "
            if (index + 1) % ROW_SIZE == 0:
                print(row)
                row = ""
