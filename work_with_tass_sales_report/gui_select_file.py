from tkinter import filedialog, messagebox, Tk


def select_file_via_gui():
    root = Tk()
    root.withdraw()

    try:
        file_path = filedialog.askopenfilename(
            initialdir="/Users/evgeniy/Downloads",
            title="Select file",
            filetypes=[("Tables", "*.xlsx")]  # You can customize the file types here
        )

        if file_path:
            return file_path
        else:
            messagebox.showwarning("Warning", "You haven't chosen a file. Program terminated.")

    finally:
        root.destroy()
