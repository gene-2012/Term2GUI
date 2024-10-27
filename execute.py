import json
import warnings

class ExecuteFile(object):
    EF_VERSION = 2

    def __init__(self, config):
        """
        Initialize the ExecuteFile class.

        :param config: Path to the configuration file.
        :raises FileNotFoundError: If the configuration file does not exist.
        """
        try:
            with open(config, "r") as f:
                self.config = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Can't find file {config}.")

        self.cfg_version = self.config.get('version', ExecuteFile.EF_VERSION)
        self.title = self.config.get('title', 'Untitled - Term2GUI V1.0')
        self.exe = self.config.get('exec', '')
        self.arg_list = self.config.get('args', {})
        self.supported = {
            'bool': self.add_bool_arg,
            'str': self.add_str_arg,
            'fmtstr': self.add_formated_arg,
            'choose': self.add_choose_arg,
            'file': self.add_file_arg,
            'path': self.add_path_arg,
            'num': self.add_num_arg
        }
        self.args = [self.exe]

        if self.cfg_version != ExecuteFile.EF_VERSION:
            self.handle_version_mismatch()

    def handle_version_mismatch(self):
        """
        Handle the case where the configuration file version does not match the current version.

        :raises UserWarning: If the configuration file version does not match the current version.
        """
        warnings.warn(
            f"ExecuteFile json version {self.cfg_version} does not match with current version {ExecuteFile.EF_VERSION}. "
            f"Consider updating your configuration file.",
            UserWarning
        )

    def get_type(self, arg_name) -> str:
        """
        Get the type of a specified argument.

        :param arg_name: The name of the argument.
        :return: The type of the argument.
        """
        return self.arg_list.get(arg_name, {}).get('type', '')

    def get_prompt(self) -> list:
        """
        Get the prompt messages for all arguments.

        :return: A list of prompt messages for the arguments.
        """
        return [arg.get('prompt', arg_name) for arg_name, arg in self.arg_list.items()]

    def add_arg(self, arg_name, *args, **kwargs) -> None:
        """
        Add an argument to the command line arguments list.

        :param arg_name: The name of the argument.
        :param args: Positional arguments.
        :param kwargs: Keyword arguments.
        :raises TypeError: If the argument type is not supported.
        """
        add_func = self.supported.get(self.get_type(arg_name))
        if not add_func:
            raise TypeError(f"Type {self.get_type(arg_name)} not supported.")
        if kwargs:
            add_func(arg_name, **kwargs)
        else:
            add_func(arg_name)

    def add_bool_arg(self, arg_name: str, value: bool = True) -> None:
        """
        Add a boolean argument to the command line arguments list.

        :param arg_name: The name of the boolean argument.
        :param value: The value of the boolean argument (default is True).
        :raises TypeError: If the argument type is not 'bool'.
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
        Add a string argument to the command line arguments list.

        :param arg_name: The name of the string argument.
        :raises TypeError: If the argument type is not 'str'.
        """
        arg_item = self.arg_list.get(arg_name, {})
        if arg_item.get('type') != 'str':
            raise TypeError(f"Expected: str, Find: {arg_item.get('type')}.")
        if arg_item.get('value'):
            self.args.append(arg_item['value'])

    def add_formated_arg(self, arg_name: str, value) -> None:
        """
        Add a formatted string argument to the command line arguments list.

        :param arg_name: The name of the formatted string argument.
        :param value: The value to be formatted.
        :raises TypeError: If the argument type is not 'fmtstr'.
        """
        arg_item = self.arg_list.get(arg_name, {})
        if arg_item.get('type') != 'fmtstr':
            raise TypeError(f"Expected: fmtstr, Find: {arg_item.get('type')}.")
        if not value: 
            return
        if arg_item.get('format', '%s'):
            self.args.append(arg_item['format'] % value)

    def add_choose_arg(self, arg_name: str, value: str) -> None:
        """
        Add a choice argument to the command line arguments list.

        :param arg_name: The name of the choice argument.
        :param value: The selected value.
        :raises TypeError: If the argument type is not 'choose'.
        """
        arg_item = self.arg_list.get(arg_name, {})
        if arg_item.get('type') != 'choose':
            raise TypeError(f"Expected: choose, Find: {arg_item.get('type')}.")
        options = arg_item.get('options', [])
        default = arg_item.get('default', '')
        format = arg_item.get('format', '%s')
        if value not in options:
            print(f"Invalid value: {value}, using default: {default}")
            value = default
        self.args.append(format % value)

    def add_file_arg(self, arg_name: str, value: str) -> None:
        """
        Add a file argument to the command line arguments list.

        :param arg_name: The name of the file argument.
        :param value: The file path.
        :raises TypeError: If the argument type is not 'file'.
        """
        arg_item = self.arg_list.get(arg_name, {})
        if arg_item.get('type') != 'file':
            raise TypeError(f"Expected: file, Find: {arg_item.get('type')}.")
        if not value: 
            return
        if arg_item.get('format', '%s'):
            self.args.append(arg_item['format'] % value)

    def add_path_arg(self, arg_name: str, value: str) -> None:
        """
        Add a path argument to the command line arguments list.

        :param arg_name: The name of the path argument.
        :param value: The path.
        :raises TypeError: If the argument type is not 'path'.
        """
        arg_item = self.arg_list.get(arg_name, {})
        if arg_item.get('type') != 'path':
            raise TypeError(f"Expected: path, Find: {arg_item.get('type')}.")
        if not value: 
            return
        if arg_item.get('format', '%s'):
            self.args.append(arg_item['format'] % value)

    def add_num_arg(self, arg_name: str, value: int) -> None:
        """
        Add a numeric argument to the command line arguments list.

        :param arg_name: The name of the numeric argument.
        :param value: The numeric value.
        :raises TypeError: If the argument type is not 'num'.
        """
        arg_item = self.arg_list.get(arg_name, {})
        if arg_item.get('type') != 'num':
            raise TypeError(f"Expected: num, Find: {arg_item.get('type')}.")
        if not value: 
            return
        if arg_item.get('min') and value < arg_item['min']:
            print(f"Value {value} is less than min {arg_item['min']}, using min")
            value = arg_item['min']
        if arg_item.get('max') and value > arg_item['max']:
            print(f"Value {value} is greater than max {arg_item['max']}, using max")
            value = arg_item['max']
        if arg_item.get('format', '%d'):
            self.args.append(arg_item['format'] % value)

    def __str__(self) -> str:
        """
        Return the command line arguments as a string.

        :return: A string representation of the command line arguments.
        """
        return ' '.join(self.args)

if __name__ == '__main__':
    try:
        ef = ExecuteFile('examples/G++Basic.json')
        ef.add_formated_arg('source', input('Source File: '))
        ef.add_formated_arg('save', input('Save As: '))
        ef.add_choose_arg('std', int(input(f'Standard{ef.arg_list["std"]["options"]}(1-3): ')))
        if input('O2(y/n): ').lower() == 'y':
            ef.add_str_arg('O2')
        print(f'Running {ef} ...')
        from os import system
        system(f'{ef}')
    except Exception as e:
        print(f"An error occurred: {e}")