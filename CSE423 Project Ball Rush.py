from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


wind_width = 400
wind_height = 500
pos_x = 70
pos_y = 100


objects_flg = 0
gameover_flg = 3
pause = False
print("Lives Left = ", gameover_flg)

reset_flg = False
cross_flg = False
lives = 3
gameScore = 0
circle_radius = 195
circle_x = 180
circle_y = 20

obj_y = wind_height + 400
right_obj_y = wind_height
obj_fall_speed = 4


# MAIN MID POINT ALGORITHM
def MidPointLine(zone, x1, y1, x2, y2):
    dx = (x2-x1)
    dy = (y2-y1)
    x = x1
    y = y1

    dInitial = 2*dy - dx

    Del_E = 2*dy
    Del_NE = 2*(dy-dx)

    while x <= x2:
        a, b = ConvertToOriginal(zone, x, y)
        drawpoints(a, b)

        if dInitial <= 0:
            x = x + 1
            dInitial = dInitial + Del_E
        else:
            x = x + 1
            y = y + 1
            dInitial = dInitial + Del_NE


def FindZone(x1, y1, x2, y2):
    dx = (x2-x1)
    dy = (y2-y1)

    if abs(dx) > abs(dy):
        if dx > 0 and dy > 0:
            return 0
        elif dx < 0 and dy > 0:
            return 3
        elif dx < 0 and dy < 0:
            return 4
        else:
            return 7
    else:
        if dx > 0 and dy > 0:
            return 1
        elif dx < 0 and dy > 0:
            return 2
        elif dx < 0 and dy < 0:
            return 5
        else:
            return 6


def ConvertToZoneZero(zone, x, y):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y


def ConvertToOriginal(zone, x, y):
    if zone == 0:
        return x, y
    if zone == 1:
        return y, x
    if zone == 2:
        return -y, x
    if zone == 3:
        return -x, y
    if zone == 4:
        return -x, -y
    if zone == 5:
        return -y, -x
    if zone == 6:
        return y, -x
    if zone == 7:
        return x, -y


def DrawLine(x1, y1, x2, y2):
    zone = FindZone(x1, y1, x2, y2)
    x1, y1 = ConvertToZoneZero(zone, x1, y1)
    x2, y2 = ConvertToZoneZero(zone, x2, y2)
    MidPointLine(zone, x1, y1, x2, y2)


# midpoint circle algorithm
def MidPointCircle(cx, cy, radius):
    d = (1 - radius)
    x = 0
    y = radius

    CirclePoints(x, y, cx, cy)

    while x < y:
        if d < 0:
            d = d + 2 * x + 3
            x = x + 1
        else:
            d = d + 2 * x - 2 * y + 5
            x = x + 1
            y = y - 1

        CirclePoints(x, y, cx, cy)


# circle at x,y coordinate and cx,cy center
def CirclePoints(x, y, cx, cy):

    glVertex2f(x + cx, y + cy)
    glVertex2f(y + cx, x + cy)

    glVertex2f(y + cx, -x + cy)
    glVertex2f(x + cx, -y + cy)

    glVertex2f(-x + cx, -y + cy)
    glVertex2f(-y + cx, -x + cy)

    glVertex2f(-y + cx, x + cy)
    glVertex2f(-x + cx, y + cy)


# THE CONTROLLING BUTTONS
def back_button():
    glColor3f(0, 1, 0)
    DrawLine(9, 89, 19, 99)
    DrawLine(9, 89, 19, 79)
    DrawLine(9, 89, 39, 89)


def cross_button():
    glColor3f(1, 0, 0)
    DrawLine(345, 75, 365, 95)
    DrawLine(345, 95, 365, 75)


# KEYBOARD CONTROL
def KeyboardListener(key, x, y):
    global pause
    if key == b" ":
        pause = not pause
    print("Pause/Start", pause)


def specialKeyboardListener(key, x, y):
    global circle_radius, circle_x

    if not pause:
        if key == GLUT_KEY_LEFT:
            circle_radius = circle_radius - 26
            circle_x = circle_x - 26
        elif key == GLUT_KEY_RIGHT:
            circle_radius = circle_radius + 26
            circle_x = circle_x + 26

    circle_radius = max(114, min(284, circle_radius))
    circle_x = max(95, min(265, circle_x))


# MOUSE CONTROL
def mouseListener(button, state, x, y):
    global reset_flg, cross_flg, wind_height

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if 9 <= x <= 35 and (wind_height - 100) <= y <= (wind_height - 80):
            reset_flg = True
            print("Reset Button")
        elif 345 <= x <= 365 and (wind_height - 100) <= y <= (wind_height - 80):
            cross_flg = True
            print("Exit Button")


def crl_boundary():
    glColor3f(0, 0, 0)
    global circle_x, circle_y
    DrawLine(circle_x, circle_y, circle_x+30, circle_y)
    # upper line
    DrawLine(circle_x, circle_y+30,
             circle_x+30, circle_y+30)
    DrawLine(circle_x, circle_y,
             circle_x+0.1, circle_y+30)
    DrawLine(circle_x+30, circle_y,
             circle_x+30.1, circle_y+30)


# path
def path():
    glColor3f(1, 0.5, 0.5)
    DrawLine(99, 0, 99.1, wind_height)
    DrawLine(301, 0, 301.1, wind_height)

# TIMER FOR 60 FPS
def timer(value):
    glutPostRedisplay()
    glutTimerFunc(13, timer, 0)
    glutPostRedisplay()

# pathSide Obstacles
def blocks_1():
    global obj_y, obj_fall_speed, objects_flg, gameScore, gameover_flg
    glColor3f(0, 0.5, 1)
    DrawLine(110, obj_y+110, 210, obj_y+110)
    DrawLine(210, obj_y+110, 210, obj_y)
    DrawLine(110, obj_y, 210, obj_y)
    DrawLine(110, obj_y+110, 110, obj_y)

    if gameover_flg != 0 and not pause:
        obj_y = obj_y - obj_fall_speed
    else:
        obj_y = obj_y

    if (200 > circle_x and
            100 < circle_x+30 and
            obj_y < circle_y and
            obj_y+100 > circle_y+30
        ):
        
        obj_y = wind_height + 400
        objects_flg = 1
        gameover_flg = gameover_flg - 1
        print("Lives Left = ", gameover_flg)
        

        if gameover_flg == 0:
            obj_fall_speed = 0
            totalScore = gameScore
            gameScore = 0
            print("=========================")
            print("Game Over!")
            print("Total Score: ", totalScore)

    elif obj_y + 100 < 0:
        obj_y = wind_height + 400
        objects_flg = 1
        gameScore = gameScore + 1
        obj_fall_speed = obj_fall_speed + 0.7
        print("Game Score = ", gameScore)


def blocks_2():
    global obj_y, obj_fall_speed, objects_flg, gameScore, gameover_flg
    glColor3f(1, 0, 0)
    DrawLine(190, obj_y+90, 290, obj_y+90)
    DrawLine(290, obj_y+90, 290, obj_y)
    DrawLine(190, obj_y, 290, obj_y)
    DrawLine(190, obj_y+90, 190, obj_y)

    if gameover_flg != 0 and not pause:
        obj_y = obj_y - obj_fall_speed
    else:
        obj_y = obj_y

    if (200 < circle_x < 300 and obj_y < circle_y < obj_y+100):

        gameover_flg = gameover_flg - 1
        print("Lives Left = ", gameover_flg)
        objects_flg = 2
        obj_y = wind_height + 400

        if gameover_flg == 0:
            obj_fall_speed = 0
            totalScore = gameScore
            gameScore = 0
            print("=============================")
            print("Game Over!")
            print("Total Score: ", totalScore)

    elif obj_y + 100 < 0:
        objects_flg = 2
        obj_y = wind_height + 400
        gameScore = gameScore + 1
        obj_fall_speed = obj_fall_speed + 0.7
        print("Game Score = ", gameScore)


def blocks_3():
    glColor3f(0, 1, 0)
    global obj_y, obj_fall_speed, objects_flg, gameScore, gameover_flg
    DrawLine(245, obj_y+100, 295, obj_y+100)
    DrawLine(295, obj_y+100, 295, obj_y)
    DrawLine(245, obj_y, 295, obj_y)
    DrawLine(245, obj_y+100, 245, obj_y)

    if gameover_flg != 0 and not pause:
        obj_y = obj_y - obj_fall_speed
    else:
        obj_y = obj_y

    if 250 < circle_x < 300 and obj_y < circle_y < obj_y+100:

        gameover_flg = gameover_flg - 1
        print("Lives Left = ", gameover_flg)
        objects_flg = 3
        obj_y = wind_height + 400

        if gameover_flg == 0:
            obj_fall_speed = 0
            totalScore = gameScore
            gameScore = 0
            print("=============================")
            print("Game Over!")
            print("Total Score: ", totalScore)

    elif obj_y + 100 < 0:
        objects_flg = 3
        obj_y = wind_height + 400
        gameScore = gameScore + 1
        obj_fall_speed = obj_fall_speed + 0.7
        print("Game Score = ", gameScore)


def blocks_4():
    glColor3f(0, 0, 1)
    global obj_y, obj_fall_speed, objects_flg, gameScore, gameover_flg
    DrawLine(120, obj_y + 100, 220, obj_y + 100)
    DrawLine(220, obj_y + 100, 220, obj_y)
    DrawLine(120, obj_y, 220, obj_y)
    DrawLine(120, obj_y + 100, 120, obj_y)

    if gameover_flg != 0 and not pause:
        obj_y = obj_y - obj_fall_speed
    else:
        obj_y = obj_y

    if 100 < circle_x < 200 and obj_y < circle_y < obj_y+100:

        gameover_flg = gameover_flg - 1
        print("Lives Left = ", gameover_flg)
        objects_flg = 4
        obj_y = wind_height + 400

        if gameover_flg == 0:
            totalScore = gameScore
            gameScore = 0
            print("=============================")
            print("Game Over!")
            print("Total Score: ", totalScore)

    elif obj_y + 100 < 0:
        objects_flg = 4
        obj_y = wind_height + 400
        gameScore = gameScore + 1
        obj_fall_speed = obj_fall_speed + 0.7
        print("Game Score = ", gameScore)


def blocks_5():
    glColor3f(0.5, 1, 0)
    global obj_y, obj_fall_speed, objects_flg, gameScore, gameover_flg
    DrawLine(245, obj_y+100, 295, obj_y+100)
    DrawLine(295, obj_y+100, 295, obj_y)
    DrawLine(245, obj_y, 295, obj_y)
    DrawLine(245, obj_y+100, 245, obj_y)

    if gameover_flg != 0 and not pause:
        obj_y = obj_y - obj_fall_speed
    else:
        obj_y = obj_y

    if 250 < circle_x < 300 and obj_y < circle_y < obj_y+100:

        gameover_flg = gameover_flg - 1
        print("Lives Left = ", gameover_flg)
        objects_flg = 0
        obj_y = wind_height + 400

        if gameover_flg == 0:
            totalScore = gameScore
            gameScore = 0
            print("=============================")
            print("Game Over!")
            print("Total Score: ", totalScore)

    elif obj_y + 100 < 0:
        objects_flg = 0
        obj_y = wind_height + 400
        gameScore = gameScore + 1
        obj_fall_speed = obj_fall_speed + 0.7
        print("Game Score = ", gameScore)


# creating the point (pixel)
def point_create():
    glColor3f(1, 1, 1)
    glPointSize(2)
    glBegin(GL_POINTS)
    MidPointCircle(circle_radius, 38, 8)

    if gameover_flg == 3:
        glColor3f(0, 0.5, 0.8)
        MidPointCircle(350, 300, lives)
        MidPointCircle(360, 300, lives)
        MidPointCircle(370, 300, lives)
    elif gameover_flg == 2:
        glColor3f(1.0, 1.0, 0)
        MidPointCircle(350, 300, lives)
        MidPointCircle(360, 300, lives)
    elif gameover_flg == 1:
        glColor3f(1, 0, 0)
        MidPointCircle(350, 300, lives)
    elif gameover_flg == 0:
        MidPointCircle(0, 0, lives)
    glEnd()


def drawpoints(x, y):
    glPointSize(2)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def iterate():
    glViewport(0, 0, wind_width, wind_height)
    glOrtho(0.0, wind_width, 0.0, wind_height, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)


def drawGameOverText():
    glColor3f(1, 0, 0)
    glRasterPos2f(130, 250)
    for char in "GAME OVER":
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Refreshing screen
    glClearColor(0, 0, 0, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()

    global reset_flg, cross_flg, gameScore, obj_y, obj_fall_speed, objects_flg, pause, gameover_flg, circle_radius, circle_x, circle_y
    if reset_flg:
        reset_flg = False
        gameScore = 0
        objects_flg = 0
        pause = False
        gameover_flg = 3
        obj_fall_speed = 4
        circle_radius = 195
        circle_x = 180
        circle_y = 20
        obj_y = wind_height + 400
        print("Reset!")
    else:
        back_button()

    if cross_flg:
        cross_button()
        glutLeaveMainLoop()
    else:
        cross_button()

    path()
    crl_boundary()
    point_create()

    if gameover_flg > 0:
        if objects_flg == 0:
            blocks_1()
        elif objects_flg == 1:
            blocks_3()
        elif objects_flg == 2:
            blocks_2()
        elif objects_flg == 3:
            blocks_4()
        elif objects_flg == 4:
            blocks_5()
    else:
        drawGameOverText() 

    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_RGBA)

glutInitWindowSize(wind_width, wind_height)
glutInitWindowPosition(pos_x, pos_y)

wind = glutCreateWindow(b"Ball Rush")
glutTimerFunc(0, timer, 0)

glutMouseFunc(mouseListener)
glutKeyboardFunc(KeyboardListener)
glutSpecialFunc(specialKeyboardListener)
glutDisplayFunc(display)

glutMainLoop()