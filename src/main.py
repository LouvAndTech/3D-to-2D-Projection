import pygame
from math import cos,sin,radians

#Taille
HAUTEUR = 720
LARGEUR = 1280

#Couleurs
WHITE = (255,255,255)
LIGHTBLUE = (114,159,207)
BLUE = (52,101,164)
GREEN = (0,255,0)
DARKGREEN = (78,154,6)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
PINK = (168,50,117)
PURPLE = (119,50,168)

class Screen():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((LARGEUR,HAUTEUR))

    """
    Method to en the pygame session
    @param: None
    @return: None
    """
    def close(self):
        pygame.display.quit()
        pygame.quit()

    """
    Method to update the screen
    @param: None
    @return: None
    """
    def updateScreen(self):
        pygame.display.flip()

    """
    Method to display the background
    @param: screen, the screen
    @return: None
    """
    def fondDecran(self):
        self.screen.fill(BLUE)
        pygame.draw.rect(self.screen,LIGHTBLUE,pygame.Rect(30,30,(1280-60),(720-60)))


    def drawLigne(self,start,end):
       pygame.draw.line(self.screen,GREEN,start,end,3)
    
    def drawCube(self,coord):
        #Back square
        self.drawLigne(coord[0],coord[1])
        self.drawLigne(coord[1],coord[2])
        self.drawLigne(coord[2],coord[3])
        self.drawLigne(coord[3],coord[0])

        #Front square
        self.drawLigne(coord[4],coord[5])
        self.drawLigne(coord[5],coord[6])
        self.drawLigne(coord[6],coord[7])
        self.drawLigne(coord[7],coord[4])

        #Sides
        self.drawLigne(coord[0],coord[4])
        self.drawLigne(coord[1],coord[5])
        self.drawLigne(coord[2],coord[6])
        self.drawLigne(coord[3],coord[7])

    def drawPyramid(self,coord):
        #Top with each
        self.drawLigne(coord[0],coord[1])
        self.drawLigne(coord[0],coord[2])
        self.drawLigne(coord[0],coord[3])
        self.drawLigne(coord[0],coord[4])

        #Bottum square
        self.drawLigne(coord[1],coord[2])
        self.drawLigne(coord[2],coord[3])
        self.drawLigne(coord[3],coord[4])
        self.drawLigne(coord[4],coord[1])


#Class To handle coordinate calculations
class Coordinates():
    def __init__(self,pos3D,offset,multiply,center):
        self.offset = offset
        self.multiply = multiply
        self.center = center
        self.pos3D = pos3D
        self.rotate(0)
        self.from3Dto2Dprojection()
        self.realCoordinates()
    
    #Project from 3D values into 2D values
    def from3Dto2Dprojection (self):
        self.pos2D = []
        for pos in (self.rotated3D):
            self.pos2D.append(self.from3Dto2D(pos[0],pos[1],pos[2]+self.offset))
    def from3Dto2D(self,x,y,z):
        return((x/z),(y/z)) 
    
    #Switch from virtual to real coordinates
    def realCoordinates (self):
        self.realPos2D = []
        for pos in (self.pos2D):
            val = round((pos[0]*self.multiply)+self.center[0]),round((pos[1]*self.multiply)+self.center[1])
            self.realPos2D.append(val)

    #Rotation on the Y axis
    def rotate(self,deg):
        angle = radians(deg)
        self.rotated3D = []
        for pos in (self.pos3D):
            self.rotated3D.append((pos[0]*cos(angle)-pos[2]*sin(angle),pos[1],pos[0]*sin(angle)+pos[2]*cos(angle)))
    
    def newRotation(self,angle):
        self.rotate(angle)
        self.from3Dto2Dprojection()
        self.realCoordinates()


"""
Check if exit is clicked
@param: an event
@return: True if exit is clicked, False otherwise)
"""
def eventQuit(a):
    return(a == pygame.QUIT)

def formSelect(forme):
    if forme == "cube":
        return [(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1),(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1)]
    elif forme == "pyramid":
        return [(0,1,0),(1,-1,1),(-1,-1,1),(-1,-1,-1),(1,-1,-1)]




if __name__ == "__main__":  

    """========== 3D -> 2D calculation =========="""
    #Init values
    forme = "cube"
    pos3D = [(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1),(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1)]
    zOffSet = -6
    multiply = 100
    center = [LARGEUR//2,HAUTEUR//2]

    #Create the object
    coord = Coordinates(pos3D,zOffSet,multiply,center)

    """========== Screen initialisation =========="""

    print("Start screen...")
    screen = Screen()
    screen.fondDecran()
    screen.updateScreen()
    print("Screen up")

    """========== GUI LOOP =========="""

    # game loop
    angle = 0.0
    time = 0
    running = True

    while running:

        #3D calculations
        coord.newRotation(angle)

        #Draw the cube
        screen.fondDecran()
        if forme == "cube":
            screen.drawCube(coord.realPos2D)
        elif forme == "pyramid":
            screen.drawPyramid(coord.realPos2D)
        screen.updateScreen()

        # for loop through the event queue  
        for event in pygame.event.get():
        
            # Check for QUIT event      
            if eventQuit(event.type):
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    forme = "cube" if forme == "pyramid" else "pyramid"
                elif event.key == pygame.K_ESCAPE:
                    running = False

                    
        #Update the angle and the distance for the next frame
        angle = 0 if (angle>=180) else angle+0.5
        coord.multiply = multiply + sin(radians(angle))*200
        coord.offset = zOffSet + coord.multiply/80

        #Automatic switch forme
        if time >= 1024:
            time = 0
            forme = "cube" if forme == "pyramid" else "pyramid"
        else:
            time += 1

        #Update the shape
        coord.pos3D = formSelect(forme)


    """========== Closing sequence =========="""

    print("Closing...")
    screen.close()