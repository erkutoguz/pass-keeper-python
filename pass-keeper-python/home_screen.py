from tkinter import *
from tkinter import messagebox
from db import DB


class Home:
    def __init__(self):
        self.root = Tk()
        self.root.title('PassKeeper')
        self.root.geometry('1280x720')

        lock_img = PhotoImage(file='img/lock.png')
        self.canvas = Canvas(width=300, height=400)
        self.canvas.create_image(150, 200, image=lock_img)
        self.canvas.pack()

        self.login_button = Button(
            text='Login', width=15, font=('Trebuchet MS', 25), fg='white',
            bg='#4191b9', activebackground='#4191b9',
            activeforeground='white', command=self.login)
        self.login_button.pack(pady=20)

        self.register_button = Button(
            text='Register', width=15, font=('Trebuchet MS', 25), fg='white',
            bg='#4191b9', activebackground='#4191b9', activeforeground='white',
            command=self.register)
        self.register_button.pack()

        self.root.mainloop()

    def login(self):
        login_screen = Toplevel(self.root)
        login_screen.geometry('400x200')
        login_screen.title('Login')
        frame1 = Frame(login_screen)
        frame1.pack(fill=X, pady=(30, 20))

        name_l = Label(frame1, text="Name: ", width=15)
        name_l.pack(side=LEFT)

        name_e = Entry(frame1)
        name_e.pack(fill=X, expand=True, padx=(0, 80))

        frame2 = Frame(login_screen)
        frame2.pack(fill=X, pady=(0, 30))

        passwd_l = Label(frame2, text="Password: ", width=15)
        passwd_l.pack(side=LEFT)

        passwd_e = Entry(frame2, show='*')
        passwd_e.pack(fill=X, expand=True, padx=(0, 80))

        login_button = Button(login_screen, text='Login',
                              command=lambda: self.check_login_info(name_e.get(), passwd_e.get(), login_screen))
        login_button.pack()

    def register(self):
        reg_screen = Toplevel(self.root)
        reg_screen.title('Register')
        reg_screen.geometry('400x200')

        frame1 = Frame(reg_screen)
        frame1.pack(fill=X, pady=(30, 20))

        name_l = Label(frame1, text="Name: ", width=15)
        name_l.pack(side=LEFT)

        name_e = Entry(frame1)
        name_e.pack(fill=X, expand=True, padx=(0, 80))

        frame2 = Frame(reg_screen)
        frame2.pack(fill=X, pady=(0, 30))

        passwd_l = Label(frame2, text="Password: ", width=15)
        passwd_l.pack(side=LEFT)

        passwd_e = Entry(frame2, show='*')
        passwd_e.pack(fill=X, expand=True, padx=(0, 80))

        reg_button = Button(reg_screen, text='Register', command=lambda: self.register_user(
            name_e.get(), passwd_e.get(), reg_screen))
        reg_button.pack()

    def check_login_info(self, name, passwd, top_lvl):
        db = DB()
        db.cursor.execute(f'''SELECT * FROM logininfo WHERE name='{name}' ''')
        data = db.cursor.fetchone()
        db.close_db()
        if name != '' and passwd != '':
            if data:
                if passwd == data[1]:
                    top_lvl.destroy()
                    # After login configure home page's labels
            else:
                messagebox.showerror('Warning', 'Name or password is wrong.')

        else:
            if name == '' and passwd == '':
                messagebox.showerror('Warning', 'You have to fill the blanks.')
            else:
                messagebox.showerror('Warning', 'You have to fill the blank.')

    def register_user(self, name, passwd, top_lvl):
        db = DB()
        is_user_exist = False
        db.cursor.execute('''SELECT name from logininfo''')
        for user_name in db.cursor.fetchall():
            if name == user_name[0]:
                is_user_exist = True

        if name != '' and passwd != '':
            if not is_user_exist:
                db.cursor.execute(
                    f'''INSERT INTO logininfo VALUES ('{name}', '{passwd}')''')
                db.connection.commit()
                db.close_db()
                top_lvl.destroy()
                # After registration configure home page's labels
            else:
                messagebox.showerror('Warning', 'Username is taken.')

        else:
            if name == '' and passwd == '':
                messagebox.showerror('Warning', 'You have to fill the blanks.')
            else:
                messagebox.showerror('Warning', 'You have to fill the blank.')
