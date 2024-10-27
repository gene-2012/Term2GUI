import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess
from execute import ExecuteFile
import warnings

class Application(tk.Tk):
    APP_VERSION = 2

    def __init__(self, config_file):
        super().__init__()
        self.ef = ExecuteFile(config_file)
        self.title(self.ef.title)
        self.entries = {}
        self.bool_vars = {}
        self.str_vars = {}
        self.create_widgets()

    def create_widgets(self):
        row = 0
        num_rows = len(self.ef.arg_list) + 1

        for arg_name, arg_item in self.ef.arg_list.items():
            arg_type = arg_item.get('type', '')
            prompt = arg_item.get('prompt', arg_name)
            label = tk.Label(self, text=prompt + ":")
            label.grid(row=row, column=0, padx=10, pady=5, sticky='e')

            if arg_type == 'bool':
                var = tk.BooleanVar()
                checkbutton = tk.Checkbutton(self, variable=var)
                checkbutton.grid(row=row, column=1, padx=10, pady=5, sticky='w')
                self.bool_vars[arg_name] = var
            elif arg_type in ['str', 'fmtstr', 'num']:
                entry = tk.Entry(self)
                entry.grid(row=row, column=1, padx=10, pady=5, sticky='ew')
                self.entries[arg_name] = entry
            elif arg_type == 'file':
                entry = tk.Entry(self)
                entry.grid(row=row, column=1, padx=10, pady=5, sticky='ew')
                self.entries[arg_name] = entry
                method = arg_item.get('method', 'open')
                extensions = arg_item.get('extensions', [])
                filetypes = [(f"{method.capitalize()} files", ' '.join(extensions)), ('All files', '*.*')]
                if method == 'open':
                    browse_button = tk.Button(self, text="Browse", command=lambda e=entry, ft=filetypes: self.open_file_dialog(e, ft))
                elif method == 'save':
                    browse_button = tk.Button(self, text="Browse", command=lambda e=entry, ft=filetypes: self.save_file_dialog(e, ft))
                else:
                    raise ValueError(f"Invalid method for file type: {method}")
                browse_button.grid(row=row, column=2, padx=10, pady=5, sticky='w')
            elif arg_type == 'path':
                entry = tk.Entry(self)
                entry.grid(row=row, column=1, padx=10, pady=5, sticky='ew')
                self.entries[arg_name] = entry
                browse_button = tk.Button(self, text="Browse", command=lambda e=entry: self.open_directory_dialog(e))
                browse_button.grid(row=row, column=2, padx=10, pady=5, sticky='w')
            elif arg_type == 'choose':
                options = arg_item.get('options', [])
                var = tk.StringVar(value=arg_item.get('default', options[0]))
                dropdown = tk.OptionMenu(self, var, *options)
                dropdown.grid(row=row, column=1, padx=10, pady=5, sticky='ew')
                self.str_vars[arg_name] = var
            else:
                raise ValueError(f"Invalid argument type: {arg_type}")

            row += 1

        # Run Button
        self.run_button = tk.Button(self, text="Run", command=self.run_command)
        self.run_button.grid(row=row, column=0, columnspan=2, padx=10, pady=10)

        # Result Text
        self.command_result = tk.Text(self, wrap=tk.WORD)  # Text Grid
        self.command_result.grid(row=0, column=3, rowspan=num_rows + 1, padx=10, pady=5, sticky='nsew')

        # Configure grid weights to make the right column expand
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(list(range(num_rows + 1)), weight=1)

    def open_file_dialog(self, entry, filetypes):
        file_path = filedialog.askopenfilename(filetypes=filetypes)
        if file_path:
            entry.delete(0, tk.END)
            entry.insert(0, file_path)

    def save_file_dialog(self, entry, filetypes):
        file_path = filedialog.asksaveasfilename(filetypes=filetypes)
        if file_path:
            entry.delete(0, tk.END)
            entry.insert(0, file_path)

    def open_directory_dialog(self, entry):
        directory_path = filedialog.askdirectory()
        if directory_path:
            entry.delete(0, tk.END)
            entry.insert(0, directory_path)

    def run_command(self):
        try:
            self.ef.args = [self.ef.exe]  # Reset args
            for arg_name, arg_item in self.ef.arg_list.items():
                arg_type = arg_item.get('type', '')
                add_func = self.ef.supported.get(arg_type)
                try:
                    if arg_type == 'bool':
                        value = self.bool_vars[arg_name].get()
                        add_func(arg_name, value)
                    elif arg_type in ['str', 'fmtstr', 'file', 'path', 'num']:
                        value = self.entries[arg_name].get()
                        add_func(arg_name, value)
                    elif arg_type == 'choose':
                        value = self.str_vars[arg_name].get()
                        add_func(arg_name, value)
                except Warning as wr:
                    messagebox.showwarning("Warning", f"A warning occurred: {wr}")
            command = str(self.ef)
            self.command_result.insert(tk.END, f"Running: {command}\n")
            # Run the command and capture the output
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()

            # Clear the Text widget and insert the output
            # self.command_result.delete(1.0, tk.END)  # Uncomment to clear previous output
            self.command_result.insert(tk.END, f"Command executed with exit code: {process.returncode}\n")
            if stdout:
                self.command_result.insert(tk.END, "Standard Output:\n")
                self.command_result.insert(tk.END, stdout)
            if stderr:
                self.command_result.insert(tk.END, "\nStandard Error:\n")
                self.command_result.insert(tk.END, stderr)
            self.command_result.insert(tk.END, f"\n{'-'*50}\n")
            self.command_result.see(tk.END)
        except Warning as wr:
            messagebox.showwarning("Warning", f"A warning occurred: {wr}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def handle_version_mismatch(self):
        if self.ef.cfg_version != ExecuteFile.EF_VERSION:
            warnings.warn(
                f"ExecuteFile json version {self.ef.cfg_version} does not match with current version {ExecuteFile.EF_VERSION}. "
                f"Consider updating your configuration file.",
                UserWarning
            )
            messagebox.showwarning("Version Mismatch", 
                                   f"ExecuteFile json version {self.ef.cfg_version} does not match with current version {ExecuteFile.EF_VERSION}. "
                                   f"Consider updating your configuration file.")

    def handle_outdated_args_type(self, *args, **kwargs):
        warnings.warn(
            f"The argument type for {args} is outdated. Consider updating your configuration file.",
            DeprecationWarning
        )
        messagebox.showwarning("Outdated Argument Type", 
                               f"The argument type for {args} is outdated. Consider updating your configuration file.")

if __name__ == "__main__":
    app = Application('cfg.json')
    app.handle_version_mismatch()
    app.mainloop()