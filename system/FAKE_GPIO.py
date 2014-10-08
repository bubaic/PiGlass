pygame = None
dwn = False

BCM = 0
IN = 0

def setmode(i):
    global pygame
    pygame = i

def setup(o, t):
    return

def input(pin):
    ev = pygame.event.poll()
    if ev.type == pygame.KEYDOWN:
        return True
    if ev.type == pygame.KEYUP:
        return False
    
        
