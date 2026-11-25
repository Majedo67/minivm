import tkinter as tk
from tkinter import ttk, filedialog, messagebox

root = tk.Tk()
root.title("MiniVM")
root.geometry("600x420")
root.configure(bg="#101827")
root.resizable(False, False)

ram = tk.StringVar(value="512 MB")
iso_path = tk.StringVar(value="No ISO selected")


def choose_iso():
    path = filedialog.askopenfilename(
        title="Select operating system ISO",
        filetypes=[("ISO files", "*.iso"), ("All files", "*.*")]
    )
    if path:
        iso_path.set(path)


def start_vm():
    messagebox.showinfo(
        "MiniVM",
        "The interface is ready! The Bochs engine is not connected yet."
    )


tk.Label(
    root,
    text="MiniVM",
    font=("Segoe UI", 28, "bold"),
    fg="#38bdf8",
    bg="#101827"
).pack(pady=(25, 5))

tk.Label(
    root,
    text="LIGHTWEIGHT VIRTUAL MACHINE",
    font=("Segoe UI", 10),
    fg="#94a3b8",
    bg="#101827"
).pack()

panel = tk.Frame(root, bg="#1e293b", padx=25, pady=20)
panel.pack(padx=35, pady=25, fill="x")

tk.Label(
    panel,
    text="Memory (RAM)",
    fg="white",
    bg="#1e293b",
    font=("Segoe UI", 12, "bold")
).pack(anchor="w")

ttk.Combobox(
    panel,
    textvariable=ram,
    values=["256 MB", "512 MB", "1 GB", "2 GB"],
    state="readonly"
).pack(fill="x", pady=(8, 18))

tk.Label(
    panel,
    text="Operating System ISO",
    fg="white",
    bg="#1e293b",
    font=("Segoe UI", 12, "bold")
).pack(anchor="w")

tk.Label(
    panel,
    textvariable=iso_path,
    fg="#94a3b8",
    bg="#1e293b",
    wraplength=470
).pack(anchor="w", pady=8)

tk.Button(
    panel,
    text="Choose ISO",
    command=choose_iso,
    bg="#334155",
    fg="white",
    relief="flat",
    padx=15,
    pady=8
).pack(anchor="w")

tk.Button(
    root,
    text="START VIRTUAL MACHINE",
    command=start_vm,
    bg="#0284c7",
    fg="white",
    font=("Segoe UI", 12, "bold"),
    relief="flat",
    padx=25,
    pady=12
).pack(pady=5)

tk.Label(
    root,
    text="MiniVM • Local Edition",
    fg="#64748b",
    bg="#101827"
).pack(side="bottom", pady=12)

root.mainloop()
