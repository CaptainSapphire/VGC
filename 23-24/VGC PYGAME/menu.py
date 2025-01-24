from PIL import Image
import pygame
import sprites

WIDTH = 400
HEIGHT = 300
BACKGROUND = (0, 0, 0)


def main():  # starting scene
  pygame.init()
  screen = pygame.display.set_mode((WIDTH, HEIGHT))
  clock = pygame.time.Clock()

  button = sprites.Button("sprites/Buttons/NewButton.png", WIDTH / 2,
                          HEIGHT / 2)  # start button
  button2 = sprites.Button("sprites/Buttons/test.png", WIDTH / 2, HEIGHT / 2 +
                           100)  # testing button for harpers scene
  button3 = sprites.Button(
      "sprites/Buttons/test.png", WIDTH / 2, HEIGHT / 2 - 100
  )  #sorry if this is not how it is supposed to be, it probably is since it is invisible, but it was necesary to get to secene 3 for testing

  background = sprites.Background("sprites/BGs/NewBG.png", WIDTH, HEIGHT)

  sceneSprites = [background, button, button2, button3]

  while True:
    for event in pygame.event.get():  # closes window
      pos = pygame.mouse.get_pos()

      if event.type == pygame.QUIT:
        pygame.quit()

    if (button.isClick()):  # checks if start button is clicked
      return 1  # tells main to add 1 to scene index

    if (button2.isClick()):  # checks if test button is clicked
      return 3  # tells main to add 2 to scene index

    if (button3.isClick()):  # checks if test button is clicked
      return 4  # tells main to add 3 to scene index

    for Sprite in sceneSprites:
      Sprite.update()
      Sprite.draw(screen)

    pygame.display.flip()  # updates screen

    clock.tick(60)  # frame rate


if __name__ == "__main__":
  main()
