import tkinter as tk
from tkinter import font
from tkinter import ttk
from data_from_ui import *


class DatabaseApp:
    def __init__(self, root):  # 初始化
        self.root = root
        self.root.title("資料庫")
        self.root.geometry("1200x600")

        self.username_label = None  # 第一個頁面
        self.password_label = None
        self.username_entry = None
        self.password_entry = None
        self.login_button = None
        self.register_button = None

        self.logout_button = None  # 第二個頁面
        self.database_button = None
        self.sql_button = None
        self.php_button = None
        self.database_entry = None

        self.name_entry = None
        self.column_entry = None

        # ------------------------------------其他function需要的資料
        self.col = None  # 資料表的欄位數
        self.datasheet_name = None  # 資料表名稱
        self.database_name = None  # 資料庫的名稱
        self.account_path = None  # 登入帳號的資料夾位置
        self.table_path = None  # 資料庫路徑

        self.first_ui_set()  # 設置第一個頁面

        self.content_frame = tk.Frame(self.root)  # 設置中心框架
        self.content_frame.pack(side="right", padx=60, pady=50)

        self.beside_frame = tk.Frame(self.root)  # 設置中心框架
        self.beside_frame.pack(side="left", padx=5, pady=50)

    # ----------------------------------主介面設置
    def first_ui_set(self):  # 登入畫面設置
        self.username_label = tk.Label(self.root, text="用戶名:", font=("Arial", 14), fg="blue")
        self.username_label.place(x=450, y=200)

        self.username_entry = tk.Entry(self.root)
        self.username_entry.place(x=550, y=200)

        self.password_label = tk.Label(self.root, text="密碼:", font=("Arial", 14), fg="green")
        self.password_label.place(x=450, y=250)

        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.place(x=550, y=250)

        self.login_button = tk.Button(self.root, text="登入", command=self.login)
        self.login_button.place(x=550, y=300)

        self.register_button = tk.Button(self.root, text="註冊", command=self.register)
        self.register_button.place(x=600, y=300)

    def second_ui_set(self):  # 設置主畫面
        self.first_ui_clear()  # 清理掉第一個ui
        button_width, button_height = 10, 1  # 調整按鈕大小
        custom_font = font.Font(size=12)  # 調整按鈕字體大小

        self.php_button = tk.Button(self.root, text="phpMyAdmin", font=custom_font,
                                    command=self.change_password_show)  # 設置phpMyAdmin按鈕
        self.php_button.config(width=button_width, height=button_height)
        self.php_button.place(x=0, y=0)

        self.database_button = tk.Button(self.root, text="資料庫", font=custom_font,
                                         command=self.add_data_base)  # 設置資料庫按鈕
        self.database_button.config(width=button_width, height=button_height)
        self.database_button.place(x=200, y=0)

        self.sql_button = tk.Button(self.root, text="SQL", font=custom_font, command=self.input_sql)  # 設置SQL按鈕
        self.sql_button.config(width=button_width, height=button_height)
        self.sql_button.place(x=300, y=0)

        self.logout_button = tk.Button(self.root, text="登出", command=self.logout, font=custom_font)  # 設置登出按鈕
        self.logout_button.config(width=button_width, height=button_height)
        self.logout_button.place(x=1000, y=0)

        self.change_password_show()

    def box_set(self):  # 設置側框和中間框
        self.content_frame_clear()  # 清空中間框
        self.beside_frame_clear()  # 清空側框
        center_box = tk.Label(self.content_frame, borderwidth=1, relief="solid", width=140, height=100)  # 設中框
        center_box.pack()
        beside_box = tk.Label(self.beside_frame, borderwidth=1, width=20, height=100)  # 設側框
        beside_box.pack()
        database_name_label = tk.Label(self.beside_frame, text="資料庫", font=("Arial", 14), fg="green")
        database_name_label.place(x=5, y=10)
        database_name = get_database_name(self.account_path)
        i = 1
        for name in database_name:  # 設置資料庫名稱的按鈕
            button = tk.Button(self.beside_frame, text=name, command=lambda idx=name: self.into_database(idx))
            button.place(x=3, y=10 + i * 35)
            i += 1

    # ----------------------------------按下跳轉介面的按鈕
    def login(self):  # 按下登入按鈕後
        username = self.username_entry.get()
        password = self.password_entry.get()
        if check_login(username, password):  # 帳密正確
            self.account_path = username + "/" + password  # 設置帳號路徑，之後會用到
            self.second_ui_set()

    def logout(self):  # 按下登出按钮後回到第一個畫面
        self.logout_button.place_forget()
        self.php_button.place_forget()
        self.database_button.place_forget()
        self.sql_button.place_forget()
        self.content_frame_clear()
        self.beside_frame_clear()
        self.first_ui_set()

    def change_password_show(self):  # 按下php，顯示修改密碼(frame)
        self.box_set()
        self.top1_button_show()
        change_password_label = tk.Label(self.content_frame, text="修改密碼", font=("Arial", 14), fg="blue")
        change_password_label.place(x=100, y=100)
        change_password_entry = tk.Entry(self.content_frame)
        change_password_entry.place(x=200, y=105)
        change_password_button = tk.Button(self.content_frame, text="送出")
        change_password_button.place(x=350, y=100)

    def add_data_base(self):  # 按下資料庫，顯示新增資料庫
        self.box_set()
        database_label = tk.Label(self.content_frame, text="建立新資料庫", font=("Arial", 14), fg="green")
        database_label.place(x=700, y=100)
        self.database_entry = tk.Entry(self.content_frame)
        self.database_entry.place(x=700, y=150)
        database_button = tk.Button(self.content_frame, text="建立", command=self.create_database)
        database_button.place(x=850, y=145)

        database_name = get_database_name(self.account_path)    #設置刪除資料庫
        i = 1
        for name in database_name:  # 設置刪除資料庫的按鈕
            label = tk.Label(self.content_frame,text=name, font=("Arial", 14), fg="green")
            label.place(x=50, y=10 + i * 35)
            button = tk.Button(self.content_frame, text="刪除", command=lambda idx=name: self.del_database(idx))
            button.place(x=180, y=10 + i * 35)
            i += 1

    def input_sql(self):  # 按下sql，下sql語法的介面
        self.box_set()
        sql_text = tk.Text(self.content_frame, width=125, height=28)
        sql_text.place(x=15, y=15)
        sql_button = tk.Button(self.content_frame, text="執行")
        sql_button.place(x=800, y=400)

    def into_database(self, name):  # 按下側欄資料庫的名稱按鈕後
        self.top1_button_clear()  # 清理掉上層的按鈕
        self.table_path = self.account_path + "/" + name  # 資料庫的資料夾路徑
        self.database_name = name  # 存入資料庫的名稱
        self.box_set()
        create_table_name = tk.Label(self.content_frame, text="建立資料表", font=("Arial", 14), fg="green")
        create_table_name.place(x=620, y=380)
        name_label = tk.Label(self.content_frame, text="名稱:", font=("Arial", 12))
        name_label.place(x=620, y=430)
        self.name_entry = tk.Entry(self.content_frame)
        self.name_entry.place(x=660, y=433)
        column_label = tk.Label(self.content_frame, text="欄位數:", font=("Arial", 12))
        column_label.place(x=800, y=430)
        self.column_entry = tk.Entry(self.content_frame)
        self.column_entry.place(x=860, y=433, width=50)
        input_button = tk.Button(self.content_frame, text="執行", command=self.create_datasheet)
        input_button.place(x=920, y=430)

        title_label = tk.Label(self.content_frame, text="資料表", font=("Arial", 12), fg="blue")
        title_label.place(x=25, y=5)
        all_datasheet = get_datasheet_name(self.table_path)  # 讀取全部"資料表"的名稱
        i = 0
        button_width, button_height = 10, 1  # 調整按鈕大小
        for datasheet in all_datasheet:  # 設置資料表的按鈕
            datasheet_button = tk.Button(self.content_frame, text=datasheet,  # 資料表名稱按鈕
                                         command=lambda idx=datasheet: self.browse_datasheet(idx)
                                         , width=button_width, height=button_height)
            datasheet_button.place(x=15, y=30 + i * 30)
            struct_button = tk.Button(self.content_frame, text="結構",  # 結構按鈕
                                      command=lambda idx=datasheet: self.struct_datasheet(idx)
                                      , width=5, height=button_height)
            struct_button.place(x=95, y=30 + i * 30)
            search_button = tk.Button(self.content_frame, text="搜尋",  # 結構按鈕
                                      command=lambda idx=datasheet: self.struct_datasheet(idx)
                                      , width=5, height=button_height)
            search_button.place(x=145, y=30 + i * 30)
            add_button = tk.Button(self.content_frame, text="新增",  # 新增按鈕
                                   command=lambda idx=datasheet: self.add_datasheet(idx)
                                   , width=5, height=button_height)
            add_button.place(x=195, y=30 + i * 30)
            del_button = tk.Button(self.content_frame, text="刪除",  # 刪除按鈕
                                   command=lambda idx=datasheet: self.add_datasheet(idx)
                                   , width=5, height=button_height)
            del_button.place(x=245, y=30 + i * 30)

            i += 1

    def create_datasheet(self):  # 按下執行建立資料表的按鈕後
        self.datasheet_name = self.name_entry.get()  # 資料表名稱
        self.col = self.column_entry.get()  # 欄位數
        try:
            col = int(self.col)
            if os.path.exists(self.table_path + "/" + self.datasheet_name + ".csv"):  # 檢查會不會重複
                messagebox.showerror("Error", "此資料表已存在")
            else:
                self.box_set()
                label_1 = tk.Label(self.content_frame, text="名稱", font=("Arial", 12))
                label_1.place(x=10, y=15)
                label_2 = tk.Label(self.content_frame, text="型態", font=("Arial", 12))
                label_2.place(x=170, y=15)
                label_3 = tk.Label(self.content_frame, text="長度", font=("Arial", 12))
                label_3.place(x=340, y=15)
                for i in range(col):
                    name_entry = tk.Entry(self.content_frame)
                    name_entry.place(x=10, y=40 + i * 25)

                    options = ["INT", "DOUBLE", "VARCHAR"]
                    selected_option = tk.StringVar()
                    combobox = ttk.Combobox(self.content_frame, textvariable=selected_option, values=options)
                    combobox.place(x=170, y=40 + i * 25)

                    len_entry = tk.Entry(self.content_frame)
                    len_entry.place(x=340, y=40 + i * 25)

                    setattr(self, f'name_entry_{i}', name_entry)
                    setattr(self, f'len_entry_{i}', len_entry)
                    setattr(self, f'combobox_{i}', combobox)
                save_button = tk.Button(self.content_frame, text="儲存", command=self.txt_structure)
                save_button.place(x=800, y=200)

        except ValueError:
            messagebox.showerror("Error", "欄位數要輸入數字")

    def txt_structure(self):  # 按下儲存後，儲存資料表的欄位名稱，type，長度
        col = self.col  # 欄位數
        name = self.datasheet_name  # 資料表的名稱
        path = self.table_path + "/" + name + ".txt"
        create_datasheet(self.table_path, name)  # 新增資料表，建立一個txt
        flag = True
        name_arr = []  # 存進csv檔的第一列
        for i in range(int(col)):
            name_value = getattr(self, f'name_entry_{i}').get()
            type_value = getattr(self, f'combobox_{i}').get()
            len_value = getattr(self, f'len_entry_{i}').get()
            if check_same_name(path, name_value):  # 沒有重複的欄位名稱
                with open(path, 'a') as file:  # 把結構寫入txt
                    file.write(name_value + ":" + type_value + ":" + len_value)
                    name_arr.append(name_value)
                    file.write("\n")
            else:  # 有重複的欄位名稱
                with open(path, 'w'):
                    pass
                flag = False
                break
        if flag:
            with open(self.table_path + "/" + name + ".csv", 'w', newline='') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(name_arr)
            self.into_database(self.database_name)  # 更新

    def browse_datasheet(self, name):  # 按下資料表的名稱後
        path = self.table_path + "/" + name + ".txt"
        self.datasheet_name = name
        print(name)

    def struct_datasheet(self, name):  # 按下結構按鈕後
        path = self.table_path + "/" + name + ".txt"
        self.datasheet_name = name
        print(name)

    def add_datasheet(self, name):  # 按下新增按鈕後
        path = self.table_path + "/" + name + ".txt"  # 更新資料
        self.datasheet_name = name
        self.box_set()
        label_1 = tk.Label(self.content_frame, text="欄位", font=("Arial", 12))
        label_1.place(x=10, y=10)
        label_2 = tk.Label(self.content_frame, text="型態", font=("Arial", 12))
        label_2.place(x=80, y=10)
        label_3 = tk.Label(self.content_frame, text="值", font=("Arial", 12))
        label_3.place(x=160, y=10)
        with open(path, 'r') as file:
            lines = file.readlines()
        i = 0
        for line in lines:
            i += 1
            result = line.split(':')
            col_1 = tk.Label(self.content_frame, text=result[0])
            col_1.place(x=10, y=10 + i * 25)
            col_2 = tk.Label(self.content_frame, text=result[1] + ":" + result[2])
            col_2.place(x=80, y=10 + i * 25)
            col_3 = tk.Entry(self.content_frame)
            col_3.place(x=160, y=10 + i * 25)
            setattr(self, f'value_entry_{i}', col_3)
        self.col = i
        append_button = tk.Button(self.content_frame, text="新增", command=self.append_value)
        append_button.place(x=500, y=10 + i * 25)

    def append_value(self):  # 新增資料至csv
        path = self.table_path + "/" + self.datasheet_name + ".csv"
        value_arr = []
        for i in range(1, int(self.col) + 1):
            value_arr.append(getattr(self, f'value_entry_{i}').get())
        with open(path, 'a', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(value_arr)
        messagebox.showinfo("OK", "新增成功")

    def del_datasheet(self, name):  # 按下刪除按鈕後
        path = self.table_path + "/" + name + ".txt"
        self.datasheet_name = name
        print(name)

    # ----------------------------------按下非跳轉介面的按鈕

    def register(self):  # 按下註冊按鈕後
        registered_username = self.username_entry.get()
        registered_password = self.password_entry.get()
        create_account(registered_username, registered_password)  # 註冊帳號

    def create_database(self):  # 按下新增資料庫按鈕後
        table_name = self.database_entry.get()
        if len(table_name) > 0:
            create_table(self.account_path, table_name)
            self.add_data_base()
        else:
            messagebox.showerror("ERROR", "請輸入資料庫名稱")
    
    def del_database(self,name):    #按下刪除資料庫後
        path=self.account_path+"/"+name
        del_file(path)
        self.add_data_base()

    # ----------------------------------隱藏畫面或恢復畫面的function
    def content_frame_clear(self):  # 清空整個content_frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def beside_frame_clear(self):  # 清空整個beside_frame
        for widget in self.beside_frame.winfo_children():
            widget.destroy()

    def first_ui_clear(self):  # 登入畫面隱藏
        self.username_label.place_forget()
        self.password_label.place_forget()
        self.username_entry.place_forget()
        self.password_entry.place_forget()
        self.login_button.place_forget()
        self.register_button.place_forget()

    def top1_button_clear(self):  # 第一種上方按鈕隱藏
        self.database_button.place_forget()
        self.sql_button.place_forget()
        self.logout_button.place_forget()

    def top1_button_show(self):  # 第一種上方按鈕隱藏顯示
        self.database_button.place(x=200, y=0)
        self.sql_button.place(x=300, y=0)
        self.logout_button.place(x=1000, y=0)


if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()
