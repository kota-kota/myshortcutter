#!/usr/bin/python3
import os
import tkinter
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import json

#------------------------------------------------------------
# ユーザデータクラス
#------------------------------------------------------------
class UserData:

    def __init__(self, path, filename):
        self.filepath = path + os.sep + filename
        self.data = {}
        self.load()
        self.remove("test", "local", "ddddd", "URL")

    def __make(self, name, url, type):
        return {"name": name, "url": url, "type": type}

    def load(self):
        if os.path.isfile(self.filepath) == False:
            return
        with open(self.filepath) as f:
            self.data = json.load(f)

    def dump(self):
        with open(self.filepath, "w") as f:
            json.dump(self.data, f, indent=4)

    def add(self, kind, name, url, type):
        d = self.__make(name, url, type)
        self.data.setdefault(kind, []).append(d)

    def remove(self, kind, name, url, type):
        list = self.data.get(kind)
        if list == None:
            return
        d = self.__make(name, url, type)
        if d in list:
            list.remove(d)


#------------------------------------------------------------
# データ追加Windowクラス
#------------------------------------------------------------
class AddDataWindow:

    def __init__(self, root, callback):
        self.callback = callback
        self.__initWindow(root)
        self.__makeMainFrame()
        self.__makeErrorFrame()
        self.__makeButtonFrame()

    def __initWindow(self, root):
        self.window = tkinter.Toplevel(root)
        self.window.title("追加")
        self.window.geometry("500x230")
        self.window.focus_set()
        self.window.grab_set()

    def __makeMainFrame(self):
        # frame
        frame = ttk.Frame(self.window, padding=10)
        frame.grid()
        # kind
        self.kind = tkinter.StringVar()
        kind_label = tkinter.Label(frame, text="kind >> ")
        kind_label.grid(sticky=tkinter.W, row=0, column=0, padx=5, pady=5)
        kind_entry = ttk.Entry(frame, textvariable=self.kind, width=50)
        kind_entry.grid(sticky=tkinter.W, row=0, column=1, padx=5, pady=5)
        # name
        self.name = tkinter.StringVar()
        name_label = tkinter.Label(frame, text="name >> ")
        name_label.grid(sticky=tkinter.W, row=1, column=0, padx=5, pady=5)
        name_entry = ttk.Entry(frame, textvariable=self.name, width=50)
        name_entry.grid(sticky=tkinter.W, row=1, column=1, padx=5, pady=5)
        # path
        self.path = tkinter.StringVar()
        path_label = tkinter.Label(frame, text="path >> ")
        path_label.grid(sticky=tkinter.W, row=2, column=0, padx=5, pady=5)
        path_entry = ttk.Entry(frame, textvariable=self.path, width=50)
        path_entry.grid(sticky=tkinter.W, row=2, column=1, padx=5, pady=5)
        path_button = ttk.Button(frame, text="参照", command=self.__onRefButtonClick)
        path_button.grid(sticky=tkinter.W, row=2, column=2, padx=5, pady=5)
        # type
        self.type = tkinter.StringVar()
        self.type.set("ie")
        type_label = tkinter.Label(frame, text="type >> ")
        type_label.grid(sticky=tkinter.W, row=3, column=0, padx=5, pady=5)
        type_entry = ttk.Entry(frame, textvariable=self.type, width=50)
        type_entry.configure(state="readonly")
        type_entry.grid(sticky=tkinter.W, row=3, column=1, padx=5, pady=5)
        type_optmenu = tkinter.OptionMenu(frame, self.type, "ie", "chrome")
        type_optmenu.grid(sticky=tkinter.W, row=3, column=2, padx=5, pady=5)

    def __makeErrorFrame(self):
        # frame
        frame = ttk.Frame(self.window, padding=1)
        frame.grid()
        # Error
        self.error = tkinter.StringVar()
        error_label = tkinter.Label(frame, textvariable=self.error, foreground="red")
        error_label.grid(row=0, column=0)

    def __makeButtonFrame(self):
        # frame
        frame = ttk.Frame(self.window, padding=1)
        frame.grid()
        # OK
        ok_button = tkinter.Button(frame, text="OK", command = self.__onOKButtonClick)
        ok_button.grid(row=0, column=0, padx=10)
        # Cancel
        cancel_button = tkinter.Button(frame, text="Cancel", command = self.__onCancelButtonClick)
        cancel_button.grid(row=0, column=1, padx=10)

    def __onRefButtonClick(self):
        fTyp = [("","*")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        filepath = filedialog.askopenfilename(filetypes=fTyp, initialdir=iDir)
        self.path.set(filepath)

    def __onOKButtonClick(self):
        kind = self.kind.get()
        if not kind:
            self.error.set("'kind' not set")
            return
        name = self.name.get()
        if not name:
            self.error.set("'name' not set")
            return
        path = self.path.get()
        if not path:
            self.error.set("'path' not set")
            return
        type = self.type.get()
        if not type:
            self.error.set("'type' not set")
            return
        self.callback(kind, name, path, type)
        self.window.destroy()

    def __onCancelButtonClick(self):
        self.window.destroy()

#------------------------------------------------------------
# MyShortcutterアプリクラス
#------------------------------------------------------------
class MyShortcutter:

    def __init__(self, path):
        filename = "myshortcutter.json"
        self.__initRoot()
        self.__initMenu()
        self.__initTreeView()
        self.__initUserData(path, filename)
        self.__start()

    def __initRoot(self):
        # メインウィンドウを作成
        self.root = tkinter.Tk()
        self.root.title("myshortcut")
        self.root.geometry("600x480")

    def __initMenu(self):
        # メニューを作成
        self.menu = tkinter.Frame(self.root, bd=2, relief="ridge")
        self.menu.pack(fill="x")
        # ボタンを作成
        self.addbutton = tkinter.Button(self.menu, text="追加", command = self.__onAddButtonClick)
        self.addbutton.pack(side="left")
        self.rmbutton = tkinter.Button(self.menu, text="削除", command = self.__onRmButtonClick)
        self.rmbutton.pack(side="left")

    def __initTreeView(self):
        # ツリービューを作成
        self.tree = tkinter.ttk.Treeview(self.root)
        self.tree.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        # 列を３列作る
        self.tree["columns"] = (1,2,3,4)
        self.tree["show"] = "headings"
        # ヘッダーテキスト
        self.tree.heading(1,text="分類")
        self.tree.heading(2,text="名前")
        self.tree.heading(3,text="パス")
        self.tree.heading(4,text="パス種別")
        # 列の幅
        self.tree.column(1,width=50)
        self.tree.column(2,width=200)
        self.tree.column(3,width=300)
        self.tree.column(4,width=50)

        # ダブルクリックしたときの処理
        self.tree.bind("<Double-1>", self.__onDoubleClick)

    def __initUserData(self, path, filename):
        self.userdata = UserData(path, filename)

    def __start(self):
        # データ挿入
        self.tree.insert("", "end", values=("local folder", "C:\\cygwin64\\home\\Kyohei", "PATH"))
        self.tree.insert("", "end", values=("remote folder", "\\\\192.168.0.10\\nas\\Documents", "PATH"))
        self.tree.insert("", "end", values=("url", "https://github.com/kota-kota", "URL"))
        self.root.mainloop()

    def __onAddButtonClick(self):
        AddDataWindow(self.root, self.__onAddDataCallBack)

    def __onAddDataCallBack(self, kind, name, path, type):
        log("__onAddDataCallBack: " + kind + "," + name + "," + path + "," + type)

    def __onRmButtonClick(self):
        log("Remove")

    def __onDoubleClick(self, event):
        item = self.tree.selection()[0]
        log(self.tree.item(item,"values"))
        #self.tree.insert("", "end", values=self.tree.item(item,"values"))

#------------------------------------------------------------
# エラー
#------------------------------------------------------------
def err(msg):
    log("!!! Error: " + msg)
    os.sys.exit(0)

#------------------------------------------------------------
# ログ出力
#------------------------------------------------------------
def log(msg):
    print(msg)

#------------------------------------------------------------
# エントリーポイント
#------------------------------------------------------------
if __name__ == '__main__':
    path, filename = os.path.split(__file__)
    log("Start " + filename)
    app = MyShortcutter(path)
    log("End")
    os.sys.exit(0)
