
import pygame
import sys
import time

run = True

def main():
  # Initialize Pygame
  pygame.init()

  def quit():
    global run
    run = False
  
  # Constants
  WIDTH, HEIGHT = 700, 375
  PLAYER_SIZE = 50
  PLAYER_COLOR = (255, 255, 255)
  GRAVITY = 1
  JUMP_STRENGTH = -15
  
  # Create the screen
  screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
  pygame.display.set_caption("Pygame Platformer")
  
  # Player attributes
  player_x = WIDTH // 2
  player_y = HEIGHT // 2
  player_vel_x = 0
  player_vel_y = 0
  is_jumping = False
  player_weight = 1
  player2_x = WIDTH // 2
  player2_y = HEIGHT // 2
  player2_vel_x = 0
  player2_vel_y = 0
  Ris_jumping = False
  player2_weight = 1
  
  # Main game loop
  update = 1
  run = True
  while run:
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              run = False
  
      # Player movement
      keys = pygame.key.get_pressed()
      if keys[pygame.K_a]:
          player_vel_x = -5
      elif keys[pygame.K_d]:
          player_vel_x = 5
      else:
          player_vel_x = 0
  
      if not is_jumping:
          if keys[pygame.K_w]:
              player_vel_y = JUMP_STRENGTH
              is_jumping = True
      if keys[pygame.K_LSHIFT] and keys[pygame.K_a]:
        player_vel_x = -10
      if keys[pygame.K_LSHIFT] and keys[pygame.K_d]:
        player_vel_x = 10
  
  
      if keys[pygame.K_LEFT]:
        player2_vel_x = -5
      elif keys[pygame.K_RIGHT]:
        player2_vel_x = 5
      else:
        player2_vel_x = 0
      if not Ris_jumping:
        if keys[pygame.K_UP]:
            player2_vel_y = JUMP_STRENGTH
            Ris_jumping = True
      if keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
        player2_vel_x = -10
      if keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
        player2_vel_x = 10
      # Apply gravity
      player_vel_y += GRAVITY
      player2_vel_y += GRAVITY
  
      # Update player position
      player_x += player_vel_x
      player_y += player_vel_y
      player2_x += player2_vel_x
      player2_y += player2_vel_y
  
      # Boundaries
      if player_x < 0:
          player_x = 0
      if player_x > WIDTH - PLAYER_SIZE:
          player_x = WIDTH - PLAYER_SIZE
      if player_y > HEIGHT - PLAYER_SIZE:
          player_y = HEIGHT - PLAYER_SIZE
          is_jumping = False
          player_vel_y = 0
      if player2_x < 0:
        player2_x = 0
      if player2_x > WIDTH - PLAYER_SIZE:
        player2_x = WIDTH - PLAYER_SIZE
      if player2_y > HEIGHT - PLAYER_SIZE:
        player2_y = HEIGHT - PLAYER_SIZE
        Ris_jumping = False
        player2_vel_y = 0
  
      # Clear the screen
      screen.fill((0, 0, 0))
  
  
      # Draw the player
      pygame.draw.rect(screen, PLAYER_COLOR, (player_x, player_y, PLAYER_SIZE, PLAYER_SIZE))
      pygame.draw.rect(screen, PLAYER_COLOR, (player2_x, player2_y, PLAYER_SIZE, PLAYER_SIZE))
  
  
      # Update the display
      if update > 0:
        pygame.display.update()
        time.sleep(1 / 60)
  
  
  # Quit Pygame
  pygame.quit()
  sys.exit()
