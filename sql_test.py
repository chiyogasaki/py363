#-*- coding: utf-8 -*-

import sqlite3
import tkinter as tk
import tkinter.ttk as ttk


#空のデータベースを作成して接続
dbname = "database.db"
c = sqlite3.connect(dbname)
c.execute("PRAGMA foreign_keys = 1")

try:
    
    ##支出データのテーブル作成
    c.execute('''CREATE TABLE cost_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date DATE NOT NULL,
                        item_name TEXT NOT NULL UNIQUE,
                        amount INTEGER,
                        bikou TEXT)''')

    ##itemテーブル作成
    c.execute('''CREATE TABLE item(item_name TEXT NOT NULL UNIQUE)''')
    #itemテーブルにitem_nameデータを登録
    c.execute("INSERT INTO item VALUES('食費')")
    c.execute("INSERT INTO item VALUES('外食費')")
    c.execute("INSERT INTO item VALUES('微少品費')")
    c.execute("COMMIT")
except:
    pass




#登録ボタンがクリックされた時の関数
def create_sql(item_name):

    #データベースに接続
    c = sqlite3.connect("database.db")
    #dateの取得
    date = entry_hiduke.get()
    #item_nameの取得
    item_name = c.execute('''
                            SELECT item_name FROM item''')
    #金額の取得
    amount = entry_amount.get()
    #備考欄の取得
    bikou = entry_bikou.get()

    #Tkinterの値をSQLを発行してDBへ登録する
    try:
        c.execute("""
                    INSERT INTO cost_data(date,item_name,amount,bikou)
                   VALUES('{}','{}',{},'{}');""".format(date,item_name,amount,bikou))
        c.execute("COMMIT")
        print("1件登録しました")
    except:
       print("エラーにより登録できませんでした")

#コンボボックスのitem_nameを作成する関数
def createitemname():
    c = sqlite3.connect("database.db")
    li = []
    for r in c.execute("SELECT item_name FROM item"):
        li.append(r)
    #リストをタプルに変換
    return tuple(li)

###
###
###

##Tkinter
#rootフレームの設定
root = tk.Tk()
root.title("テスト1")
root.geometry("1300x220")

#メニューの設定
frame_menu = tk.Frame(root,bd=2,relief="ridge")
frame_menu.pack(fill="x")
button_itemtouroku = tk.Button(frame_menu,text="項目登録")
button_itemtouroku.pack(side="left")


#日付ラベルとエントリー
frame_hiduke = tk.Frame(root,pady=10)
frame_hiduke.pack(side="left")
label_hiduke = tk.Label(frame_hiduke,font=("",14),text="日付:")
label_hiduke.pack(side="left")
entry_hiduke = tk.Entry(frame_hiduke,font=("",14),justify="left",width=13)
entry_hiduke.pack(side="left")

#項目ラベルとエントリー
frame_item = tk.Frame(root,pady=10)
frame_item.pack(side="left")
label_item = tk.Label(frame_item,font=("",14),text="内訳：")
label_item.pack(side="left")
 #項目のコンボボックス作成
combo = ttk.Combobox(frame_item, state="readonly",font=("",14),width=13)
combo["values"] = createitemname()
combo.current(0)
combo.pack()

#金額ラベルとエントリー
frame_amount = tk.Frame(root,pady=10)
frame_amount.pack(side="left")
label_amount = tk.Label(frame_amount,font=("",14),text="金額：")
label_amount.pack(side="left")
entry_amount = tk.Entry(frame_amount,font=("",14),justify="left",width=15)
entry_amount.pack(side="left")

#備考欄ラベルとエントリー
frame_bikou = tk.Frame(root,pady=10)
frame_bikou.pack(side="left")
label_bikou = tk.Label(frame_bikou,font=("",14),text="備考欄：")
label_bikou.pack(side="left")
entry_bikou = tk.Entry(frame_bikou,font=("",14),justify="left",width=40)
entry_bikou.pack(side="left")

#登録ボタンの設定
button_touroku  = tk.Button(root,text="登録",
                            font=("",16),
                            width=10,bg="gray",
                            command=lambda:create_sql(combo.get()))
button_touroku .pack()

root.mainloop()
