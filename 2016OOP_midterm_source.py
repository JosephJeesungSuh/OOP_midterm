from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
from random import *
from math import *
import time

wordsize = 17
wordarr = ["\start func","\end func","\start option","\end option","number",
           "dimension","size","init","fin","flip","breakthrough","saveway","row","column","own","True","False"]
bpix = 50
lpix = 2
mainfont = ("Times New Roman", 13)

class Writecode:
    def __init__(self):
        tk = Tk()
        self.tk = tk
        self.tk.title("new panel")
        self.isalive = False
        paper = CustomText(tk)
        paper.tag_config("orange", foreground = "#ffa500", font = ("Times new Roman", "14", "italic"))
        paper.tag_config("green", foreground = "#03a938")
        paper.tag_config("purple", foreground = "#8157ea")
        paper.tag_config("red", foreground = "#ff0000")
        self.paper = paper
        self.paper.insert(INSERT, "Write code here.")
        self.paper.bind_all("<Key>", self.highlight)
        paper.pack()
        self.button = Button(tk, text = "Make game", command = self.makegame)
        self.button.pack(side = RIGHT)
        
    def makegame(self):
        if self.isalive:
            self.gamewindow.quit()
        optionlist = self.getline()
        if len(optionlist) < 1 : return
        self.gamewindow = Game(optionlist)
        self.isalive = True
        
    def highlight(self, event):
        if event.keycode == 3342463 : self.paper.backspace()
        else : self.paper.highlight_pattern()
        
    def getline(self):
        ret = []
        input_ = self.paper.get("1.0",'end-1c')
        ar = input_.split('\n')
        col = len(ar)-1
        nl = 0
        sz = 0
        color = [""] * 50
        nxt = [0] * 50
        wrong = False
        while ar[nl].strip(" ") == "":
            nl += 1
            if nl > col:
                wrong = True
                self.errmg("Need more lines to complete.")
                break
        if not wrong and ar[nl].strip(" ") != "\start func" :
            self.errmg("Beginning must start with '\start func.'")
            wrong = True
        if not wrong :
            nl += 1
            if nl > col:
                wrong = True
                self.errmg("Need more lines to complete.")
        if not wrong :
            nowlist = ar[nl].split("=")
            if nowlist[0].strip(" ") != "number" or nowlist[1].strip(" ").isdigit() == False:
                self.errmg("number of state must be declared in the beginning.")
                wrong = True
            elif nowlist[1].strip(" ") == 0:
                self.errmg("There must be more than one state.")
                wrong = True
        if not wrong :
            sz = int(nowlist[1].strip(" "))
            for i in range(0,sz):
                    nl += 1
                    if nl > col:
                       wrong = True
                       break
                    nowlist = ar[nl].split(":")
                    if len(nowlist) < 2:
                       self.errmg("missing color statement(s)")
                       wrong = True
                    elif nowlist[0].strip(" ").isdigit() == False:
                        self.errmg("error occured in line {}.".format(str(nl+1)))
                        wrong = True
                        break
                    else:
                        color[int(nowlist[0].strip(" "))] = nowlist[1].strip(" ")
        if not wrong :
            nl += 1
            if nl > col:
                 wrong = True
                 self.errmg("Need more lines to complete.")
        if not wrong :
            nowlist = ar[nl].split(",")
            for i in range(0,len(nowlist)):
                if wrong :
                    break
                nowlist_ = nowlist[i].split("->")
                for j in range(0,len(nowlist_)):
                    nowlist_[j] = nowlist_[j].strip(" ")
                    if nowlist_[j].isdigit() == False:
                        self.errmg("error occured in line {}.".format(str(nl+1)))
                        wrong = True
                        break
                if not wrong :      
                    for j in range(0,len(nowlist_)-1):
                        if nxt[int(nowlist_[j])] != 0 :
                            wrong = True
                            self.errmg("error at state change function : next state must be declared uniquely.")
                        nxt[int(nowlist_[j])] = int(nowlist_[j+1])
        if not wrong :
            nl += 1
            if nl > col:
                wrong = True
                self.errmg("Need more lines to complete.")
        if not wrong :
            if ar[nl].strip(" ") != "\end func" :
                self.errmg("Missing '\end func' in the proper place.")
                wrong = True                        
        if not wrong :
            wrong = self.logic(sz, color, nxt)
            if wrong :
                self.errmg("Logical error : carefully check your function again. There must be missing state function or access to large index.")
        if not wrong :
            nl += 1
            if nl > col :
                wrong = True
                self.errmg("Need more lines to complete.")
        if not wrong :
            while ar[nl].strip("") == "":
                nl += 1
                if nl > col:
                    wrong = True
                    self.errmg("Need more lines to complete.")
        if not wrong and ar[nl].strip(" ") != "\start option" :
            wrong = True
            self.errmg("After function, '\start option' is missing.")
        if not wrong :
            while not wrong :
                nl += 1
                if nl > col :
                    wrong = True
                    self.errmg("Need more lines to complete.")
                nowlist = ar[nl]
                if nowlist.strip(" ") == "\end option" :
                    break
                else :
                    nowlist = ar[nl].split("=")
                    if len(nowlist) < 2: 
                        wrong = True
                        self.errmg("invalid option written in line {}.".format(nl+1))
                    else:
                        newoption = self.optiongetter(nowlist[0].strip(" "), nowlist[1].strip(" "))
                        if newoption[0] == "":
                            wrong = True
                            self.errmg("invalid option written in line {}.".format(nl+1))
                        else :
                            ret.append(newoption)
        if not wrong :
            wrong = self.optionlogic(ret, sz)
            if wrong == 1 :
                self.errmg("Too many declarations : Make sure each option is declared exactly once.")
            elif wrong == 2 :
                self.errmg("Lacking declarations : dimension, size, initial state, final state, flip must be declared.")
            elif wrong == 3 :
                self.errmg("Over index : Used index over size at initial of final state.")
            elif wrong == 4 :
                self.errmg("Dimension / size failure : Make sure the dimension, and size of initial / final state is correct.")
            elif wrong == 5 :
                self.errmg("If dimension is 1, you can't use column flip.")
            else :
                pansize = 0
                for i in ret :
                    if i[0] == "size" :
                        if len(i) > 2 : pansize = i[1] * i[2]
                        else : pansize = i[1]
                if pansize > 40 :
                    self.errmg("Too Large Gamesize : maximum is 40.")
                else :
                    for i in range(len(ret)) :
                        if (ret[i][0] == "fin" or ret[i][0] == "init") and ret[i][1] == "random" :
                            ret[i].remove("random")
                            appending = []
                            for j in range(pansize) :
                                appending.append(randint(1,sz))
                            ret[i].append(appending)
                    ret.append(["number",sz])
                    ret.append(["color",color])
                    ret.append(["nxt",nxt])
                    return ret
        return []
            
    def logic(self, number, color, nxt):
        for i in range(1,number+1):
            if color[i] == "" : return True
        for i in range(1,number+1):
            if nxt[i] == 0 or nxt[i] > number : return True
        return False

    def optiongetter(self, name, value):
        if name == "dimension" :
            if len(value) > 2 or len(value) < 1 or not value[0].isdigit() or int(value[0]) > 2 or int(value[0]) < 0 : return ["",""]
            if len(value) > 1 and value[1].isdigit() : return ["",""]
            return ["dimension", int(value[0])]
        elif name == "size" :
            seperate = value.strip(" ").split("*")
            if len(seperate) < 1 or len(seperate) > 2 or len(seperate[0]) == 0 : return ["",""]
            if len(seperate) == 1 :
                if value.strip(" ").isdigit() == False : return ["",""]
                return ["size", int(value.strip(" "))]
            else :
                if seperate[0].strip(" ").isdigit() == False or seperate[1].strip(" ").isdigit() == False :
                    return ["",""]
                return ["size", int(seperate[0].strip(" ")), int(seperate[1].strip(" "))]
        elif name == "init" or name == "fin":
            ret = []
            seperate = value.strip("'").split(",")
            if seperate[0] == "random" :
                return [["init","fin"][name=="fin"],"random"]
            for i in range(0, len(seperate)) :
                now = seperate[i].strip(" ").strip("[").strip("]")
                if now.isdigit() == False :
                    return ["",""]
                else :
                    ret.append(int(now))
            return [["init","fin"][name=="fin"],ret]
        elif name == "flip" :
            ret = [0] * 5                               # 0 - row, 1 - column, 2 - own
            seperate = value.split("+")
            for i in range(0, len(seperate)) :
                now = seperate[i].strip(" ")
                if now[:3] != "row" and now[:3] != "own" and now[:6] != "column" :
                    return ["",""]
                else :
                    if now[:3] == "row" :
                        if ret[0] or ret[1] or len(now) < 8 or now[3] != "(" or now[5] != "," or now[7] != ")" : return ["",""]
                        try :
                            ret[0] = int(now[4])
                            ret[1] = int(now[6])
                        except :
                            return ["",""]
                    elif now[:3] == "own" :
                        if ret[4] : return ["",""]
                        ret[4] = 1
                    else :
                        if ret[2] or ret[3] or len(now) < 11 or now[6] != "(" or now[8] != "," or now[10] != ")" : return ["",""]
                        try :
                            ret[2] = int(now[7])
                            ret[3] = int(now[9])
                        except :
                            return ["",""]
            return ["flip",ret]
        elif name == "breakthrough" or name == "saveway":
            now = value.strip(" ")
            if now != "False" and now != "True" :
                return ["",""]
            return [["breakthrough","saveway"][name=="saveway"],[True,False][now=="False"]]
        return ["",""]

    def optionlogic(self, ret, sz): # each retnum indicates : 0 - good
                                    # 1 - multi declare of option, 2 - lack declare, 3 - over index, 4 - dimension or size fault, 4 - column
       dimension = 0
       size = []
       init = None
       fin = None
       flip = None
       checker = [False] * 10
       for i in range(0, len(ret)) :
           now = ret[i][0]
           for j in range(5,10) :
               if now == wordarr[j] :
                    if checker[j-5] == False :
                        checker[j-5] = True
                        if j == 5 : dimension = ret[i][1]
                        elif j == 6 :
                            size.append(ret[i][1])
                            if len(ret[i]) == 3 : size.append(ret[i][2])
                        else:
                            if j == 7 : init = ret[i][1]
                            elif j == 8 : fin = ret[i][1]
                            else : flip = ret[i][1]
                    else :
                        return 1
       summa = 0
       for j in range(0,5) :
           summa += int(checker[j])
       if summa < 5 : return 2
       if fin != "random" :
           for i in fin :
               if i > sz : return 3
       if init != "random" :
           for i in init :
               if i > sz : return 3
       if dimension == 1 :
           if len(size) > 1 : return 4
           if init != "random" and size[0] != len(init) :
               return 4
           if fin != "random" and size[0] != len(fin) :
               return 4
           if flip[2] or flip[3] : return 5
       else :
           if len(size) < 2 : return 4
           if init != "random" and size[0]*size[1] != len(init) :
               return 4
           if fin != "random" and  size[0]*size[1] != len(fin) :
               return 4
       return 0
    
    def errmg(self, string):
       messagebox.showerror("Failure",string)

class Game:
    frame = 0
    def __init__(self,optionlist):
        if self.pseudo_initialize() : return
        self.define(optionlist)
        C = self.checker()
        if C == 0 :
            self.errmg("Warning", "Impossible to make final state.")
        elif C == 1 :
            self.errmg("Warning", "The program cananot decide if there is a solution. It may be one of two cases:\n"
                       +" 1.The state has more than one cycle.\n 2. The state has a single cycle but the period isn't prime number.")
        else :
            self.C = C
            print(C)
    
        self.cwidth = 50 * self.size[1] + 50
        self.cheight = 50 * self.size[0] + 50
        self.block = [[0] * self.size[1] for i in range(self.size[0])]
        for i in range(self.size[0]) :
            for j in range(self.size[1]) :
                self.block[i][j] = self.init[i*self.size[1] + j]
        self.tk = Tk()
        self.tk.title("Finite Linear Game")

        self.canvas = Canvas(self.tk, width = int(self.cwidth*1.6), height = self.cheight, bg = "white")
        self.canvas.pack()
        self.tk.bind("<Key>",self.keymove)
        self.canvas.bind("<Button-1>",self.onclick)
        secondx = int(self.cwidth*1.1)
        secondy = self.cheight/3
        for i in range(self.size[1]+1) :
            self.canvas.create_line(bpix/2+bpix*i, bpix/2, bpix/2+bpix*i, self.cheight-bpix/2, width = lpix)
            self.canvas.create_line(secondx+bpix/4+bpix*i/2, secondy+bpix/4, secondx+bpix/4+bpix*i/2, self.cheight*5/6-bpix/4, width = lpix/2) 
        for i in range(self.size[0]+1) :
            self.canvas.create_line(bpix/2, bpix/2+bpix*i, self.cwidth-bpix/2, bpix/2+bpix*i, width = lpix)
            self.canvas.create_line(secondx+bpix/4, secondy+bpix/4+bpix*i/2, int(self.cwidth*1.6)-bpix/4, secondy+bpix/4+bpix*i/2, width = lpix/2)
        for i in range(self.size[0]) :
            for j in range(self.size[1]) :
                self.canvas.create_rectangle(secondx+bpix/4+bpix*j/2, secondy+bpix/4+bpix*i/2, secondx+bpix/4+bpix*(j+1)/2-lpix/4, secondy+bpix/4+bpix*(i+1)/2-lpix/4, fill = self.color[self.fin[i*self.size[1]+j]])
        self.canvas.create_text(int(self.cwidth*1.35), self.cheight/3, text = "final state", font = mainfont)
        self.entry = Entry(self.tk)
        self.entry.config(justify=CENTER)
        self.entry.pack()
        self.pointx = self.pointy = 0
        self.button = Button(self.tk, text = 'quit', command = self.quit)
        self.button.pack(side = LEFT)
        self.resetbtn = Button(self.tk, text = 'reset', command = self.reset)
        self.resetbtn.pack(side = RIGHT)
        self.breakbtn = Button(self.tk, text = 'breakthrough', command = self.breakthrough_)
        self.breakbtn.pack(side = BOTTOM)
        self.start_time = time.time()
        self.update()
        self.update_line()
        
    def quit(self):
        try:
            self.tk.destroy()
        except:
           pass

    def errmg(self, str1, str2) :
        messagebox.showerror(str1,str2)

    def pseudo_initialize(self) :
        tk = Tk()
        center(tk)
        tk.protocol("WM_DELETE_WINDOW", lambda param=tk : on_closing(param))
        tk.title("Initializing...")
        canvas = Canvas(tk,width=200,height=200)
        canvas.pack()
        for i in range(4) :
            for j in range(1,12) :
                try :
                    frame = PhotoImage(master = canvas, file = "loading.gif", format = "gif - {}".format(j))
                    canvas.create_image(100,100,anchor=CENTER, image = frame)
                    tk.update()
                    time.sleep(0.1)
                except :
                    break
        try :
            tk.destroy()
        except :
            return True
        return False

    def define(self, optionlist) :
        self.breakthrough = False
        self.saveway = False
        for i in optionlist :
            if i[0] == 'dimension' :
                self.dimension = i[1]
            elif i[0] == 'size' :
                if len(i) > 2 :
                    self.size = [i[1],i[2]]
                else : self.size = [1,i[1]]
            elif i[0] == 'init' or i[0] == 'fin' :
                if i[0] == 'init' : self.init = i[1]
                else : self.fin = i[1]
            elif i[0] == 'flip' :
                self.flip = i[1]
            elif i[0] == 'breakthrough' :
                self.breakthrough = i[1]
            elif i[0] == 'saveway' :
                self.saveway = i[1]
            elif i[0] == 'number' :
                self.number = i[1]
            elif i[0] == 'color' :
                self.color = i[1]
            elif i[0] == 'nxt' :
                self.nxt = i[1]
        pass
    def update(self) :
        end = True
        for i in range(self.size[0]) :
            for j in range(self.size[1]) :
                self.canvas.create_rectangle(bpix/2+bpix*j, bpix/2+bpix*i, bpix/2+bpix*j+bpix-lpix/2, bpix/2+bpix*i+bpix-lpix/2, fill=self.color[self.block[i][j]])
                if self.color[self.block[i][j]] != "black" :
                    self.canvas.create_text(bpix*(j+1), bpix*(i+1), text = str(self.block[i][j]), font = mainfont)
                else :
                    self.canvas.create_text(bpix*(j+1), bpix*(i+1), text = str(self.block[i][j]), font = mainfont, fill = "#ffffff")
                if self.color[self.block[i][j]] != self.color[self.fin[i*self.size[1]+j]] : end = False
        if self.color[self.block[self.pointy][self.pointx]] != "black" :
            self.line_id = [self.canvas.create_line(bpix/2+bpix*self.pointx+3, bpix/2+bpix*self.pointy+3, bpix/2+bpix*(self.pointx+1)-3, bpix/2+bpix*self.pointy+3, dash=(4,1), dashoff=self.frame),
                            self.canvas.create_line(bpix/2+bpix*self.pointx+3, bpix/2+bpix*self.pointy+3, bpix/2+bpix*self.pointx+3, bpix/2+bpix*(self.pointy+1)-3, dash=(4,1), dashoff=self.frame),
                            self.canvas.create_line(bpix/2+bpix*(self.pointx+1)-3, bpix/2+bpix*self.pointy+3, bpix/2+bpix*(self.pointx+1)-3, bpix/2+bpix*(self.pointy+1)-3, dash=(4,1), dashoff=self.frame),
                            self.canvas.create_line(bpix/2+bpix*self.pointx+3, bpix/2+bpix*(self.pointy+1)-3, bpix/2+bpix*(self.pointx+1)-3, bpix/2+bpix*(self.pointy+1)-3, dash=(4,1), dashoff=self.frame)]
        else :
            self.line_id = [self.canvas.create_line(bpix/2+bpix*self.pointx+3, bpix/2+bpix*self.pointy+3, bpix/2+bpix*(self.pointx+1)-3, bpix/2+bpix*self.pointy+3, dash=(4,1), dashoff=self.frame, fill = "white"),
                            self.canvas.create_line(bpix/2+bpix*self.pointx+3, bpix/2+bpix*self.pointy+3, bpix/2+bpix*self.pointx+3, bpix/2+bpix*(self.pointy+1)-3, dash=(4,1), dashoff=self.frame, fill = "white"),
                            self.canvas.create_line(bpix/2+bpix*(self.pointx+1)-3, bpix/2+bpix*self.pointy+3, bpix/2+bpix*(self.pointx+1)-3, bpix/2+bpix*(self.pointy+1)-3, dash=(4,1), dashoff=self.frame, fill = "white"),
                            self.canvas.create_line(bpix/2+bpix*self.pointx+3, bpix/2+bpix*(self.pointy+1)-3, bpix/2+bpix*(self.pointx+1)-3, bpix/2+bpix*(self.pointy+1)-3, dash=(4,1), dashoff=self.frame, fill= "white")]
        self.tk.update()
        if end == True :
            messagebox.showerror("Wow!", "Finished!\nTime spent : %s seconds" % round(time.time() - self.start_time))

    def reset(self) :
        self.start_time = time.time()
        for i in range(self.size[0]) :
            for j in range(self.size[1]) :
                self.block[i][j] = self.init[i*self.size[1]+j]
        self.pointx = self.pointy = 0
        self.update()
    
    def update_line(self):
        self.frame+=1
        if self.color[self.block[self.pointy][self.pointx]] == "black" :
            for i in self.line_id :
                self.canvas.itemconfigure(i, dashoff = self.frame, fill = "white")
        else :
            for i in self.line_id :
                self.canvas.itemconfigure(i, dashoff=self.frame)
        currenttime = round(time.time() - self.start_time)
        self.entry.configure(state='normal')
        self.entry.delete(0,END)
        self.entry.insert(0, "Time = {} : {}".format(currenttime//60, currenttime%60))
        self.entry.configure(state='disabled')
        self.tk.after(150,self.update_line)

    def onclick(self, event) :
        x = int((event.x - bpix/2) // bpix)
        y = int((event.y - bpix/2) // bpix)
        self.fliping(x,y)
        self.update()
        
    def keymove(self, event) :
        if event.keysym != "Up" and event.keysym != "Down" and event.keysym != "Left" and event.keysym != "Right" and event.keysym != "Return" : return
        if event.keysym == "Return" :
            self.fliping(self.pointx, self.pointy)
            self.update()
            return
        orix = self.pointx
        oriy = self.pointy
        if event.keysym == "Up" :
            self.pointy -= 1
            self.pointy = max(0, self.pointy)
        elif event.keysym == "Down" :
            self.pointy += 1
            self.pointy = min(self.size[0]-1, self.pointy)
        elif event.keysym == "Left" :
            self.pointx -= 1
            self.pointx = max(0, self.pointx)
        elif event.keysym == "Right" :
            self.pointx += 1
            self.pointx = min(self.size[1]-1, self.pointx)
        self.canvas.create_rectangle(bpix/2+bpix*orix, bpix/2+bpix*oriy, bpix/2+bpix*orix+bpix-lpix/2, bpix/2+bpix*oriy+bpix-lpix/2, fill=self.color[self.block[oriy][orix]])
        self.canvas.create_rectangle(bpix/2+bpix*self.pointx, bpix/2+bpix*self.pointy, bpix/2+bpix*self.pointx+bpix-lpix/2, bpix/2+bpix*self.pointy+bpix-lpix/2, fill=self.color[self.block[self.pointy][self.pointx]])
        self.canvas.create_text(bpix*(orix+1), bpix*(oriy+1), text = str(self.block[oriy][orix]), font = mainfont, fill = ["black","white"][self.color[self.block[oriy][orix]]=="black"])
        self.canvas.create_text(bpix*(self.pointx+1), bpix*(self.pointy+1), text = str(self.block[self.pointy][self.pointx]), font = mainfont, fill = ["black","white"][self.color[self.block[self.pointy][self.pointx]]=="black"])
        if self.color[self.block[self.pointy][self.pointx]] == "black" :
            self.line_id = [self.canvas.create_line(bpix/2+bpix*self.pointx+3, bpix/2+bpix*self.pointy+3, bpix/2+bpix*(self.pointx+1)-3, bpix/2+bpix*self.pointy+3, dash=(4,1), dashoff=self.frame, fill = "white"),
                            self.canvas.create_line(bpix/2+bpix*self.pointx+3, bpix/2+bpix*self.pointy+3, bpix/2+bpix*self.pointx+3, bpix/2+bpix*(self.pointy+1)-3, dash=(4,1), dashoff=self.frame, fill = "white"),
                            self.canvas.create_line(bpix/2+bpix*(self.pointx+1)-3, bpix/2+bpix*self.pointy+3, bpix/2+bpix*(self.pointx+1)-3, bpix/2+bpix*(self.pointy+1)-3, dash=(4,1), dashoff=self.frame, fill = "white"),
                            self.canvas.create_line(bpix/2+bpix*self.pointx+3, bpix/2+bpix*(self.pointy+1)-3, bpix/2+bpix*(self.pointx+1)-3, bpix/2+bpix*(self.pointy+1)-3, dash=(4,1), dashoff=self.frame, fill= "white")]
        else :
            self.line_id = [self.canvas.create_line(bpix/2+bpix*self.pointx+3, bpix/2+bpix*self.pointy+3, bpix/2+bpix*(self.pointx+1)-3, bpix/2+bpix*self.pointy+3, dash=(4,1), dashoff=self.frame),
                            self.canvas.create_line(bpix/2+bpix*self.pointx+3, bpix/2+bpix*self.pointy+3, bpix/2+bpix*self.pointx+3, bpix/2+bpix*(self.pointy+1)-3, dash=(4,1), dashoff=self.frame),
                            self.canvas.create_line(bpix/2+bpix*(self.pointx+1)-3, bpix/2+bpix*self.pointy+3, bpix/2+bpix*(self.pointx+1)-3, bpix/2+bpix*(self.pointy+1)-3, dash=(4,1), dashoff=self.frame),
                            self.canvas.create_line(bpix/2+bpix*self.pointx+3, bpix/2+bpix*(self.pointy+1)-3, bpix/2+bpix*(self.pointx+1)-3, bpix/2+bpix*(self.pointy+1)-3, dash=(4,1), dashoff=self.frame)]            
        self.tk.update()
        return

    def fliping(self,x,y) :
        if x<0 or x>=self.size[1] or y<0 or y>=self.size[0] :
            return
        self.pointx = x
        self.pointy = y
        if self.flip[4] :
            self.block[y][x] = self.nxt[self.block[y][x]]
        for i in range(max(0,x-self.flip[0]), x) :
            self.block[y][i] = self.nxt[self.block[y][i]]
        for i in range(x+1, min(self.size[1], x+self.flip[1]+1)) :
            self.block[y][i] = self.nxt[self.block[y][i]]
        for i in range(max(0,y-self.flip[2]), y) :
            self.block[i][x] = self.nxt[self.block[i][x]]
        for i in range(y+1, min(self.size[0], y+self.flip[3]+1)) :
            self.block[i][x] = self.nxt[self.block[i][x]]
        
    def checker(self) :
        ind = [0] * 50
        visit = [False] * 50
        paint = [0] * 50
        color = 0
        cyclecnt = 0
        for i in range(1,self.number+1) :
            if not visit[i] :
                color += 1
                now = i
                while True :
                    now = self.nxt[now]
                    if visit[now] :
                        if paint[now] == color : cyclecnt += 1
                        break
                    visit[now] = True
                    paint[now] = color
        if cyclecnt > 1 : return 1
        cyclecnt = 100
        for i in range(1,self.number+1) :
            visit_ = [False]*50
            cycnt = 0
            now = i
            while not visit_[now] :
                visit_[now] = True
                cycnt += 1
                now = self.nxt[now]
            cyclecnt = min(cyclecnt, cycnt)
        self.cyclecnt = cyclecnt
        if isprime(cyclecnt) == False : return 1
        A = self.construct_matrix()
        b = self.construct_constant()
        x = gj_Solve(A,b,cyclecnt)
        if not b or x == False: return 0
        return x

    def breakthrough_(self) :
        try :
            self.C
            solution = [0] * (self.size[0]*self.size[1])
            for i in range(self.size[0]*self.size[1]-1,-1,-1) :
                temp = self.C[i]
                pivot = -1
                for j in range(len(temp)) :
                    if temp[j] != 0.0 :
                        pivot = j
                        break
                if pivot > -1 :
                    if pivot == self.size[0]*self.size[1] :
                        self.C = None
                        break
                    solution[pivot] = temp[len(temp)-1]
                    for j in range(pivot+1,len(temp)-1) :
                        solution[pivot] -= temp[j] * solution[j]
                    solution[pivot] /= temp[pivot]
            string = ""
            for i in range(self.size[0]*self.size[1]) :
                string += "Press {},{}    :   {} times.\n".format(i//self.size[1], int(i%self.size[1]), int(solution[i]))
            string += "If above way does not give a solution, press some places {} times.".format(self.cyclecnt)
            messagebox.showinfo("Breakthrough", string)
        except:
            self.C = None
        if self.C == None :
            self.errmg("Impossible", "The program can't find the solution.")
        return
    
    def construct_matrix(self) :
        ret = []
        for i in range(self.size[0] * self.size[1]) :
            appending = []
            (nowx, nowy) = (i % self.size[1], i // self.size[1])
            for j in range(self.size[0] * self.size[1]) :
                (dx, dy) = (j % self.size[1], j // self.size[1])
                if nowx != dx and nowy != dy : appending.append(0)
                else : 
                    if nowx == dx and nowy == dy :
                        if self.flip[4] : appending.append(1)
                        else : appending.append(0)
                    elif nowy == dy :
                        dis = dx - nowx
                        if self.flip[1] >= dis and dis >= -self.flip[0] : appending.append(1)
                        else : appending.append(0)
                    else :
                        dis = dy - nowy
                        if self.flip[3] >= dis and dis >= -self.flip[2] : appending.append(1)
                        else : appending.append(0)
            ret.append(appending)
        return ret

    def construct_constant(self) :
        ret = []
        for i in range(self.size[0] * self.size[1]) :
            now = self.init[i]
            cnt = 0
            while now != self.fin[i] :
                cnt += 1
                now = self.nxt[now]
                if cnt > 100 :
                    return False
            ret.append(cnt)
        return ret

class CustomText(Text):
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)
    def highlight_pattern(self):
        for i in range(0,wordsize):
            pattern = wordarr[i]
            pos = '1.0'
            if i<4 : tag = "orange"
            elif i<12 : tag = "green"
            elif i<15 : tag = "purple"
            else : tag = "red"
            while True:
                idx = self.search(pattern, pos, END)
                if not idx: break
                pos = '{}+{}c'.format(idx, len(pattern))
                self.tag_add(tag, idx, pos)
    def backspace(self):
        pos = '1.0'
        self.tag_delete("orange")
        self.tag_delete("green")
        self.tag_delete("purple")
        self.tag_delete("red")
        self.tag_config("orange", foreground = "#ffa500", font = ("Times new Roman", "14", "italic"))
        self.tag_config("green", foreground = "#03a938")
        self.tag_config("purple", foreground = "#8157ea")
        self.tag_config("red", foreground = "#ff0000")
        self.highlight_pattern()
    def linecnt(self):
        return int(self.index('end-1c').split('.')[0])

def on_closing(tk) :
    if messagebox.askokcancel("Quit", "Do you really want to quit?") :
        tk.destroy()

def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()



    
def idMatx(size):            # identity matrix
  id = []
  for i in range(size):
    id.append([0]*size)
  for i in range(size):
    id[i][i] = 1
  return(id)
 
def tranMtx(inMtx):          # transpose matrix
  tMtx = []
  for row in range(0, len(inMtx[0])):
    tRow = []
    for col in range(0, len(inMtx)):
      ele = inMtx[col][row]
      tRow.append(ele)
    tMtx.append(tRow)
  return(tMtx)
 
# the solver ...

def isprime(X) :
    limit = int(sqrt(X))
    for i in range(2,limit+1) :
        if X % i == 0 : return False
    return True
 
def gj_Solve(A, b, prime):
  """ A gauss-jordan method to solve an augmented matrix for
      the unknown variables, x, in Ax = b.
      The degree of rounding is 'tuned' by altering decPts = 4.
      In the case where b is not supplied, b = ID matrix, and therefore
      the output is the inverse of the A matrix.
  """
  if not b == False:
    # first, a test to make sure that A and b are conformable
    if (len(A) != len(b)):
      print('A and b are not conformable')
      return False
    Ab = A[:]
    Ab.append(b)
    m = tranMtx(Ab)
  else:
    ii = idMatx(len(A))
    Aa = A[:]
    for col in range(len(ii)):
      Aa.append(ii[col])
    tAa = tranMtx(Aa)
    m = tAa[:]
  (eqns, colrange, augCol) = (len(A), len(A), len(m[0]))
  # permute the matrix -- get the largest leaders onto the diagonals
  # take the first row, assume that x[1,1] is largest, and swap if that's not true
  for rrcol in range(0, colrange):
    bigrow = rrcol
    if m[bigrow][rrcol] == 0 :
        for row in range(rrcol+1, colrange) :
            if abs(m[row][rrcol]) > abs(m[bigrow][rrcol]) :
                bigrow = row
                (m[rrcol], m[bigrow]) = (m[bigrow], m[rrcol])
                break
    for rr in range(rrcol+1, eqns):
      cc = 0
      for i in range(0,prime):
          if i * m[rrcol][rrcol] % prime == m[rr][rrcol] :
              cc = i
              break
      for j in range(augCol):
        m[rr][j] = (m[rr][j] - cc*m[rrcol][j]) % prime
  # final reduction -- the first test catches under-determined systems
  # these are characterised by some equations being all zero
  for rb in reversed(range(eqns)):
    if ( m[rb][rb] == 0):
      if m[rb][augCol-1] == 0:
        continue
      else:
        return False
    else:
      # you must loop back across to catch under-determined systems
      cc = 0
      for i in range(1,prime) :
         if i * m[rb][rb] % prime == 1 :
             cc = i
             break
      for backCol in reversed(range(rb, augCol)):
        m[rb][backCol] = m[rb][backCol] * cc % prime
      # knock-up (cancel the above to eliminate the knowns)
      # again, we must loop to catch under-determined systems
      if not (rb == 0):
        for kup in reversed(range(rb)):
          kk = 0
          for i in range(1,prime) :
              if i * m[rb][rb] % prime == m[kup][rb] :
                  kk = i
                  break
          for kleft in reversed(range(rb, augCol)):
            m[kup][kleft] = (m[kup][kleft] - kk * float(m[rb][kleft])) % prime
  if not b == False:
    return m
  else:
    mOut = []
    for row in range(len(m)):
      rOut = []
      for col in range(augCol//2, augCol):
        rOut.append(m[row][col])
      mOut.append(rOut)
    return mOut


def main() :
    writecode = Writecode()

if __name__ == '__main__' :
    main()

