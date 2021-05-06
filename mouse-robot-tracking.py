# Simple pygame program

# Import and initialize the pygame library
import pygame as pg
import numpy as np
import matplotlib.pyplot as plt
class pfBasic :
    def __init__(self,N=500,bound=(800,600)):
        self.N = N
        self.particles = np.hstack([ np.random.uniform(0,bound[0],(N,1)),np.random.uniform(0,bound[1],(N,1)) ])
        self.weights   = np.ones(N) * (1./N)

    def loop(self, r, theta, measure, R=1e+4):
        self.weights.fill(1.)
        for i in range(self.N):
            r_particle = r + np.random.normal(0.1,5)
            self.particles[i] += np.array([r_particle*np.cos(theta),-r_particle*np.sin(theta)])
            self.weights[i] = (1/np.sqrt(2*np.pi*R))*np.exp(-.5*(np.linalg.norm(measure-self.particles[i])**2)/R)
        self.weights /= self.weights.sum() 
        indexes = np.random.choice(self.N,size=self.N,p=self.weights)    
        self.particles = self.particles[indexes]
    def get_topk(self,k=10):
        top_indexes = self.weights.argsort()[-k:][::-1]
        return self.particles[top_indexes]
    
bound = (800,600)
N = 1000
K = N//2
pf = pfBasic(N=N,bound=bound)
pg.init()
# Set up the drawing window
screen = pg.display.set_mode(bound)

# Run until the user asks to quit
running = True
click = False
# Fill the background with white
screen.fill((255, 255, 255))
myfont = pg.font.SysFont("Comic Sans MS", 20)
prev = np.array([400,300])
f = 0
err_hist = []
while running:
    f += 1
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
        
        absolute = np.array(pg.mouse.get_pos())
        delta    = absolute - prev
        r,theta = np.linalg.norm(delta), np.arctan2(-delta[1],delta[0])
        r_robot =  r + np.random.normal(0.1,5)
        real = prev + np.array([r_robot*np.cos(theta),-r_robot*np.sin(theta)])
        measure = (real[0] * np.random.uniform(0.6,1.4) + 0.2,
                   real[1] * np.random.uniform(0.6,1.4))
        
        # particle filter
        pf.loop(r,theta,measure)
        prev = absolute
        
        topk = pf.get_topk(K)
        estimate = topk.mean(0)
        # print('topk:\n',topk)
        # draw topk particles
        for pt in topk:
            pg.draw.circle(screen, (255, 180, 255), (pt[0], pt[1]), 1)
        # Draw target and measure and estimation
        pg.draw.circle(screen, (255, 0, 0), tuple(real), 5)
        pg.draw.circle(screen, (0, 255, 0), tuple(measure), 5)
        pg.draw.circle(screen, (255, 0, 255), tuple(estimate), 5,2)
        # pg.image.save(screen, f"doc/media/{f}.jpeg")
        
        # add legend
        pg.draw.circle(screen, (255, 0, 0), (20,30), 5)
        pg.draw.circle(screen, (0, 255, 0), (20,50), 5)
        pg.draw.circle(screen, (255, 0, 255), (20,70), 5,2)
        # write text
        label = myfont.render("real pos", 1, (255, 0, 0))
        screen.blit(label, (30, 25))
        label = myfont.render("measurement", 1, (0, 255, 0))
        screen.blit(label, (30, 45))        
        label = myfont.render("estimation", 1, (255, 0, 255))
        screen.blit(label, (30, 65))
        label = myfont.render(f"Particles: {N}", 1, (255, 150, 255))
        screen.blit(label, (20,550))           
        
        # error log
        err_hist.append(np.linalg.norm(real - estimate))
            
            
    click = False

    # Flip the display
    pg.display.flip()
    
plt.plot(err_hist)
plt.title('Estimation error')
plt.xlabel('Step')
plt.ylabel('MSE')
plt.show()
# Done! Time to quit.
pg.quit()