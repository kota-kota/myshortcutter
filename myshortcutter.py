#!/usr/bin/python3
import os
import tkinter as tk
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
        self.load()
        self.sort()
        self.dump()

    def __make(self, name, path, type):
        return {"name": name, "path": path, "type": type}

    def load(self):
        self.data = {}
        if os.path.isfile(self.filepath) == False:
            return
        with open(self.filepath) as f:
            self.data = json.load(f)

    def dump(self):
        with open(self.filepath, "w") as f:
            json.dump(self.data, f, indent=4)

    def sort(self):
        sortdata = {}
        for d in sorted(self.data.items(), key=lambda x:x[0]):
            sortdata[d[0]] = sorted(d[1], key=lambda x:x['name'])
        self.data = sortdata

    def getKinds(self):
        return list(self.data.keys())

    def get(self, kind):
        return self.data.get(kind)

    def add(self, kind, name, path, type):
        d = self.__make(name, path, type)
        list = self.data.get(kind)
        if list == None:
            self.data.setdefault(kind, []).append(d)
        else:
            if not d in list:
                self.data.setdefault(kind, []).append(d)

    def remove(self, kind, name, path, type):
        list = self.data.get(kind)
        if list == None:
            return
        d = self.__make(name, path, type)
        if d in list:
            list.remove(d)


#------------------------------------------------------------
# MyTreeFrameクラス
#------------------------------------------------------------
class MyTreeFrame(tk.ttk.Treeview):

    def __init__(self, root, userdata):
        super().__init__(root)
        self.userdata = userdata
        self.selitem = 0
        self.columns = ('name', 'path', 'type')
        self.bind('<<TreeviewSelect>>', self.__onItemSelected)
        self.__setHeaders()
        self.update()

    # ヘッダ設定
    def __setHeaders(self):
        self.column('#0')
        self.heading('#0', text='kind')
        self["columns"] = self.columns
        for col in self.columns:
            self.column(col)
            self.heading(col, text=col)

    # 項目選択
    def __onItemSelected(self, event):
        self.selitem = self.focus()
        log('__onItemSelected: ' + str(self.selitem))
        log(self.item(self.selitem))

    # 更新
    def update(self):
        self.delete(*self.get_children())
        kinds = self.userdata.getKinds()
        for kind in kinds:
            id = self.insert('', 'end', text=kind)
            data = self.userdata.get(kind)
            for d in data:
                values = (d[self.columns[0]], d[self.columns[1]], d[self.columns[2]])
                self.insert(id, 'end', values=values)

    # 追加
    def add(self, kind, name, path, type):
        log('add: ' + kind + ',' + name + ',' + path + ',' + type)
        self.userdata.add(kind, name, path, type)
        self.userdata.sort()
        self.userdata.dump()
        self.update()

    # 削除
    def remove(self):
        log('remove: ')

#------------------------------------------------------------
# MyAddMenuクラス
#------------------------------------------------------------
class MyAddMenu:

    def __init__(self, root, mytreeframe):
        self.root = root
        self.mytreeframe = mytreeframe

    def start(self):
        self.__initWindow(self.root)
        self.__makeMainFrame()
        self.__makeErrorFrame()
        self.__makeButtonFrame()

    def __initWindow(self, root):
        self.window = tk.Toplevel(root)
        self.window.title('追加')
        self.window.geometry('500x230')
        self.window.focus_set()
        self.window.grab_set()

    def __makeMainFrame(self):
        # frame
        frame = ttk.Frame(self.window, padding=10)
        frame.grid()
        # kind
        self.kind = tk.StringVar()
        kind_label = tk.Label(frame, text='kind >> ')
        kind_label.grid(sticky=tk.W, row=0, column=0, padx=5, pady=5)
        kind_entry = ttk.Entry(frame, textvariable=self.kind, width=50)
        kind_entry.grid(sticky=tk.W, row=0, column=1, padx=5, pady=5)
        # name
        self.name = tk.StringVar()
        name_label = tk.Label(frame, text='name >> ')
        name_label.grid(sticky=tk.W, row=1, column=0, padx=5, pady=5)
        name_entry = ttk.Entry(frame, textvariable=self.name, width=50)
        name_entry.grid(sticky=tk.W, row=1, column=1, padx=5, pady=5)
        # path
        self.path = tk.StringVar()
        path_label = tk.Label(frame, text='path >> ')
        path_label.grid(sticky=tk.W, row=2, column=0, padx=5, pady=5)
        path_entry = ttk.Entry(frame, textvariable=self.path, width=50)
        path_entry.grid(sticky=tk.W, row=2, column=1, padx=5, pady=5)
        path_button = ttk.Button(frame, text='参照', command=self.__onRefButtonClick)
        path_button.grid(sticky=tk.W, row=2, column=2, padx=5, pady=5)
        # type
        self.type = tk.StringVar()
        self.type.set('IE')
        type_label = tk.Label(frame, text='type >> ')
        type_label.grid(sticky=tk.W, row=3, column=0, padx=5, pady=5)
        type_combobox = ttk.Combobox(frame, textvariable=self.type, width=50)
        type_combobox.bind('<<ComboboxSelected>>', self.__onComboboxSelected)
        type_combobox['values']=('IE', 'chrome', 'explorer')
        type_combobox.set('IE')
        type_combobox.grid(sticky=tk.W, row=3, column=1, padx=5, pady=5)

    def __onComboboxSelected(self, event):
        log('type: ' + self.type.get())

    def __makeErrorFrame(self):
        # frame
        frame = ttk.Frame(self.window, padding=1)
        frame.grid()
        # Error
        self.error = tk.StringVar()
        error_label = tk.Label(frame, textvariable=self.error, foreground='red')
        error_label.grid(row=0, column=0)

    def __makeButtonFrame(self):
        # frame
        frame = ttk.Frame(self.window, padding=1)
        frame.grid()
        # OK
        ok_button = ttk.Button(frame, text='OK', command = self.__onOKButtonClick)
        ok_button.grid(row=0, column=0, padx=10)
        # Cancel
        cancel_button = ttk.Button(frame, text='Cancel', command = self.__onCancelButtonClick)
        cancel_button.grid(row=0, column=1, padx=10)

    def __onRefButtonClick(self):
        fTyp = [('','*')]
        iDir = os.path.abspath(os.path.dirname(__file__))
        filepath = filedialog.askopenfilename(filetypes=fTyp, initialdir=iDir)
        self.path.set(filepath)

    def __onOKButtonClick(self):
        kind = self.kind.get()
        if not kind:
            self.error.set('kind not set')
            return
        name = self.name.get()
        if not name:
            self.error.set('name not set')
            return
        path = self.path.get()
        if not path:
            self.error.set('path not set')
            return
        type = self.type.get()
        if not type:
            self.error.set('type not set')
            return
        self.mytreeframe.add(kind, name, path, type)
        self.window.destroy()

    def __onCancelButtonClick(self):
        self.window.destroy()

#------------------------------------------------------------
# MyDelMenuクラス
#------------------------------------------------------------
class MyDelMenu:

    def __init__(self, root, mytreeframe):
        self.root = root
        self.mytreeframe = mytreeframe

    def start(self):
        self.mytreeframe.remove()


#------------------------------------------------------------
# MySetMenuクラス
#------------------------------------------------------------
class MySetMenu:

    def __init__(self, root, mytreeframe):
        self.root = root
        self.mytreeframe = mytreeframe

    def start(self):
        self.mytreeframe.delete()

#------------------------------------------------------------
# MyShortcutterアプリクラス
#------------------------------------------------------------
class MyShortcutter:

    def __init__(self, path):
        # ルートウィンドウ作成
        self.root = tk.Tk()
        self.root.title('MyShortcutter')
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        # ユーザデータ
        userdata = UserData(path, 'myshortcutter.json')
        # ツリーフレーム + スクロールバー
        mytreeframe = MyTreeFrame(self.root, userdata)
        scrollbar = ttk.Scrollbar(self.root, orient='v', command=mytreeframe.yview)
        mytreeframe.configure(yscrollcommand=scrollbar.set)
        # メニュー
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        menu.add_cascade(label='追加', command=MyAddMenu(self.root, mytreeframe).start)
        menu.add_cascade(label='削除', command=MyDelMenu(self.root, mytreeframe).start)
        menu.add_cascade(label='設定', command=MySetMenu(self.root, mytreeframe).start)
        # スクロールバーの表示
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # ツリーフレームの表示
        mytreeframe.pack()

    def start(self):
        # メインループ開始
        self.root.mainloop()

#------------------------------------------------------------
# エラー
#------------------------------------------------------------
def err(msg):
    log('!!! Error: ' + msg)
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
    app = MyShortcutter(path)
    app.start()
    os.sys.exit(0)
