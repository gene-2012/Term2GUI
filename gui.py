import tkinter as tk
from tkinter import messagebox
import subprocess
from execute import ExecuteFile

class Application(tk.Tk):
    def __init__(self, config_file):
        super().__init__()
        self.ef = ExecuteFile(config_file)
        self.title(self.ef.title)
        self.entries = {}
        self.bool_vars = {}
        self.create_widgets()

    def create_widgets(self):
        row = 0
        num_rows = len(self.ef.arg_list) + 1

        for arg_name, arg_item in self.ef.arg_list.items():
            arg_type = arg_item.get('type', '')
            prompt = arg_item.get('prompt', arg_name)
            label = tk.Label(self, text=prompt + ":")
            label.grid(row=row, column=0, padx=10, pady=5, sticky='e')

            if arg_type == 'str':
                var = tk.BooleanVar()
                checkbutton = tk.Checkbutton(self, variable=var)
                checkbutton.grid(row=row, column=1, padx=10, pady=5, sticky='w')
                self.bool_vars[arg_name] = var
            elif arg_type == 'fmtstr':
                entry = tk.Entry(self)
                entry.grid(row=row, column=1, padx=10, pady=5, sticky='ew')
                self.entries[arg_name] = entry
            elif arg_type == 'bool':
                var = tk.BooleanVar()
                checkbutton = tk.Checkbutton(self, variable=var)
                checkbutton.grid(row=row, column=1, padx=10, pady=5, sticky='w')
                self.bool_vars[arg_name] = var

            row += 1

        # Run Button
        self.run_button = tk.Button(self, text="Run", command=self.run_command)
        self.run_button.grid(row=row, column=0, columnspan=2, padx=10, pady=10)

        # Result Text
        self.command_result = tk.Text(self, wrap=tk.WORD)  # Text Grid
        self.command_result.grid(row=0, column=2, rowspan=num_rows + 1, padx=10, pady=5, sticky='nsew')

        # Configure grid weights to make the right column expand
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(list(range(num_rows + 1)), weight=1)

    def run_command(self):
        try:
            self.ef.args = [self.ef.exe]  # Reset args
            for arg_name, arg_item in self.ef.arg_list.items():
                arg_type = arg_item.get('type', '')
                add_func = self.ef.supported.get(arg_type)
                if arg_type == 'str':
                    if self.bool_vars[arg_name].get():
                        add_func(arg_name)
                elif arg_type == 'fmtstr':
                    value = self.entries[arg_name].get()
                    add_func(arg_name, value)
                elif arg_type == 'bool':
                    value = self.bool_vars[arg_name].get()
                    add_func(arg_name, value)
            command = str(self.ef)
            print(f'Running {command} ...')

            # Run the command and capture the output
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()

            # Clear the Text widget and insert the output
            # self.command_result.delete(1.0, tk.END)
            self.command_result.insert(tk.END, f"Command executed with exit code: {process.returncode}\n")
            if stdout:
                self.command_result.insert(tk.END, "Standard Output:\n")
                self.command_result.insert(tk.END, stdout)
            if stderr:
                self.command_result.insert(tk.END, "\nStandard Error:\n")
                self.command_result.insert(tk.END, stderr)
            self.command_result.insert(tk.END, f"\n{'-'*50}\n")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


if __name__ == "__main__":
    app = Application('cfg.json')
    app.mainloop()