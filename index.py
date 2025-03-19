
import streamlit as st
import numpy as np
import time

# Game settings
GRID_SIZE = 20
GRID_WIDTH = GRID_SIZE
GRID_HEIGHT = GRID_SIZE
GAME_SPEED = 0.2

class SnakeGame:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.snake = [(GRID_WIDTH//2, GRID_HEIGHT//2)]
        self.direction = 'RIGHT'
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False

    def generate_food(self):
        while True:
            food = (np.random.randint(0, GRID_WIDTH), np.random.randint(0, GRID_HEIGHT))
            if food not in self.snake:
                return food

    def move_snake(self):
        if self.game_over:
            return

        head = self.snake[0]
        if self.direction == 'UP':
            new_head = (head[0], head[1] - 1)
        elif self.direction == 'DOWN':
            new_head = (head[0], head[1] + 1)
        elif self.direction == 'LEFT':
            new_head = (head[0] - 1, head[1])
        else:  # RIGHT
            new_head = (head[0] + 1, head[1])

        # Check for collisions
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
            new_head in self.snake):
            self.game_over = True
            return

        self.snake.insert(0, new_head)
        
        # Check if snake ate food
        if new_head == self.food:
            self.score += 1
            self.food = self.generate_food()
        else:
            self.snake.pop()

def main():
    st.set_page_config(page_title="Snake Game", layout="centered")
    st.title("🐍 Snake Game")

    # Initialize game state
    if 'game' not in st.session_state:
        st.session_state.game = SnakeGame()
        st.session_state.key = 'RIGHT'

    # Game controls
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.write("Use arrow keys to control the snake!")
        if st.button("New Game"):
            st.session_state.game.reset_game()

    # Handle keyboard input
    def handle_input():
        if st.session_state.key == 'UP' and st.session_state.game.direction != 'DOWN':
            st.session_state.game.direction = 'UP'
        elif st.session_state.key == 'DOWN' and st.session_state.game.direction != 'UP':
            st.session_state.game.direction = 'DOWN'
        elif st.session_state.key == 'LEFT' and st.session_state.game.direction != 'RIGHT':
            st.session_state.game.direction = 'LEFT'
        elif st.session_state.key == 'RIGHT' and st.session_state.game.direction != 'LEFT':
            st.session_state.game.direction = 'RIGHT'

    # Game display
    game_display = st.empty()
    score_display = st.empty()

    while not st.session_state.game.game_over:
        # Create game board
        board = np.zeros((GRID_HEIGHT, GRID_WIDTH))
        
        # Draw snake
        for segment in st.session_state.game.snake:
            board[segment[1], segment[0]] = 1
        
        # Draw food
        food = st.session_state.game.food
        board[food[1], food[0]] = 2

        # Update display
        game_display.text(f"Score: {st.session_state.game.score}\n" + "\n".join(
            ["".join(["🟩" if cell == 1 else "🍎" if cell == 2 else "⬜️" 
                     for cell in row]) for row in board]))

        # Move snake
        handle_input()
        st.session_state.game.move_snake()
        time.sleep(GAME_SPEED)
        st.experimental_rerun()

    if st.session_state.game.game_over:
        st.write(f"Game Over! Final Score: {st.session_state.game.score}")

if __name__ == "__main__":
    main()