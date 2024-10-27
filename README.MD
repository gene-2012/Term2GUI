# Term2GUI

## Introduction

Term2GUI is a graphical user interface (GUI) application designed to simplify the execution of command-line programs. It reads configuration files in JSON format to dynamically generate a user-friendly interface for setting command-line arguments. The application supports various argument types, including string, formatted string, and boolean.

## Features

- **Dynamic UI Generation**: Automatically generates input fields based on the provided JSON configuration.
- **Argument Types**: See in [`ConfigurationGuide.md`](ConfigurationGuide.md).
- **Real-time Command Preview**: Displays the constructed command before execution.
- **Output Display**: Captures and displays the standard output and error of the executed command.

## Installation

To install and run Term2GUI, follow these steps:

### Download

**Clone the Repository**
```sh
git clone https://github.com/gene-2012/Term2GUI.git
cd Term2GUI
```
or

**Download Release(Windows Only)**

[Download Here](https://github.com/gene-2012/Term2GUI/releases/latest/)


### Build(Optional)

Look at [here](#build-executable) for more details.

## Configuration

The configuration for Term2GUI is defined in a JSON file, `cfg.json` as default. You can find some example in the `example` directory. More example can be found [here](https://github.com/gene-2012/T2G-library).

Here's a basic example of a configuration file:

```json
// cfg.json
{
    "title": "Your Application Title",
    "exec": "command_to_execute",
    "args": {
        "input": {
            "type": "fmtstr",
            "format": "-i %s",
            "prompt": "Input File"
        },
        "output": {
            "type": "fmtstr",
            "format": "%s",
            "prompt": "Output File"
        },
        "option": {
            "type": "bool",
            "true": "-o",
            "false": ""
        },
        "flag": {
            "type": "str",
            "value": "-f"
        }
    }
}
```

## Useage

To run Term2GUI, simply execute the `main.py` script:

```sh
# If you want to use the default configuration filename
python main.py
# Or specify your own config filename
python main.py your_config_filename
```

> **Attention:**
The `main.py` script will automatically detect the `cfg.json` file in the current directory. If you want to use a different configuration file, you need to specify the filename as an argument when running the script.

## Build Executable

To build an executable file from the Python script, you can use tools like PyInstaller. Here's a basic example:

```sh
virtualenv venv
. venv/Scripts/activate
pip install pyinstaller
pyinstaller -F main.py
```

This will create an executable file named `main.exe` in directory `./dist/`.

## Contact

For any questions or feedback, please contact me at:
- **Email**: [geneluo@qq.com](mailto://geneluo@qq.com).
- **Github**: [@gene-2012](https://github.com/gene-2012).

You can also issue a pull request or open an issue on the GitHub repository.

## License

This project is licensed under the GPL 3.0 License.