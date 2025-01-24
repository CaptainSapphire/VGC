from PIL import Image
from PIL.ImageFilter import FIND_EDGES
import pygame as pg


class CollideManager:  ########## collide manager #########

  def __init__(self, WIDTH, HEIGHT):
    self.Player = Player
    self.wall_group = pg.sprite.Group()
    self.box_group = pg.sprite.Group()
    self.shadow_group = pg.sprite.Group()
    self.door_group = pg.sprite.Group()
    self.guard_group = pg.sprite.Group()
    self.collect_group = pg.sprite.Group()
    self.inventory = pg.sprite.Group()
    self.screenWidth = WIDTH
    self.screenHeight = HEIGHT

  def searchInventory(self, name):
    for collectable in self.inventory:
      if collectable.name == name:
        return True
    return False

  def checkCollisions(self):
    collided_walls = pg.sprite.spritecollide(self.Player, self.wall_group,
                                             False)
    collided_boxes = pg.sprite.spritecollide(self.Player, self.box_group,
                                             False)
    collided_shadows = pg.sprite.spritecollide(self.Player, self.shadow_group,
                                               False)
    collided_doors = pg.sprite.spritecollide(self.Player, self.door_group,
                                             False)
    collided_collect = pg.sprite.spritecollide(self.Player, self.collect_group,
                                               False)
    collided_enemies = pg.sprite.spritecollide(self.Player, self.guard_group,
                                               False)

    for collect in collided_collect:
      collect.collected()

    if len(collided_enemies) > 0:
      self.Player.killed()

    if self.Player.rect.x < 0:
      self.Player.rect.x = 0
    if self.Player.rect.x + self.Player.rect.width > self.screenWidth:
      self.Player.rect.x = self.screenWidth - self.Player.rect.width
    if self.Player.rect.y < 0:
      self.Player.rect.y = 0
    if self.Player.rect.y + self.Player.rect.height > self.screenHeight:
      self.Player.rect.y = self.screenHeight - self.Player.rect.height

    for door in collided_doors:
      door.isOpen = True
      self.collision(self.Player, door)
      break

    if (len(collided_walls) > 0 or len(collided_boxes) > 0):
      self.Player.collidingreal = True
    else:
      self.Player.collidingreal = False
    if (len(collided_shadows) > 0):
      self.Player.collidingshadow = True
    else:
      self.Player.collidingshadow = False

    for wall in collided_walls:
      self.collision(self.Player, wall)

    if not (self.Player.PShadow):
      for box in collided_boxes:
        if self.Player.holding:
          box.grabbed = True
        else:
          self.collision(self.Player, box)

      for box in self.box_group:
        if self.Player.holding:
          if box.grabbed:
            box.preX = box.rect.x  # moving a held box
            box.preY = box.rect.y
            box.rect.x += self.Player.rect.x - self.Player.preX
            box.rect.y += self.Player.rect.y - self.Player.preY
        else:
          box.grabbed = False

        box_wall_col_group = pg.sprite.spritecollide(
            box, self.wall_group, False)  # box * wall collision
        for wall in box_wall_col_group:
          boxPreX = box.rect.x
          boxPreY = box.rect.y
          self.collision(box, wall)
          self.Player.rect.x += box.rect.x - boxPreX
          self.Player.rect.y += box.rect.y - boxPreY

        boxPreX = box.rect.x  # box * screen collision
        boxPreY = box.rect.y
        if box.rect.x < 0:
          box.rect.x = 0
        if box.rect.x + box.rect.width > self.screenWidth:
          box.rect.x = self.screenWidth - box.rect.width
        if box.rect.y < 0:
          box.rect.y = 0
        if box.rect.y + box.rect.height > self.screenHeight:
          box.rect.y = self.screenHeight - box.rect.height
        self.Player.rect.x += box.rect.x - boxPreX
        self.Player.rect.y += box.rect.y - boxPreY

    else: # player * shadow collision
      collided_shadows = pg.sprite.spritecollide(self.Player,
                                                 self.shadow_group, False)
      for shadow in collided_shadows:
        self.collision(self.Player, shadow)

  def collision(self, movingCol, collidable):
    [obx, oby, obw, obh] = collidable.rect

    if movingCol.preX < obx + obw and movingCol.preX + movingCol.rect.width > obx:
      if movingCol.rect.y > oby:
        movingCol.rect.y = oby + obh
      else:
        movingCol.rect.y = oby - movingCol.rect.height
    if movingCol.preY < oby + obh and movingCol.preY + movingCol.rect.height > oby:
      if movingCol.rect.x > obx:
        movingCol.rect.x = obx + obw
      else:
        movingCol.rect.x = obx - movingCol.rect.width


class Sprite(pg.sprite.Sprite):  ######### sprite #########

  def __init__(self, image, startx, starty, *groups):
    super().__init__(*groups)

    self.image = pg.image.load(image)
    self.rect = self.image.get_rect()

    self.rect.center = [startx, starty]

  def update(self):
    pass

  def draw(self, screen):
    screen.blit(self.image, self.rect)


class Collider(Sprite):  ########## collider #############

  def __init__(self,
               image,
               startx,
               starty,
               manager,
               shadow=False,
               wall=False,
               *groups):
    super().__init__(image, startx, starty, *groups)
    if (wall):
      manager.wall_group.add(self)
    elif (shadow):
      manager.shadow_group.add(self)
    self.manager = manager


class Collectable(Collider):  ####### Colectable #########

  def __init__(self, image, startx, starty, name, manager, *groups):
    keyImage = Image.open("sprites/Collectables/key.png")
    keyImage.resize((25, 25)).save("sprites/Collectables/newKey.png")

    self.inInventor = False
    self.name = name
    super().__init__(image, startx, starty, manager, *groups)
    manager.collect_group.add(self)

  def collected(self):
    self.manager.inventory.add(self)
    self.inInventor = True

  def draw(self, screen):
    if (self.inInventor):
      pass
    else:
      screen.blit(self.image, self.rect)


class Player(Collider):  ############ player ##############

  def __init__(self, startx, starty, manager, playerSpeed, *groups):
    playerImage = Image.open("sprites/Player/player.png")
    playerImage.resize((25, 25)).save("sprites/Player/NewPlayer.png")

    shadowImage = Image.open("sprites/Player/NewPlayer.png")
    shadowImage = shadowImage.filter(FIND_EDGES)
    shadowImage.putalpha(128)
    shadowImage.save("sprites/Player/PlayerShadow.png")

    self.preX = startx
    self.preY = starty

    super().__init__("sprites/Player/NewPlayer.png", startx, starty, manager,
                     *groups)

    self.collidingreal = False
    self.collidingshadow = False
    self.PShadow = False
    self.hold = False
    self.collidingreal = False
    self.collidingshadow = False
    self.holding = False
    manager.Player = self
    self.speed = playerSpeed
    self.alive = True

  def update(self):
    self.preX = self.rect.x
    self.preY = self.rect.y

    keys = pg.key.get_pressed()
    if keys[pg.K_a]:
      self.move(-self.speed, 0)
    elif keys[pg.K_d]:
      self.move(self.speed, 0)

    if keys[pg.K_w]:
      self.move(0, -self.speed)
    elif keys[pg.K_s]:
      self.move(0, self.speed)

    if keys[pg.K_SPACE]:
      if not (self.holding):
        self.holding = True
    else:
      self.holding = False

    if keys[pg.K_LSHIFT] and not (self.holding) and not (self.collidingshadow):
      self.image = pg.image.load("sprites/Player/PlayerShadow.png")
      self.PShadow = True
    elif keys[pg.K_LSHIFT] is False and not (self.collidingreal):
      self.image = pg.image.load("sprites/Player/NewPlayer.png")
      self.PShadow = False

  def move(self, x, y):
    self.rect.move_ip([x, y])

  def killed(self):
    self.alive = False


class Guard(Collider):  ############ guard ############

  def __init__(self,
               image,
               startx,
               starty,
               distance,
               speed,
               manager,
               hor=True,
               *groups):
    guardImage = Image.open("sprites/Guards/Guard.png")
    guardImage.resize((25, 25)).save("sprites/Guards/newGuardE.png")
    guardImage = Image.open("sprites/Guards/newGuardE.png")
    guardImage.rotate(180, expand=True).save("sprites/Guards/newGuardW.png")
    guardImage = Image.open("sprites/Guards/newGuardE.png")
    guardImage.rotate(90, expand=True).save("sprites/Guards/newGuardS.png")
    guardImage = Image.open("sprites/Guards/newGuardE.png")
    guardImage.rotate(-90, expand=True).save("sprites/Guards/newGuardN.png")

    if hor:
      guardImage = "sprites/Guards/newGuardE.png"
      self.initial = startx
      self.final = startx + distance
    else:
      guardImage = "sprites/Guards/newGuardS.png"
      self.initial = starty
      self.final = starty + distance

    self.speed = speed
    self.hor = hor
    self.turn = False

    super().__init__(guardImage, startx, starty, manager, *groups)
    manager.guard_group.add(self)

  def update(self):
    if self.hor:
      if not (self.turn):
        if self.rect.x < self.final:
          self.rect.x += self.speed
        else:
          self.image = pg.image.load("sprites/Guards/newGuardW.png")
          self.turn = True
      else:
        if self.rect.x > self.initial:
          self.rect.x -= self.speed
        else:
          self.image = pg.image.load("sprites/Guards/newGuardE.png")
          self.turn = False
    else:
      if not (self.turn):
        if self.rect.y < self.final:
          self.rect.y += self.speed
        else:
          self.image = pg.image.load("sprites/Guards/newGuardN.png")
          self.turn = True
      else:
        if self.rect.y > self.initial:
          self.rect.y -= self.speed
        else:
          self.image = pg.image.load("sprites/Guards/newGuardS.png")
          self.turn = False


class Box(Collider):  ############### box ################

  def __init__(self, image, startx, starty, manager, *groups):
    boxImage = Image.open("sprites/Boxes/box_moveable.png").crop(
        (90, 100, 400, 410))
    boxImage.resize((25, 25)).save("sprites/Boxes/NewBox.png")

    super().__init__(image, startx, starty, manager, *groups)
    manager.box_group.add(self)

    self.preX = self.rect.x
    self.preY = self.rect.y

    self.grabbed = False


class Door(Collider):  ############# door ###########

  def __init__(self, image, startx, starty, manager, *groups):
    doorImage = Image.open("sprites/Doors/door.png")
    doorImage.thumbnail((50, 50))
    doorImage.save("sprites/Doors/NewDoorW.png")
    doorImage = Image.open("sprites/Doors/NewDoorW.png")
    doorImage.rotate(180, expand=True).save("sprites/Doors/NewDoorE.png")

    super().__init__(image, startx, starty, manager, *groups)
    manager.door_group.add(self)
    self.isOpen = False

  def open(self):
    if self.isOpen:
      return True


class Button(Sprite):  ############# button ##################

  def __init__(self, image, startx, starty, *groups):
    buttonImage = Image.open("sprites/Buttons/settingsButton.png")
    buttonImage.thumbnail((50, 50))
    buttonImage.save("sprites/Buttons/NewSetButton.png")

    buttonImage = Image.open("sprites/Buttons/Button.png")
    newImage = buttonImage.crop((50, 200, 550, 400))
    newImage.thumbnail((200, 200))
    newImage.save("sprites/Buttons/NewButton.png")

    buttonImage2 = Image.open("sprites/Buttons/testbutton.png")
    buttonImage2.thumbnail((100, 100))
    buttonImage2.save("sprites/Buttons/test.png")

    super().__init__(image, startx, starty, *groups)

  def isClick(self, *groups):
    mouse_pos = pg.mouse.get_pos()
    mouse_click = pg.mouse.get_pressed()

    if self.rect.collidepoint(mouse_pos):
      if mouse_click[0]:
        return True


class Wall(Collider):  ############# wall  ##################

  def __init__(self, startx, starty, manager, vertical, num, *groups):
    wallImage = Image.open("sprites/Walls/wall.png")
    wallImage = wallImage.crop((0, 0, 85, 400))
    wallImage.resize(
        (15, 50)).save("sprites/Walls/newWallV.png")  # walls are 10 x 50

    wallImage = Image.open("sprites/Walls/newWallV.png")
    wallImage.rotate(270, expand=True).save("sprites/Walls/newWallH.png")

    wallImage = Image.open("sprites/Walls/solidWall.png")
    wallImage = wallImage.crop((0, 0, 125, 400))
    wallImage.resize(
        (15, 50)).save("sprites/Walls/newSWallV.png")  # walls are 10 x 50

    wallImage = Image.open("sprites/Walls/newSWallV.png")
    wallImage.rotate(270, expand=True).save("sprites/Walls/newSWallH.png")

    self.vertical = vertical  # boolean
    self.num = num  # number of walls
    if (self.vertical):
      self.image = "sprites/Walls/newWallV.png"
    else:
      self.image = "sprites/Walls/newWallH.png"
    super().__init__(self.image, startx, starty, manager, wall=True, *groups)

    self.startx = startx
    self.starty = starty

    if (self.vertical):
      tempImage = Image.open("sprites/Walls/newWallV.png")
      self.width = tempImage.width
      self.height = tempImage.height
      self.rect = pg.Rect(startx, starty, self.width, self.height * num)
      self.rect.center = [
          startx + self.width // 2, starty + self.height * num // 2
      ]
    else:
      tempImage = Image.open("sprites/Walls/newWallH.png")
      self.width = tempImage.width
      self.height = tempImage.height
      self.rect = pg.Rect(startx, starty, self.width * num, self.height)
      self.rect.center = [
          startx + self.width * num // 2, starty + self.height // 2
      ]

  def draw(self, screen):
    for i in range(self.num):
      if (self.vertical):
        tempRect = pg.Rect((self.startx, self.starty + i * self.height),
                           (self.width, self.height))
        screen.blit(self.image, tempRect)
      else:
        tempRect = pg.Rect(self.startx + i * self.width, self.starty,
                           self.width, self.height)
        screen.blit(self.image, tempRect)


class Background(Sprite):  ##########  BG  ###############

  def __init__(self, image, WIDTH, HEIGHT):
    BG = Image.open("sprites/BGs/edge.png")
    BG.thumbnail((50, 50))
    BG.save("sprites/BGs/NewBG.png")

    super().__init__(image, 0, 0)
    self.screenWidth = WIDTH
    self.screenHeight = HEIGHT
    self.image = pg.image.load(image)
    self.rect = self.image.get_rect()

  def draw(self, screen):
    for col in range(self.screenWidth // self.rect.width):
      for row in range(self.screenHeight // self.rect.height):
        tempRect = pg.Rect(col * self.rect.width, row * self.rect.height, col,
                           row)
        screen.blit(self.image, tempRect)
