import os
import csv
import shutil
from tkinter import messagebox


def create_account(username, password):  # 註冊帳號
    account = username
    path = username + "/" + password
    if os.path.exists(account):  # 如果帳號存在的話
        messagebox.showerror("Error", "帳號已存在")
    else:  # 不存在就建立資料夾
        os.makedirs(path)
        messagebox.showinfo("OK", "註冊成功")


def check_login(username, password):  # 檢查登入的帳密是否正確
    account = username
    path = username + "/" + password
    if os.path.exists(account):  # 如果帳號存在的話，檢查密碼
        if os.path.exists(path):
            return True
        else:
            messagebox.showerror("Error", "密碼錯誤")
            return False
    else:
        messagebox.showerror("Error", "帳號不存在")
        return False


def create_table(path, name):  # 創建資料庫
    table_path = path + "/" + name
    if os.path.exists(table_path):
        messagebox.showerror("Error", "資料庫已存在")
    else:
        os.makedirs(table_path)  # 創建資料庫的資料夾


def create_datasheet(path, name):  # 建立一個空的txt
    with open(path + "/" + name + ".txt", 'w', newline=''):
        pass


def get_database_name(path):  # 讀取資料庫的名稱
    try:
        all_entries = os.listdir(path)
        return all_entries
    except OSError as e:
        return []


def get_datasheet_name(path):
    try:
        all_entries = os.listdir(path)
        csv_entries = [entry[:-4] for entry in all_entries if entry.endswith(".csv")]
        return csv_entries
    except OSError as e:
        return []


def check_same_name(path, name):
    flag = True
    with open(path, 'r') as file:
        lines = file.readlines()
    for line in lines:
        result = line.split(':')
        if name == result[0]:
            messagebox.showerror("Error", "欄位名稱重複")
            flag = False
            break
        else:
            flag = True
    if flag:
        return True
    else:
        return False
    
def del_file(path):
    try:
        shutil.rmtree(path)
        messagebox.showinfo("OK","刪除成功")
    except OSError as e:
        messagebox.showinfo("ERROR","刪除失敗")



