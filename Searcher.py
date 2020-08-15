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
        self.init_window_name.geometry('1100x700')
        #self.init_window_name["bg"] = "pink"                                    #窗口背景色
        #self.init_window_name.attributes("-alpha",0.9)                          #虚化，值越小虚化程度越高
        #标签
        self.init_data_label = Label(self.init_window_name, text="Ctrl+V 输入说明书")
        self.init_data_label.grid(row=0, column=0)
        self.result_data_label = Label(self.init_window_name, text="结果输出")
        self.result_data_label.grid(row=0, column=17)
        #文本框        
        self.init_data_Text = Text(self.init_window_name, width=70, height=50, undo = True)  #原始数据录入框
        #self.init_data_Text.grid(row=1, column=0, rowspan=10, columnspan=10)
        self.init_data_Text.grid(row=1, column=0)
        #列表框
        self.result_data_Listbox = Listbox(self.init_window_name, width=70, height=50)  #处理结果展示
        self.result_data_Listbox.grid(row=1, column=12, rowspan=15, columnspan=10)

        #纵向滚动条
        self.L_scroll=Scrollbar(self.init_window_name)
        self.L_scroll.grid(row=1, column= 10, sticky=S + N)#指定 上下展开
        self.L_scroll.config(command=self.init_data_Text.yview)
        self.init_data_Text.config(yscrollcommand=self.L_scroll.set)
        self.R_scroll=Scrollbar(self.init_window_name)
        self.R_scroll.grid(row=1, column= 22, sticky=S + N)#指定 上下展开
        self.R_scroll.config(command=self.result_data_Listbox.yview)
        self.result_data_Listbox.config(yscrollcommand=self.R_scroll.set)
        #按钮
        self.smsfind_button = Button(self.init_window_name, text="提交", bg="lightblue", width=10, command=self.sms_find)  # 调用内部方法  加()为直接调用
        self.smsfind_button.grid(row=1, column=11)
  
    #功能函数
    def sms_find(self):
        #初始化text（去空格）和Listbox（清空）
        ls = ['本申请信息如下：']
        flag = [] #存在的错误
        src = self.init_data_Text.get(1.0,END) 
        src = src.replace(r' ','')
        text_content = (src.replace(" ","")).split("\n")
        text_content.pop()#列表最后一个元素是空删除它
        #print(text_content)
        self.init_data_Text.delete(1.0, END)
        self.init_data_Text.insert(END, src)
        self.result_data_Listbox.delete(0, END)
        lspic, a = self.sms_pic(src) #附图查找
        etitle = self.sms_titles(src)#标题查找
        wh = self.sms_wh(src)#查找是否有？
        error1 = self.sms_error1(src)#查找是否有“引用源错误”
        if(a + etitle + wh + error1):
            flag = [r'==================分割线==================' ,'说明书存在以下错误：']
            flag   = flag + a + etitle + wh + error1
            for i in range(len(flag)-2):
                flag[i+2] = str(i+1) + '、' + flag[i+2]
        else:
            flag.append('说明书正常')
        print(flag)
        title  = self.sms_info(src)
        
        ls = ls + title + lspic + flag #所有结果列表汇总
        self.ptlist(ls)#输出


    #查找说明书格式标记\n",
    def sms_titles(self,src):
        lstitle = []
        pttitle = []
        if(src.count('技术领域') == 0):
            lstitle.append(r'没有“技术领域”')
        elif(src.count('技术领域') > 1):
            lstitle.append('出现'+str(src.count('技术领域')) +'次“技术领域”')
            pttitle.append(r'技术领域')
        else:
            pttitle.append(r'技术领域')

        if(src.count('背景技术') == 0):
            lstitle.append(r'没有“背景技术”')
        elif(src.count('背景技术') > 1):
            lstitle.append(r'出现'+str(src.count('背景技术')) +'次“背景技术”')
            pttitle.append(r'背景技术')
        else:
            pttitle.append(r'背景技术')

        if(src.count('发明内容') == 0):
            lstitle.append(r'没有“发明内容”')
        elif(src.count('发明内容') > 1):
            lstitle.append(r'出现'+str(src.count('发明内容')) +'次“发明内容”')
            pttitle.append(r'发明内容')
        else:
            pttitle.append(r'发明内容')

        if(src.count('附图说明') == 0):
            lstitle.append(r'没有“附图说明”')
        elif(src.count('附图说明') > 1):
            lstitle.append(r'出现'+str(src.count('附图说明')) +'次“附图说明”')
            pttitle.append(r'附图说明')
        else:
            pttitle.append(r'附图说明')

        if(src.count('具体实施方式') == 0):
            lstitle.append(r'没有“具体实施方式”')
        elif(src.count('具体实施方式') > 1):
            lstitle.append(r'出现'+str(src.count('具体实施方式')) +'次“具体实施方式”')
            pttitle.append(r'具体实施方式')
        else:
            pttitle.append(r'具体实施方式')
            
        self.sms_highlight(pttitle, 'title')#高亮
        return lstitle

    
    #图片标号查找                
    def sms_pic(self,scrp):
        rs = []#结果
        lspic = []
        nums = []
        flag = []
        sel = r'图\d+[a-zA-Z]?-?图?\d*[a-zA-Z]?' #可匹配  图11A-图14A
        #p = re.compile(sel, re.X)
        lspic = re.findall(sel, scrp) #正则匹配 “图+数字+字母”
        lspic = set(lspic) #去重
        lspic = sorted(lspic) #排序
        lspic.sort(key = lambda x:int(re.match('图(\d+)[a-zA-Z]?',x).group(1)))#排序
        if(lspic):
            rs.append('附图如下：')
            rs = rs + lspic
        else:
            rs.append('说明书不包含附图！')

        self.sms_highlight(lspic, 'pic')#高亮

        #查找是否缺少附图标号
        if(len(lspic) > 1):
            num = int(re.search('\d+', lspic[len(lspic)-1]).group())#获得最大值
            nums = set(re.findall(r'\d+', ''.join(lspic))) #拼接成字符串
            if(len(nums) != num):
                flag.append('附图图号不连续')
                
        #查找附图标号有字母且有数字
        sel = r'(图\d+)[a-zA-Z]'
        nums = set(re.findall(sel, ''.join(lspic))) #拼接成字符串
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
            wh.append('具有' + str(scrp.count('?')+scrp.count('？'))  + '个问号')
        self.sms_highlight(['?','？'],'wh')
        return wh
        
    #查找是否有“未找到引用源”并高亮
    def sms_error1(self,scrp):
        error1 = []
        if(scrp.count('未找到引用源') > 0):
            error1.append('具有' + str(scrp.count('未找到引用源')) + r'个“未找到引用源”')
        self.sms_highlight(['未找到引用源'],'error1')
        return error1

    #发明名称，段落数
    def sms_info(self,scrp):
        title = ''
        info = []
        text_content = (scrp.replace(" ","")).split("\n")
        text_content.pop()#列表最后一个元素是空删除它
        #text_content = re.findall(r'*\n',scrp)
        #print(text_content)
        title = '发明名称：' + text_content[0]

        pa = ''
        tp = re.findall('\\[\d\d\d\d\\]', scrp)
        pa = '总计段落：'+ str(len(tp)) 
        info.append(title)
        info.append(pa)
        return info


    #高亮
    def sms_highlight(self, lspic,tagh):
        self.init_data_Text.tag_config('pic', background='yellow') #配置字体  图号
        self.init_data_Text.tag_config('title', background='pink') #配置字体  标题
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
    tmp.write(base64.b64decode('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'))
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