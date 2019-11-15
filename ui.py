import sys
import tkinter as tk
import tkinter.ttk as ttk

from main import consolidate_portfolio


class TextWidget(tk.Text):

    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.bind('<Control-c>', self.copy)
        self.bind('<Control-x>', self.cut)
        self.bind('<Control-v>', self.paste)

    def copy(self, event=None):
        self.clipboard_clear()
        text = self.get(tk.SEL_FIRST, tk.SEL_LAST)
        self.clipboard_append(text)

    def cut(self, event):
        self.copy()
        self.delete(tk.SEL_FIRST, tk.SEL_LAST)

    def paste(self, event):
        text = self.selection_get(selection='CLIPBOARD')
        #self.insert('insert', text)


class PortFolioMain:

    def reset_url(self, event):
        # TODO:: reset all other messages
        self.text_url.delete("1.0", tk.END)

    def load_url(self, event):
        if self.is_loading:
            self.label_msg.config(text="Already Loading... Keep Calm!")
            return

        url_str = self.text_url.get("1.0", tk.END).strip()
        if url_str == "":
            self.label_msg.config(text="Enter some URL!")
            return

        self.label_msg.config(text="Loading...")
        self.is_loading = True

        urls = url_str.split("\n")[:]
        # TODO:: below must be execute currently
        # each url can be obtained concurrently
        # after all data is obtained
        # consolidate the data and return
        # after that trigger display data
        data = consolidate_portfolio(urls)
        self.display_table(data)

    # add type hint
    def display_table(self, data):
        for d in data:
            self.tree_view.insert('', 'end', values=d)
        self.is_loading = False
        self.label_msg.config(text="Finished!")

    def __init__(self, top=None):
        self.is_loading = False
        '''This class configures and populates the toplevel window.
               top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#ececec'  # Closest X11 color: 'gray92'
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.', background=_bgcolor)
        self.style.configure('.', foreground=_fgcolor)
        self.style.configure('.', font="TkDefaultFont")
        self.style.map('.', background=
        [('selected', _compcolor), ('active', _ana2color)])

        top.geometry("600x450+344+139")
        top.minsize(1, 1)
        top.maxsize(1351, 738)
        top.resizable(1, 1)
        top.title("Portfolio Aggregator")

        self.text_url = TextWidget(top)
        self.text_url.place(relx=0.017, rely=0.022, relheight=0.387, relwidth=0.96)
        self.text_url.configure(background="white")
        self.text_url.configure(font="TkTextFont")
        self.text_url.configure(selectbackground="#c4c4c4")
        self.text_url.configure(wrap="word")

        self.label_msg = tk.Label(top)
        self.label_msg.place(relx=0.233, rely=0.444, height=21, width=311)
        self.label_msg.configure(text='''enter a valid url and click load portfolio button''')

        self.btn_load = tk.Button(top)
        self.btn_load.place(relx=0.3, rely=0.889, height=31, width=121)
        self.btn_load.configure(text='''Load PortFolio''')
        self.btn_load.bind("<Button-1>", self.load_url)

        self.btn_reset = tk.Button(top)
        self.btn_reset.place(relx=0.55, rely=0.889, height=31, width=65)
        self.btn_reset.configure(text='''Reset''')
        self.btn_reset.bind('<Button-1>', self.reset_url)

        self.style.configure('Treeview', font="TkDefaultFont")
        self.tree_view = ttk.Treeview(top)
        self.tree_view.place(relx=0.033, rely=0.511, relheight=0.313, relwidth=0.933)
        self.tree_view.configure(columns=["Stocks", "Holdings", "Avg %"])
        self.tree_view["show"] = 'headings'

        self.tree_view.heading("0", text="Stock Name")
        self.tree_view.heading("0", anchor="center")
        self.tree_view.column("0", width="75")

        self.tree_view.heading("1", text="Total %")
        self.tree_view.heading("1", anchor="center")
        self.tree_view.column("1", width="75")

        self.tree_view.heading("2", text="Avg. %")
        self.tree_view.heading("2", anchor="center")
        self.tree_view.column("2", width="75")


if __name__ == '__main__':
    test_urls = '''https://www.moneycontrol.com/mutual-funds/nav/mirae-asset-tax-saver-fund-direct-plan/MMA150
https://www.moneycontrol.com/mutual-funds/nav/tata-india-tax-savings-fund-direct-plan-growth/MTA1114'''

    root = tk.Tk()
    top = PortFolioMain(root)

    top.text_url.insert("1.0", test_urls)

    root.mainloop()
