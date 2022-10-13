from sqlite3.dbapi2 import connect
from tkinter import *
from tkinter import messagebox
from db import DB


##### GUI #####
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
        self.current_user = None
        self.current_page = 0
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
                    self.hidden_data(name)
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

    def hidden_data(self, name):
        db = DB()
        db.cursor.execute(f'''SELECT * FROM userinfo WHERE uname='{name}' ''')
        self.data = db.cursor.fetchall()
        self.pages = self.split_page(self.data)
        self.canvas.destroy()
        self.login_button.destroy()
        self.register_button.destroy()

        self.header_frame = Frame(self.root)
        self.header_frame.pack(pady=20)

        self.username_label = Label(
            self.header_frame, text=f'Current user is {name}', font=('Courage', 14, 'bold'))
        self.username_label.grid(column=0, row=3, columnspan=3, pady=(20, 0))
        self.add_button = Button(self.header_frame, text='Add Password',
                                 command=lambda: self.add_pass(name))
        self.add_button.grid(column=1, row=0)

        self.exit_button = Button(
            self.header_frame, text='Sign Out', command=self.root.destroy)
        self.exit_button.grid(
            column=2, row=0)

        self.main_frame = Frame(self.root, relief=RAISED)
        self.main_frame.pack(pady=45)
        for user_data in self.pages[self.current_page]:
            inner_frame = Frame(self.main_frame, relief=RAISED)
            inner_frame.pack(pady=(0, 10))
            item = Label(inner_frame, bg='white',
                         text=user_data[1], font=('Arial', 15), width=30)
            item.grid(column=0, row=1)

            item2 = Label(inner_frame, bg='white',
                          text=user_data[2], font=('Arial', 15), width=30)
            item2.grid(column=1, row=1)

            item3 = Label(inner_frame, bg='white',
                          text=user_data[3], font=('Arial', 15), width=30)
            item3.grid(column=2, row=1)

        control_frame = Frame(self.root, relief=RAISED)
        control_frame.place(x=0, y=610)
        page_number = Label(
            control_frame, text=f'{self.current_page+1}/{len(self.pages)}')
        page_number.pack()

        next_page = Button(control_frame, text='→',
                           command=lambda: self.refresh(name, +1))
        next_page.pack(side=RIGHT, padx=(0, 600))

        back_page = Button(control_frame, text='←',
                           command=lambda: self.refresh(name, -1))
        back_page.pack(side=LEFT, padx=(600, 0))

    def add_pass(self, name):
        pop_up = Toplevel(self.root)
        pop_up.title('Add Password')

        frame1 = Frame(pop_up)
        frame1.pack(fill=X, pady=(30, 20))

        email_l = Label(frame1, text="Email: ", width=15)
        email_l.pack(side=LEFT)

        email_e = Entry(frame1)
        email_e.pack(fill=X, expand=True, padx=(0, 80))

        frame2 = Frame(pop_up)
        frame2.pack(fill=X, pady=(0, 20))

        site_l = Label(frame2, text="Site: ", width=15)
        site_l.pack(side=LEFT)

        site_e = Entry(frame2)
        site_e.pack(fill=X, expand=True, padx=(0, 80))

        frame3 = Frame(pop_up)
        frame3.pack(fill=X, pady=(0, 30))

        passwd_l = Label(frame3, text='Password: ', width=15)
        passwd_l.pack(side=LEFT)

        passwd_e = Entry(frame3, show='*')
        passwd_e.pack(fill=X, expand=True, padx=(0, 80))

        add_button = Button(pop_up, text='Add Password',
                            command=lambda: self.add_refresh_page(name, email_e.get(), site_e.get(), passwd_e.get(), pop_up))
        add_button.pack(pady=(0, 30))

    def add_refresh_page(self, name, email, site, passwd, pop_up):
        db = DB()
        db.cursor.execute(
            f'''INSERT INTO userinfo VALUES ('{name}', '{email}', '{site}', '{passwd}')''')
        db.connection.commit()
        pop_up.destroy()
        self.main_frame.destroy()
        self.header_frame.destroy()
        self.hidden_data(name)

    def split_page(self, data):
        pages = []
        page = []
        for i in range(1, len(data)+1):
            page.append(data[i-1])
            if i % 8 == 0:
                pages.append(page)
                page = []

        if page != []:
            pages.append(page)
        return pages

    def refresh(self, name, page_number):
        self.current_page += page_number

        if self.current_page < 0:
            self.current_page = len(self.pages) - 1
        elif self.current_page >= len(self.pages):
            self.current_page = 0

        self.main_frame.destroy()
        self.header_frame.destroy()
        self.hidden_data(name)


a = Home()
