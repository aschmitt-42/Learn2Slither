import pygame
import sys
from agent import Agent
from board import Board

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
DARK_GREEN = (0, 200, 0)

# Constantes
CELL_SIZE = 30
BORDER_SIZE = 2
ACTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


class SnakeVisualizer:
    """Visualiseur graphique pour le jeu Snake en temps réel"""
    
    def __init__(self, board, rows=10, cols=10, cell_size=CELL_SIZE):
        self.board = board
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.width = cols * cell_size + 200  # +200 pour les infos
        self.height = rows * cell_size + 100
        self.screen = None
        self.clock = None
        self.running = True
        self.paused = False
        self.step_by_step = False
        self.current_step = 0
        self.step_requested = False
        
    def init_pygame(self):
        """Initialise pygame et crée la fenêtre"""
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Learn2Slither - Visualisation")
        self.clock = pygame.time.Clock()
        self.font_small = pygame.font.Font(None, 24)
        self.font_large = pygame.font.Font(None, 36)
        
    def draw_grid(self):
        """Dessine la grille du jeu"""
        for row in range(self.rows + 1):
            pygame.draw.line(self.screen, GRAY, 
                           (0, row * self.cell_size),
                           (self.cols * self.cell_size, row * self.cell_size), 1)
        for col in range(self.cols + 1):
            pygame.draw.line(self.screen, GRAY,
                           (col * self.cell_size, 0),
                           (col * self.cell_size, self.rows * self.cell_size), 1)
    
    def draw_cell(self, pos, color):
        """Dessine une cellule à la position donnée"""
        row, col = pos
        x = col * self.cell_size + BORDER_SIZE
        y = row * self.cell_size + BORDER_SIZE
        size = self.cell_size - 2 * BORDER_SIZE
        pygame.draw.rect(self.screen, color, (x, y, size, size))
    
    def draw_board(self):
        """Dessine tout le contenu du board"""
        # Dessiner la tête du snake (jaune)
        if self.board.snake:
            self.draw_cell(self.board.snake[0], YELLOW)
            
            # Dessiner le corps du snake (vert foncé)
            for segment in self.board.snake[1:]:
                self.draw_cell(segment, DARK_GREEN)
        
        # Dessiner les pommes vertes (vert clair)
        for apple in self.board.green_apples:
            self.draw_cell(apple, GREEN)
        
        # Dessiner la pomme rouge (rouge)
        self.draw_cell(self.board.red_apple, RED)
    
    def draw_info(self):
        """Affiche les informations à droite de l'écran"""
        info_x = self.cols * self.cell_size + 20
        info_y = 20
        
        # Longueur du snake
        length_text = self.font_small.render(f"Longueur: {len(self.board.snake)}", True, WHITE)
        self.screen.blit(length_text, (info_x, info_y))
        
        # Étape actuelle
        step_text = self.font_small.render(f"Étape: {self.current_step}", True, WHITE)
        self.screen.blit(step_text, (info_x, info_y + 30))
        
        # État (Pausé/En cours)
        state_text = "PAUSÉ" if self.paused else "EN COURS"
        state_color = RED if self.paused else GREEN
        state_surf = self.font_small.render(f"État: {state_text}", True, state_color)
        self.screen.blit(state_surf, (info_x, info_y + 60))
        
        # Contrôles
        controls = [
            "Contrôles:",
            "SPACE: Pause",
            "Right: Étape suivante",
            "R: Réinitialiser",
            "Q: Quitter"
        ]
        for i, control in enumerate(controls):
            text = self.font_small.render(control, True, WHITE)
            self.screen.blit(text, (info_x, info_y + 100 + i * 25))
    
    def handle_events(self):
        """Gère les événements clavier"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_RIGHT:
                    self.step_requested = True
                elif event.key == pygame.K_r:
                    # Réinitialiser le board
                    self.board = Board(self.rows, self.cols)
                    self.current_step = 0
                    self.paused = False
                    self.step_requested = False
    
    def close(self):
        """Ferme pygame"""
        pygame.quit()


def play_visual(agent, board=None, step_by_step=True, max_steps=500):
    """
    Lance la visualisation graphique d'une partie de snake
    
    Args:
        agent: L'agent IA pour jouer
        board: Le board à utiliser (crée un nouveau si None)
        step_by_step: Active le mode pas à pas
        max_steps: Nombre maximal de steps (par défaut 500)
    """
    if board is None:
        board = Board()
    
    # Initialiser le visualiseur
    visualizer = SnakeVisualizer(board, board.rows, board.cols)
    visualizer.init_pygame()
    visualizer.step_by_step = step_by_step
    
    # Configuration de l'agent
    agent.epsilon = 0  # Pas d'exploration, exploitation seulement
    
    done = False
    state = board.get_state()
    steps = 0
    
    clock_tick = 5  # 5 FPS pour l'affichage normal (ou 60 pour mode pas à pas)
    if step_by_step:
        visualizer.paused = True  # Commencer en pause pour le mode pas à pas
    
    try:
        while visualizer.running and not done and steps < max_steps:
            visualizer.handle_events()
            
            # Logique du jeu
            if not visualizer.paused or (step_by_step and visualizer.step_requested):
                # Choisir une action et se déplacer
                action_idx = agent.choose_action(state)
                direction = ACTIONS[action_idx]
                done, reward = board.move(direction)
                state = board.get_state()
                steps += 1
                visualizer.current_step = steps
                visualizer.step_requested = False
            
            # Affichage
            visualizer.screen.fill(BLACK)
            visualizer.draw_grid()
            visualizer.draw_board()
            visualizer.draw_info()
            pygame.display.flip()
            
            # Contrôler la vitesse
            visualizer.clock.tick(60)  # 60 FPS pour la fluidité
    
    finally:
        visualizer.close()
    
    # Afficher les résultats finaux
    print(f"\n=== Résultats ===")
    print(f"Longueur finale: {len(board.snake)}")
    print(f"Étapes totales: {steps}")
    print(f"Jeu terminé: {done}")
    
    return len(board.snake), steps


def play_multiple_visual(agent, num_games=3, max_steps=500):
    """
    Lance plusieurs parties avec visualisation
    
    Args:
        agent: L'agent IA pour jouer
        num_games: Nombre de parties à jouer
        max_steps: Nombre maximal de steps par partie
    """
    agent.epsilon = 0  # Pas d'exploration
    
    total_length = 0
    total_steps = 0
    
    for game_num in range(num_games):
        print(f"\n=== Partie {game_num + 1}/{num_games} ===")
        board = Board()
        length, steps = play_visual(agent, board, max_steps=max_steps)
        total_length += length
        total_steps += steps
    
    avg_length = total_length / num_games
    avg_steps = total_steps / num_games
    
    print(f"\n=== Moyennes ===")
    print(f"Longueur moyenne: {avg_length:.2f}")
    print(f"Étapes moyennes: {avg_steps:.2f}")
