from tkinter import filedialog, messagebox, Tk


def select_file_via_gui():
    root = Tk()
    root.withdraw()

    choose_file = filedialog.askopenfile(initialdir="/Users/evgeniy/Downloads", title="Select file")

    if choose_file:
        return choose_file.name
    else:
        messagebox.showwarning("Warning", "You haven't chosen a file. Program terminated.")

    root.destroy()
