import random, pygame, sys, copy, math, key_input as IN, node
random.seed(0)
pygame.init()
width = 400
height = 400
s = pygame.display.set_mode((width,height))
p_clock = pygame.time.Clock()

graph = [node.node(random.randint(int(width/3),int(2/3 * width)), random.randint(int(height/3), int(2/3 * height))) for x in range(200)]
def dist(n1,n2): return abs(n1.x-n2.x)+abs(n1.y-n2.y)

data = []

repulsive_min_1 = 30
repulsive_max_1 = 32
repulsive_min_2 = 15
repulsive_max_2 = 12
viewing_range = 30

while True:

    pygame.draw.rect(s,(20,20,20),(0,0,width,height))

    # Each actor maintains a repulsive field, though the size of this field varies depending on the state of the actors
    # in close proximity. Namely, if no other actors have a larger field, switch to a larger field.
    # If all other actors have a larger field, switch to a larger field. With a very low probability, randomly switch
    # to a larger field. This acts as a catalyst for breaking up larger groups.
    # As is perhaps obvious the more groups the higher probability any one becomes the catalyst - hence larger groups
    # quickly disperse into smaller ones.
    # As the density changes, reformation into smaller clusters is more stable.
    for n1 in graph:
        n1.x += random.random()-0.5
        n1.y += random.random()-0.5
        n1.draw(s)

        # Pressing ASD shows the repulsion ranges and the viewing range.
        if IN.down( pygame.K_d ):
                pygame.draw.circle(s,(120,120,120),(int(n1.x),int(n1.y)),viewing_range,1)
        if IN.down( pygame.K_s ) and n1.value == 0:
                pygame.draw.circle(s,(255,0,255),(int(n1.x),int(n1.y)),repulsive_min_2,1)
        if IN.down( pygame.K_a ) and n1.value == 255:
                pygame.draw.circle(s,(150,255,0),(int(n1.x),int(n1.y)),repulsive_min_1,1)


        others = list(filter( lambda n: n!=n1 and dist(n,n1)<viewing_range, graph))
        #if (all([n.value == 255 for n in others]) or all([n.value != 255 for n in others])) and random.random()<0.9999: # V1
        #if random.random() < 0.999 and all([n.value != 255 for n in others]): # V2
        #if random.random() > 0.99 or sum([1 if n.value == 255 else 0 for n in others]) > 2: # V3
        #if random.random() > 0.999 or sum([1 if n.value == 255 else 0 for n in others]) > 0: # V4

        # Essentially this controls the probability of catalyst creation and the ease of contagion.
        if random.random() > 0.995 or sum([1 if n.value == 255 else 0 for n in others]) > 1: # V5
            n1.value = 255
        else: n1.value = 0

        spd = 1
        for o in others:
            dir = math.atan2(o.y-n1.y,o.x-n1.x)
            if n1.value == 255:
                if dist(n1,o) > repulsive_max_1:
                    n1.x += math.cos(dir)*spd
                    n1.y += math.sin(dir)*spd
                elif dist(n1,o) < repulsive_min_1:
                    n1.x -= math.cos(dir)*spd
                    n1.y -= math.sin(dir)*spd
            else:
                if dist(n1,o) > repulsive_max_2:
                    n1.x += math.cos(dir)*spd
                    n1.y += math.sin(dir)*spd
                elif dist(n1,o) < repulsive_min_2:
                    n1.x -= math.cos(dir)*spd
                    n1.y -= math.sin(dir)*spd

    # Refresh the graph when space is hit.
    if IN.pressed( pygame.K_SPACE ):
        graph = [node.node(random.randint(int(width/3),int(2/3 * width)), random.randint(int(height/3), int(2/3 * height))) for x in range(100)]

    # Update input state(s).
    IN.last_keys_down = copy.deepcopy(IN.keys_down)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.KEYDOWN: IN.keys_down[str(event.key)] = True
        elif event.type == pygame.KEYUP: IN.keys_down[str(event.key)] = False
        elif event.type == pygame.MOUSEBUTTONUP: IN.keys_down[str(event.button)] = False
        elif event.type == pygame.MOUSEBUTTONDOWN: IN.keys_down[str(event.button)] = True
        elif event.type == pygame.MOUSEMOTION: IN.mouse_position = event.pos

    pygame.display.flip()
    p_clock.tick(60)