from gui import Application
from sys import argv
if __name__ == '__main__':
    app = Application(argv[1] if len(argv) > 1 else 'cfg.json')
    app.mainloop()