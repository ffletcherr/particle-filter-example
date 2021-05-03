# Simple pygame program

# Import and initialize the pygame library
import pygame as pg
import numpy as np

class pfBasic :
    def __init__(self,N=500,bound=(800,600)):
        self.N = N
        self.particles = np.hstack([ np.random.uniform(0,bound[0],(N,1)),np.random.uniform(0,bound[1],(N,1)) ])
        self.weights   = np.ones(N) * (1./N)

    def loop(self, velocity, measure, R=1e+4):
        self.weights.fill(1.)
        for i in range(self.N):
            self.particles[i] += velocity + np.random.normal(0.1,5,2)
            self.weights[i] = (1/np.sqrt(2*np.pi*R))*np.exp(-.5*(np.linalg.norm(measure-self.particles[i])**2)/R)
        self.weights /= self.weights.sum() 
        indexes = np.random.choice(self.N,size=self.N,p=self.weights)    
        self.particles = self.particles[indexes]
    def get_topk(self,k=10):
        top_indexes = self.weights.argsort()[-k:][::-1]
        return self.particles[top_indexes]
    
bound = (800,600)
pf = pfBasic(N=500,bound=bound)
pg.init()
# Set up the drawing window
screen = pg.display.set_mode(bound)

# Run until the user asks to quit
running = True
click = False
# Fill the background with white
screen.fill((255, 255, 255))
prev_x,prev_y = 400,300
while running:
    pg.time.delay(100) 
    # Did the user click the window close button?
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        # handle MOUSEBUTTONUP
        elif event.type == pg.MOUSEBUTTONUP:
            click = True
    if True :
        # Fill the background with white
        screen.fill((255, 255, 255))
        # get mouse position (x,y)
        pos = pg.mouse.get_pos()
        absolute_x,absolute_y = list(pg.mouse.get_pos())
        real_x,real_y = absolute_x + np.random.normal(0.1,5), absolute_y + np.random.normal(0.1,5)
        measure_x,measure_y = (real_x * np.random.uniform(0.6,1.4) + 0.2,
                               real_y * np.random.uniform(0.6,1.4))
        # particle filter
        velocity    = np.array([absolute_x-prev_x,absolute_y-prev_y])
        measure     = np.array([measure_x,measure_y])
        pf.loop(velocity,measure)
        prev_x,prev_y = absolute_x,absolute_y
        # Draw a solid blue circle in the center
        # pg.draw.circle(screen, (0, 0, 255), (absolute_x, absolute_y), 5)
        pg.draw.circle(screen, (255, 0, 0), (real_x, real_y), 5)
        pg.draw.circle(screen, (0, 255, 0), (measure_x, measure_y), 5)
        topk = pf.get_topk(100)
        # print('topk:\n',topk)
        for pt in topk:
            pg.draw.circle(screen, (255, 0, 255), (pt[0], pt[1]), 1)
        pg.draw.circle(screen, (255, 0, 255), tuple(topk.mean(0)), 5,2)
        
        
        
            
            
    click = False

    # Flip the display
    pg.display.flip()

# Done! Time to quit.
pg.quit()