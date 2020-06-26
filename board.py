import random
import collections
import colorama
import settings

State = collections.namedtuple('State', ['is_bomb', 'is_covered', 'is_board_empty'])


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
        self.num_free_tiles = settings.NUM_TILES - settings.NUM_BOMBS
        self.grid = [Cell('-') for _ in range(settings.ROW_SIZE) for _ in range(settings.COLUMN_SIZE)]
        self.create_bombs()
        self.calculate_adjacent_bombs()

    def create_bombs(self):
        """ Umieszczanie min na losowych komórkach planszy. """
        empty_positions = [i for i in range(settings.NUM_TILES) if not self.grid[i].is_bomb]
        bomb_positions = random.sample(empty_positions, settings.NUM_BOMBS)
        for i in bomb_positions:
            self.grid[i].is_bomb = True

    def calculate_adjacent_bombs(self):
        """ Obliczanie liczby min sąsiadujących z każdą komórką. """
        for index, cell in enumerate(self.grid):
            check_up = index > (settings.ROW_SIZE - 1)
            check_down = index < (settings.NUM_TILES - settings.ROW_SIZE)
            check_left = index % settings.ROW_SIZE != 0
            check_right = (index + 1) % settings.ROW_SIZE != 0

            check_up_left = check_up and check_left
            check_up_right = check_up and check_right
            check_down_left = check_down and check_left
            check_down_right = check_down and check_right

            if check_up and self.grid[index - settings.ROW_SIZE].is_bomb:
                cell.adjacent_bombs_counter += 1
            if check_down and self.grid[index + settings.ROW_SIZE].is_bomb:
                cell.adjacent_bombs_counter += 1
            if check_left and self.grid[index - 1].is_bomb:
                cell.adjacent_bombs_counter += 1
            if check_right and self.grid[index + 1].is_bomb:
                cell.adjacent_bombs_counter += 1
            if check_up_left and self.grid[index - settings.ROW_SIZE - 1].is_bomb:
                cell.adjacent_bombs_counter += 1
            if check_up_right and self.grid[index - settings.ROW_SIZE + 1].is_bomb:
                cell.adjacent_bombs_counter += 1
            if check_down_left and self.grid[index + settings.ROW_SIZE - 1].is_bomb:
                cell.adjacent_bombs_counter += 1
            if check_down_right and self.grid[index + settings.ROW_SIZE + 1].is_bomb:
                cell.adjacent_bombs_counter += 1

    def uncover_cell(self, index):
        """ Odkrywanie pojedynczej komórki planszy. """
        self.grid[index].display_character = str(self.grid[index].adjacent_bombs_counter)
        self.grid[index].is_covered = False
        self.num_free_tiles -= 1

    def uncover_board(self, index):
        """ Odkrywanie wszystkich komórek sąsiadujących z daną aż do napotkania komórki z miną. """
        if not self.grid[index].is_covered:
            return
        self.uncover_cell(index)
        if self.grid[index].adjacent_bombs_counter != 0:
            return

        check_up = index > (settings.ROW_SIZE - 1)
        check_down = index < (settings.NUM_TILES - settings.ROW_SIZE)
        check_left = index % settings.ROW_SIZE != 0
        check_right = (index + 1) % settings.ROW_SIZE != 0

        if check_up:
            self.uncover_board(index - settings.ROW_SIZE)
        if check_down:
            self.uncover_board(index + settings.ROW_SIZE)
        if check_left:
            self.uncover_board(index - 1)
        if check_right:
            self.uncover_board(index + 1)

    def check_cell(self, index):
        """ Sprawdzanie czy komórka zawiera minę. """
        is_bomb = self.grid[index].is_bomb
        is_covered = self.grid[index].is_covered
        self.uncover_board(index)
        is_board_empty = (self.num_free_tiles <= 0)
        return State(is_bomb=is_bomb, is_covered=is_covered, is_board_empty=is_board_empty)

    def display_board(self):
        """ Wyświetlanie planszy do gry. """
        print()
        print(colorama.Back.BLUE + "                 S A P E R               ", colorama.Style.RESET_ALL)
        for row_size_index in range(settings.ROW_SIZE + 1):
            print(colorama.Fore.LIGHTBLUE_EX + "%-4d" % row_size_index, end="")
        print(colorama.Style.RESET_ALL)
        row = ''
        column_size_index = 1
        for index in range(len(self.grid)):
            if column_size_index <= settings.COLUMN_SIZE and not row:
                print(colorama.Fore.LIGHTBLUE_EX + "%-4d" % column_size_index, end="")
                print(colorama.Style.RESET_ALL, end="")
                column_size_index += 1
            row += self.grid[index].display_character + '   '
            if (index + 1) % settings.ROW_SIZE == 0:
                print(row)
                row = ''

    def display_bombs(self):
        """ Wyświetlanie rozmieszaczenia min na planszy. """
        print(colorama.Back.BLUE + "            ROZMIESZCZENIE MIN           ", colorama.Style.RESET_ALL)
        for row_size_index in range(settings.ROW_SIZE + 1):
            print(colorama.Fore.BLUE + "%-4d" % row_size_index, end="")
        print(colorama.Style.RESET_ALL)
        row = ""
        column_size_index = 1
        for index in range(len(self.grid)):
            if column_size_index <= settings.COLUMN_SIZE and not row:
                print(colorama.Fore.BLUE + "%-4d" % column_size_index, end="")
                print(colorama.Style.RESET_ALL, end="")
                column_size_index += 1
            if self.grid[index].is_bomb:
                row += "*   "
            else:
                row += self.grid[index].display_character + "   "
            if (index + 1) % settings.ROW_SIZE == 0:
                print(row)
                row = ""

    def display_number_of_adjacent_bombs(self):
        """ Wyświetlanie liczby min sąsiadujących z poszczególną komórką. """
        print()
        print(colorama.Back.BLUE + "              MINY SĄSIADUJĄCE           ", colorama.Style.RESET_ALL)
        for row_size_index in range(settings.ROW_SIZE + 1):
            print(colorama.Fore.BLUE + "%-4d" % row_size_index, end="")
        print(colorama.Style.RESET_ALL)
        row = ""
        column_size_index = 1
        for index in range(len(self.grid)):
            if column_size_index <= settings.COLUMN_SIZE and not row:
                print(colorama.Fore.BLUE + "%-4d" % column_size_index, end="")
                print(colorama.Style.RESET_ALL, end="")
                column_size_index += 1
            row += str(self.grid[index].adjacent_bombs_counter) + "   "
            if (index + 1) % settings.ROW_SIZE == 0:
                print(row)
                row = ""
