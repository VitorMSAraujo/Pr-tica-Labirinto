# -*- coding: utf-8 -*-
import time
from maze import Maze
from collections import deque  # Importa deque para usar como pilha no backtracking

# Caminho do arquivo CSV que contém a matriz do labirinto
maze_csv_path = "labirinto1.txt"

# Criação do objeto Maze e carregamento do labirinto a partir do arquivo CSV
maze = Maze() 
maze.load_from_csv(maze_csv_path)

# Inicia a exibição gráfica do labirinto
maze.run()

# Inicializa a posição do jogador e do prêmio dentro do labirinto
maze.init_player()

def solve_maze_backtracking(maze):
    """
    Função que resolve o labirinto utilizando a estratégia de backtracking com pilha.
    
    O jogador se movimenta explorando os caminhos disponíveis e retrocede caso encontre um beco sem saída.
    
    Parâmetros:
        maze (Maze): Objeto que representa o labirinto.
    
    Retorna:
        bool: True se o prêmio for encontrado, False caso contrário.
    """
    stack = deque()  # Pilha para armazenar os caminhos explorados
    visited = set()  # Conjunto para armazenar as posições já visitadas
    start_pos = maze.get_init_pos_player()  # Obtém a posição inicial do jogador
    stack.append(start_pos)  # Empilha a posição inicial
    
    while stack:  # Enquanto houver caminhos a explorar
        current_pos = stack.pop()  # Remove o último elemento da pilha (backtracking)
        
        # Verifica se a posição atual contém o prêmio
        if maze.find_prize(current_pos):
            print("Prêmio encontrado na posição:", current_pos)
            return True  # Fim da busca
        
        # Se a posição ainda não foi visitada, adiciona ao conjunto e processa os vizinhos
        if current_pos not in visited:
            visited.add(current_pos)
            maze.mov_player(current_pos)  # Atualiza a posição visual do jogador
            
            # Definição das direções possíveis (cima, baixo, esquerda, direita)
            directions = [
                (current_pos[0]-1, current_pos[1]),  # Cima
                (current_pos[0]+1, current_pos[1]),  # Baixo
                (current_pos[0], current_pos[1]-1),  # Esquerda
                (current_pos[0], current_pos[1]+1)   # Direita
            ]
            
            # Explora cada direção possível
            for neighbor in directions:
                if maze.is_free(neighbor) and neighbor not in visited:
                    stack.append(neighbor)  # Adiciona à pilha para explorar depois
        
        time.sleep(0.1)  # Pequena pausa para visualização do progresso no labirinto
        
    print("Caminho não encontrado!")  # Caso o labirinto não tenha solução
    return False

# Inicia a resolução do labirinto
solve_maze_backtracking(maze)
