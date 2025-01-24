import menu
import scene_1_a
import scene_1_b
import scene_2
import scene_3
import pygame

scenes = [menu, scene_1_a, scene_1_b, scene_2, scene_3]
sceneIndex = 0


def runScene(scene):
  output = scene.main(
  )  # in main() of scene when you want to move scene, add a return int where int is the scene Index you want to go to after it ends

  if (output == 0):  # a way to return in menu
    output = menu.main()

  return output


def main():
  pygame.init()
  global sceneIndex
  while True:
    sceneIndex = runScene(scenes[sceneIndex])


if __name__ == "__main__":
  main()
