from gui import Application
from execute import ExecuteFile
from sys import argv
if __name__ == '__main__':
    if ExecuteFile.EF_VERSION != ExecuteFile.EF_VERSION:
        print('Config File Version Mismatch!')
        exit()
    app = Application(argv[1] if len(argv) > 1 else 'cfg.json')
    app.mainloop()