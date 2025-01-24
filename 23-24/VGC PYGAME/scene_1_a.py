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

  wall1 = spr.Wall(100, 0, gameManager, True, 2)
  wall2 = spr.Wall(155, 105, gameManager, False, 5)

  background = spr.Background("sprites/BGs/NewBG.png", WIDTH, HEIGHT)

  player = spr.Player(100, 200, gameManager, 2.9)

  all_sprites = pg.sprite.Group()
  wall_group = pg.sprite.Group(wall1, wall2)
  box_group = pg.sprite.Group(spr.Box(boxImage, 130, 105, gameManager),
                              spr.Box(boxImage, 200, 200, gameManager))
  shadow_group = pg.sprite.Group()
  door_group = pg.sprite.Group(
      spr.Door("sprites/Doors/NewDoorW.png", 390, 200, gameManager))
  collectable_group = pg.sprite.Group(
      spr.Collectable("sprites/Collectables/newKey.png", 300, 50, "key", gameManager))

  all_sprites.add(background, wall_group, box_group, door_group, collectable_group, player, shadow_group, setButton)

  while True:
    for event in pg.event.get():  # closes window
      pos = pg.mouse.get_pos()

      if event.type == pg.QUIT:
        quit()

    pg.event.pump()
    if (setButton.isClick()):  # checks if start button is clicked
      return 0

    all_sprites.update()
    gameManager.checkCollisions()
    for door in door_group:
      if door.isOpen and gameManager.searchInventory("key"):
        return 2
      else:
        door.isOpen = False
    for sprite in all_sprites:
      sprite.draw(screen)

    pg.display.flip()

    clock.tick(60)


if __name__ == "__main__1":
  main()
