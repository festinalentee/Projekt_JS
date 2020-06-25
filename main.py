import minesweeper


def main():
    game = minesweeper.Minesweeper()
    game.run()


if __name__ == "__main__":
    NUMBER_OF_BOMBS = (20*10) // 10
    print(NUMBER_OF_BOMBS)
    main()
