import random


class RsaCryptography:
    _privateKey = []
    _publicKey = []

    @staticmethod
    def _is_prime(n):
        if n == 1:
            return True

        for i in range(2, n):
            if (n % i) == 0:
                return False

        return True

    @staticmethod
    def _mod_inverse(e, delta):
        for d in range(3, delta):
            if (d * e) % delta == 1:
                return d

        raise ValueError("Inverse does not exist")

    def _generate_prime_numbers(self, start, end):
        primes = []
        for i in range(start, end):
            if self._is_prime(i):
                primes.append(i)

        return primes

    def encrypt(self, message):
        # 1 - E
        # 0 - N
        # print(self.pu)
        encoded_message = [ord(char) for char in message]
        encrypted_message = [pow(ch, self._publicKey[1], self._publicKey[0]) for ch in encoded_message]

        return encrypted_message

    def decrypt(self, encrypted_message):
        # 1 - D
        # 0 - N
        encoded_message = [pow(ch, self._privateKey[1], self._privateKey[0]) for ch in encrypted_message]
        decrypted_message = "".join(chr(cha) for cha in encoded_message)

        return decrypted_message

    def calculate_rsa_variables(self):
        initial_primes = self._generate_prime_numbers(1000, 10000)

        p = initial_primes[random.randint(0, len(initial_primes) - 1)]

        initial_primes = self._generate_prime_numbers(p + 1, 10000)

        q = initial_primes[random.randint(0, len(initial_primes) - 1)]

        # p = 3
        # q = 11

        while q == p:
            q = initial_primes[random.randint(0, len(initial_primes) - 1)]

        n = p * q
        delta = (p - 1) * (q - 1)

        print("P= ", p)
        print("Q= ", q)
        print("N= ", n)
        print("Delta= ", delta)

        initial_primes = self._generate_prime_numbers(q + 1, delta)

        #aux = "DIGITE UM NUMERO mdc(" + str(delta) + ",e) =1 ; 1 < e < " + str(delta) + ":"
       # e = initial_primes[random.randint(0, len(initial_primes) - 1)]
        e = 17
        d = self._mod_inverse(e, delta)

        print("E= ", e)
        print("D= ", d)

        self._privateKey = [n, d]
        self._publicKey = [n, e]


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
    rsa = RsaCryptography()

    rsa.calculate_rsa_variables()
    a = rsa.encrypt('test123')
    b = rsa.decrypt(a)

    print(a, b)

    play()
