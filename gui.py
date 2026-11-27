import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from recovery import recover, NAME

def run(apply):
    if not messagebox.askyesno("Safety", "Have you completely closed ChatGPT and Codex?"):
        return
    db = filedialog.askopenfilename(title="Select "+NAME)
    if not db:
        return
    dest = filedialog.askdirectory(title="Choose private backup location")
    if not dest:
        return
    if apply and not messagebox.askyesno("Confirm", "Attempt recovery on original after verified backup and copy test?"):
        return
    try:
        result = recover(Path(db), Path(dest), apply)
        messagebox.showinfo("Integrity OK", "Backup: "+str(result))
    except Exception as e:
        messagebox.showerror("Stopped", str(e))
root = tk.Tk()
root.title("Codex Recovery Toolkit")
root.geometry("480x250")
tk.Label(root,text="Codex Recovery Toolkit",font=("Segoe UI",20)).pack(pady=20)
tk.Button(root,text="Backup and test copy",command=lambda:run(False)).pack(pady=8)
tk.Button(root,text="Backup, test and recover original",command=lambda:run(True)).pack(pady=8)
tk.Label(root,text="Independent utility • No automatic deletion").pack(pady=12)
root.mainloop()
