import json
import random
import socket


class RsaCryptography:
    _privateKey = []
    _publicKey = []

    def __init__(self, n=None, e=None, d=None):
        if n is not None and d is not None:
            self._privateKey = [n, d]
        else:
            self._privateKey = []

        if n is not None and e is not None:
            self._publicKey = [n, d]
        else:
            self._publicKey = []

        if len(self._privateKey) == 0 and len(self._publicKey) == 0:
            self._calculate_rsa_variables()

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
        encoded_message = [ord(char) for char in message]
        encrypted_message = [pow(ch, self._publicKey[1], self._publicKey[0]) for ch in encoded_message]

        return encrypted_message

    def decrypt(self, encrypted_message):
        # 1 - D
        # 0 - N
        encoded_message = [pow(ch, self._privateKey[1], self._privateKey[0]) for ch in encrypted_message]
        decrypted_message = "".join(chr(cha) for cha in encoded_message)

        return decrypted_message

    def get_public_key(self):
        return self._publicKey

    def _calculate_rsa_variables(self):
        min_random_prime = 0
        max_random_prime = 100

        initial_primes = self._generate_prime_numbers(min_random_prime, max_random_prime)

        p = initial_primes[random.randint(0, len(initial_primes) - 1)]

        initial_primes = self._generate_prime_numbers(p + 1, max_random_prime)

        q = initial_primes[random.randint(0, len(initial_primes) - 1)]

        while q == p:
            q = initial_primes[random.randint(0, len(initial_primes) - 1)]

        n = p * q
        delta = (p - 1) * (q - 1)

        initial_primes = self._generate_prime_numbers(q + 1, delta)

        e = initial_primes[random.randint(0, len(initial_primes) - 1)]
        d = self._mod_inverse(e, delta)

        self._privateKey = [n, d]
        self._publicKey = [n, e]


class TicTacToeGame:
    table = [
        [' ', ' ', ' '],
        [' ', ' ', ' '],
        [' ', ' ', ' ']
    ]

    def print_table(self):
        print('\n')
        for rowIdx, row in enumerate(self.table):
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

    def verify_victory(self, player):
        for row in self.table:
            if all(place == player for place in row):
                return True

        for column in range(3):
            if all(self.table[row][column] == player for row in range(3)):
                return True

        leftScoreCount = 0
        for diagonal in range(3):
            if self.table[diagonal][diagonal] == player:
                leftScoreCount += 1

        rightScoreCount = 0
        for diagonal in range(3):
            if self.table[diagonal][2 - diagonal] == player:
                rightScoreCount += 1

        if leftScoreCount == 3 or rightScoreCount == 3:
            return True

        return False

    def verify_draw(self):
        for row in self.table:
            if ' ' in row:
                return False

        return True

    def make_move(self, grid_place, player):
        line = 0 if grid_place == 0 else grid_place // 3
        column = 0 if grid_place == 0 else grid_place % 3

        if self.table[line][column] != ' ':
            print("Posicao ja ocupada. Escolha outra posição.")
            return False

        self.table[line][column] = player
        return True

    def play(self,
             sock: socket,
             player_symbol: str,
             opponent_symbol: str,
             player_rsa: RsaCryptography,
             opponent_rsa: RsaCryptography):
        playingGame = True
        current_player = 'X'

        while playingGame:
            self.print_table()
            print(f"Vez do jogador: {current_player}")

            if current_player == player_symbol:
                gridPlace = -1

                while gridPlace < 0 or gridPlace > 8:
                    try:
                        gridPlace = int(input("Digite um número de 0 a 8: "))
                    except ValueError:
                        print("Entrada invalida. Digite um numero de 0 a 8.")
                        continue

                if not self.make_move(gridPlace, player_symbol):
                    continue

                encrypted_move = opponent_rsa.encrypt(str(gridPlace))
                sock.sendall(json.dumps(Message("MOVE", data=encrypted_move)))
            else:
                server_raw_data = sock.recv(4096)
                message = json.loads(server_raw_data.decode())
                if message['type'] == "MOVE":
                    encrypted = message['data']
                    position = int(player_rsa.decrypt(encrypted))
                    self.make_move(position, opponent_symbol)

            if self.verify_victory(current_player):
                self.print_table()
                print(f"Jogador {current_player} venceu!")
                sock.sendall(json.dumps(Message("END", result=current_player)))
                break

            if self.verify_draw():
                self.print_table()
                print("Empate de jogo")
                sock.sendall(json.dumps(Message("END", result="DRAW")))
                break

            current_player = 'O' if current_player == 'X' else 'X'


class Message:
    def __init__(self, type, **options):
        type = type
        options = options


def run_socket_client(host, port):
    # Cria instancia da classe gerando uma chave privada e publica unica
    cl_rsa = RsaCryptography()
    cl_pub_key = cl_rsa.get_public_key()

    # Cria conexão socket com um host e porta
    sock = socket.socket()
    sock.connect((host, port))

    # envia informação da chave publica para o server conectado
    sock.sendall(json.dumps(Message("KEY_EXCH", e=cl_pub_key[1], n=cl_pub_key[0])).encode())

    # aguarda resposta do server conectado para receber a chave pública
    server_raw_response = sock.recv(1024)
    server_data = json.loads(server_raw_response.decode())
    server_pub_key = [server_data["n"], server_data["e"]]

    # cria instancia colocando a chave pública do servidor para poder criptografar dados
    server_rsa = RsaCryptography(server_pub_key[0], server_pub_key[1])

    # confirma recebimento da chave
    sock.sendall(json.dumps(Message("KEY_ACK")).encode())

    game = TicTacToeGame()
    player_symbol, opponent_symbol = 'O', 'X'

    game.play(sock, player_symbol, opponent_symbol, cl_rsa, server_rsa)

    # Fecha conexão socket
    sock.close()


def run_socket_server(host, port):
    # Cria instancia da classe gerando uma chave privada e publica unica
    sv_rsa = RsaCryptography()
    sv_pub_key = sv_rsa.get_public_key()

    # Cria conexão socket com um host e porta
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(1)

    conn, addr = sock.accept()

    # aguarda resposta do server conectado para receber a chave pública
    client_raw_response = sock.recv(1024)
    client_data = json.loads(client_raw_response.decode())
    client_pub_key = [client_data["n"], client_data["e"]]

    # envia informação da chave publica para o server conectado
    conn.sendall(json.dumps(Message("KEY_EXCH", e=sv_pub_key[1], n=sv_pub_key[0])).encode())

    # cria instancia colocando a chave pública do servidor para poder criptografar dados
    client_rsa = RsaCryptography(client_pub_key[0], client_pub_key[1])

    # confirma se cliente recebeu chave
    conn.recv(1024)

    game = TicTacToeGame()
    player_symbol, opponent_symbol = 'X', 'O'

    game.play(conn, player_symbol, opponent_symbol, sv_rsa, client_rsa)

    # Fecha conexão socket
    conn.close()
    sock.close()


# if __name__ == '__main__':
#
#
#     a = rsa.encrypt('test123')
#     b = rsa.decrypt(a)
#
#     print(a, b)
#
#     game = TicTacToeGame()
#
#     game.play()
