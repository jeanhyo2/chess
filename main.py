import sys
import chess
import chess.svg
from PyQt5.QtCore import Qt
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel, QMessageBox

class ChessWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Jogo de Xadrez")
        self.setGeometry(100, 100, 400, 450)

        self.board = chess.Board()
        self.selected_square = None
        self.playing_against_computer = False

        self.svg_widget = QSvgWidget(self)
        self.svg_widget.setGeometry(10, 10, 380, 380)

        layout = QVBoxLayout()
        layout.addWidget(self.svg_widget)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.update_board()

        self.move_button = QPushButton("Mover", self)
        self.move_button.setGeometry(290, 400, 100, 30)
        self.move_button.clicked.connect(self.on_move_button_clicked)

        self.move_input = QLineEdit(self)
        self.move_input.setGeometry(10, 400, 270, 30)

        self.toggle_computer_button = QPushButton("Jogar contra o computador", self)
        self.toggle_computer_button.setGeometry(10, 440, 380, 30)
        self.toggle_computer_button.clicked.connect(self.toggle_computer)

    def update_board(self):
        svg_board = chess.svg.board(board=self.board)
        self.svg_widget.load(svg_board.encode())

    def on_move_button_clicked(self):
        move = self.move_input.text()

        try:
            move = chess.Move.from_uci(move)
        except ValueError:
            self.show_message("Movimento inválido", "O movimento inserido é inválido.")
            return

        if move in self.board.legal_moves:
            self.board.push(move)
            self.update_board()
            if self.board.is_game_over():
                self.show_message("Fim do jogo!", "Resultado: " + self.board.result())
            elif self.playing_against_computer:
                self.computer_move()
        else:
            self.show_message("Movimento inválido", "O movimento inserido é inválido.")

        self.move_input.clear()

    def toggle_computer(self):
        self.playing_against_computer = not self.playing_against_computer
        self.toggle_computer_button.setText("Jogar contra o computador" if not self.playing_against_computer else "Jogar contra o jogador")

        if self.playing_against_computer:
            self.computer_move()

    def computer_move(self):
        # Implemente a lógica para que o computador faça sua jogada aqui.
        # Por exemplo, você pode usar a biblioteca 'chess.engine' para conectar a um motor de xadrez.
        # Neste exemplo, o computador fará uma jogada aleatória para fins ilustrativos.
        import random

        legal_moves = list(self.board.legal_moves)
        if legal_moves:
            move = random.choice(legal_moves)
            self.board.push(move)
            self.update_board()
            if self.board.is_game_over():
                self.show_message("Fim do jogo!", "Resultado: " + self.board.result())

    def show_message(self, title, text):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChessWindow()
    window.show()
    sys.exit(app.exec())
