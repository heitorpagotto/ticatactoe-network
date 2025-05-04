table = [
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', ' ']
]


def printTable():
    print('\n')
    for rowIdx, row in enumerate(table):
        line = ''
        for itemIdx, item in enumerate(row):
            if itemIdx == 1:
                line += f"| {item} |"
            else:
                line += f" {item} "

        print(f" {line} ")
        if rowIdx < 2:
            print(f"----+---+----")

    print('\n')


def verifyVictory(player):
    for row in table:
        if all(place == player for place in row):
            return True

    for column in range(3):
        if all(table[row][column] == player for row in range(3)):
            return True

    leftScoreCount = 0
    for diagonal in range(3):
        if table[diagonal][diagonal] == player:
            leftScoreCount += 1

    rightScoreCount = 0
    for diagonal in range(3):
        if table[diagonal][2 - diagonal] == player:
            rightScoreCount += 1

    if leftScoreCount == 3 or rightScoreCount == 3:
        return True

    return False


def verifyDraw():
    for row in table:
        if ' ' in row:
            return False

    return True


def play():
    playingGame = True
    currentPlayer = 'X'

    while playingGame:
        printTable()
        print(f"Vez do jogador: {currentPlayer}")
        gridPlace = 0

        while gridPlace < 1 or gridPlace > 9:
            try:
                gridPlace = int(input("Digite um número de 1 a 9: "))
            except ValueError:
                print("Entrada invalida. Digite um numero de 1 a 9.")
                continue

        line = (gridPlace - 1) // 3
        column = (gridPlace - 1) % 3

        if table[line][column] != ' ':
            print("Posicao ja ocupada. Escolha outra posição.")
            continue

        table[line][column] = currentPlayer

        if verifyVictory(currentPlayer):
            printTable()
            print(f"Jogador {currentPlayer} venceu!")
            break

        if verifyDraw():
            printTable()
            print("Empate de jogo")
            break

        currentPlayer = 'O' if currentPlayer == 'X' else 'X'


if __name__ == '__main__':
    play()
