
import pygame
import sys
from engine_util import obs, thingmanag

WIDTH = 400
HEIGHT = 300
FPS = 30
# Will's code thing, if you want to make an edited version you need your own engine_util too, unless you are going to leave
# WASD movement and LShift for shadow mode


def main():

  def quit():
    global run
    run = False

  Player_height = 50
  Player_width = 50
  Player_x = int((WIDTH + Player_width) /
                 2)  #for start of a level start in the center of a room
  Player_y = int((HEIGHT + Player_height) / 2)
  Player2_
  move = True  #make move false while in cutscene or in menu
  White = (255, 255, 255)
  Black = (0, 0, 0)
  Red = (255, 0, 0)
  Green = (0, 255, 0)
  Blue = (0, 0, 255)
  gray = (100, 100, 100)
  PShadow = False
  hold = False
  collidingreal = False
  collidingshadow = False
  distx = 0
  disty = 0
  manager = thingmanag()

  ob1 = obs(manager, pygame.Rect(0, 200, 75, 25), grabable=True)

  ob2 = obs(manager, pygame.Rect(200, 0, 100, 50))

  ob3 = obs(manager, pygame.Rect(200, 250, 100, 50), shadow=True)

  ob4 = obs(manager, pygame.Rect(100, 100, 25, 100), wall=True)

  movet = 0
  Playerhitbox = pygame.Rect(Player_x, Player_y, Player_width, Player_height)

  clock = pygame.time.Clock()

  screen = pygame.display.set_mode((WIDTH, HEIGHT))

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      keys = pygame.key.get_pressed()

      Player_xpre = Player_x
      Player_ypre = Player_y

      if keys[pygame.K_w] and move == True:  #inputs for movement
        Player_y -= 5
      if keys[pygame.K_s] and move == True:
        Player_y += 5
      if keys[pygame.K_a] and move == True:
        Player_x -= 5
      if keys[pygame.K_d] and move == True:
        Player_x += 5
      if keys[pygame.K_SPACE]:
        if hold == False:
          for obj in manager.getobs():
            if obj.grabable == True:
              ob = obj.pos
              [obx, oby, obw, obh] = ob
              if obx == Player_x + Player_width or obx + obw == Player_x or oby == Player_y + Player_height or oby + obh == Player_y:
                hold = True
                distx = obx - Player_x
                disty = oby - Player_y
                obj.grabbed = True
      else:
        hold = False
        for obj in manager.getobs():
          obj.grabbed = False

      if Player_x < 0:
        Player_x = 0
      if Player_x + Player_width > WIDTH:
        Player_x = WIDTH - Player_width
      if Player_y < 0:
        Player_y = 0
      if Player_y + Player_height > HEIGHT:
        Player_y = HEIGHT - Player_height

      Playerhitbox = pygame.Rect(Player_x, Player_y, Player_width,
                                 Player_height)
      #edges of the room stoping movement, though may need to be changed to allow for room to draw walls

      for obj in manager.getobs():
        ob = obj.pos
        shadow = obj.shadow
        wal = obj.wall
        grabbed = obj.grabbed

        if Playerhitbox.colliderect(ob) and grabbed == False:
          if PShadow == shadow or wal == True:

            #if the object and you are both real do collisions
            [obx, oby, obw, obh] = ob
            Player_rx = Player_xpre + Player_width
            Player_dy = Player_ypre + Player_height
            obrx = obx + obw
            obdy = oby + obh
            if Player_xpre < obrx and Player_rx > obx:
              vercolpos = True
            else:
              vercolpos = False
            if Player_ypre < obdy and Player_dy > oby:
              horcolpos = True
            else:
              horcolpos = False

            if horcolpos:
              if Player_x > obx:
                Player_x = obx + obw
              else:
                Player_x = obx - Player_width
            if vercolpos:
              if Player_y > oby:
                Player_y = oby + obh
              else:
                Player_y = oby - Player_height
        Playerhitbox = pygame.Rect(Player_x, Player_y, Player_width,
                                   Player_height)
      for obj in manager.getobs():
        ob = obj.pos
        if Playerhitbox.colliderect(ob):
          if PShadow == True:
            collidingreal = True
          else:
            collidingshadow = True

      if hold == True:
        for obj in manager.getobs():
          if obj.grabbed == True:
            ob = obj.pos
            obshad1 = obj.shadow
            [obx, oby, obw, obh] = ob
            obxp = obx
            obx = Player_x + distx
            obyp = oby
            oby = Player_y + disty
            ob = [obx, oby, obw, obh]
            obrect = pygame.Rect(obx, oby, obw, obh)
            obj.pos = ob
            for obj2 in manager.getobs():
              grabbed2 = obj2.grabbed
              obshad2 = obj2.shadow
              obwal2 = obj2.wall
              if obwal2 == True:
                obshad2 = obshad1
              ob2 = obj2.pos
              [obx2, oby2, obw2, obh2] = ob2
              if obrect.colliderect(
                  ob2) and grabbed2 == False and obshad1 == obshad2:
                obrx = obxp + obw
                obdy = obyp + obh
                obrx2 = obx2 + obw2
                obdy2 = oby2 + obh2

                if obxp < obrx2 and obrx > obx2:
                  vercolposob = True
                else:
                  vercolposob = False
                if obyp < obdy2 and obdy > oby2:
                  horcolposob = True
                else:
                  horcolposob = False

                if horcolposob:
                  if obx > obx2:
                    Player_x = obx2 + obw2 - distx
                  else:
                    Player_x = obx2 - obw - distx
                if vercolposob:
                  if oby > oby2:
                    Player_y = oby2 + obh2 - disty
                  else:
                    Player_y = oby2 - obh - disty
                obx = Player_x + distx
                oby = Player_y + disty
                ob = [obx, oby, obw, obh]
                obj.pos = ob
            if obx < 0:
              obx = 0
              Player_x = obx - distx
            if oby < 0:
              oby = 0
              Player_y = oby - disty
            if oby + obh > HEIGHT:
              oby = HEIGHT - obh
              Player_y = oby - disty

            if obx + obw > WIDTH:
              obx = WIDTH - obw
              Player_x = obx - distx
            ob = [obx, oby, obw, obh]
            obj.pos = ob
      if keys[pygame.K_LSHIFT] and collidingshadow == False:
        player_color = Black
        PShadow = True
      elif keys[pygame.K_LSHIFT] == False and collidingreal == False:
        player_color = Red
        PShadow = False
      collidingshadow = False
      collidingreal = False
      Playerhitbox = pygame.Rect(Player_x, Player_y, Player_width,
                                 Player_height)
      screen.fill(White)
      for obj in manager.getobs():
        ob = obj.pos
        if obj.shadow == True:
          pygame.draw.rect(screen, Black, ob)
      for obj in manager.getobs():
        wal = obj.wall
        shadow = obj.shadow
        ob = obj.pos
        grabable = obj.grabable
        if wal == True:
          pygame.draw.rect(screen, gray, ob)
        elif grabable == True:
          pygame.draw.rect(screen, Red, ob)
        elif obj.shadow == False:
          pygame.draw.rect(screen, Blue, ob)
      pygame.draw.rect(screen, player_color, Playerhitbox)  #player being drawn

      pygame.display.update()

      clock.tick(FPS)
