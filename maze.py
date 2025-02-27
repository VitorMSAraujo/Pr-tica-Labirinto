import pygame
import numpy as np
import csv
import random
import threading

class Maze:
    """
    Classe que representa um labirinto utilizando uma matriz binária.
    
    - 0 (WALL) representa uma parede.
    - 1 (HALL) representa um caminho livre.
    - 2 (PLAYER) representa a posição do jogador.
    - 3 (PRIZE) representa o prêmio a ser encontrado.
    """

    WALL = 0
    HALL = 1
    PLAYER = 2
    PRIZE = 3
    
    def __init__(self):
        """ Inicializa a matriz do labirinto e o ambiente gráfico com pygame. """
        self.M = None  # Matriz que representa o labirinto
        pygame.init()

    def load_from_csv(self, file_path: str):
        """
        Carrega a matriz do labirinto a partir de um arquivo CSV.
        
        Parâmetros:
            file_path (str): Caminho do arquivo CSV contendo a matriz do labirinto.
        """
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            self.M = np.array([list(map(int, row)) for row in reader])  # Converte os dados em matriz NumPy

    def init_player(self):
        """
        Define posições aleatórias para o jogador e para o prêmio dentro do labirinto.
        Ambos são colocados em posições válidas (caminhos livres).
        """
        # Escolhendo posição aleatória válida para o jogador
        while True:
            posx = random.randint(2, 39)
            posy = random.randint(2, 39)
            if self.M[posx, posy] == Maze.HALL:
                self.init_pos_player = (posx, posy)
                break
        
        # Escolhendo posição aleatória válida para o prêmio
        while True:
            posx = random.randint(2, 39)
            posy = random.randint(2, 39)
            if self.M[posx, posy] == Maze.HALL:
                self.M[posx, posy] = Maze.PRIZE
                break

    def find_prize(self, pos: (int, int)) -> bool:
        """
        Verifica se a posição fornecida contém o prêmio.
        """
        return self.M[pos[0], pos[1]] == Maze.PRIZE
        
    def is_free(self, pos: (int, int)) -> bool:
        """
        Verifica se a posição fornecida está livre para movimento (é um corredor ou contém o prêmio).
        """
        return self.M[pos[0], pos[1]] in [Maze.HALL, Maze.PRIZE]
        
    def mov_player(self, pos: (int, int)) -> None:
        """
        Move o jogador para a nova posição e apaga sua posição anterior.
        """
        # Apaga a posição anterior do jogador, caso exista
        if hasattr(self, 'player_pos'):
            prev_pos = self.player_pos
            if self.M[prev_pos[0], prev_pos[1]] == Maze.PLAYER:
                self.M[prev_pos[0], prev_pos[1]] = Maze.HALL
        
        # Atualiza a posição do jogador na matriz
        if self.M[pos[0], pos[1]] == Maze.HALL:
            self.M[pos[0], pos[1]] = Maze.PLAYER
            self.player_pos = pos
        
    def get_init_pos_player(self) -> (int, int):
        """
        Retorna a posição inicial do jogador.
        """
        return self.init_pos_player
            
    def run(self):
        """
        Inicia uma thread para a exibição gráfica do labirinto.
        """
        th = threading.Thread(target=self._display)
        th.start()
    
    def _display(self, cell_size=15):
        """
        Método privado que exibe o labirinto visualmente usando pygame.
        
        - Cada célula do labirinto tem `cell_size` pixels.
        - Cores são definidas para cada tipo de célula.
        """
        rows, cols = self.M.shape
        width, height = cols * cell_size, rows * cell_size
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Labirinto")
    
        # Definição das cores
        BLACK = (0, 0, 0)
        GRAY = (192, 192, 192)
        BLUE = (0, 0, 255)
        GOLD = (255, 215, 0)
    
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
    
            screen.fill(BLACK)  # Fundo preto para o labirinto
    
            # Percorre a matriz e desenha os elementos do labirinto
            for y in range(rows):
                for x in range(cols):
                    if self.M[y, x] == Maze.WALL:
                        color = BLACK
                    elif self.M[y, x] == Maze.HALL:
                        color = GRAY
                    elif self.M[y, x] == Maze.PLAYER:
                        color = BLUE
                    elif self.M[y, x] == Maze.PRIZE:
                        color = GOLD
                    
                    pygame.draw.rect(screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))
    
            pygame.display.flip()
