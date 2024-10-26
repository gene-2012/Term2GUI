import json

class ExecuteFile(object):
    def __init__(self, config):
        try:
            with open(config, "r") as f:
                self.config = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Can't find file {config}.")
        
        self.title = self.config.get('title', 'Untitled - Term2GUI V1.0')
        self.exe = self.config.get('exec', '')
        self.arg_list = self.config.get('args', {})
        self.supported = {
            'bool': self.add_bool_arg,
            'str': self.add_str_arg,
            'fmtstr': self.add_formated_arg
        }
        self.args = [self.exe]

    def get_type(self, arg_name) -> str:
        return self.arg_list.get(arg_name, {}).get('type', '')

    def get_prompt(self) -> list:
        return [arg.get('prompt', arg_name) for arg_name, arg in self.arg_list.items()]

    def add_arg(self, arg_name, *args, **kwargs) -> None:
        add_func = self.supported.get(self.get_type(arg_name))
        if not add_func:
            raise TypeError(f"Type {self.get_type(arg_name)} not supported.")
        if kwargs:
            add_func(arg_name, **kwargs)
        else:
            add_func(arg_name)

    def add_bool_arg(self, arg_name: str, value: bool = True) -> None:
        """
        json e.g.
        {"arg_name" : {"type" : "bool", "true" : "some arg", "false" : "some arg"}}
        """
        arg_item = self.arg_list.get(arg_name, {})
        if arg_item.get('type') != 'bool':
            raise TypeError(f"Expected: bool, Find: {arg_item.get('type')}.")
        if value and arg_item.get('true'):
            self.args.append(arg_item['true'])
        elif not value and arg_item.get('false'):
            self.args.append(arg_item['false'])

    def add_str_arg(self, arg_name: str) -> None:
        """
        json e.g.
        {"arg_name" : {"type":"str", "value":"value"}}
        """
        arg_item = self.arg_list.get(arg_name, {})
        if arg_item.get('type') != 'str':
            raise TypeError(f"Expected: str, Find: {arg_item.get('type')}.")
        if arg_item.get('value'):
            self.args.append(arg_item['value'])

    def add_formated_arg(self, arg_name: str, value) -> None:
        """
        json e.g.
        {"arg_name" : {"type":"fmtstr", "format":"%s"}}
        """
        if not value:
            return
        arg_item = self.arg_list.get(arg_name, {})
        if arg_item.get('type') != 'fmtstr':
            raise TypeError(f"Expected: fmtstr, Find: {arg_item.get('type')}.")
        if arg_item.get('format'):
            self.args.append(arg_item['format'] % value)

    def __str__(self) -> str:
        return ' '.join(self.args)

if __name__ == '__main__':
    try:
        ef = ExecuteFile('cfg.json')
        ef.add_formated_arg('source', input('Source File: '))
        ef.add_formated_arg('save', input('Save As: '))
        ef.add_formated_arg('std', input('Standard (Leave Blank to Use C++11): '))
        if input('O2(y/n): ').lower() == 'y':
            ef.add_str_arg('O2')
        print(f'Running {ef} ...')
        from os import system
        system(f'{ef}')
    except Exception as e:
        print(f"An error occurred: {e}")