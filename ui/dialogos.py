class addressDataBase():
    def __init__(self):
        import tkinter
        from tkinter import filedialog
        import shelve
        tk = tkinter.Tk()
        tk.withdraw()
        filename = filedialog.askopenfile(parent=tk, mode='r', defaultextension='*.mdb', filetypes=[('Microsoft Access Driver', '*.mdb')])