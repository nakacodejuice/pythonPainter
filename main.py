
import sys,os
from PyQt5.QtWidgets import QWidget, QApplication,QPushButton,QVBoxLayout,QLabel
from PyQt5.QtGui import QPainter, QColor, QPen, QFont,QPolygonF,QImage,QBrush
from PyQt5.QtCore import Qt,QPointF,QPoint
import sys, math, random
from PIL import Image
import sqlite3 as lite
import datetime
import uuid
import threading

namedb = "base.db"
class painter(QWidget):
    def __init__(self,x,y):
        super().__init__()
        self.x = x
        self.y = y
        self.isproc = False
        self.workpoint = ''
        self.painter = ''
        self.errsum = 0
        self._im = QImage(self.width(), self.height(), QImage.Format_ARGB32)
        self._im.fill(QColor("white"))
        self.initUI()

    def initUI(self):
        #self.setGeometry(100, 100, self.x, self.y)
        self.setWindowTitle('Painter')
        self.show()
        self.setFixedSize(self.x, self.y)
        self.getsumerr()


    # def paintEvent(self, e):
    #     self.qp.begin(self)
    #     self.drawPoly(self.qp)
    #     self.qp.end()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if (self.isproc==False):
            self.isproc = True
            self.painter = QPainter(self._im)
            self.painter.setPen(QPen(QColor("#000000"), 1, Qt.SolidLine, Qt.RoundCap))
            self.painter.setBrush(QBrush(QColor("#fc6c2d"), Qt.SolidPattern))
            #painter.drawEllipse(event.pos(), 10, 10)
            workpoint = self.getwork(self.width()/2,self.height()/2)

            self.drawPoly(self.painter,QPoint(workpoint['x'],workpoint['y']),
                                         workpoint['uid'],workpoint['r'],workpoint['g'],workpoint['b'])
            self.workpoint = workpoint
            self.startTimer(10)
            self.isproc == True
        else:
            self.isproc == False
        # i=0
        # while(i<=20):
        #     workpoint = self.getwork(self.workpoint['x'],self.workpoint['y'])
        #     self.drawPoly(self.painter, QPoint(workpoint['x'], workpoint['y']),
        #                   workpoint['uid'], workpoint['r'], workpoint['g'], workpoint['b'])
        #     # Перерисуемся
        #     # тут какие-то действия с перерисовкой
        #     self.update()
        #     i=i+1
        # self.update()
    def timerEvent(self, event):

        workpoint = self.getwork(self.workpoint['x'], self.workpoint['y'])
        print(workpoint)
        self.drawPoly(self.painter, QPoint(workpoint['x'], workpoint['y']),
                          workpoint['uid'], workpoint['r'], workpoint['g'], workpoint['b'])
        # Перерисуемся
        self.setUpdatesEnabled(True)
        self.update()
        #self.setUpdatesEnabled(False)
        if (self.isproc == False):
            self.killTimer()
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.drawImage(0, 0, self._im)

    def createPoly(self, n, r, s,pos):
        polygon = QPolygonF()
        w = 360 / n  # angle per step
        maxX=0
        maxY=0
        minX = 0
        minY = 0
        first = True
        for i in range(n):  # add the points of polygon
            t = w * i + s
            rand = random.randint(80,100)/100
            rad =  r *rand
            x = rad * math.cos(math.radians(t))
            y = rad * math.sin(math.radians(t))
            Xpos=pos.x() + x
            Ypos = pos.y() + y
            if Xpos>maxX:
                maxX =Xpos
            if Ypos>maxY:
                maxY =Ypos
            if Xpos<minX:
                minX =Xpos
            if Ypos < minY:
                minY = Ypos
            if(first):
                maxX = Xpos
                maxY = Ypos
                minX = Xpos
                minY = Ypos
                first=False
            polygon.append(QPointF(Xpos,Ypos))

        return {'polygon':polygon,'maxX':maxX,'maxY':maxY,'minX':minX,'minY':minY}

    def drawText(self, event, qp):
        qp.setPen(QColor(168, 34, 3))
        qp.setFont(QFont('Decorative', 10))
        qp.drawText(event.rect(), Qt.AlignCenter, 'dfsdfsdf')

    def drawPoly(self, qp,pos,uid,r,g,b):
        q= QColor(r, g, b)
        pen = QPen(q, 1, Qt.SolidLine)
        qp.setPen(pen)
        qp.setBrush(q)
        polystr = self.createPoly(80, 2, 0,pos)
        polygon = polystr['polygon']
        qp.drawPolygon(polygon)
        j = int(polystr['minY'])
        listOfPoints=[]
        while j<=getnum(polystr['maxY']):
            i = int(polystr['minX'])
            while i <= getnum(polystr['maxX']):
                if(polygon.containsPoint(QPointF(i,j),True)):
                    listOfPoints.append({'x':i,'y':j,'r':r,'g':g,'b':b})
                i=i+1
            j=j+1
        con = lite.connect(namedb)
        cur = con.cursor()
        today = datetime.datetime.today()
        for point in listOfPoints:
            cur.execute('update pictemp set r = ' + str(point['r']) + ', g=' + str(point['g']) + ', b=' + str(point['b']) + ', datetimechange="'+today.strftime("%Y-%m-%d %H:%M:%S")+'" where uid = "' + uid + '" and x=' + str(point['x']) + ' and y=' + str(point['y']))
        con.commit()

    def getwork(self,xold,yold):
        con = lite.connect(namedb)
        cur = con.cursor()
        cur.execute('select p.x,p.y ,p.r,p.g,p.b,p.uid, abs(p.r-temp.r)+abs(p.g-temp.g) +abs(p.b-temp.b) as er_sum,temp.datetimechange as tchange, abs(p.x-'+str(int(xold))+')*abs(p.x-'+str(int(xold))+') + abs(p.y-'+str(int(yold))+')*abs(p.y-'+str(int(yold))+') as xy from pic as p left join pictemp as temp on p.uid=temp.uid and p.x=temp.x  and p.y=temp.y '
                    'where abs(p.r-temp.r)+abs(p.g-temp.g) +abs(p.b-temp.b) > 0  '
                    'order by tchange,xy, er_sum desc limit 1')
        for row in cur:
            x = row[0]
            y = row[1]
            r = row[2]
            g = row[3]
            b = row[4]
            uid = row[5]
            err_sum = row[6]

        return {'x':x,'y':y,'r':r,'g':g,'b':b,'uid':uid,'err_sum':err_sum}

    def getsumerr(self):
        con = lite.connect(namedb)
        cur = con.cursor()
        cur.execute('select sum(abs(p.r-temp.r)+abs(p.g-temp.g) +abs(p.b-temp.b)) as er_sum from pic as p left join pictemp as temp on p.uid=temp.uid and p.x=temp.x  and p.y=temp.y')
        for row in cur:
            self.errsum =  row[0]

def readpic(pix,uid,i,event_for_wait, event_for_set,im):
    event_for_wait.wait()
    event_for_wait.clear()
    con = lite.connect(namedb)
    cur = con.cursor()
    j = 1
    while j <= im.size[0]:
        cur = con.cursor()
        color = pix[j - 1, i - 1] #изначально перепутал x и y
        #print(color)
        cur.execute('INSERT INTO pic (uid,x,y,r,g,b) values(?,?,?,?,?,?)',
                        (uid, i, j, color[0], color[1], color[2]))
        j = j + 1
    con.commit()
    event_for_set.set()

def setwhite(uid,i,event_for_wait, event_for_set,im):
    event_for_wait.wait()
    event_for_wait.clear()
    con = lite.connect(namedb)
    cur = con.cursor()
    j = 1
    while j <= im.size[0]:
        cur = con.cursor()
        color = (255,255,255)
        #print(str(i) + "-"+str(color))
        cur.execute('INSERT INTO pictemp (uid,x,y,r,g,b) values(?,?,?,?,?,?)',
                        (uid, i, j, color[0], color[1], color[2]))
        j = j + 1
    con.commit()
    event_for_set.set()

def getnum(num):
    if(num/ int(num) != 1):
        return int(num)+1
    else:
        return int(num)

if __name__ == '__main__':
    con = lite.connect(namedb)
    path = "E:\img.jpg"
    name = os.path.splitext(path)[0]
    im = Image.open(path)
    # pix = im.load()
    # i=1
    # #запишем изображение
    # cur = con.cursor()
    # uid = str(uuid.uuid4())
    # cur.execute('INSERT INTO picinfo (uid,name,sizex,sizey)  values(?,?,?,?)',(uid,name,im.size[0],im.size[1]))
    # con.commit()
    # listthread = []
    # eold = threading.Event()
    # firste = eold
    # while i <= im.size[1]:
    #     e = threading.Event()
    #     listthread.append(threading.Thread(target=readpic, args=(pix, uid, i, eold, e, im)))
    #     eold = e
    #     i = i + 1
    #
    # for thread in listthread:
    #     thread.start()
    # firste.set()
    #
    #
    # #запишем белый лист
    # i=1
    # listthreadwhite= []
    # eoldw = eold
    # while i <= im.size[1]:
    #     ew = threading.Event()
    #     listthreadwhite.append(threading.Thread(target=setwhite, args=(uid,i,eoldw,ew,im)))
    #     eoldw = ew
    #     i=i+1
    #
    # for threadwhite in listthreadwhite:
    #     threadwhite.start()

    app = QApplication(sys.argv)
    if(im.size[0]>600|im.size[1]>600):
        erx = im.size[0]-600
        ery = im.size[1]-600
        if(erx<ery):
            m = im.size[0]
        else:
            m = im.size[1]
        k = getnum(m / 600)
    else:
        k=1
    ex = painter(im.size[0]/k, im.size[1]/k)
    sys.exit(app.exec_())
