#試算表 ver.1.4
#2019/1/13      制作開始
#2019/1/13      制作終了

"""
・項目にその他を追加

■ver.2.0に向けて

【Facebook 2018/2/3 #python #試算表】を参照

"""

# -*- coding: utf-8 -*-

import tkinter as tk
# python2の場合は、import Tkinter as tk
import tkinter.ttk as ttk
#メッセージボックス
import tkinter.messagebox as tkmsg
# python2の場合は、import ttk
import sqlite3

# 登録画面のGUI
def create_gui():
    # ----------------------------------------
    # コールバック関数群
    # ----------------------------------------    
    # 表示ボタンが押下されたときのコールバック関数
    def select_button():
        root.destroy()
        select_gui()
    # ----------------------------------------
    # 終了ボタンが押下されたときのコールバック関数
    def quit_button():
        root.destroy()
    # ----------------------------------------
    # 項目表示ボタンが押された時のコールバック関数
    def itemselect_button():
        root.destroy()
        itemselect_gui()
    # ----------------------------------------
    # 登録ボタンがクリックされた時にデータをDBに登録するコールバック関数
    def create_sql(item_name):

        # データベースに接続
        c = sqlite3.connect("database.db")
        # item_nameをWHERE句に渡してitem_codeを取得する
        item_code = c.execute("""
                    SELECT item_code FROM item
                    WHERE item_name = '{}'
                    """.format(item_name))
        item_code = item_code.fetchone()[0]
        # 日付の読み取り
        acc_data = entry1.get().replace("/","-")
        # 金額の読み取り
        amount = entry3.get()
        #備考欄の読み取り
        bikou = entry4.get()

        # SQLを発行してDBへ登録
        # python2の場合は、ユニコード文字列でsqlite3に渡す
        # また、コミットする場合は、commitメソッドを用いる
        try:
            c.execute("""
            INSERT INTO acc_data(acc_date,item_code,amount,bikou)
            VALUES('{}',{},{},'{}');
            """.format(acc_data,item_code,amount,bikou))
            c.execute("COMMIT;")
            print("1件登録しました")
            tkmsg.showinfo()
        # ドメインエラーなどにより登録できなかった場合のエラー処理
        except:
            tkmsg.showwarning()
            print("エラーにより登録できませんでした")
    # ----------------------------------------
    # 内訳テーブル(item)にあるitem_nameのタプルを作成する
    def createitemname():
        # データベースの接続
        c = sqlite3.connect("database.db")
        # 空の「リスト型」を定義
        li = []
        # SELECT文を発行し、item_nameを取得し、for文で回す
        for r in c.execute("SELECT item_name FROM item"):
            # item_nameをリストに追加する
            li.append(r)
        # リスト型のliをタプル型に変換して、ファンクションに戻す
        return tuple(li)
    # ----------------------------------------
    
    # 空のデータベースを作成して接続する
    dbname = "database.db"
    c = sqlite3.connect(dbname)
    c.execute("PRAGMA foreign_keys = 1")

    # 既にデータベースが登録されている場合は、ddlの発行でエラーが出るのでexceptブロックで回避する
    try:
        # itemテーブルの定義
        ddl = """
        CREATE TABLE item
        (
           item_code INTEGER PRIMARY KEY AUTOINCREMENT,
           item_name TEXT NOT NULL UNIQUE
        )
         """
        # SQLの発行
        c.execute(ddl)
        # acc_dataテーブルの定義    
        ddl = """
        CREATE TABLE acc_data
        ( 
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            acc_date DATE NOT NULL,
            item_code INTEGER NOT NULL,
            amount INTEGER,
            bikou TEXT,
            FOREIGN KEY(item_code) REFERENCES item(item_code)
        )
        """
        # itemテーブルへリファレンスデータの登録
        # このitem_codeとitem_nameを途中で変更したら、今までのデータはどうなるんだろう？変更する際は、その前に確認作業をすること。
        c.execute(ddl)
        c.execute("INSERT INTO item VALUES(1,'食費')")
        c.execute("INSERT INTO item VALUES(2,'微消品費')")
        c.execute("INSERT INTO item VALUES(3,'移動費')")
        c.execute("INSERT INTO item VALUES(4,'外食費')")
        c.execute("INSERT INTO item VALUES(5,'子供費')")
        c.execute("INSERT INTO item VALUES(6,'書籍費')")
        c.execute("INSERT INTO item VALUES(7,'日用品費')")
        c.execute("INSERT INTO item VALUES(8,'遊興費')")
        c.execute("INSERT INTO item VALUES(9,'医療費')")
        c.execute("INSERT INTO item VALUES(10,'衣服費')")
        c.execute("INSERT INTO item VALUES(11,'贈答費')")
        c.execute("INSERT INTO item VALUES(12,'芸術費')")
        c.execute("INSERT INTO item VALUES(13,'車両関係費')")
        c.execute("INSERT INTO item VALUES(14,'旅行費')")
        c.execute("INSERT INTO item VALUES(15,'その他')")
        c.execute("INSERT INTO item VALUES(16,'家賃')")
        c.execute("INSERT INTO item VALUES(17,'水道光熱費')")
        c.execute("INSERT INTO item VALUES(18,'通信費')")
        c.execute("INSERT INTO item VALUES(19,'月謝')")
        c.execute("INSERT INTO item VALUES(20,'保険料')")
        c.execute("COMMIT")
    except:
        pass

    # rootフレームの設定
    root = tk.Tk()
    root.title("試算表")
    root.geometry("1300x220")

    # メニューの設定
    frame = tk.Frame(root,bd=2,relief="ridge")
    frame.pack(fill="x")
    button1 = tk.Button(frame,text="入力")
    button1.pack(side="left")
    button2 = tk.Button(frame,text="表示",command=select_button)
    button2.pack(side="left")
    button4 = tk.Button(frame,text="項目表示",command=itemselect_button)
    button4.pack(side="left")
    button3 = tk.Button(frame,text="終了",command=quit_button)
    button3.pack(side="right")


    
    # 入力画面ラベルの設定
    label1 = tk.Label(root,text="【入力画面】",font=("",16),height=2)
    label1.pack(fill="x")

    # 日付のラベルとエントリーの設定
    frame1 = tk.Frame(root,pady=10)
    frame1.pack(side="left")
    label2 = tk.Label(frame1,font=("",14),text="日付：")
    label2.pack(side="left")
    entry1 = tk.Entry(frame1,font=("",14),justify="left",width=13)
    entry1.pack(side="left")

    # 内訳のラベルとエントリーの設定
    frame2 = tk.Frame(root,pady=10)
    frame2.pack(side="left")
    label3 = tk.Label(frame2,font=("",14),text="内訳：")
    label3.pack(side="left")
    # 内訳コンボボックスの作成
    combo = ttk.Combobox(frame2, state='readonly',font=("",14),width=13)
    combo["values"] = createitemname()
    combo.current(0)
    combo.pack()

    # 金額のラベルとエントリーの設定
    frame3 = tk.Frame(root,pady=10)
    frame3.pack(side="left")
    label4 = tk.Label(frame3,font=("",14),text="金額：")
    label4.pack(side="left")
    entry3 = tk.Entry(frame3,font=("",14),justify="left",width=15)
    entry3.pack(side="left")

    # 備考欄のラベルとエントリーの設定
    frame4 = tk.Frame(root,pady=10)
    frame4.pack(side="left")
    label5 = tk.Label(frame4,font=("",14),text="備考欄：")
    label5.pack(side="left")
    entry4 = tk.Entry(frame4,font=("",14),justify="left",width=40)
    entry4.pack(side="left")

    # 登録ボタンの設定
    button4 = tk.Button(root,text="登録",
                        font=("",16),
                        width=10,bg="gray",
                        command=lambda:create_sql(combo.get()))
    button4.pack()

   


    
    root.mainloop()

# 表示画面のGUI
def select_gui():
    # ----------------------------------------
    # コールバック関数群
    # ----------------------------------------    
    # 登録ボタンが押下されたときのコールバック関数
    def create_button():
        root.destroy()
        create_gui()
    # ----------------------------------------
    # 終了ボタンが押下されたときのコールバック関数
    def quit_button():
        root.destroy()
    # ----------------------------------------
    # 項目表示ボタンが押された時のコールバック関数
    def itemselect_button():
        root.destroy()
        itemselect_gui()
    # ----------------------------------------
    # 表示ボタンが押下されたときのコールバック関数
    def select_sql(start,end):
        # treeviewのアイテムをすべて削除
        tree.delete(*tree.get_children())
        # 開始日と終了日が空欄だったらデフォルト値の設定
        if start == "":
            start = "1900-01-01"
        if end == "":
            end = "2100-01-01"
        #SELECT文の作成
        sql = """
        SELECT id,acc_date,item_name,amount,bikou
        FROM acc_data as a,item as i
        WHERE a.item_code = i.item_code AND
        acc_date BETWEEN '{}' AND '{}'
        ORDER BY acc_date
        """.format(start,end)
        # ツリービューにアイテムの追加
        i=0
        for r in c.execute(sql):
            # 金額(r[2])を通貨形式に変換
            r = (r[0],r[1],r[2],"¥{:,d}".format(r[3]),r[4])
            tree.insert("","end",tags=i,values=r)
            if i & 1:
                tree.tag_configure(i,background="#CCFFFF")
            i+=1

        #ツリービューに変動費、固定費、総計を表示
        tree2.delete(*tree2.get_children())
        sql2 = """
                SELECT i.item_code,item_name, sum(a.amount)
                FROM acc_data as a, item as i
                WHERE a.item_code = i.item_code AND a.acc_date BETWEEN '{}' AND '{}'
                GROUP BY item_name
                """.format(start,end)
        sort = []
        for q in c.execute(sql2):
            q = (q[0],q[1],"\{:,d}".format(q[2]))
            q = list(q)
            sort.append(q)
        sort = sorted(sort)
        sort = list(sort)
        
        pick = 0
        soukei = []
        hendou = []
        kotei = []
    
        for n in sort:
            n = sort[pick]
            soukei.append(int(n[2].replace(",","").replace("\\","")))
            if n[0] <= 14:
                hendou.append(int(n[2].replace(",","").replace("\\","")))
            else:
                kotei.append(int(n[2].replace(",","").replace("\\","")))
            del(n[0])
            pick +=1
            tree2.insert("","end",values=n)
        hendou = ("変動費","\{:,d}".format(sum(hendou)))
        kotei =  ("固定費","\{:,d}".format(sum(kotei)))
        soukei = ("総計","\{:,d}".format(sum(soukei)))

        tree2.insert("","end",values=("---","---"))
        tree2.insert("","end",values=hendou)
        tree2.insert("","end",values=kotei)
        tree2.insert("","end",values=soukei)
                
    # ----------------------------------------
    
    # 空のデータベースを作成して接続する
    dbname = "database.db"
    c = sqlite3.connect(dbname)
    c.execute("PRAGMA foreign_keys = 1")

    # rootフレームの設定
    root = tk.Tk()
    root.title("試算表")
    root.geometry("750x950")

    # メニューの設定
    frame = tk.Frame(root,bd=2,relief="ridge")
    frame.pack(fill="x")
    button1 = tk.Button(frame,text="入力",command=create_button)
    button1.pack(side="left")
    button2 = tk.Button(frame,text="表示")
    button2.pack(side="left")
    button4 = tk.Button(frame,text="項目表示",command=itemselect_button)
    button4.pack(side="left")
    button3 = tk.Button(frame,text="終了",command=quit_button)
    button3.pack(side="right")

    # 入力画面ラベルの設定
    label1 = tk.Label(root,text="【表示画面】",font=("",16),height=2)
    label1.pack(fill="x")

    # 期間選択のラベルエントリーの設定
    frame1 = tk.Frame(root,pady=10)
    frame1.pack()
    label2 = tk.Label(frame1,font=("",14),text="期間 ")
    label2.pack(side="left")
    entry1 = tk.Entry(frame1,font=("",14),justify="center",width=12)
    entry1.pack(side="left")
    label3 = tk.Label(frame1,font=("",14),text="　～　")
    label3.pack(side="left")
    entry2 = tk.Entry(frame1,font=("",14),justify="center",width=12)
    entry2.pack(side="left")

    # 表示ボタンの設定
    button4 = tk.Button(root,text="表示",
                        font=("",16),
                        width=10,bg="gray",
                        command=lambda:select_sql(entry1.get(),entry2.get()))
    button4.pack()

    # ツリービューの作成
    tree = ttk.Treeview(root,height=5,padding=10)
    tree["columns"] = (1,2,3,4,5)
    tree["show"] = "headings"
    tree.column(1,width=50)
    tree.column(2,width=100)
    tree.column(3,width=130)
    tree.column(4,width=110)
    tree.column(5,width=350)
    tree.heading(1,text="No.")
    tree.heading(2,text="日付")
    tree.heading(3,text="内訳")
    tree.heading(4,text="金額")
    tree.heading(5,text="備考欄")


    tree2 = ttk.Treeview(root,height=25,padding=20)
    tree2["columns"] = (1,2)
    tree2["show"] = "headings"
    tree2.column(1,width=100)
    tree2.column(2,width=110)
    tree2.heading(1,text="項目")
    tree2.heading(2,text="合計")
    

    

    # ツリービューのスタイル変更
    style = ttk.Style()
    # TreeViewの全部に対して、フォントサイズの変更
    style.configure("Treeview",font=("",14))
    # TreeViewのHeading部分に対して、フォントサイズの変更と太字の設定
    style.configure("Treeview.Heading",font=("",14,"bold"))

    # ツリービューの配置
    tree.pack(fill="x",padx=10,pady=10)
    tree2.pack(fill="y", padx=10,pady=20)

    # メインループ
    root.mainloop()

# 項目表示画面
def itemselect_gui():
    # ----------------------------------------
    # コールバック関数群
    # ----------------------------------------    
    # 登録ボタンが押下されたときのコールバック関数
    def create_button():
        root.destroy()
        create_gui()
    # ----------------------------------------
    # 終了ボタンが押下されたときのコールバック関数
    def quit_button():
        root.destroy()
    # -----------------------------------------
    # 表示ボタンが押された時のコールバック関数
    def select_button():
        root.destroy()
        select_gui()
    # ----------------------------------------
    # 項目表示ボタンが押下されたときのコールバック関数
    def itemselect_sql(start,end):
        # treeviewのアイテムをすべて削除
        tree.delete(*tree.get_children())
        ## itemselectに選択された項目を代入
        itemselect = combo.get()     
        # 開始日と終了日が空欄だったらデフォルト値の設定
        if start == "":
            start = "1900-01-01"
        if end == "":
            end = "2100-01-01"
        #SELECT文の作成
        sql = """
        SELECT id,acc_date,item_name,amount,bikou
        FROM acc_data as a,item as i
        WHERE item_name = '{}' AND a.item_code = i.item_code AND
        acc_date BETWEEN '{}' AND '{}'
        ORDER BY acc_date
        """.format(itemselect,start,end)
        # ツリービューにアイテムの追加
        i=0
        ## 項目の合計のためリスト作成
        goukei = []
        for r in c.execute(sql):
            # 金額をappend
            goukei.append(r[3])

            # 金額(r[2])を通貨形式に変換
            r = (r[0],r[1],r[2],"¥{:,d}".format(r[3]),r[4])
            tree.insert("","end",tags=i,values=r)
            if i & 1:
                tree.tag_configure(i,background="#CCFFFF")
            i+=1    
    # ----------------------------------------
        goukei = sum(goukei)
        goukei = ("","","","\{:,d}".format(goukei),"")
        #goukei = "\{:,d}".format(goukei)
        print(goukei)
        tree.insert("","end",values=("---","---","---","---","---"))
        tree.insert("","end",values=goukei)
       
    # 内訳テーブル(item)にあるitem_nameのタプルを作成する
    def createitemname():
        # データベースの接続
        c = sqlite3.connect("database.db")
        # 空の「リスト型」を定義
        li = []
        # SELECT文を発行し、item_nameを取得し、for文で回す
        for r in c.execute("SELECT item_name FROM item"):
            # item_nameをリストに追加する
            li.append(r)
        # リスト型のliをタプル型に変換して、ファンクションに戻す
        return tuple(li)
    
    # 空のデータベースを作成して接続する
    dbname = "database.db"
    c = sqlite3.connect(dbname)
    c.execute("PRAGMA foreign_keys = 1")

    # rootフレームの設定
    root = tk.Tk()
    root.title("試算表")
    root.geometry("750x900")

    # メニューの設定
    frame = tk.Frame(root,bd=2,relief="ridge")
    frame.pack(fill="x")
    button1 = tk.Button(frame,text="入力",command=create_button)
    button1.pack(side="left")
    button2 = tk.Button(frame,text="表示",command=select_button)
    button2.pack(side="left")
    button3 = tk.Button(frame,text="終了",command=quit_button)
    button3.pack(side="right")
    button4 = tk.Button(frame,text="項目表示")

    # 入力画面ラベルの設定
    label1 = tk.Label(root,text="【項目表示】",font=("",16),height=2)
    label1.pack(fill="x")

    # 期間選択のラベルエントリーの設定
    frame1 = tk.Frame(root,pady=10)
    frame1.pack()
    label4 = tk.Label(frame1,font=("",14),text="項目")
    label4.pack(side="left")

    # 項目コンボボックスの作成
    combo = ttk.Combobox(frame1, state='readonly',font=("",14),width=13)
    combo["values"] = createitemname()
    combo.current(0)
    combo.pack()
    
    label2 = tk.Label(frame1,font=("",14),text="期間 ")
    label2.pack(side="left")
    entry1 = tk.Entry(frame1,font=("",14),justify="center",width=12)
    entry1.pack(side="left")
    label3 = tk.Label(frame1,font=("",14),text="　～　")
    label3.pack(side="left")
    entry2 = tk.Entry(frame1,font=("",14),justify="center",width=12)
    entry2.pack(side="left")

    # 表示ボタンの設定
    button4 = tk.Button(root,text="項目表示",
                        font=("",16),
                        width=10,bg="gray",
                        command=lambda:itemselect_sql(entry1.get(),entry2.get()))
    button4.pack()

    # ツリービューの作成
    tree = ttk.Treeview(root,padding=10)
    tree["columns"] = (1,2,3,4,5)
    tree["show"] = "headings"
    tree.column(1,width=50)
    tree.column(2,width=100)
    tree.column(3,width=130)
    tree.column(4,width=110)
    tree.column(5,width=350)
    tree.heading(1,text="No.")
    tree.heading(2,text="日付")
    tree.heading(3,text="内訳")
    tree.heading(4,text="金額")
    tree.heading(5,text="備考欄")

    # ツリービューのスタイル変更
    style = ttk.Style()
    # TreeViewの全部に対して、フォントサイズの変更
    style.configure("Treeview",font=("",12))
    # TreeViewのHeading部分に対して、フォントサイズの変更と太字の設定
    style.configure("Treeview.Heading",font=("",14,"bold"))

    #ツリービューの配置
    tree.pack(fill="x",padx=50,pady=90)

   


    # メインループ
    root.mainloop()


# GUI画面の表示
create_gui()
