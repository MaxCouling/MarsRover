import pygame
from pygame import *
from files.player import Player
from files.ground import Ground
from files.background import Background
from files.camera import *
import sys

#initating window and clocPlayergroup = pygame.sprite.Group()



class Game:
  def __init__(self):
    pygame.init()
    WINDOW_W, WINDOW_H = 600, 400
    self.canvas = pygame.Surface((WINDOW_W*10,WINDOW_H))#setting the canvas
    self.window = pygame.display.set_mode(((WINDOW_W,WINDOW_H)))#setting the window
    self.clock = pygame.time.Clock()#pygame clock
    self.dababy = pygame.image.load("dababy.jpg")
    
    
    #loading player, scenes and self.
    self.player = Player()
    self.groundgroup = pygame.sprite.Group()

    for i in range(0,4000, 600):#this is making the ground tile
      g = Ground(i, 280)
      self.groundgroup.add(g)

    self.background = Background()
    
    self.camera = Camera(self.player)
   # auto = Auto(self.camera,self.player)#its called borderself.
    self.follow = Follow(self.camera, self.player)
    self.animationspeed = 0
    
    
    
  
  def game(self):
    self.camera.setmethod(self.follow)
    while True:#main loop
      self.clock.tick(60)
      pygame.display.update()
      #key inputs
      for event in pygame.event.get():#exits the game 
        if event.type == pygame.QUIT:
          sys.exit()
        if event.type == KEYDOWN:
          if event.key == K_SPACE:
            self.jump()
          if event.key == K_j:
            self.player.acc.x += -self.player.ACC#making it so when you press the left arrow key the acc goes down
        

      self.canvas.fill((255,169,120))#background colour
      
      #updating and animating sprites
      self.player.move()#uses the player move funciton
      
      self.animationspeed += 1
      if self.animationspeed == 10:
      
      
        self.player.update()#playeranimation
        self.animationspeed = 0
      self.gravity_check()
      self.camera.scroll()
      
      #updating window and display
      #rendering the background
      #self.canvas.blit(self.background.sky,(self.background.skyX - (self.camera.offset.x/5), self.background.skyY - (self.camera.offset.y/5)))
      self.canvas.blit(self.background.mountains0, (self.background.mountains0X - (self.camera.offset.x/5), self.background.mountains0Y - (self.camera.offset.y/5)))
      self.canvas.blit(self.background.mountains1, (self.background.mountains1X - (self.camera.offset.x/3), self.background.mountains1Y - (self.camera.offset.y/3)))
      self.canvas.blit(self.background.mountains2, (self.background.mountains2X - (self.camera.offset.x/2), self.background.mountains2Y - (self.camera.offset.y/2)))
      
      
      
      self.canvas.blit(self.player.image,(self.player.rect.x- self.camera.offset.x, self.player.rect.y - self.camera.offset.y))
      
      for ground in self.groundgroup:
        self.canvas.blit(ground.image,(ground.rect.x - self.camera.offset.x, ground.rect.y - self.camera.offset.y))
      
      self.window.blit(self.canvas, (0,0))
      
      
    
      
  
  def gravity_check(self):
    
    hits = pygame.sprite.spritecollide(self.player ,self.groundgroup, False)
    if self.player.vel.y > 0:
      if hits:
        lowest = hits[0]#the first one in the list is the lowest
        if self.player.pos.y < lowest.rect.bottom:#if the player is touching the ground
          self.player.pos.y = lowest.rect.top +1#add one so it is above the ground
          self.player.vel.y = 0#set the verticle velocity to 0, it is on the ground now
          self.player.jumping = False#if player is touching the ground, it cannot be in the state of jump (duh)

  def jump(self):
    self.player.rect.x += 1
 
    # Check to see if payer is in contact with the ground
    hits = pygame.sprite.spritecollide(self.player, self.groundgroup, False)
     
    self.player.rect.x -= 1
 
    # If touching the ground, and not currently jumping, cause the player to jump.
    if hits and not self.player.jumping:
       self.player.jumping = True
       self.player.vel.y = -self.player.jump_height

       
      