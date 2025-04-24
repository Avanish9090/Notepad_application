from tkinter import *
from tkinter import filedialog, messagebox, colorchooser
from tkinter.simpledialog import askinteger

class MyNotepad:
    current_file = "no-file"

    # UPDATED: Method to change the background color of selected text
    def change_backcolor(self):
        c=colorchooser.askcolor()
        self.txt_area.configure(background=c[1])
        # try:
        #     start_index = self.txt_area.index("sel.first")  # Get start index of selection
        #     end_index = self.txt_area.index("sel.last")    # Get end index of selection
        #     c = colorchooser.askcolor()
        #     if c[1]:  # If a color is chosen
        #         self.txt_area.tag_add("background", start_index, end_index)
        #         self.txt_area.tag_configure("background", background=c[1])
        # except TclError:
        #     messagebox.showwarning("No Selection", "Please select text to change background color.")

    # UPDATED: Method to change the foreground color of selected text
    def change_forecolor(self):
        try:
            start_index = self.txt_area.index("sel.first")  # Get start index of selection
            end_index = self.txt_area.index("sel.last")    # Get end index of selection
            c = colorchooser.askcolor()
            if c[1]:  # If a color is chosen
                self.txt_area.tag_add("foreground", start_index, end_index)
                self.txt_area.tag_configure("foreground", foreground=c[1])
        except TclError:
            messagebox.showwarning("No Selection", "Please select text to change foreground color.")

    # def change_font_size(self, size):
    #     try:
    #         self.txt_area.configure(font=("Arial", size))  # Change font size globally
    #     except Exception as e:
    #         messagebox.showerror("Error", f"Could not change font size: {str(e)}")

    def set_font_size_by_number(self):
        try:
            size = askinteger("Font Size", "Enter font size (e.g., 10, 12, 16):", minvalue=1, maxvalue=100)
            if size:
                self.txt_area.configure(font=("Arial", size))
        except Exception as e:
            messagebox.showerror("Error", f"Could not change font size: {str(e)}")


    def exit_file(self):
        s = self.txt_area.get(1.0, END)
        if not s.strip():
            quit()
        else:
            result = messagebox.askyesnocancel("Save Dialog Box", "Do you want to save this file? Yes, No, Cancel")
            if result == True:
                self.saveas_file()
            elif result == False:
                self.clear()

    def clear(self):
        self.txt_area.delete(1.0, END)

    def new_file(self):
        s = self.txt_area.get(1.0, END)
        if not s.strip():
            pass
        else:
            result = messagebox.askyesnocancel("Save Dialog Box", "Do you want to save this file? Yes, No, Cancel")
            if result == True:
                self.saveas_file()
            elif result == False:
                self.clear()

    def saveas_file(self):
        f = filedialog.asksaveasfile(mode="w", defaultextension="*.txt")
        if f:
            data = self.txt_area.get(1.0, END)
            f.write(data)
            self.current_file = f.name
            f.close()

    def save_file(self):
        if self.current_file == "no-file":
            self.saveas_file()
        else:
            with open(self.current_file, mode="w") as f:
                f.write(self.txt_area.get(1.0, END))

    def open_file(self, event=""):
        result = filedialog.askopenfilename(initialdir="E:\\ALL", title="Open File Dialog",
                                            filetypes=(("Text File", "*.txt"), ("All File", "*.*")))
        if result:
            with open(result, "r") as f:
                self.txt_area.delete(1.0, END)
                self.txt_area.insert(INSERT, f.read())
                self.current_file = result

    def copy_file(self):
        self.txt_area.clipboard_clear()
        self.txt_area.clipboard_append(self.txt_area.selection_get())

    def paste_file(self):
        self.txt_area.insert(INSERT, self.txt_area.clipboard_get())

    def cut_file(self):
        self.copy_file()
        self.txt_area.delete("sel.first", "sel.last")

    def del_file(self):
        self.txt_area.delete("sel.first", "sel.last")

    def __init__(self, master):
        self.master = master
        master.title("My Notepad")
        master.wm_iconbitmap("notepad.ico")
        master.bind("<Control-o>", self.open_file)
        master.bind("<Control-O>", self.open_file)

        self.txt_area = Text(master, padx=5, pady=5, wrap=WORD, selectbackground="red", bd=2, insertwidth=5, undo=True)
        self.txt_area.pack(fill=BOTH, expand=1)

        self.main_menu = Menu()
        self.master.config(menu=self.main_menu)

        self.file_menu = Menu(self.main_menu, tearoff=False)
        self.main_menu.add_cascade(label="FILE", menu=self.file_menu)
        self.file_menu.add_command(label="New", accelerator="Ctrl+N", command=self.new_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Open", accelerator="Ctrl+O", command=self.open_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Save As", accelerator="Ctrl+D", command=self.saveas_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", accelerator="Ctrl+X", command=self.exit_file)

        self.edit_menu = Menu(self.main_menu, tearoff=False)
        self.main_menu.add_cascade(label="EDIT", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=self.txt_area.edit_undo)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Redo", command=self.txt_area.edit_redo)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=self.cut_file)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Copy", command=self.copy_file)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Paste", command=self.paste_file)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Delete", command=self.del_file)
        self.color_menu = Menu(self.main_menu, tearoff=False)
        self.main_menu.add_cascade(label="COLOR", menu=self.color_menu)
        self.color_menu.add_command(label="Background Color", command=self.change_backcolor)
        self.color_menu.add_command(label="Foreground Color", command=self.change_forecolor)

        # self.font_size = Menu(self.main_menu, tearoff=False)
        # self.main_menu.add_cascade(label="FONT SIZE", menu=self.font_size)
        # self.font_size.add_command(label="Increase Font Size", command=lambda: self.change_font_size(16))
        # self.font_size.add_command(label="Default Font Size", command=lambda: self.change_font_size(12))
        # self.font_size.add_command(label="Decrease Font Size", command=lambda: self.change_font_size(10))


        self.font_size = Menu(self.main_menu, tearoff=False)
        self.main_menu.add_cascade(label="FONT SIZE", menu=self.font_size)
        self.font_size.add_command(label="Set Font Size", command=self.set_font_size_by_number)


        

root = Tk()

b = MyNotepad(root)
root.mainloop()
