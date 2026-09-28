try:
    import pyi_splash # type: ignore
except:
    pass    
from pathlib import Path
import threading
from os import remove
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkinter import messagebox
from tkinter import font
import pickle
import re
import keyboard
import webbrowser
import customtkinter as ctk 
from google.api_core.exceptions import InvalidArgument
from google.api_core.exceptions import ResourceExhausted
from google.api_core.exceptions import NotFound
#win_color, menu_bg, menu_fg, menu_hover, text_bg, text_fg, ins, highlight_bg, highlight_color, selectcolor, btncolor, btnhover
Themes = (("#180C24","#270B47",'#FFFFFF','#0a011f','#0a011f',"#FFFFFF","#FFFFFF","#21083B","#270B47","#220F50","#2C1542","#170A38"),
          ('#050505','#0C0C0C','#FFFFFF','#2c2c2c','#0C0C0C','#FFFFFF','#FFFFFF','#363636','#1A1A1A','#2c2c2c','#1D1D1D','#000000'),
          ('#F0F0F0','#FFFFFF','#000000','#d3d3d3','#FFFFFF','#000000','#000000','#4E4E4E','#ADADAD','#2c2c2c','#BBBBBB','#807F7F'),
          ("#530000","#500000","#FFFFFF","#290000","#380000","#FFFFFF","#FFFFFF","#2E0000","#4E0000","#b81111","#360000","#6B0000"),
          ("#0F1E19","#114700","#FFFFFF","#0a1210","#11231f","#b5f2c2","#FFFFFF","#024e13","#063000","#327223","#11231f","#004700"),
          ("#060E1F","#00277C","#FFFFFF","#0a1210","#001B57","#FFFFFF","#FFFFFF","#07439e","#001130","#0C4368","#001B55","#011135"))
try:
    pyi_splash.close()
except:
    pass    
#querybox highlightbackground "#FFFFFF"
#text highlightbackground "#21083B" index 7
#to be differnt querybox highlightbackground
current_theme = 0
if current_theme == 0:
    high_bg = '#FFFFFF'
else:
    high_bg = Themes[current_theme][7]
   
##Functions##
def init_api():
        print("started init_api")
        import google.generativeai as genai
        genai.configure(api_key=api)    
        global aichat,aimodel
        aimodel = genai.GenerativeModel(model)
        aichat = aimodel.start_chat()
        print(model)
        print("Initialized sucessfully")

def get_api():
    def retrieve():
        global api
        api = ent.get()
        gkey.destroy()
    def keycheck():    
        if keyboard.is_pressed('enter'):
            retrieve()
            gkey.destroy()
        gkey.after(100,keycheck)    
    global sc_width,sc_height
    gkey = tk.Tk()
    sc_width = gkey.winfo_screenwidth()
    sc_height = gkey.winfo_screenheight()
    spl_x,spl_y = int(sc_width/3),int(sc_height/4)
    gkey.resizable(False,False)
    gkey.title("API key")
    gkey.geometry(f'350x150+{spl_x}+{spl_y}')
    lbl = ttk.Label(text="Enter API Key")
    ent = ttk.Entry(textvariable="Enter :",width=40)
    btn = ttk.Button(text='OK',width=20,command=lambda:[retrieve()])
    gapi_btn = ttk.Button(text='Get API Key',width=20,command=lambda:webbrowser.open('www.aistudio.google.com/apikey'))
    for i in range(3):
        gkey.columnconfigure(i,weight=1)
        gkey.rowconfigure(i,weight=1)
    lbl.grid(row= 0, columnspan=3)    
    ent.grid(row=1,columnspan=3)
    btn.grid(row=2,column=2)
    gapi_btn.grid(row=2,column=0)
    keycheck()
    gkey.mainloop()



test_win = tk.Tk()
test_win.withdraw()
sc_height = test_win.winfo_screenheight()
sc_width = test_win.winfo_screenwidth()
spl_x,spl_y = int(sc_width/3),int(sc_height/4)
test_win.destroy()
appfont = 'segoe_ui'
d_path = Path.home()/'Documents'
apipath = str(d_path) + r'\geminiapi.bin'
print(apipath)
try:
    with open(apipath,'rb') as f:
        f_data = pickle.load(f)
        f_info = f_data.split('~')
        api = f_info[0]
        print(f_info)
except FileNotFoundError:
    print('file not found')  
    get_api()
    save_yes_no = messagebox.askyesno("Save","Do you wish to store the api key in this device for future use?")
    if save_yes_no == True:
        with open(apipath,'wb') as f:
                pickle.dump(api +'~',f)
except EOFError:
    remove(apipath)            
    get_api()
    
    with open(apipath,'wb') as f:
            pickle.dump(api +'~',f)
def pick_model():
        model_win = tk.Tk()
        model_win.resizable(False,False)
        model_win.lift()
        global sc_height,sc_width
        sc_height = model_win.winfo_screenheight()
        sc_width = model_win.winfo_screenwidth()
        spl_x,spl_y = int(sc_width/3),int(sc_height/4)
        model_win.geometry(f'350x150+{spl_x}+{spl_y}')
        model_win.title("Choose a Model")
        model_ops = ['Gemini 1.5 Flash','Gemini 1.5 Flash 8B','Gemini 1.5 Pro','Gemini 2.0 Flash','Gemini 2.0 Flash Lite','Gemini 2.5 Flash','Gemini 2.5 Flash Preview 04-17','Gemini 2.5 Pro','Gemini 2.5 Flash Lite Preview 06 17']
        for i in range(5):
            model_win.columnconfigure(i,weight=1)
            model_win.rowconfigure(i,weight=1)
        model_combo = ttk.Combobox(model_win,values=model_ops,width=30)
        model_selbtn = ttk.Button(model_win,text="Select",width=18,command=lambda:choose_model())
        model_helpbtn = ttk.Button(model_win,text="Help",width =20,command=lambda:webbrowser.open("https://ai.google.dev/gemini-api/docs/pricing"))
        print(prev_model)
        print(model)
        if prev_model:
            model_combo.set(model)
        model_combo.grid(columnspan = 5,row=1)
        model_selbtn.grid(column=3,row=3)
        model_helpbtn.grid(column=1,row=3)
        def choose_model():
            global model
            model = model_combo.get()
            
            with open(apipath,'wb') as f:
                pickle.dump(api +'~'+ model,f)
            model = model.replace(' ','-').lower()#####added to try & solve proper model not getting updated in 1st instance
            model_win.destroy()
        def keycheck():
            if keyboard.is_pressed('enter'):
                choose_model()
            model_win.after(80,keycheck)
        try:
           pass
        except:
            print("Error occured while deleting models variables")
            pass    



        keycheck()
        model_win.mainloop()    
print(api)
try:
    model = f_info[1] 
    model = model.replace(' ','-').lower() #######edited######
    print("the proper model is",model)
    if len(model) >2:
        prev_model = True
    else:
        raise AssertionError
except:   
    prev_model = False
    model =''
    pick_model()

     
print(model)
###main window###
main_x = int(sc_width/14)
main_y = int(sc_height/14)

print(main_x,main_y)
def mainfunc():
    main = ctk.CTk()
    main.title("Chat")
    main.configure(fg_color=Themes[current_theme][0])
    main.geometry(f'{sc_width-150}x{sc_height-150}+{main_x}+{main_y}')
    btn_text =tk.StringVar(value='Enter')
    for i in range(5):
        main.rowconfigure(i,weight = 1)
    for i in range(10)    :
        main.columnconfigure(i,weight=1)
    
    ###
    menu_bar = tk.Menu(main)
    main.config(menu=menu_bar,)
    menu_file = tk.Menu(menu_bar,tearoff=0,fg=Themes[current_theme][2],bg=Themes[current_theme][1],borderwidth=0,activebackground=Themes[current_theme][3])
    menu_bar.add_cascade(label='Options',menu=menu_file)#label=File
    menu_file.add_command(label='Change API Key',command=lambda:[main.destroy(),get_api(),mem_api(),init_api(),mainfunc()])
    menu_file.add_command(label='Change Model',command=lambda:[main.destroy(),pick_model(),mem_api(),init_api(),mainfunc()])
    menu_file.add_command(label='New Chat',command=lambda:new_chat())
    #
    menu_font = tk.Menu(menu_bar,tearoff=0,fg=Themes[current_theme][2],bg=Themes[current_theme][1],activebackground=Themes[current_theme][3])
    menu_bar.add_cascade(label='Fonts',menu=menu_font)
    menu_font.add_radiobutton(label='Segoe Ui',command=lambda:change_font('segoe_ui'))
    menu_font.add_radiobutton(label='Cambria',command=lambda:change_font('cambria'))
    menu_font.add_radiobutton(label='Verdana',command=lambda:change_font('verdana'))
    menu_font.add_radiobutton(label='Calibri',command=lambda:change_font('calibri'))
    menu_font.add_radiobutton(label='Trebuchet MS',command=lambda:change_font('trebuchet_ms'))
    #
    menu_theme = tk.Menu(menu_bar,tearoff=0,fg=Themes[current_theme][2],bg=Themes[current_theme][1],activebackground=Themes[current_theme][3])
    menu_bar.add_cascade(label='Themes',menu= menu_theme)
    menu_theme.add_radiobutton(label='Default',command=lambda:change_theme(0))
    menu_theme.add_radiobutton(label='Light',command=lambda:change_theme(2))
    menu_theme.add_radiobutton(label='Dark',command=lambda:change_theme(1))
    menu_theme.add_radiobutton(label='Blue',command=lambda:change_theme(5))
    menu_theme.add_radiobutton(label='Red',command=lambda:change_theme(3))
    menu_theme.add_radiobutton(label='Green',command=lambda:change_theme(4))
    

    ###
    text = tk.Text(main,width=130,height=25)#wid = 120
    text.config(state='disabled',wrap='word',bg=Themes[current_theme][4],foreground=Themes[current_theme][5],insertbackground=Themes[current_theme][6],borderwidth=0,highlightbackground=Themes[current_theme][7],highlightcolor=Themes[current_theme][8],highlightthickness=0.9,selectbackground=Themes[current_theme][9],font=appfont)
    text.grid(row=0,column=5,columnspan=2,pady=8,padx=5)
    query_box = tk.Text(main,width =77,height=6) #width 100 layout perfect
    query_box.config(bg=Themes[current_theme][4],foreground=Themes[current_theme][5],insertbackground=Themes[current_theme][6],borderwidth=0,highlightbackground=high_bg,highlightcolor=Themes[current_theme][8],highlightthickness=0.9,selectbackground=Themes[current_theme][9],font=appfont)
    query_box.grid(row=1,column=5,padx=5,ipadx=170)
    query_btn = ctk.CTkButton(main,width=100,height=85,text='Enter',fg_color=Themes[current_theme][10],hover_color=Themes[current_theme][11],command=lambda:[query_retreive(),cursor_work(),search(),query_btn.configure(text='Enter'),query_box.delete(1.0,'end'),cursor_default()],cursor = 'hand2')
    query_btn.grid(row=1,column=6)
    query_box.focus_set()
    text_scroll = tk.Scrollbar(main,orient='vertical',command=text.yview)
    text_scroll.grid(row=0,column=7,sticky='ns')
    text.config(yscrollcommand=text_scroll.set)
    
    bold_font = font.Font(text,text.cget('font'))
    bold_font.configure(weight='bold')
    text.tag_configure('bold',font=bold_font)
    
    
    # def apply_bold():
    #     for match in re.finditer(r'\*\*(.+?)\*\*',result):
    #         start_index = match.start(1)
    #         end_index = match.end(1)
    #         start = f"1.0 + {start_index} chars"
    #         end = f"1.0 + {end_index} chars"
    #         text.tag_add('bold',start,end)
    # def BOLD():
    #     line = 0
    #     char = 0
    #     for i in range(len(result)):
    #         if result[i] == '\n':
    #             line +=1
    #             char = 0
    #         elif result[i] == '*' and result[i+1]   == '*':
    #             idx_start = i+2
    #             for j in range(i+2,len(result)):
    #                 if result[j]=='*' and result[j+1] =='*':
                        




    def change_theme(t):
        current_theme = t
        if t == 2:
            query_btn.configure(text_color = '#000000')
        else:
            query_btn.configure(text_color = '#FFFFFF')    
        main.configure(fg_color = Themes[current_theme][0])
        text.config(bg=Themes[current_theme][4],foreground=Themes[current_theme][5],insertbackground=Themes[current_theme][6],borderwidth=0,highlightbackground=Themes[current_theme][7],highlightcolor=Themes[current_theme][8],highlightthickness=0.9,selectbackground=Themes[current_theme][9],font=appfont)
        query_box.config(bg=Themes[current_theme][4],foreground=Themes[current_theme][5],insertbackground=Themes[current_theme][6],borderwidth=0,highlightbackground=high_bg,highlightcolor=Themes[current_theme][8],highlightthickness=0.9,selectbackground=Themes[current_theme][9],font=appfont)
        query_btn.configure(fg_color=Themes[current_theme][10],hover_color=Themes[current_theme][11])
        menu_file.configure(fg=Themes[current_theme][2],bg=Themes[current_theme][1],activebackground=Themes[current_theme][3])
        menu_font.configure(fg=Themes[current_theme][2],bg=Themes[current_theme][1],activebackground=Themes[current_theme][3])
        menu_theme.configure(fg=Themes[current_theme][2],bg=Themes[current_theme][1],activebackground=Themes[current_theme][3])

    def change_font(f):
        text.configure(font=f)
        query_box.configure(font=f)
    def cursor_work():
        main.config(cursor='watch')
        main.update()
    def cursor_default():
        main.config(cursor='')
        main.update()


    def mem_api():
        with open(apipath,'wb') as f:
            print("Running mem_api. model is ",model)
            pickle.dump(api + '~' + model,f)
    

    def query_retreive():
        global query
        query= query_box.get(1.0,'end-1c')
        print(len(query))##
        if query.endswith('\n'):
            print('yes')
            query = query.rstrip('\n')
        print(len(query))##
        text.config(state='normal')
        text.insert('end','>'+query+'\n\n\t')
        text.config(state='disabled')
        query_btn.configure(text='Loading')
    def search():
        global result
        try:
            response = aichat.send_message(query)
        except ResourceExhausted :
            print("RESOURCE HAS BEEN EXHAUSTED")  
            messagebox.showwarning("Quota Limit","Quota for this model has been exhausted. Please choose a different model")  
        except InvalidArgument as e:
            print("INVALID ARGUMENT ERROR OCCURED")    
            if 'API key not valid' in str(e):
                messagebox.showerror("Error","Invalid API Key")
            else:
                messagebox.showerror("Error","Invalid Arguement")  
        except NotFound:
            messagebox.showerror("Error 404",f"Invalid Model")  
        result = response.text
        text.config(state='normal')
        text.insert('end',result+'\n------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')        
        #apply_bold()
        text.config(state='disabled')
        query_btn.configure(text='Enter')
        
    def new_chat():
        query_btn.configure(text='Wait')
        text.configure(state='normal')
        text.delete(1.0,'end')
        query_box.delete(1.0,'end')
        text.configure(state='disabled')
        global aichat,aimodel
        del aichat, aimodel
        init_api()
        query_btn.configure(text='Enter')
    def listener(event=None):
        query_retreive()
        cursor_work()
        search()
        cursor_default()
        query_box.delete(1.0,'end')
        query_box.mark_set('insert','1.0')
        query_box.see('insert')
        #query_box.insert(1.0,r'')
        return "break"
    query_box.bind('<Return>',listener)    
         
    main.mainloop()
print("PRevmodel",prev_model)    
if prev_model == True:
    threading.Thread(target=init_api,daemon=True).start()
else:    
    init_api()
mainfunc()