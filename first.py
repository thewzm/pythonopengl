from OpenGL.GL import *
from OpenGL.GLUT import *

import openmesh as om

GLUT_WHEEL_UP = 3
GLUT_WHEEL_DOWN = 4
#  鼠标交互有关的
mousetate = 0  # 鼠标当前的状态
Oldx = 0.0  # 点击之前的位置
Oldy = 0.0

# # 与实现角度大小相关的参数，只需要两个就可以完成
xRotate = 0.0
yRotate = 0.0
ty = 0.0
tx = 0.0
scale = 0.004

showFaceList = []
showWireList = []

showsatate = 1
showFace = True
showWire = False
showFlatlines = False

currentfile = 1

# mesh = om.TriMesh()


# mesh = om.read_trimesh("../objdata/bunny.obj")


# mesh = om.read_trimesh("cube.obj")
mesh = om.read_trimesh("Vase01.obj")


def setLightRes():
    lightPosition = [0, 1, 0, 0]
    glLightfv(GL_LIGHT0, GL_POSITION, lightPosition)
    glEnable(GL_LIGHTING)  # 启用光源
    glEnable(GL_LIGHT0)  # 使用指定灯光


def setupRC():
    # 当你想剔除背面的时候，
    # 你只需要调用glEnable(GL_CULL_FACE)就可以了，
    # OPENGL状态机会自动按照默认值进行CULL_FACE，默认是glFrontFace（GL_CCW）  GL_CCW逆时针为正，GL_CW顺时针
    glEnable(GL_DEPTH_TEST)
    glFrontFace(GL_CCW)
    glEnable(GL_CULL_FACE)

    glEnable(GL_LIGHTING)  # 启用光照计算
    ambientLight = [1, 0, 0, 0]  # 指定环境光强度（RGBA）  此时可以控制模型的显示颜色
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, ambientLight)  # 设置光照模型，将ambientLight所指定的RGBA强度值应用到环境光

    #  启用颜色追踪 设置多边形正面的环境光和散射光材料属性，追踪glColor
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)


def initGL():
    global showFaceList, showWireList
    glClearColor(1.0, 1.0, 1.0, 0.0)
    glClearDepth(2.0)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_DEPTH_TEST)

    setLightRes()  # 启用指定光源
    setupRC()  # 设置环境光

    showFaceList = glGenLists(1)  # 创建分配一个显示列表
    showWireList = glGenLists(1)

    glNewList(showWireList, GL_COMPILE)
    glDisable(GL_LIGHTING)
    glLineWidth(1.0)
    glColor3f(0.5, 0.5, 0.5)  # 灰色
    glBegin(GL_LINES)
    for it in mesh.halfedges():
        glVertex3fv(mesh.point(mesh.from_vertex_handle(it)))  # 半边的起始点
        glVertex3fv(mesh.point(mesh.to_vertex_handle(it)))  # 半边的终点
    glEnd()
    glEnable(GL_LIGHTING)
    glEndList()

    #  绘制flat
    glNewList(showFaceList, GL_COMPILE)
    for face in mesh.faces():
        glBegin(GL_TRIANGLES)
        for v in mesh.fv(face):
            glNormal3fv(mesh.normal(v))
            # print('v的法向量的坐标', mesh.normal(v))
            # print('v的坐标', mesh.point(v))
            glVertex3fv(mesh.point(v))
        # print('-------')
        glEnd()
    glEndList()


def reShape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    if w > h:
        glOrtho(-w / h, w / h, -1.0, 1.0, -100.0, 100.0)
    else:
        glOrtho(-1.0, 1.0, -h / w, h / w, -100.0, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def mySpecial(key, x, y):
    global showFace, showWire, showFlatlines

    global xRotate, yRotate, tx, ty, scale, currentfile

    if key == GLUT_KEY_F1:
        if showFace:
            showFace = False
            showWire = True
            print('切换显示模式为：WireFrame')
        elif showWire:
            showWire = False
            showFlatlines = True
            print("切换显示模式为：Flatlines")
        elif showFlatlines:
            showFlatlines = False
            showFace = True
            print("切换显示模式为：Flat")
    if key == GLUT_KEY_LEFT:
        tx -= 0.01

    if key == GLUT_KEY_RIGHT:
        tx += 0.01

    if key == GLUT_KEY_UP:
        ty -= 0.01

    if key == GLUT_KEY_DOWN:
        ty += 0.01
    glutPostRedisplay()


def myMouse(button, state, x, y):
    global mousetate, Oldx, Oldy, scale
    # 鼠标左键按下或者松开
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        mousetate = 1
        Oldy = y
        Oldx = x

    if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
        mousetate = 0

    # 滚轮事件 ,scale 增加就是放大 减小就是缩小,currentfile 对不同的模型用不用的scale
    if state == GLUT_UP and button == GLUT_WHEEL_DOWN:
        if currentfile == 1:
            scale += 0.0005
            print("666")

    if state == GLUT_UP and button == GLUT_WHEEL_UP:
        if currentfile == 1:
            scale -= 0.0005

    glutPostRedisplay()


def onMouseMove(x, y):
    global xRotate, yRotate, Oldx, Oldy
    if mousetate:
        yRotate += x - Oldx
        glutPostRedisplay()
        Oldx = x
        xRotate += y - Oldy
        glutPostRedisplay()
        Oldy = y


def myDisplay():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glRotatef(xRotate, 1.0, 0.0, 0.0)
    glRotatef(yRotate, 0.0, 1.0, 0.0)
    glTranslatef(tx, ty, 0)
    glScalef(scale, scale, scale)
    if showFace:
        glCallList(showFaceList)
    if showFlatlines:
        glCallList(showFaceList)
        glCallList(showWireList)
    if showWire:
        glCallList(showWireList)
    glutSwapBuffers()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)  # GLUT_Double表示使用双缓存而非单缓存
    glutInitWindowPosition(100, 100)
    glutInitWindowSize(1280, 720)
    glutCreateWindow("半边结构")

    initGL()
    glutMouseFunc(myMouse)
    glutMotionFunc(onMouseMove)
    glutSpecialFunc(mySpecial)
    glutReshapeFunc(reShape)
    glutDisplayFunc(myDisplay)
    glutMainLoop()


main()
