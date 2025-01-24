from PIL import Image
import pygame as pg
import sprites as spr

WIDTH = 400
HEIGHT = 300
BACKGROUND = (0, 0, 0)


def main():  # first scene
  pg.init()
  screen = pg.display.set_mode((WIDTH, HEIGHT))
  clock = pg.time.Clock()

  gameManager = spr.CollideManager(WIDTH, HEIGHT)

  setButton = spr.Button("sprites/Buttons/NewSetButton.png", 370, 30)

  boxImage = "sprites/Boxes/NewBox.png"

  wall1 = spr.Wall(100, 100, gameManager, True, 4)
  wall2 = spr.Wall(200, 0, gameManager, True, 4)

  background = spr.Background("sprites/BGs/NewBG.png", WIDTH, HEIGHT)

  player = spr.Player(35, 200, gameManager, 2.9)

  all_sprites = pg.sprite.Group()
  wall_group = pg.sprite.Group(wall1, wall2)
  box_group = pg.sprite.Group(spr.Box(boxImage, 150, 50, gameManager))
  shadow_group = pg.sprite.Group()
  door_group = pg.sprite.Group(
      spr.Door("sprites/Doors/NewDoorE.png", 10, 200, gameManager))
  enemy_group = pg.sprite.Group(
      spr.Guard("sprites/Guards/newGuard.png", 160, 250, 150, 1.5,
                gameManager))

  all_sprites.add(door_group, box_group, player, shadow_group, enemy_group,
                  setButton)

  while True:
    for event in pg.event.get():  # closes window
      pos = pg.mouse.get_pos()

      if event.type == pg.QUIT:
        quit()

    pg.event.pump()
    if (setButton.isClick()):  # checks if start button is clicked
      return 0

    background.draw(screen)
    wall1.draw(screen)
    wall2.draw(screen)
    all_sprites.update()
    gameManager.checkCollisions()
    for i in range(len(door_group)):
      if door_group.sprites()[i].isOpen:
        if i == 0:
          return 1
        if i == 1:
          return 3
    all_sprites.draw(screen)

    if not(player.alive):
      return 2

    pg.display.flip()

    clock.tick(60)


if __name__ == "__main__1":
  main()
