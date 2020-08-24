#################################################################
#author: xiaomililkx
#################################################################
from tkinter import *
import base64
import re
import os

LOG_LINE_NUM = 0

class MY_GUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name

    #设置窗口
    def set_init_window(self):
        self.init_window_name.title("Searcher   by: xiaomilifather")           #窗口名
        self.init_window_name.geometry('1024x768')
        #self.init_window_name["bg"] = "pink"                                    #窗口背景色
        #self.init_window_name.attributes("-alpha",0.9)                          #虚化，值越小虚化程度越高
        #标签
        self.lbl=LabelFrame(self.init_window_name, width=452, height=710, text='Ctrl+V 输入说明书')
        self.lbl.grid(row=0,column=0,columnspan=8 ,rowspan=8, padx=15)

        self.lbr=LabelFrame(self.init_window_name, width=452, height=710, text='结果输出')
        self.lbr.grid(row=0, column=10,columnspan=8 ,rowspan=8)

        self.buttonframe= Frame(self.init_window_name, width=70, height=710)
        self.buttonframe.grid(row=0, column=9)

        #文本框        
        #self.init_data_Text = Text(self.init_window_name, width=70, height=50, undo = True)  #原始数据录入框
        self.init_data_Text = Text(self.lbl,  undo = True)  #原始数据录入框
        self.init_data_Text.place(x=0,y=0,width=430,height=680)

        #列表框
        self.result_data_Listbox = Listbox(self.lbr)  #处理结果展示
        self.result_data_Listbox.place(x=0,y=0,width=430,height=660)

        #纵向滚动条
        self.L_scroll=Scrollbar(self.lbl , orient=VERTICAL)
        self.L_scroll.place(x=430,y = 0,height=680)
        self.L_scroll.config(command=self.init_data_Text.yview)
        self.init_data_Text.config(yscrollcommand=self.L_scroll.set)
        self.R_scroll=Scrollbar(self.lbr , orient=VERTICAL)
        self.R_scroll.place(x=430, height=660)#指定 上下展开
        self.R_scroll.config(command=self.result_data_Listbox.yview)
        self.result_data_Listbox.config(yscrollcommand=self.R_scroll.set)
        #横向滚动轴
        self.Rd_scroll=Scrollbar(self.lbr ,orient=HORIZONTAL)
        self.Rd_scroll.place(y = 660, width = 430)#指定 左右展开
        self.Rd_scroll.config(command=self.result_data_Listbox.xview)
        #键盘事件
        self.init_data_Text.bind("<KeyRelease>", lambda event: self.sms_find())
        #self.init_data_Text.bind('<Control-Key-V>',self.sms_find())  KeyRelease  <Control-KeyPress-V>
        #按钮
        #self.smsfind_button = Button(self.init_window_name, text="提交", bg="lightblue", command=self.sms_find)  # 调用内部方法  加()为直接调用
        #self.smsfind_button.grid(row=0, column=9)
  
    #功能函数
    def sms_find(self):
        #初始化text（去空格）和Listbox（清空）
        ls = ['本申请信息如下：']
        flag = [] #存在的错误
        self.result_data_Listbox.delete(0, END)#清空listbox
        src = self.init_data_Text.get(1.0,END)
        #print('111:'+str(len(src))+'111'+src+'222')
        if(re.search('\S',src) == None):
            return

        
        lspic, a = self.sms_pic(src) #附图查找
        etitle = self.sms_titles(src)#标题查找
        wh = self.sms_wh(src)#查找是否有？
        error1 = self.sms_error1(src)#查找是否有“引用源错误”
        title, pa  = self.sms_info(src)
        if(a + etitle + wh + error1 + pa):
            flag = [r'==================分割线==================']
            stp = '说明书存在以下' +str(len(a + etitle + wh + error1 + pa)) + '个问题：'
            flag.append(stp)
            flag   = flag + a + etitle + wh + error1 + pa
            for i in range(len(flag)-2):
                flag[i+2] = str(i+1) + '、' + flag[i+2]
        else:
            flag = [r'==================分割线==================' ,'说明书正常']
        
        
        ls = ls + title + lspic + flag #所有结果列表汇总
        self.ptlist(ls)#输出


    #查找说明书格式标记\n",
    def sms_titles(self,src):
        lstitle = []
        pttitle = []
        count = 0

        rel = re.findall(r'技 ?术 ?领 ?域 ?\s?\n', src)
        count = len(rel)
        if(count == 0):
            lstitle.append(r'没有“技术领域”')
        elif(count > 1):
            lstitle.append('出现'+str(len(re.findall(r'技术领域\s?\n', src)) > 1) +'次“技术领域”')
            pttitle = pttitle + rel
        else:
            pttitle = pttitle + rel

        rel = re.findall(r'背 ?景 ?技 ?术 ?\s?\n', src)
        count = len(rel)
        if(count == 0):
            lstitle.append(r'没有“背景技术”')
        elif(count > 1):
            lstitle.append(r'出现'+str(len(re.findall(r'背景技术\s?\n', src))) +'次“背景技术”')
            pttitle = pttitle + rel
        else:
            pttitle = pttitle + rel

        rel = re.findall(r'发 ?明 ?内 ?容 ?\s?\n', src)
        count = len(rel)
        if(count == 0):
            lstitle.append(r'没有“发明内容”')
        elif(count > 1):
            lstitle.append(r'出现'+str(len(re.findall(r'发明内容\s?\n', src))) +'次“发明内容”')
            pttitle = pttitle + rel
        else:
            pttitle = pttitle + rel

        rel = re.findall(r'附 ?图 ?说 ?明 ?\s?\n', src)
        count = len(rel)
        if(count == 0):
            lstitle.append(r'没有“附图说明”')
        elif(count > 1):
            lstitle.append(r'出现'+str(len(re.findall(r'附图说明\s?\n', src))) +'次“附图说明”')
            pttitle = pttitle + rel
        else:
            pttitle = pttitle + rel

        rel = re.findall(r'具 ?体 ?实 ?施 ?方 ?式 ?\s?\n', src)
        count = len(rel)
        if(count == 0):
            lstitle.append(r'没有“具体实施方式”')
        elif(count > 1):
            lstitle.append(r'出现'+str(len(re.findall(r'具体实施方式\s?\n', src))) +'次“具体实施方式”')
            pttitle = pttitle + rel
        else:
            pttitle = pttitle + rel
            
        self.sms_highlight(pttitle, 'title')#高亮
        return lstitle

    
    #图片标号查找                
    def sms_pic(self,scrp):
        rs = []#结果
        lspic = []
        nums = []
        flag = []
        sel = r'图 ?\d ?\d? ?\d? ?[a-zA-Z]? ?-?\d*[a-zA-Z]?' #可匹配  图 1 1 A -图14A
        #p = re.compile(sel, re.X)
        lspic = re.findall(sel, scrp) #正则匹配 “图+数字+字母”
        lspic = set(lspic) #去重
        lspic = sorted(lspic) #排序
        self.sms_highlight(lspic, 'pic')#高亮 带空格附图号
        lspic = re.findall(sel, ''.join(lspic).replace(' ',''))#输出不带空格附图号
        lspic = set(lspic) #去重
        lspic = sorted(lspic) #排序
        lspic.sort(key = lambda x:int(re.match('图 ?(\d ?\d? ?\d?) ?[a-zA-Z]?',x).group(1)))#排序
        if(lspic):
            rs.append('附图如下：')
            rs = rs + lspic
        else:
            rs.append('说明书不包含附图！')      

        #查找是否缺少附图标号
        if(len(lspic) > 1):
            num = int(re.search('\d+', lspic[len(lspic)-1]).group().replace(' ', ''))#获得最大值
            nums = set(re.findall(r'\d+', ''.join(lspic).replace(' ',''))) #拼接成字符串
            if(len(nums) != num):
                flag.append('附图图号不连续，请核对')
                
        #查找附图标号有字母且有数字
        sel = r'(图\d+)[a-zA-Z]'
        nums = set(re.findall(sel, ''.join(lspic).replace(' ',''))) #拼接成字符串
        #a = [x for x in list1 if x in list2] #两个列表中都存在
        #b = [y for y in (list1 + list2) if y not in a] #两个列表中的不同元素
        picnumerror = [x for x in nums if x in lspic]
        if(picnumerror): #两个列表中都存在
            st = '可能存在错误的图号：' +  ', '.join(sorted(picnumerror))
            flag.append(st)

        return rs, flag
    
    #查找是否有？并高亮
    def sms_wh(self,scrp):
        wh = []
        if(scrp.count('?' or '？') > 0):
            tp = '具有' + str(scrp.count('?')+scrp.count('？'))  + '个问号'
            wh.append(tp)
        self.sms_highlight(['?','？'],'wh')
        return wh
        
    #查找是否有“未找到引用源”并高亮
    def sms_error1(self,scrp):
        error1 = []
        if(scrp.count('未找到引用源') > 0):
            tp = '具有' + str(scrp.count('未找到引用源')) + r'个“未找到引用源”'
            error1.append(tp)
        self.sms_highlight(['未找到引用源'],'error1')
        return error1

    #发明名称，段落数
    def sms_info(self,scrp):
        title = ''
        info = []
        flag =[]
        text_content = (scrp.replace(" ","")).split("\n")
        text_content.pop()#列表最后一个元素是空删除它
        #text_content = re.findall(r'*\n',scrp)
        #print(text_content)
        for s in text_content:
            if (re.search('\S',s) != None):
                title = '发明名称：' + s
                break
        pa = ''
        tp = re.findall('\\[\d\d\d\d\\]', scrp)#[00xx]标记的数量
        #print('000' + str(scrp.count(r'\n')))
        if(scrp.count('\n') < len(tp)):
            pa = '总计段落：'+ str(scrp.count('\n'))
            flag = ['段落数出现异常！']
        elif(len(tp) == 0):
            pa = '总计段落：'+ str(scrp.count('\n'))
            flag = ['段落数标记出现异常！']
        #elif(int(re.search(r'\d+',tp[len(tp)-1])) > len(tp)):
        #    flag = ['段落数出现异常']
        else:
            pa = '总计段落：'+ str(len(tp)) 
        
        lengh = '字数统计：' + str(len(''.join(re.findall('\S',scrp))))
        info.append(title)
        info.append(pa)
        info.append(lengh)
        return info, flag
        
    #高亮
    def sms_highlight(self, lspic,tagh):
        self.init_data_Text.tag_config('pic', background='yellow') #配置字体  图号
        self.init_data_Text.tag_config('title', background='green') #配置字体  标题
        self.init_data_Text.tag_config('wh', background='red') #配置字体  出现问号
        self.init_data_Text.tag_config('error1', background='red') #配置字体 未找到引用源
        if (tagh == 'pic'):
            for i in range(len(lspic)):#循环显示图号高亮
                self.searchtag(self.init_data_Text, lspic[i], 'pic')
        elif(tagh == 'title'):
            for i in range(len(lspic)):#循环标题高亮
                self.searchtag(self.init_data_Text, lspic[i], 'title')
        elif(tagh == 'wh'):
            for i in range(len(lspic)):#循环问号高亮
                self.searchtag(self.init_data_Text, lspic[i], 'wh')
        elif(tagh == 'error1'):
            for i in range(len(lspic)):#循环未找到引用源高亮
                self.searchtag(self.init_data_Text, lspic[i], 'error1')
                
     #高亮查找字符串子函数
    def searchtag(self,text_widget, keyword, tag):
        pos = '1.0'
        while True:
            idx = text_widget.search(keyword, pos, END)
            if not idx:
                break
            pos = '{}+{}c'.format(idx, len(keyword))
            text_widget.tag_add(tag, idx, pos)

    #打印
    def ptlist(self,lspic):
        for n in range(len(lspic)):
            self.result_data_Listbox.insert(END,lspic[n]+'\n')
               
#创建图标
def icocreate():
    tmp = open("tmp.ico", "wb+")
    tmp.write(base64.b64decode('AAABAAEAQEAAAAEAIAAoQgAAFgAAACgAAABAAAAAgAAAAAEAIAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD///8Q////XP///53////L////6f////n/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////+f///+n////L////nf///1z///8QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP///xT///+V////9f//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////9f///5X///8UAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP///0L9/f3n/v7+//7+/v/+/v7//v7+//7+/v/+/v7//v7+//39/f/9/f3//f39//39/f/+/v7//v7+//7+/v/+/v7//v7+//7+/v/+/v7//v7+//7+/v/+/v7//v7+//7+/v/+/v7//v7+//7+/v/+/v7//v7+//7+/v/+/v7//v7+//7+/v/+/v7//v7+//7+/v/+/v7//v7+//7+/v/+/v7//v7+//7+/v/9/f3//f39//39/f/+/v7//v7+//7+/v/+/v7//v7+//7+/v/+/v7/////////////////////5////0IAAAAAAAAAAAAAAAAAAAAAAAAAAP///0L////3/v7+//7+/v/9/f3//f39//v7+//4+Pf/9PT0//P09f/y8vL/8vLy//Ly8v/x8vL/8fHx//Hx8f/x8fH/8fHx//Hx8f/x8fH/8fHx//Hx8f/x8fH/8fHx//Hx8f/x8fH/8fHx//Hx8f/x8fH/8fHx//Hx8f/x8fH/8fHx//Hx8f/x8fH/8fHx//Hx8f/x8fH/8fHx//Hx8f/x8fH/8fHx//Hx8f/x8fH/8vLy//Ly8v/z8/T/9fX1//n5+P/7+vr//f39//39/f/+/v7//v7+///////////////////////////3////QgAAAAAAAAAAAAAAAP///xT////n/v7+//v7+//6+vr/9PT0/+zs7P/e3+T/2tjT/83NyP+7w8X/vru9/7m4uf+xtLT/r7S0/7Gzsf+ys7D/srOw/7KzsP+ys7L/srOy/7Kzsv+ys7L/tbG0/7WxtP+1sbT/tbG0/7ezs/+3s7P/tbKy/7Wysv+1s7D/tbOw/7WzsP+1s7D/tbOw/7WzsP+3tLH/t7Sx/7eytf+3srX/tbG0/7WxtP+3s7P/t7Sz/7m2tf++u7v/vL/H/9DKx//e18//4d/d/+vr6//z8/P/+Pj4//z8/P/8/Pz//v7+/////////////////////+f///8UAAAAAAAAAAD///+V/f39//z8/P/5+fn/8PDw/+Li4v/Ozs//rrC9/5uanv+Lh4P/e3p3/2Jrfv9XZHf/UmN1/1Bjdf9MYXb/TGF2/0xhdv9MYXb/TGF1/0xhdf9MYXX/TGF1/09gdv9PYHf/T2B3/09gd/9QYHr/UGB6/09fef9PX3n/T2B2/09gdv9PYHb/T2B2/09gdv9PYHb/UGJ4/1BieP9QYXj/UGF4/09gd/9PYHb/UGJ3/1Bid/9SZHj/WGl9/2t1ev9+goP/kZSU/6irr//IyMj/39/f/+zs7P/4+Pj/+vr6//z8/P//////////////////////////lQAAAAD///8Q////9fz8/P/6+vr/9vb2/+3t7f/b29v/xMPC/6qhmv9xe4f/NVV5/xlFeP8LQX7/C0J//wdCf/8GQn//BUKB/wVCgf8FQ4H/BUOB/wVDff8FQ33/BUN9/wVDff8GQ3z/BkJ8/wZEff8GRH7/BkN//wZDgP8GQX7/BkF+/wZDff8GQ33/B0R+/wdEfv8GQnz/BkJ8/wZDff8GQ33/BkN9/wZDff8FQnz/BkJ8/wVBfP8GQXz/BkN9/wZBfP8MRXr/IE10/1Zrev+Xl5L/urm5/9XV1f/p6en/9PT0//r6+v/8/Pz//v7+//7+/v////////////////X///8Q////XP/////+/v7//Pz8//r7+v/19fX/6Ofn/8vO0v9yjKP/G0l2/wxKiP8wdLX/RI/Q/1Oi4v9TpeX/Uabl/1ep5f9XqeX/Wqzo/1qs6P9cr+X/XK/k/1yv5P9csOT/XrDi/1+w4v9er+D/Xq/g/16w3f9esd3/XK/c/1yv2/9YrNb/WKzW/1er1f9Xq9X/U6fR/1On0f9QpM//TaHL/0yezv9Mns//SJrL/0WWx/9DlMj/QJDF/z+Qxf83hrz/LHWs/xNYlP8KQXn/OWCK/7a6wP/g4OH/8vHx//j4+f/8/Pz//v7+//7+/v/+/v7/////////////////////XP///53//////////////v/5/fr/9Pb8//Dq5/9+mrz/D0J+/ylurP9LoOH/S6To/0im7v9KqO//S6ru/0qr7P9Qre3/Uq/u/1Wz7v9VtO3/V7Tt/1e07P9Zt+z/Wbjr/1m36/9buOr/Xbjn/1+55v9cuuP/Wrjh/1m34P9Xtd//WbTf/1iy3v9Vr9v/VK7a/06s1/9MqtX/S6nU/0mn0v9Fos//Q6DO/0Cdy/8+m8n/OZXF/zWQw/80jsT/MozD/y2Kwf8ziMD/MXmz/w1Lh/8wWo//yNPi//r08P/6+f3//v7//////////////////////////////////////53////L//////////////7//v74/+/x9/+vvdH/E0N5/zJ0vf9Qo+r/Sabt/0il7f9AmNr/NIzL/zCJxf8wisP/MYnC/zOMwv81jsD/NY6//zeNwP83jr//OJG9/ziRvP84kb3/OpG8/z2Suf8/krj/P5K3/z2Rtf88j7T/Oo2y/ziOsv82jbD/No2w/zWLr/81iKz/M4aq/zKFqf8wg6f/J3+l/yV9o/8ieqD/IXif/yB3n/8ccp3/G3Ce/x1xov8gea3/LIW6/y+Gu/8sgbf/DkqH/1VzlP/k5+z//vv5/////v/////////////////////////////////////L////6f///////////v/+//v59f/f5Oz/N2GS/x9gof9Qoe7/SaXx/zub5P8shs3/M4fH/zWKxv82jcX/OI/G/zyQxv89k8b/PpXF/z6Ww/9ClcX/QZXD/0SZxP9EmsL/Q5rE/0SZwP9Hmb7/SJm8/0OZvf9CmL3/RJu//0uhxf9Opsb/SqLB/0CYt/86krH/Oo+u/ziMrP82iqr/M4io/zGFqf8tgqb/K4Cj/yd8oP8leZ7/IXWc/x9xnP8bbZv/FGmb/xJpm/8jfK//K4e5/yx5sv8PQXX/nbDJ//X28f/9/fz//v7+////////////////////////////////6f////n///////////7+///w9vr/sLvK/wc+f/9Lltf/Uafx/zya4f8ticz/N4vN/zSNz/83j9D/N5LO/zuUz/89ls//P5jP/z6Yy/9BnM3/Rp3R/0Obzf9Dncr/R6LN/0+p1/9Iocz/SJ7H/0mfxv8/pc7/TrTe/13D7P9XvOX/R6bK/z6cv/9CocP/SafK/0yt0P9PsNP/ULHT/0ipy/88lbz/Loat/yuDq/8ogKf/JX2l/yF4pP8fdaT/G3Ci/xhtnf8VaZn/F2iY/yp5qf82hbP/F1WS/0Zplf/g6uz//P38//7+/v////////////////////////////////n///////////7+/v/9/fz/8PHu/2qJq/8TUpP/WKvr/1Ck6P81jM//NI7R/zSR0v8xl83/PJPW/zaazf9KltX/QprS/0Sd0/9Jn9D/SqLM/1au4P9Rp9//RqXM/0uv1v9Qu+T/R6fT/0qnz/9Rtdf/TsPr/2TJ7/9ct9n/R6PE/0as0P9Zv+H/Ysnn/2fN6P9uyuf/b8rn/2/J6P9rxeT/WbDS/zSLr/8xhq3/LYOr/ymBp/8lfaX/IXik/x1zof8XcZ//Fm2b/xZrmf8WaJf/LoGw/yhxqf8OQnn/0tfh//v7+v/////////////////////////////////////////////////+/v7//f38/+nr6f9Ja5H/KGqr/1mu7/9Cl9r/O5HV/zqU1/87l9n/P4vS/zlsyv9Am9z/QaDY/0ej1P9KpNb/SZ3V/0iY1/9Qptb/Wbbi/0Wb0f9Io9z/Vcbv/1XA5P9dyOf/Wsvq/2DQ6v9ZveH/S6TP/1y14f9ry+//cM7w/3bN7v96zuz/e9Hk/3vQ5v94yuj/cMHk/0KYuf85j7L/NYqx/zGGr/8thKz/KYCq/yV7qf8hd6f/G3aj/xpxn/8XbZv/GGqZ/yJ0of81gLX/CDx0/7a+y//39/f//v7+/////////////////////////////////////////////v7+//39/P/j5+j/O2CJ/y5yt/9VrPD/PZHV/z2T1/89l9r/Ppnc/yZWqf8BB4T/Kle2/1Sk5/9PqOD/T6nb/1Ol4/8mb8H/O4TL/1u96P81htT/JGy6/17O9f9i0O//X8zz/0Wx6f8Zdcn/GnHQ/y+A4P8rdMf/RJDO/2Cx3v9+1Oz/ftfg/37S7P98z+v/ecvp/2a42P9Bl7j/PJO2/0KXvv9PpM3/UqnU/0OZx/8ug7X/JXqt/x54pv8cc6H/G3Gf/xxunf8hb5j/OoO2/wY9d/+lsMH/9/b3//////////////////////////////////////////////////7+/v/9/fz/3+Xo/zheiP8ucrn/U6vx/z+T1/9Dmt3/Q53g/0Sg4v9Cgs//CwaQ/wUGg/8gPJf/UKDn/1ew5v9br+n/S5Pn/w9Jr/9UtO3/FmjN/xxmwf9iye3/Y8ns/0ip5P8Lacj/HZPv/yyc8v9BouX/dcnu/4bX7P93y+r/UqrW/0Cbz/9AlMb/R5vJ/2e+4v9btND/RZy8/1SpzP9jt9//Z7zl/2C14/9cseH/U6fb/z2Rx/8ifKv/HnWk/x1zof8fcZ//I2+W/zuEtf8EOnb/n63B//b29//////////////////////////////////////////////////+/v7//f39/+Hj5/82Xob/MnW3/16u7f9Kmdr/SJ/g/0ij4/9NpOT/VKXm/xQpjf8FBYL/AgaE/xcqiP9Vndb/Vbbf/2G18P8PU8L/Fnfj/wZx2f8getX/ZLft/zCLy/8Ga9L/EI31/yuZ8P9Lp9v/csXl/1624f8wjcj/I37J/ziS5f9Eoe3/VKbp/06b5f8+jMv/WKzQ/2K00v9uwOL/cL/m/2y65v9mteX/YLDk/1ms4f9Rpt7/OpfT/yR+tv8hdaf/InOf/yNxnv89ha3/BTh3/56twP/09PT//v7+/////////////////////////////////////////////v7+//39/f/h4+f/Nl6G/zJ1tv9eru3/Tp3e/0yk5P9Oqen/U6vq/1Cv5v9FfMr/AApx/wQEd/8TFYz/BhB3/0p2vP9lteD/CmnZ/wmC+f8Ggvn/DXfp/wVu1P8Ke9//Gof6/yub9P9buOb/dtH3/zaTyP8afsr/OJ3p/0up9/9Yrvj/X7L0/2Gw9P9dqu//W6nf/3LE5f91xuf/c8Tl/3DB4/9sveH/Z7Xl/2Gw5P9ZrOH/Uabe/0eg3/8/l9P/LYG4/yFyp/8jcZ//Poat/wU4d/+ercD/9PT0//7+/v////////////////////////////////////////////7+/v/9/f3/4+Xo/zVdhf80d7j/YLDv/1Oi4/9RqOn/Uazs/1at7f9StOr/X7Lv/xk5jP8FC3D/J0GW/z5Wtv8CCnX/BhV7/w9izv8Nifn/AYn+/wOH/f8Eh/7/C43+/yeS+v9Lqeb/idz4/y2IwP8pjd//PqT7/0er/v9Rr/j/YLT1/2iz8/9krvX/W6fj/2m44f9xw9z/Zrfa/2S02v9nteD/bLjn/2e15v9gsOT/WKvh/1Km3/9Kn+H/Rprb/0GT0/8tfr3/JnSj/z2FrP8ENnX/nazA//T09P/+/v7////////////////////////////////////////////+/v7//f39/+Pl6P81XYb/NXa4/2Cw7/9Xpuf/Va3t/1ey8v9ds/P/X7fz/1669P9am+P/BhJ1/xUdhP9UhdT/PnrR/wopn/8EDXT/CTyo/w5z4/8Sivj/DpD8/w+O9P8Rcsv/h9f4/0+j1v8pid//QKP+/1Gr9v9Rrvr/WLP0/2C18/9lsfj/ZKv0/1Se1f+D0vP/gdLn/3rJ7f9eqdn/K3Cw/zR1wP9RnNP/Wafe/1ir4f9Sp97/Tp7h/0iZ3f9ClNr/O47U/zF/r/8+ha7/BDZ1/52sv//09PT//v7+/////////////////////////////////////////////v7+//39/f/j5Oj/NliH/zh1uf9qs+3/Wqvs/1yx8v9ft/j/X7n5/1+89P9bvvf/b77+/z5nsf8HE3j/HDOi/yd+3/8Gdez/Dm/r/xI9rf8BEG7/Cit+/xVgw/8fhPD/F3zV/1Cl2P8fhtr/P6P5/0yr+v9Urvf/XLH7/2Gy+P9msPP/a7Dx/2Ch5/9iptn/itH0/4rO8v9Picn/OG6+/0t73f9Bbdn/I1K6/yRauf87gsv/SqDT/0eh2v9Im9r/RpXZ/z+P1f88iMj/P4PA/wU2cv+hrcD/9PT1//7+/v////////////////////////////////////////////7+/v/9/f3/5OTo/zZYh/86drr/abLr/16w7/9gtvX/ZLv6/2O+/P9nwfz/YsX7/2rI+/95yPj/GzqG/wQMbv8vVa7/A2/d/wCJ+f8Tj/X/Fm7Q/w9HrP8CInT/BS11/xpeqP8pkeP/O6f0/0eq+P9XrP3/YKz+/2Gx+P9ksvf/Z7Dz/2uv8/9Skd3/cbrc/4rT7/9NiMf/RHjL/1eI5f9Vguv/Tnfp/0tv5P84XdX/FT+u/ytdvv9LkNX/O5fT/zqb0v9Dk8v/QYzM/0eKyP8FNnL/oa3A//T09f/+/v7////////////////////////////////////////////+/v7//f39/+Tl6f81V4b/OnW6/2y17f9hs+//ZLz2/2fA+/9nw/z/bMT//2zI/v9pxff/eNH8/3i56/8LInb/Bg5n/wxm0v8XgfL/DoHp/wt43v8UhvH/JJL1/yVzv/8LO3j/BSZs/yNRl/9WmN3/X7L1/1ay9f9nsvT/abH0/2iu9f9mqvP/TIvW/3W75f9RlMX/RnfU/1mH6/9Vguv/T3nq/0px6f9JaOb/Q2Dl/zhV3f8gQMD/EDWZ/zFvxP8+kdL/O5DF/0CMy/9MkM7/BDRx/6Csvv/09PX//v7+/////////////////////////////////////////////v7+//39/f/k5On/NVeG/zp1uf9tte3/Zbnx/2nB+P9rxf3/a8j+/2/K//93yv//Yazm/1Wd3f96yvv/WJrY/wIUbf8RXc7/Bnbl/x6A5v8afN7/F4zv/yue+/80ofv/RaT3/0OS3f8uba3/Djt2/xlHe/9Cdab/WpvY/22w8/9orPP/ZKfx/02O0/9Zldn/QXbO/1iE8P9Wgu//T3nq/0hx6P9Daeb/PmLg/zpb3v82Vdn/MFHN/yZCx/8UJJv/IUei/zSKzf89isn/So7M/wQ0cP+grL7/9PT1//7+/v////////////////////////////////////////////7+/v/9/f3/4OPs/zpWh/8/drf/cLjo/2u87/9vw/b/csj7/3HK/f90zP7/edH8/33P/f89hND/JWzO/ylwyP8RR6X/FlW8/wJv2f8lh+j/HoTk/yCM7v84ovr/Qqb7/0yr+/9Rrvn/WLH3/12u8/9Hjc//LWSk/xlBd/8XQnn/MlyX/0d4tf9Nhcv/UYXY/1aF6P9Uf+7/Tnvr/0dz5f9BbeL/OmTd/zlb3f82Vdj/NE/S/zFJzf8uRsL/KDy4/xMlmP8VKYv/TIPG/0uLx/8DNGz/n6u6//T09P/+/v7////////////////////////////////////////////+/v7//f39/+Dk6/86V4X/PnWz/3K76P9wwfD/dMn4/3fN/P910P7/eNL//33Y+/9+2Pn/gNL7/zN8zf8Hb87/F4Lu/x9q3f8QbtT/GVy5/ziP6v8hj+r/Qqb9/0qq/f9Srvr/WLH4/1uw9/9jsff/a7H1/2+v8v9vrO//YJnf/0Bzvf8wWaX/H0KI/xY5gv8mRZL/NFOm/z1iw/9Lctr/Q2bZ/zxc2P81UN7/MkzW/zBJzP8tRcP/Kj+9/yg4uv8hL63/ESCR/xAidf9QeML/BDJv/5msu//09PT//v7+/////////////////////////////////////////////v7+//39/f/f5ej/N1WA/z95s/9yvOb/csXy/3fM+v950P3/d9P+/3rX/v9/2/v/g9/5/4jg+v+E2Pv/DIHL/xKV9P8vlPH/I3fV/wIie/8gTqP/L5Dk/0qo/P9Rq/v/Wq/5/16w9v9jrvf/Zq/2/2qv8/9rrfD/Z6b1/2Wh8/9lmvH/YpPu/12L7v9UgeX/P2vR/ypVuf8aPpP/DS6G/xMykP8cOpz/JUqq/zBQvv8uRsT/KjrE/yg6tf8kMrP/ICur/xwmnv8PGIP/CxNs/wsmbP+cq7r/9PT0//7+/v////////////////////////////////////////////7+/v/9/f3/4OXn/zdWfv8/eLD/dL/m/3TI8v950Pn/fdb+/3zY//9+3vz/g9/+/4Xf/v+J4v3/e83z/w1syf8kk/z/Nab5/yuE2f8UNYr/ARRm/z+L2v9OqPn/Wa/9/16v+P9jsPT/Z673/2mu9f9prfH/cbP1/22f8v9nm/H/XZPt/1aM6v9Zguv/U3ro/05z5/9Ia+T/QWLd/zZZz/82W8r/H0Ww/xUzmf8JJof/DiuD/xEvg/8cMJv/Hi6k/x0noP8YIZX/FhqT/w4PeP8CBlP/mJqt//T09P/+/v3///7+///+///////////////////////////////////+/v7//f39/+Pn5v85VID/QHev/3jC4P91yvX/e9L7/4Ha/v+C3P7/gOD+/4Tj/v+I5P3/jOb9/1Os2v8Rdtv/KJ/w/024/f83neb/P4HO/w40hP8nXKP/W7T3/1yw9/9ksfn/aa/5/2av9f9lq/D/YaPn/3i19/9nm+7/YpTt/1yM6/9Wher/VHvs/01z5/9Ha+T/QWXh/zla3v8oScX/M1HL/zZO0/8tRMr/KD+//yM5sP8cMqL/FCyJ/wwhfv8NH33/DR19/w0Zhf8PFIT/CQto/xMYTv/Ky9X/9/3y//z+/f///v7////+/////////////////////////////v7+//39/f/k5+b/OVSA/z91rf96xeH/dc70/3vW+v+B3v3/g+D9/4rl/v+O5/7/k+n+/5br/v82jsT/HIXo/y+m/P9ArPL/bL7i/06q3v80h9f/EUCT/1yf4v92u/r/a7Lz/2uz8/9oqvX/Zqbz/1KQ3v9Uj93/Y5bv/12N6/9WhOn/UX3o/0106P9Ga+P/QGXg/zte3P83Vdr/JkTC/zJOx/8zTMf/KD7B/yQ6uf8gM63/HS6l/xsoo/8WIpf/FSCN/xEcg/8JG23/CRF0/woLdf8FBGX/JiNU/+rt8f/+/v7//v79/////v////////////////////////////7+/v/9/f3/4+bl/zdSff8+da3/fcjk/33S8v+F3Pn/ieL7/43m/f+X6v7/m+z+/6Hv/f+i7/3/HXbC/yOP6v8+qPv/WLbk/6nw//8iib//M5zt/1CY7P8kXKb/crDx/4PE/P9ztfH/bqnw/2mk7/9Pitr/UYzg/12O7P9WhOn/Un3p/0t15v9Ga+T/QWXg/zpd3P81V9j/NVDT/y5HyP8eNa7/QlvI/y9Evv8iNK7/IC+p/xooof8YH6D/FRuY/xIWjP8PE4P/Cw5//wkMeP8HDW3/Bg5i/wgHUf+en6////3///z+/f/+//7////////////////////////////+/v7//f39/+Pm5f83UX7/PnSr/4DK5f+N2PX/luL8/5vo/v+e7P7/oOz9/6Tv/f+q8vz/pu76/wxnw/8wmu//RJzr/6Pt+P99y+X/JIPI/0Gl+P9Vr/f/V57t/yRfrP9gneP/hr76/4W++v93svP/YJrl/0uH2P9aiur/WITu/0546f9GbeT/QGXf/zte3P81V9f/MFHT/zFLzf8uRMf/Fiuj/1py0f8rP7D/LD2z/xwpov8XIpr/FB+N/xEZh/8QFYT/DQ9//woMdv8HCXD/Awhs/xAWe/8iJnT/lJak///+/v/7/v7//v/+/////////////////////////////v7+//39/f/h5uf/O06C/0p6ov+a1ef/l932/57l+/+i6/3/o+79/6Tw//+r8v7/rfj6/4vV6/8PbsX/L5jv/3HE5f+w+v3/SpnJ/zWT4P9Jqv3/Vq/1/1Sy9/9Wp+3/GU2W/zReqv9fluD/baPw/2yc9f9Petr/bKr2/0F01/9kh/n/Z4T8/15/+f9YdvP/U2zu/01j5/9IW9v/QlPV/y5Bvf8dMZ3/ZnvM/yw8of8zPq//Hyqc/xIbjP8NFYP/CxJ9/wwQef8TF3j/JxmE/yYtgv8tKXv/aF6E//Lu+P///v7//v7///////////////////////////////////7+/v/9/f3/4Obo/ztOg/9MfKT/ndjo/5vg9v+i6Pv/pu79/6fx/f+n9P7/r/X+/7D5+v+Dy+P/DHDL/zSY4f+o8Pv/tvj9/yh7uP9DoO3/T678/1mx9/9Xsff/YbL5/2eo8P8dTZf/AiZk/zdgpv9dk+L/Q4HW/22v8/9gmen/Q3HT/z5m0P87W9L/OFPO/ztS0f89UdP/PU7R/z5Jz/9BScn/MTmp/3OOtf+attj/NUeK/zAyo/80NKb/MzGg/zIvmv8yLpb/LS2H/y8od/8bKl7/d3+V//Lw9f/9/Pz////+///+///////////////////////////////////+/v7//f39/+Hn6f86TYL/THyk/5/Z6f+i5Pf/qe39/6zx/f+t9P3/rPf7/7T3/f+2+/r/hMjl/xNyx/9dtOH/v/r8/53e6/8kfcP/TKjy/1Wv+P9bsfb/XrL5/2Ky+f9lrvb/aa31/y1fnP8BI2P/P2mr/2+w8f9trvH/bazv/26q9P9tpfj/bqLz/2+f8v9mken/W4Pe/1h/3f9de9X/XXK5/4CTw/+Cmb7/xOP0/77e7f92jrb/R1eP/zpHf/9FUIT/WmWW/3GFn/+XqcX/EyZi/6Gnwf/09/D//v79///+//////7////+/////////////////////////////v7+//39/f/h5+j/Ok2C/018pP+j3u3/pub4/63v/f+w8/3/sfb9/7H6+f+4+v3/uvz6/47O6/8fc7v/i9bq/8n9+/93wN3/LIrW/1Cr9P9asPX/XLL1/2Ky+f9isvn/YrH4/2Gv9/9nrvf/Pmyx/wYkYv80XpT/b6rx/2qr7P9nq+z/Zabx/2Oj7/9joO7/ZJ3u/2KY7v9upfj/Y5DW/7vg+v/M7vX/yOz3/8jq+//F6Pv/wuf2/8Xl+//C4ff/yOP2/8jg9P+92fD/tdTq/wgmaP+cq7v/9PT0//77/////P/////7/////v////////////////////////////7+/v/9/f3/4Ofn/zlKgf9SfaP/quHn/6vo9v+y8fv/tvf9/7j5/f+7+f//vf76/779+/+e2Ov/NnnB/7r0/v/O/vT/YbDX/zqU2/9ZsPb/X7L5/2Gy+f9hs/f/Y7L3/2ay9/9osff/Z672/3Gu8/9LfL7/Bitq/yZLgv9noOf/ZKTz/2ij7f9mnu//Z5zu/2aa7/9kmfL/UYTY/5q95P/S7Pv/0O76/83s+P/D5fz/m7/i/3OZyf9igLv/gqTM/8Xj+P/O4PX/xOD0/8PT9f8EI2b/n6m8//T09P/+/v7///7//////v/////////////////////////////////+/v7//f39/+Dn5/85SoH/VH+l/63j6f+v6/b/tfP8/7r5/v+8+/7/wPv//8L+/f/B/fz/te35/1qYyv/C+v//0P33/2Su2f9BmN7/W7D2/2Gy+f9jsvn/Y7L3/2Wy9/9psff/a7D3/2uu9f9sr/P/a6zw/06O0P8INnf/Ezhv/2eUz/9noev/Ypvv/16Y8f9bk/D/TIHd/11/v//H6/r/xuz0/6HI6v9ag7z/KFCi/yVKtv8sTc3/LUnR/xgzrv9ngsf/yuf1/8bm7//K3fP/BCVj/6Cnv//09PT//v7+/////////////////////////////////////////////v7+//39/f/g5+f/OEmB/1N+pP+w5uv/te/3/7r1+/+++vz/wP39/8T9///E/v7/xv/+/8X+/v+Vz+P/yfz9/9H9+v9yueH/RJfe/2Cx+P9jsfn/ZrH5/2ay9/9psff/aq71/2yu9f9tr/T/aa3z/2ar8/9jqfP/XZji/x1Khf8JLGP/RXS2/2ib6P9blu//UYro/zxsvf+w2e3/qdPp/011tf8oS7v/NF3U/z9r3/9BcN3/QXHa/0Bs2/81XNb/HT2o/2aBwv/I4/j/zuD4/wMkX/+fpcD/9PT1//7+/v////////////////////////////////////////////7+/v/9/f3/4Ofn/zhJgP9VgKb/sujt/7nx+P+++Pv/wv39/8T+/f/F/f//xv3//8j//v/I//v/yPz6/8z9+//S/f3/gsXn/0uc4v9hsPf/ZrH4/2ix+P9psff/a7H3/2yu9f9urvT/aq3y/2mq8v9rpvT/a6P0/2ii7f9ene3/LGOr/wgsZP8oTY7/WI3f/1SI3v9wmdv/c5nS/y9UtP88Zdj/RXPj/0x25/9Lcuf/Sm7n/0dp5v9JZeT/P2Tc/zNVz/8YMLD/fI7E/9Lg/v8DJF//nqW///T09f/+/v7////////////////////////////////////////////+/v7//f39/+Tm5/82SH3/WoGl/73q6/+88/b/wPn6/8T9/v/F/v//yv/+/8z//v/P//7/0f/+/8v+/v/W//r/0vz8/5zX6P9SqOn/Xar1/2i17v9qsfb/a671/2uu9f9srvX/aqzz/26u9f9xsff/Z6Xw/2Wi7/9noe//ZZ7v/2Oa7v9JfdH/D0F//w4zcf9Ib7r/UH3Z/0hx1v9Ndt//THfo/0t17f9MdOb/SW/k/0ds5v9EZ+X/RGHl/0Be4f87Wdz/LUvP/xQrnv+Optb/CSRc/5ylvv/09PX//v7+/////////////////////////////////////////////v7+//39/f/k5uf/Nkh9/1yDpv/B7O3/wPX4/8T7/P/G/f7/yP7//8z//v/P//7/0v/+/9P//v/P/v7/2P/7/9T8/P+97vf/Xqfi/2Wt+v9ns/P/a6/6/2yt9f9srvX/aqzz/2iq8f9ysPP/drP1/2ei7/9mn+//ZZ7u/2Sb7v9glu3/XZLs/1iQ5P8sXan/BCdu/ytOlv9VfOL/U3Xu/0907P9IeNv/SnHl/0ds5P9DaOP/QGPh/0Ff4v8+XN//OVfa/zdV2P8kRcT/GS6T/wUWbP+iq7D/9fXz//7+/v////////////////////////////////////////////7+/v/9/f3/5ebo/zVHfP9cg6b/wu3u/8H09//G+vz/y////8v////P//7/0v/+/9X//v/X/v7/1f///9n//v/a/v7/1/3//3mz2/95vPv/ZbL0/2mt9/9srvb/aqzz/2qs8/9lp+7/crDv/3Ov8f9mnu7/Zpzy/2Oa7/9hl+7/XZLt/1uP7f9ZjO7/V4no/0Z0yv8TOYL/DzZx/0Nrxv9Qcuv/TG3v/0Zr5f9DZ+L/QGTi/z1f4P89W97/Oljb/zhW2f82VNj/LU3U/x84t/8BDoL/oaa7//X09P/+/v7////////////////////////////////////////////+/v7//f39/+Xm6P81R3z/XIOm/8Lt7v/G9vn/y/z9/87////O////0f/+/9T//v/X/v7/2f7+/9n//v/Z/v//3v/+/+H+/P+p2un/ba/p/3jI/P9ssfL/aqzz/2iq8f9pqvH/YKHo/3Cs6P94sOn/X5Pl/2aY8f9hl+7/X5Tu/1uP7f9ajOz/YInq/1SD7/9Pfu3/T3ff/yZPnf8EKmr/J0+g/0pt4v9FaOT/QWTi/z5h4v86XOD/O1nc/zhW2f82VNf/NFLW/zVN0/8sScT/Diiq/2JkqP/z8/f//v79///+/////v7////+/////////////////////////////v7+//39/f/i5Ob/NUZ7/1+Dp//K7vD/yff3/879/P/Q//7/0P/+/9P////W////2P///9v////c////3P///93+///e//7/2vr7/3mx3f90vPr/hsz5/2+18f9qq+//bKby/1+U5f+Br+X/hbLe/1KI5f9iluv/YZPu/1+Q7v9cjO3/WYfs/1eD6/9Tf+r/UHvq/0136P9Nc+T/M2K+/wo0ef8YOXj/QGDM/0Be4P87W+P/Nlva/zlW2f84VNf/NVHU/zFN0P8yTc7/MknJ/yY8vf8IGJD/s7zY//r88///+/7//f77/////v////////////////////////////7+/v/9/f3/4uTm/zVGe/9fg6f/y+7w/8z29//R/Pv/1P/+/9T//v/W////1////9v////d/v//3/7//9/+///f/v//3/7+/9v8+v/N8fn/dKjS/3W8+v+IzP7/fbz1/2yn6/9Ui9X/j7vm/4y23f9Jft3/X5Lr/1+Q7v9eje7/Wojt/1eE6/9UgOv/UXzp/0546f9Lc+j/TW7m/0Nu4P85adD/FECb/wUrZv8rSqr/P1rY/zpV1v84VNf/NlLV/zNP0v8vS87/MEvL/zBHyP8sQsP/Gy2s/zM4iP/v9fr//v73//3+/v///v/////////////////////////////+/v7//f39/+Ll5v80RHn/X4On/8zv8v/R+fn/1P38/9f////X////2P///9v////e/v//4P7//+P////j////4////+L////h//7/5//7/8ru+P9upNn/fbbu/4zF/f+Jwv3/W5Tc/6PL6f+Wv97/Q3bW/1yO7f9cjO3/WYfs/1eE7f9UgOv/UXzr/0546f9LdOn/SG/n/0ts5P9AZ+f/N1/d/1B25f8kS6z/BTJr/xU6f/85UND/N1LW/zJO0f8vS87/LkrM/yxHyP8sQ8T/KkDB/yU4uv8OGZX/hYq4//r99v/5+fz///7//////////////////////////////v7+//38/f/l6Or/OUp+/1x+o//O8PP/0/j5/9b8/P/Z////2f///9v////d/v//4P7//+L9///m////5v///+b////m/v//5/7//+H//v/d/P3/1vP6/3+u4P9toOP/fbL7/2Oa6/+01+7/psvn/0V11/9XiOz/WYjt/1eE6/9Tf+r/UHvo/0136P9Kc+f/R2/n/0Rr5f9Ea93/P2Lj/z1b2P9ietv/LlTP/yxSx/8OOIz/BjFm/yZDuv8xTc7/LknN/yxIyv8rRcX/KkHC/yk+v/8nOrv/Fius/xcZef/f4ev/+vv8///+//////////////////////////////7+/v/9/P7/6Ovy/1Jkif9NY5P/1PDv/9X29//Y+/v/3P7+/93////h////4f///+H////h////5P///+T////k////5P///+f////m////5v///+b//v/e+/v/sdTp/22X2P9Cb8n/0OP3/77a7P9dien/aJvy/1iK6P9Rgub/T33o/0166v9Oden/SnDn/0ht5v9EaOT/Pmbe/z1f4f8rUtH/bYTW/ytQxf83UNH/OFPL/xVAo/8GK2n/GTeV/y5Hxf8pQ8f/LEO//yw9wf8rOb//Kji3/yIxtP8NHon/YGKg//z69/////7////////////////////////////+/v7//f38/+/08P+Hkbj/HSpo/8/t8f/X9vb/2/r7/979/v/g/v//4////+P////j////4////+b////n////5////+f////p////6f///+n////p//7/5v70/+P8+//b+Pz/tdPh/+P5+//a8/n/TnzO/26h/v92pf3/Y5Dy/1J86P9Mdub/THPn/0hu5f9Ga+T/Qmbj/z5i3v89XOD/JUvJ/3qQ2P8uTcP/MUjN/zZO0v8wUMz/JUS+/ww1fP8KLnD/KkCx/ytBv/8qOsD/Kji8/yg3sv8jNKr/GCaj/wsNb//X2eP//v/+/////////////////////////////////////v/6+vb/y9Hm/xgiWf+JosD/1/T2/9n29//e+/z/4Pz9/+X+/v/m/v7/5f7+/+X+/v/p////6f///+n////p////6////+z////s////7P7//+38///u/P7/7vv9/+78/P/n+///7fX//32c0v9Ye9n/a5b2/3Oe/f9vmPz/WoDw/0lw5P9FauH/Qmfg/z5i3/8/XuD/Pljf/yFEwf9+ktT/QFvI/ypExP8zStP/M0fN/yxKw/8qRMD/Gjee/wcocP8aNpz/Jzyy/yY2tP8mNbD/JDGp/xopq/8MEYv/XWGQ//39/v/8/Pz///////////////////////////////7//fj8/+jw6P9vep3/Gitp/8Pc4//d9vf/3/j5/+D5/P/l/fz/5v38/+f9/f/n/f3/6v/+/+r//v/q//7/6v/+/+3+/v/t/v7/7f7+/+3+/v/r/v3/6v79/+j8/v/m/P7/5f75//j7+f/i+Pb/t87q/12E1/9Ue93/ZYv1/2uQ/v9mjPv/UXfs/0Bl3v89X97/P1rg/z5W3P8gQL7/dIfL/2F5zv8kQbr/MErN/zZEyv8yQ8T/LT7H/yg/wf8dP6v/DC98/xApiP8iNqn/IzCu/yEor/8YLKP/FCCZ/wsNZv/g4ef//P38/////v/+////////+f///////////v////3+/f/9+fX/3Nvt/zZEdP8zQHT/wdjj/9/58f/m9/j/5vn2/+j7+P/o+vv/6Pn8/+f8+//n/Pv/5/z7/+f8+//p+/v/6fv7/+j7+v/p+/r/7Pv6/+z7+v/s+/v/7Pv7/+76+//w+vv/7/r7/+75/P/p9f7/rcHi/1l1yf9LbOf/XH/4/2WK+v9ihPn/Tmjv/0BY2/8+WNH/IjvN/2V2uf+Pm9D/KTfJ/ydKxv8xRcL/MUHC/y0+vv8qPLv/Jji3/yA5sP8YOJT/DSZ9/xwwm/8cKqX/HCem/xggm/8FDXf/cHKc//j59f///vz/+f7/+f///+n///////////7////3/v7//v34//T09P/Iz+H/Nkd6/x0rXv+Qnbv/3+70/+j0+P/q9/j/6/n1/+v69P/w+vj/8fr4//H6+P/x+vj/8vn4//P5+P/0+vr/9fr6//T5+P/0+fj/9Pn4//T5+P/4+fr/+Pn6//j5+v/4+fr/+vv1//T59v/q8vv/rrfc/1Nqyv9NZN//WHX3/1qB+f9befr/TGbm/yU+x/9VXqT/s8Hk/zJCwP8lQcP/L0HF/y9AwP8rPLv/KTq5/yU2tf8gNbH/IDGv/x0wof8NIn//FSmS/xknmv8ZIZr/DhSL/xITWP/v8Pb///3+//v+/+n////L///////////+////+f/+//3/+//9/vj/9PTw/+be4v9/fKD/FSJX/xEsWv9SZo//bIKm/26Fpf9uhqT/cYSn/3GEp/9zhaj/c4Wo/3aGqf92hqn/doap/3aGqf91hqn/dYap/3WGqf91hqn/d4Wp/3eFqv93har/d4Wq/3iDrP96hqn/fYao/3+Dqf9ugp//MEKR/yk8sv9AWtn/UWvs/19z+v9KaOj/O0Sl/3CAo/8uP6T/L0LH/ys/wf8rPLv/Jzi3/yU2tf8hMrH/IDGs/x4psf8eKaj/HS6T/wkef/8UJ4v/FiGR/xIYk/8FBWX/m5u0///7///8/v7L////nf/////////////+/////P///v7//P7+//z9/P/2+Pn/6Ozx/83U4P+Pl63/VmGM/zxHd/82QHP/Nj91/zRBc/8zQXP/MkBx/zJAcf82QXP/NkFz/zZBc/81QXP/M0Jz/zNCc/8zQnP/M0Jz/zVBdP81QXT/NUF0/zVBdP8yQHb/NEJy/zdBcv85Pnj/Oj13/zZBcP8xQXb/OEmQ/0FRvP8/TdH/OlvY/ys2sv80QHT/Lz2S/z1Kzf8qQrr/KTq5/yY2tv8jNLP/HzCw/x8wp/8eLaH/Hyqg/x0kn/8VKJH/CRt8/xIhhv8SGo3/CAh7/z49aP/++v///f7+nf///1z///////////////////7////////////+/////P3+//v8/P/5+vr/9PT1/+zt7//p6uv/5eXn/+Xl6P/k5ef/5OXn/+Tl5//k5ef/5eXn/+Xl5//l5ef/5eXn/+Tm5//k5uf/5Obn/+Tm5//k5ef/5OXn/+Tl5//k5ef/5OXn/+Tm5//k5ef/5eXo/+Xk6f/k5ej/5OXo/+Tl6P/f4e7/r7DX/2Fhrf8vLJL/x8XZ/8TL4/83Pqj/O1TU/y48vf8lNLP/ITGx/xwtr/8hK6P/Hiie/xwmnP8YIpn/GyCY/xgfj/8KFXn/EyB+/wkOhv8CB0z/1t7j//r6+Fz///8Q////9f////////////////////////////////7+/v/+/v7//v7+//39/f/9/f3//f39//39/f/9/f3//f39//39/f/9/f3//f39//39/f/9/f3//f39//39/f/9/f3//f39//39/f/9/f3//f39//39/f/9/f3//f39//39/f/9/f3//f39//39/f/9/f3//f39//39/f/8/fz/+f70//b8+P/z9vv/19jo/+Hf6f/z+/r/gorB/zlBu/9EW9L/OE7G/yU5r/8cL6H/Hyqg/xwmnP8aJJr/FiCW/xoelf8XHY7/ExyE/woWeP8NFoH/BwZk/5OTsPX9/fwQAAAAAP///5X//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////v7+//z+/v/+/v3///78////+//8/f7//f77/+/z+v9jX6v/M0Cu/0VPzv9GUNb/P0zK/zdCuP8rNav/ICqg/xchl/8XHJL/FhuN/xUcif8YIYr/FyOG/ywqjP8/PG+VAAAAAAAAAAD///8U////5////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////v///v3//v7+//z+///7/v///P77///6/v/9/fT/8ez5/3Z6sf8yNJP/Mzuu/zZHuP8/Sb7/QUrA/z5Iv/89Rr3/PkK4/zxBtP86QLD/NT2r/yUwkv8nLHnnLjFfFAAAAAAAAAAAAAAAAP///0L////3///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////+/////v/+/////v////7+/v///v/////+///+/v/9+/r/2Nfo/4aIs/9FSY7/LC2J/zAxlP8xMp3/LzGh/zQzoP8yM5v/LDCP/yguhv8sLHH3Ki5gQgAAAAAAAAAAAAAAAAAAAAAAAAAA////Qv///+f///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////7//f34//v8+f/6/Pz/+vv8/9zd7P+vscb/jpGs/3Z6mv9saJT/a2eR/3Z0mf+HhqfnamqQQgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD///8U////lf////X///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////7///36/////P////7+///++////f7///3///7+///8/v////3+///9/vX//f6V//3/FAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD///8Q////XP///53////L////6f////n////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////+/v///vz//v79//v+/v/5/v///v7++f3+/un7//7L+f/+nf3//Vz+//0QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/wAAAAAAAP/4AAAAAAAAH/AAAAAAAAAP4AAAAAAAAAfAAAAAAAAAA4AAAAAAAAABgAAAAAAAAAGAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAABgAAAAAAAAAGAAAAAAAAAAcAAAAAAAAAD4AAAAAAAAAfwAAAAAAAAD/gAAAAAAAAf/wAAAAAAAP8='))
    # tmp.write(base64.b64decode('粘贴icon.py字符串内容'))
    tmp.close()

def gui_start():
    init_window = Tk()              #实例化出一个父窗口
    init_window.resizable(width=False, height=False)#禁用拉伸
    icocreate() #创建图标
    init_window.iconbitmap("tmp.ico")
    os.remove("tmp.ico")  #删除icon文件
    ZMJ_PORTAL = MY_GUI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()
    init_window.mainloop()          #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示

gui_start()#启动