import tkinter
from tkinter import ttk 
from tkinter import messagebox
from users import *
from products import *
from tkinter import filedialog

import setting

def btn_login():
    global current_user,session
    user=txt_user.get()
    pas=txt_pass.get()
    result=current_user.login(user,pas)
    if not result:
        lbl_msg.configure(text="wrong username or password!",fg="red")
    else:
        
        lbl_msg.configure(text=f"welcome {result[1]}" , fg='green')
        btn_login1.configure(state="disabled")
        btn_logout1.configure(state="active")
        
        dic_acces=current_user.get_user_acces(result[5])
        btn_setting1.configure(state=dic_acces["setting"])
        btn_shop1.configure(state=dic_acces["shop"])
        btn_cart1.configure(state=dic_acces["shop"])
        btn_admin1.configure(state=dic_acces["adminpanel"])
        btn_delete1.configure(state=dic_acces["del"])
        btn_submit1.configure(state=dic_acces["submith"])

        if user=="admin":
            btn_delete1.configure(state="disabled")

        txt_user.delete(0,"end")
        txt_pass.delete(0,"end")
        session=user
        
def btn_submit():
    # --------------------------
    def signup():
        global current_user
        user=txt_user.get()
        pas=txt_pass.get()
        cpas=txt_cpass.get()
        name=txt_name.get()
        addr=txt_addr.get()
        acceslvl=txt_acces.get()
        
        result,msg=current_user.submit(user,pas,cpas,name,addr,acceslvl)
        if not result:
            lbl_msg.configure(text=msg,fg="red")
        else:
            lbl_msg.configure(text=msg,fg="green")
            txt_user.delete(0,"end")
            txt_pass.delete(0,"end")
            txt_cpass.delete(0,"end")
            txt_name.delete(0,"end")
            txt_addr.delete(0,"end")
            txt_acces.delete(0,"end")
    # -----------------------
    
    submit_win=tkinter.Toplevel(win)
    submit_win.geometry("300x400")  
    submit_win.title("submit")
    lbl_user=tkinter.Label(submit_win,text="username:")
    lbl_user.pack()
    
    txt_user=tkinter.Entry(submit_win,width=20)
    txt_user.pack()
    
    lbl_pass=tkinter.Label(submit_win,text="password:")
    lbl_pass.pack()
    
    txt_pass=tkinter.Entry(submit_win,width=20)
    txt_pass.pack()
    
    lbl_cpass=tkinter.Label(submit_win,text="password confirm:")
    lbl_cpass.pack()
    
    txt_cpass=tkinter.Entry(submit_win,width=20)
    txt_cpass.pack()
    
    lbl_name=tkinter.Label(submit_win,text="name:")
    lbl_name.pack()
    
    txt_name=tkinter.Entry(submit_win,width=20)
    txt_name.pack()
    
    lbl_addr=tkinter.Label(submit_win,text="address:")
    lbl_addr.pack()
    
    txt_addr=tkinter.Entry(submit_win,width=20)
    txt_addr.pack()
    
    lbl_acces=tkinter.Label(submit_win,text="Access lvel (a,b,c,d):")
    lbl_acces.pack()

    txt_acces=tkinter.Entry(submit_win,width=20)
    txt_acces.pack()

    lbl_msg=tkinter.Label(submit_win,text="")
    lbl_msg.pack()
    
    btn_signup=tkinter.Button(submit_win,text="submit",command=signup)
    btn_signup.pack()
    
    
    submit_win.mainloop()

def btn_delete():
    confirm=messagebox.askyesno("message","are you sure?")
    if confirm:
        global session
        result=current_user.deleteUser(session)
        if result:
            lbl_msg.configure(text="your account has been deleted!",fg="green")
            session=""
            btn_login.configure(state="active")
            btn_delete.configure(state="disabled")
        else:
            lbl_msg.configure(text="something went wrong",fg="red") 
    
def btn_logout():
    global session
    session=""
    btn_cart1.configure(state="disabled")
    btn_logout1.configure(state="disabled")
    btn_login1.configure(state="active")
    btn_delete1.configure(state="disabled")
    btn_admin1.configure(state="disable")
    btn_shop1.configure(state="disabled")
    btn_setting1.configure(state="disabled")
    
    lbl_msg.configure(text="")

def btn_admin():
    def btn_psave():
        global current_product
        pname=txt_pname.get()
        qnt=txt_qnt.get()
        price=txt_price.get()
        if pname=="" or qnt=="" or price=="":
             lbl_pmsg.configure(text="please fill the inputs",fg="red")
             return
        result=current_product.save_product(pname,qnt,price)
        if result:
            lbl_pmsg.configure(text="ptoduct saved to database!",fg="green")
            txt_pname.delete(0,"end")
            txt_qnt.delete(0,"end")
            txt_price.delete(0,"end")
        else:
            lbl_pmsg.configure(text="something went wrong!",fg="red")
        
            
    win_btn=tkinter.Toplevel(win)
    win_btn.geometry("300x400")
    win_btn.title("Admin Panel")
    
    lbl_pname=tkinter.Label(win_btn,text="product name:")
    lbl_pname.pack()
    
    txt_pname=tkinter.Entry(win_btn,width=20)
    txt_pname.pack()
    
    lbl_qnt=tkinter.Label(win_btn,text="Quantity:")
    lbl_qnt.pack()
    
    txt_qnt=tkinter.Entry(win_btn,width=20)
    txt_qnt.pack()
    
    lbl_price=tkinter.Label(win_btn,text="Price:")
    lbl_price.pack()
    
    txt_price=tkinter.Entry(win_btn,width=20)
    txt_price.pack()
    
    lbl_pmsg=tkinter.Label(win_btn,text="")
    lbl_pmsg.pack()
    
    btn_psave=tkinter.Button(win_btn,text="save",command=btn_psave)
    btn_psave.pack()

    win_btn.mainloop()    

def btn_shop():
    def refresh_list_box():
        global plist
        plist=current_product.products_list()
        for product in plist:
            text=f"id:{product[0]} , Name:{product[1]} , QNT:{product[2]} , price:{product[3]}"
            lstbox.insert(0,text)

    def final_shop():
        global plist
        pid=int(pid_text.get())
        qnt=int(pqnt_text.get())
        is_id_exist=False
        for product in plist:
            if product[0]==pid:
                is_id_exist=True
                pqnt=product[2]
        if not is_id_exist:
            lbl_msg.configure(text="worng product id",fg="red")
            return
        if int(qnt)>pqnt:
            lbl_msg.configure(text="not enough product",fg="red")
            return
        result=current_product.save_to_cart(pid,qnt,session)
        if result:
            lbl_msg.configure(text="saved to cart",fg="green")
            pid_text.delete(0,"end")
            pqnt_text.delete(0,"end")
            lstbox.delete(0,"end")
            refresh_list_box()
            
        else:
            lbl_msg.configure(text="somthing went wrong",fg="red")

    global plist
    win_shop=tkinter.Toplevel(win)
    
    win_shop.geometry("300x300")
    win_shop.title("shop")
    
   
    lstbox=tkinter.Listbox(win_shop,width=70)
    lstbox.pack()
    
    refresh_list_box()
        
    
    lbl_pid=tkinter.Label(win_shop,text="product ID:")
    lbl_pid.pack()
    
    pid_text=tkinter.Entry(win_shop)
    pid_text.pack()
    
    lbl_pqnt=tkinter.Label(win_shop,text="quantity:")
    lbl_pqnt.pack()
    
    pqnt_text=tkinter.Entry(win_shop)
    pqnt_text.pack()
    
    btn_final_shop=tkinter.Button(win_shop,text="finalize shop",command=final_shop)
    btn_final_shop.pack()
    
    lbl_msg=tkinter.Label(win_shop,text="")
    lbl_msg.pack()

    win_shop.mainloop()

def btn_cart():
    win_cart=tkinter.Toplevel(win)
    win_cart.title("Cart")
    win_cart.geometry("400x300")

    lstbox=tkinter.Listbox(win_cart,width=70)
    lstbox.pack()
    cart_list = current_product.get_from_cart(session)

    for product in cart_list:
        text=f"Name : {product[0]} , Price : {product[1]} , QNT : {product[2]} , Total price : {product[1]*product[2]}"
        lstbox.insert(0,text)


    win_cart.mainloop()

def btn_setting():
    def btn_select_path():
        file_path = filedialog.askdirectory()
        if file_path != "":
            file_path=file_path.replace('\\','/')
            l14.configure(text=f"{file_path}/Shop.db")

    def btn_defult():
        result=messagebox.askyesno("Defult setting","Are you sure to defult setting ?")
        if result:
            setting.write_defullt_setting()
            messagebox.showinfo("defult Setting","Please close program and run agane")

    def btn_save():
        if txt_form_color.get()=="" or txt_btn_color.get()=="" or txt_btn_txtcolor.get()=="" or txt_btn_fontname.get()=="" or txt_btn_fontsize.get()=="" or txt_txt_color.get()=="" or txt_txt_txtcolor.get()=="" or txt_txt_fontname.get()=="" or txt_txt_fontsize.get()=="" or txt_lbl_color.get()=="" or txt_lbl_txtcolor.get()=="" or txt_lbl_fontname.get()=="" or txt_lbl_fontsize.get()=="" :
            messagebox.showerror("Error","Please complete all requested values !")
            return
        result=messagebox.askyesno("Save setting","Are you sure to save setting ?")
        if result:
            list_form=setting.get_Stile('form')
            list_form["background"]=txt_form_color.get()
            list_button=setting.get_Stile('button')
            list_button["background"]=txt_btn_color.get()
            list_button["foreground"]=txt_btn_txtcolor.get()
            list_button["font"]=[txt_btn_fontname.get(),int(txt_btn_fontsize.get())]
            list_entry=setting.get_Stile('entry')
            list_entry["background"]=txt_txt_color.get()
            list_entry["foreground"]=txt_txt_txtcolor.get()
            list_entry["font"]=[txt_txt_fontname.get(),int(txt_txt_fontsize.get())]
            list_label=setting.get_Stile('label')
            list_label["background"]=txt_lbl_color.get()
            list_label["foreground"]=txt_lbl_txtcolor.get()
            list_label["font"]=[txt_lbl_fontname.get(),int(txt_lbl_fontsize.get())]
            list_path=setting.get_Stile('path')
            list_path["dbpath"]=l14.cget("text")
            setting.set_Stile({"form":list_form,'button':list_button,'entry':list_entry,'label':list_label,'path':list_path})
            messagebox.showinfo("defult Setting","Please close program and run agane")

    global setting
    win_setting=tkinter.Toplevel(win)
    win_setting.title("Setting")
    win_setting.geometry("450x550+300+200")
# ----------------------------------------Form--------------------
    frame_form=ttk.LabelFrame(win_setting,text="Forms setting",height=100,width=280)
    frame_form.pack()
    frame_form.config(padding=(10,10))

    lbl_form=ttk.Label(frame_form,text=f"Color : ")
    lbl_form.grid(row=0,column=0)
    txt_form_color=ttk.Entry(frame_form)
    txt_form_color.grid(row=0,column=1)
    txt_form_color.insert(0,setting.get_Stile('form')['background'])

# ----------------------------------------Button--------------------
    # tkinter.Label(win_setting).grid(row=2,column=0)
    frame_btn=ttk.LabelFrame(win_setting,text="Button setting",height=100,width=280)
    frame_btn.pack()
    frame_btn.config(padding=(10,10))

    l1=ttk.Label(frame_btn,text=f"Button color : ")
    l1.grid(row=0,column=0)

    txt_btn_color=ttk.Entry(frame_btn)
    txt_btn_color.grid(row=0,column=1)
    txt_btn_color.insert(0,setting.get_Stile('button')['background'])

    l2=ttk.Label(frame_btn,text=f"Text color : ")
    l2.grid(row=1,column=0)

    txt_btn_txtcolor=ttk.Entry(frame_btn)
    txt_btn_txtcolor.grid(row=1,column=1)
    txt_btn_txtcolor.insert(0,setting.get_Stile('button')['foreground'])

    l3=ttk.Label(frame_btn,text=f"Font name : ")
    l3.grid(row=2,column=0)

    txt_btn_fontname=ttk.Entry(frame_btn)
    txt_btn_fontname.grid(row=2,column=1)
    txt_btn_fontname.insert(0,setting.get_Stile('button')['font'][0])

    l4=ttk.Label(frame_btn,text=f"Font size : ")
    l4.grid(row=3,column=0)

    txt_btn_fontsize=ttk.Entry(frame_btn)
    txt_btn_fontsize.grid(row=3,column=1)
    txt_btn_fontsize.insert(0,setting.get_Stile('button')['font'][1])

 # ----------------------------------------Text--------------------
    frame_text=ttk.LabelFrame(win_setting,text="Text View setting",height=1,width=1)
    frame_text.pack()
    frame_text.config(padding=(10,10))

    l8=ttk.Label(frame_text,text=f"color : ")
    l8.grid(row=0,column=0)

    txt_txt_color=ttk.Entry(frame_text)
    txt_txt_color.grid(row=0,column=1)
    txt_txt_color.insert(0,setting.get_Stile('label')['background'])
    
    l5=ttk.Label(frame_text,text=f"Text color : ")
    l5.grid(row=0,column=0)

    txt_txt_txtcolor=ttk.Entry(frame_text)
    txt_txt_txtcolor.grid(row=0,column=1)
    txt_txt_txtcolor.insert(0,setting.get_Stile('label')['foreground'])

    l6=ttk.Label(frame_text,text=f"Font name : ")
    l6.grid(row=1,column=0)

    txt_txt_fontname=ttk.Entry(frame_text)
    txt_txt_fontname.grid(row=1,column=1)
    txt_txt_fontname.insert(0,setting.get_Stile('label')['font'][0])

    l7=ttk.Label(frame_text,text=f"Font size : ")
    l7.grid(row=2,column=0)

    txt_txt_fontsize=ttk.Entry(frame_text)
    txt_txt_fontsize.grid(row=2,column=1)   
    txt_txt_fontsize.insert(0,setting.get_Stile('label')['font'][1])

 # ----------------------------------------Label--------------------
    frame_label=ttk.LabelFrame(win_setting,text="Lable View setting",height=1,width=1)
    frame_label.pack()
    frame_label.config(padding=(10,10))

    l9=ttk.Label(frame_label,text=f"color : ")
    l9.grid(row=0,column=0)

    txt_lbl_color=ttk.Entry(frame_label)
    txt_lbl_color.grid(row=0,column=1)
    txt_lbl_color.insert(0,setting.get_Stile('label')['background'])

    l10=ttk.Label(frame_label,text=f"Text color : ")
    l10.grid(row=0,column=0)

    txt_lbl_txtcolor=ttk.Entry(frame_label)
    txt_lbl_txtcolor.grid(row=0,column=1)
    txt_lbl_txtcolor.insert(0,setting.get_Stile('label')['foreground'])

    l11=ttk.Label(frame_label,text=f"Font name : ")
    l11.grid(row=1,column=0)

    txt_lbl_fontname=ttk.Entry(frame_label)
    txt_lbl_fontname.grid(row=1,column=1)
    txt_lbl_fontname.insert(0,setting.get_Stile('label')['font'][0])

    l12=ttk.Label(frame_label,text=f"Font size : ")
    l12.grid(row=2,column=0)

    txt_lbl_fontsize=ttk.Entry(frame_label)
    txt_lbl_fontsize.grid(row=2,column=1)   
    txt_lbl_fontsize.insert(0,setting.get_Stile('label')['font'][1])

    l13=ttk.Label(frame_label,text=f"Font size : ")
    l13.grid(row=2,column=0)

 # ----------------------------------------DB Path--------------------
    frame_path=ttk.LabelFrame(win_setting,text="Setting file path",height=1,width=1)
    frame_path.pack()
    frame_path.config(padding=(10,10))
    
    l14=ttk.Label(frame_path,text=f"{setting.get_Stile('path')['dbpath']}")
    l14.pack()
    btn_path=ttk.Button(frame_path,text="Select path DB",command=btn_select_path)
    btn_path.pack()

# ----------------------------------------save btn--------------------
    btn_defult1=ttk.Button(win_setting,text="Defullt",command=btn_defult)
    btn_defult1.pack_configure(side="left",fill="x",ipadx=20,padx=10)
    btn_save1=ttk.Button(win_setting,text="Save",command=btn_save)
    btn_save1.pack_configure(side="left",fill="x",ipadx=20,padx=10)



    win_setting.mainloop()

if __name__=="__main__":
    
    current_user=users()
    current_product=products()
    session=""

    setting=setting.Setting()

    win=tkinter.Tk()
    win.title("login")
    win.geometry("280x380+550+200")
    win.resizable(False,False)
    win.configure(setting.get_Stile("form")) 
    
    # ------------------login widgets------------
    lbl_user=tkinter.Label(win,text="username:")
    lbl_user.pack()
    lbl_user.configure(setting.get_Stile("label")) 

    txt_user=tkinter.Entry(win,width=20)
    txt_user.pack()
    txt_user.configure(setting.get_Stile("entry")) 
    
    lbl_pass=tkinter.Label(win,text="password:")
    lbl_pass.pack()
    lbl_pass.configure(setting.get_Stile("label")) 
    
    txt_pass=tkinter.Entry(win,width=20)
    txt_pass.pack()
    txt_pass.configure(setting.get_Stile("entry")) 

    lbl_msg=tkinter.Label(win,text="")
    lbl_msg.pack()
    lbl_msg.configure(setting.get_Stile("label"))
    
    btn_login1=tkinter.Button(win,text="login",command=btn_login)
    btn_login1.pack()
    btn_login1.configure(setting.get_Stile("button"))
    
    btn_submit1=tkinter.Button(win,text="submit",command=btn_submit)
    btn_submit1.pack()
    btn_submit1.configure(setting.get_Stile("button"))

    btn_delete1=tkinter.Button(win,text="delete",command=btn_delete,state="disabled")
    btn_delete1.pack()
    btn_delete1.configure(setting.get_Stile("button"))
    
    btn_logout1=tkinter.Button(win,text="logout",command=btn_logout,state="disabled")
    btn_logout1.pack()
    btn_logout1.configure(setting.get_Stile("button"))

    btn_admin1=tkinter.Button(win,text="admin panel",command=btn_admin,state="disabled")
    btn_admin1.pack()
    btn_admin1.configure(setting.get_Stile("button"))

    btn_shop1=tkinter.Button(win,text="shop",command=btn_shop,state="disabled")
    btn_shop1.pack()
    btn_shop1.configure(setting.get_Stile("button"))

    btn_cart1=tkinter.Button(win,text="My Cart",command=btn_cart,state="disabled")
    btn_cart1.pack()
    btn_cart1.configure(setting.get_Stile("button"))
   
    btn_setting1=tkinter.Button(win,text="Setting",command=btn_setting,state="disabled")
    btn_setting1.pack()
    btn_setting1.configure(setting.get_Stile("button")) 

    
    tkinter.mainloop()