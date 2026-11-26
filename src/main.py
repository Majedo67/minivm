import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import subprocess

root = tk.Tk()
root.title("MiniVM")
root.geometry("600x420")
root.configure(bg="#101827")
root.resizable(False, False)

ram = tk.StringVar(value="256 MB")

project_dir = Path(__file__).resolve().parent.parent
bochs_exe = Path(r"C:\Program Files\Bochs-3.1\bochs.exe")
config_file = project_dir / "config" / "bochsrc"


def start_vm():
    if not bochs_exe.is_file():
        messagebox.showerror(
            "Bochs not found",
            "Bochs was not found at:\n" + str(bochs_exe)
        )
        return

    if not config_file.is_file():
        messagebox.showerror(
            "Configuration missing",
            "Could not find config\\bochsrc in the MiniVM folder."
        )
        return

    try:
        config_text = config_file.read_text(encoding="utf-8")
        ram_mb = {"256 MB": 256, "512 MB": 512, "1 GB": 1024, "2 GB": 2048}[ram.get()]
        lines = config_text.splitlines()
        updated = []
        replaced = False

        for line in lines:
            if line.strip().lower().startswith("megs:"):
                updated.append(f"megs: {ram_mb}")
                replaced = True
            else:
                updated.append(line)

        if not replaced:
            updated.insert(0, f"megs: {ram_mb}")

        launch_config = project_dir / "config" / "bochsrc.launch"
        launch_config.write_text("\n".join(updated) + "\n", encoding="utf-8")

        subprocess.Popen(
            [str(bochs_exe), "-f", str(launch_config)],
            cwd=str(project_dir)
        )
    except Exception as error:
        messagebox.showerror("MiniVM error", str(error))


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
    text="Operating System",
    fg="white",
    bg="#1e293b",
    font=("Segoe UI", 12, "bold")
).pack(anchor="w")

tk.Label(
    panel,
    text="MiniVM OS 1.0 (built-in disk image)",
    fg="#94a3b8",
    bg="#1e293b"
).pack(anchor="w", pady=8)

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
