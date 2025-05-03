import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import threading
import os

class ArticleGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Article Generator")
        self.root.geometry("700x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#f2f2f2")

        # Title
        title_label = tk.Label(
            root,
            text="🤖 AI Article Generator",
            font=("Segoe UI", 24, "bold"),
            bg="#f2f2f2",
            fg="#333"
        )
        title_label.pack(pady=20)

        # Domain Selection
        domain_frame = tk.Frame(root, bg="#f2f2f2")
        domain_frame.pack(pady=10)

        tk.Label(domain_frame, text="Select Domain:", font=("Segoe UI", 12), bg="#f2f2f2").pack(side=tk.LEFT, padx=10)

        self.domain_var = tk.StringVar()
        self.domain_dropdown = ttk.Combobox(
            domain_frame,
            textvariable=self.domain_var,
            values=["AI", "Health", "Tech", "Business", "Data Science", "Self Improvement"],
            state="readonly",
            width=20,
            font=("Segoe UI", 11)
        )
        self.domain_dropdown.pack(side=tk.LEFT)
        self.domain_dropdown.set("AI")  # Default value

        # Button Frame
        btn_frame = tk.Frame(root, bg="#f2f2f2")
        btn_frame.pack(pady=15)

        self.buttons = {
            "Generate Topics": self.run_generate_topics,
            "Generate Articles": self.run_generate_articles,
            "Cleanup Old Files": self.run_cleanup,
            "View Output Folder": self.open_output_folder
        }

        self.btn_list = []
        for idx, (text, cmd) in enumerate(self.buttons.items()):
            btn = tk.Button(
                btn_frame,
                text=text,
                width=22,
                command=cmd,
                bg="#0078D7",
                fg="white",
                font=("Segoe UI", 11),
                relief="flat",
                padx=10,
                pady=8
            )
            btn.grid(row=idx // 2, column=idx % 2, padx=10, pady=6)
            self.btn_list.append(btn)

        # Status Bar / Log Box
        self.status = tk.Label(
            root,
            text="Ready",
            bd=1,
            relief=tk.SUNKEN,
            anchor="w",
            font=("Segoe UI", 10),
            bg="#e0e0e0"
        )
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

        # Progress Bar
        self.progress = ttk.Progressbar(
            root,
            orient="horizontal",
            length=550,
            mode="indeterminate"
        )
        self.progress.pack(pady=10)

        # Log Box
        self.log_box = tk.Text(
            root,
            height=10,
            width=80,
            state='disabled',
            wrap='word',
            font=("Segoe UI", 10),
            bg="#ffffff",
            fg="#333"
        )
        self.log_box.pack(pady=10)

        # Thread Management
        self.running_thread = None

    def log(self, message):
        self.log_box.config(state='normal')
        self.log_box.insert(tk.END, f"{message}\n")
        self.log_box.config(state='disabled')
        self.log_box.see(tk.END)

    def toggle_buttons(self, enable=True):
        for btn in self.btn_list:
            btn.config(state=tk.NORMAL if enable else tk.DISABLED)

    def run_script_in_thread(self, script_name, use_domain=False):
        self.toggle_buttons(False)
        self.progress.start()

        def target():
            try:
                domain = self.domain_var.get() if use_domain else "AI"
                result = subprocess.run(
                    ["python", script_name, domain],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace"
                )

                if result.returncode == 0:
                    self.log(f"[SUCCESS] {script_name}")
                    self.log(result.stdout)
                else:
                    self.log(f"[ERROR] {script_name}")
                    self.log(result.stderr)
            except Exception as e:
                self.log(f"[CRITICAL] Failed to run {script_name}: {str(e)}")
            finally:
                self.root.after(0, self.cleanup_after_script)

        self.running_thread = threading.Thread(target=target)
        self.running_thread.start()

    def cleanup_after_script(self):
        self.progress.stop()
        self.toggle_buttons(True)
        self.running_thread = None

    def run_generate_topics(self):
        self.log("[ACTION] Running: Generate Topics")
        self.run_script_in_thread("generate_topics.py", use_domain=True)

    def run_generate_articles(self):
        self.log("[ACTION] Running: Generate Articles")
        self.run_script_in_thread("generate_all_articles.py")

    def run_cleanup(self):
        self.log("[ACTION] Running: Cleanup Old Files")
        self.run_script_in_thread("cleanup_old_articles.py")

    def open_output_folder(self):
        if os.path.exists("outputs"):
            os.startfile("outputs") if os.name == 'nt' else subprocess.run(["open", "outputs"])
        else:
            messagebox.showinfo("Info", "Output folder does not exist yet.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ArticleGeneratorApp(root)
    root.mainloop()