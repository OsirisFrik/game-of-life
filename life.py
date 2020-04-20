## game life
import pygame
import numpy as np
import time

pygame.init()

## screen size
width, height = 1000, 1000
screen = pygame.display.set_mode((height, width))

## background color
bg = 25, 25, 25
screen.fill(bg)

## num of cells
nxC, nyC = 25, 25

## dimensions of cells
dimCw = width / nxC
dimCh = height / nyC

## create a matrix by num of cells
gameState = np.zeros((nxC, nyC))

## pause state
pause = True


## set window title
def setTile(state):
  if (state): ## if game is paused
    pygame.display.set_caption('Press SPACE to start | Click cell to toggle state | Press R to reset')
  else:
    pygame.display.set_caption('Press SPACE to pause')

setTile(pause)    

while True:
  ev = pygame.event.get()
  
  ## copy gameState
  _gameState = np.copy(gameState)
  
  
  ## check events
  for event in ev:
    if event.type == pygame.KEYDOWN:
      ## pause game
      if event.key == 32:
        pause = not pause
        setTile(pause)
      
      ## reset game
      elif event.key == 114:
        _gameState = np.zeros((nxC, nyC))
        pause = True
        setTile(pause)
    
    ## mouse click event  
    mouseClick = pygame.mouse.get_pressed()

    if sum(mouseClick) > 0:
      ## get mouse position on px
      posX, posY = pygame.mouse.get_pos()
      ## convert to cells
      celX, celY = int(np.floor(posX / dimCw)), int(np.floor(posY / dimCh))
      
      ## get cell
      celVal = gameState[celX, celY]
      
      ## invert cell val
      if celVal == 1:
        _gameState[celX, celY] = 0
      else:
        _gameState[celX, celY] = 1
  
  ## clear screen
  screen.fill(bg)
  
  for y in range(0, nxC):
    for x in range(0, nyC):
      if not pause:
        ## get number of neigh
        n_neigh = gameState[(x - 1) % nxC, (y - 1) % nyC] + \
                  gameState[(x)     % nxC, (y - 1) % nyC] + \
                  gameState[(x + 1) % nxC, (y - 1) % nyC] + \
                  gameState[(x - 1) % nxC, (y)     % nyC] + \
                  gameState[(x + 1) % nxC, (y)     % nyC] + \
                  gameState[(x - 1) % nxC, (y + 1) % nyC] + \
                  gameState[(x)     % nxC, (y + 1) % nyC] + \
                  gameState[(x + 1) % nxC, (y + 1) % nyC]
                 
        ## rules of the life 
        if gameState[x, y] == 0 and n_neigh == 3:
          _gameState[x, y] = 1
        elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
          _gameState[x, y] = 0
      
      poly = [
        ((x)     * dimCw, y       * dimCh),
        ((x + 1) * dimCw, y       * dimCh),
        ((x + 1) * dimCw, (y + 1) * dimCh),
        ((x)     * dimCw, (y + 1) * dimCh)
      ]
          
      ## draw
      if _gameState[x, y] == 0:
        pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
      else:
        pygame.draw.polygon(screen, (255, 255, 255), poly, 0)
  
  ## update gamestate
  gameState = np.copy(_gameState)
  pygame.display.flip()
  time.sleep(0.1)
