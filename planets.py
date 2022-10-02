import math, pygame

pygame.init()
WIDTH, HEIGHT = 800, 600

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 30
G = 0.07

class Planet:
    def __init__(self,  pos, velocity=[0, 0], radius=10, static=False):
        self.radius = radius
        self.mass = ((radius ** 3) * 9) // 4
        self.pos = [pos[0], pos[1]]
        self.vel = velocity
        self.static = static

    def render(self):
        if not self.static: pygame.draw.circle(screen, (250, 100, 100), self.pos, self.radius)
        else: pygame.draw.circle(screen, (250, 250, 100), self.pos, self.radius)

    def update_pos(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

    def update(self):
        self.update_pos()
        self.render()



class Physics:
    def __init__(self, G = 0.07):
        self.G = G

    def calc_acceleration(self, planet_1, planet_2):
        return (self.G * planet_2.mass) / (math.hypot(planet_1.pos[0] - planet_2.pos[0], planet_1.pos[1] - planet_2.pos[1]) ** 2)

    def update_vel(self, one, two):
        radians = math.atan2(one.pos[0] - two.pos[0], one.pos[1] - two.pos[1])
        one.vel[0] -= math.sin(radians) * self.calc_acceleration(one, two)
        one.vel[1] -= math.cos(radians) * self.calc_acceleration(one, two)


    def update(self, planets):
        for i in planets:   i.update()
        if len(planets) >= 2:
            for planet in range(len(planets)):
                for i in range(len(planets)):
                    if planet != i and planets[planet].static == False:
                        self.update_vel(planets[planet], planets[i])

def main():
    slowed = 20
    temp_x = 0
    time = 0
    time_multiply = 15
    button = 0
    planets = []
    physics = Physics()

    while True:
        screen.fill((0, 0, 0))
        clock.tick(FPS)
        time += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        
            if event.type == pygame.MOUSEBUTTONDOWN:
                temp_x, temp_y = event.pos[0], event.pos[1]
                time = 0
                button = event.button
                
            if event.type == pygame.MOUSEBUTTONUP: # F = m * a   F = G*m*M/r**2    a = G*M/r**2
                if event.button == 3:
                    planets.append(Planet((event.pos[0], event.pos[1]), [(temp_x - event.pos[0]) / slowed, (temp_y - event.pos[1]) / slowed], (time * time_multiply) / FPS, True))
                elif event.button == 1:
                    planets.append(Planet((event.pos[0], event.pos[1]), [(temp_x - event.pos[0]) / slowed, (temp_y - event.pos[1]) / slowed], (time * time_multiply) / FPS, False))
                button = 0
                temp_x, temp_y = 0, 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: planets = []
            

        if temp_x:  
            pygame.draw.line(screen, (250, 250, 250), (temp_x, temp_y), pygame.mouse.get_pos())
            if button == 1: pygame.draw.circle(screen, (250, 100, 100), pygame.mouse.get_pos(), (time * time_multiply) / FPS)
            elif button == 3: pygame.draw.circle(screen, (250, 250, 100), pygame.mouse.get_pos(), (time * time_multiply) / FPS)

        physics.update(planets)

        pygame.display.update()


if __name__ == "__main__":
    main()