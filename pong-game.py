import tkinter as tk
import random
import pygame
import os

class PongGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Sigma Pong")
        
        # Initialize pygame mixer for sound effects
        pygame.mixer.init()
        
        # Load sound effects
        self.hit_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "hit.wav"))
        self.score_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "score.wav"))
        
        # Create canvas
        self.canvas = tk.Canvas(root, width=800, height=400, bg="black")
        self.canvas.pack()
        
        # Create game elements
        self.ball = self.canvas.create_oval(390, 190, 410, 210, fill="white")
        self.paddle1 = self.canvas.create_rectangle(50, 150, 70, 250, fill="white")
        self.paddle2 = self.canvas.create_rectangle(730, 150, 750, 250, fill="white")
        
        # Create score display
        self.score1 = 0
        self.score2 = 0
        self.score_display = self.canvas.create_text(400, 50, text=f"{self.score1} - {self.score2}",
                                                   fill="white", font=("Arial", 20))
        
        # Ball movement
        self.ball_speed_x = 3
        self.ball_speed_y = 3
        
        # Paddle movement
        self.paddle_speed = 5
        self.paddle1_move = 0
        self.paddle2_move = 0
        
        # Bind keys
        self.root.bind("<KeyPress>", self.handle_keypress)
        self.root.bind("<KeyRelease>", self.handle_keyrelease)
        
        # Start game loop
        self.update()
    
    def handle_keypress(self, event):
        if event.keysym == "w":
            self.paddle1_move = -self.paddle_speed
        elif event.keysym == "s":
            self.paddle1_move = self.paddle_speed
        elif event.keysym == "Up":
            self.paddle2_move = -self.paddle_speed
        elif event.keysym == "Down":
            self.paddle2_move = self.paddle_speed
    
    def handle_keyrelease(self, event):
        if event.keysym in ["w", "s"]:
            self.paddle1_move = 0
        elif event.keysym in ["Up", "Down"]:
            self.paddle2_move = 0
    
    def update(self):
        # Move ball
        self.canvas.move(self.ball, self.ball_speed_x, self.ball_speed_y)
        
        # Move paddles
        self.canvas.move(self.paddle1, 0, self.paddle1_move)
        self.canvas.move(self.paddle2, 0, self.paddle2_move)
        
        # Get positions
        ball_pos = self.canvas.coords(self.ball)
        paddle1_pos = self.canvas.coords(self.paddle1)
        paddle2_pos = self.canvas.coords(self.paddle2)
        
        # Ball collision with top and bottom
        if ball_pos[1] <= 0 or ball_pos[3] >= 400:
            self.ball_speed_y = -self.ball_speed_y
            self.hit_sound.play()
        
        # Ball collision with paddles
        if self.canvas.find_overlapping(*ball_pos):
            if self.paddle1 in self.canvas.find_overlapping(*ball_pos) or \
               self.paddle2 in self.canvas.find_overlapping(*ball_pos):
                self.ball_speed_x = -self.ball_speed_x
                self.hit_sound.play()
        
        # Keep paddles in bounds
        if paddle1_pos[1] < 0:
            self.canvas.moveto(self.paddle1, 50, 0)
        elif paddle1_pos[3] > 400:
            self.canvas.moveto(self.paddle1, 50, 150)
            
        if paddle2_pos[1] < 0:
            self.canvas.moveto(self.paddle2, 730, 0)
        elif paddle2_pos[3] > 400:
            self.canvas.moveto(self.paddle2, 730, 150)
        
        # Score points
        if ball_pos[0] <= 0:
            self.score2 += 1
            self.reset_ball()
            self.score_sound.play()
        elif ball_pos[2] >= 800:
            self.score1 += 1
            self.reset_ball()
            self.score_sound.play()
        
        # Update score display
        self.canvas.itemconfig(self.score_display, text=f"{self.score1} - {self.score2}")
        
        # Continue game loop
        self.root.after(16, self.update)
    
    def reset_ball(self):
        self.canvas.coords(self.ball, 390, 190, 410, 210)
        self.ball_speed_x = 3 * random.choice([-1, 1])
        self.ball_speed_y = 3 * random.choice([-1, 1])

if __name__ == "__main__":
    root = tk.Tk()
    game = PongGame(root)
    root.mainloop()
