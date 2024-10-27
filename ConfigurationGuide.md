# Configuration Guide

This guide will help you understand how to configure Term2GUI to suit your needs.

## Quick Start - Hello World

In this part, we will create a simple configuration file that allows you to execute the `echo` command with a custom message.

1. Open your favorite text editor and create a new file named `cfg.json`.
2. Paste the following code into the file:
   ```json
   {
       "title": "Hello World",
       "exec": "echo",
       "version": 2,
       "args": {
           "message": {
              "type": "fmtstr",
              "format": "%s",
              "prompt": "Message"
           }
       }
   }
   ```
3. Save the file.
4. Execute the `main.py` script with the `cfg.json` file as an argument:
    ```sh
    python main.py cfg.json
    ```
5. You should see a window with a text field labeled "Message". Enter your message and click the "Run" button. The message should be printed in the output window.

    The output should be like this:
    ```
    Running: echo Hello World!
    Command executed with exit code: 0
    Standard Output:
    Hello World!

    --------------------------------------------------
    ```

## Structure

### Basic Information

The basic information of the application is defined in the root of the JSON object.

```json
{
    "title": "Your Application Title",
    "exec": "command_to_execute",
    "version": 2
}
```

- **title**: The title of the application. Take blank to use `Untitled - Term2GUI [version]`.
- **exec**: The command to execute. e.g. `g++`, `ffmpeg` etc.
- **version**: The version id of the configuration file.

**Version ID and Version Tag**

| Version ID | Version Tag |
| --- | --- |
| 1 | V1.0 Pre-release |
| 2 | V1.0 Release |

### Arguments

The arguments are defined in the `args` object.
```json
"args": {
    "arg1": {
        "type": "type",
        "some thing": "based on type",
        "prompt": "Prompt"
    },
    "arg2": {
        "type": "type",
        "some thing": "based on type",
        "prompt": "Prompt"
    }
}
```

**An Argument**

A single argument is defined as an object with the following properties:

```json
"arg1": {
    "type": "type",
    "some thing": "based on type",
    "prompt": "Prompt"
}
```

- **type**: The type of the argument.
- **body(something)**: The body of the argument, which is different based on the type.
- **prompt**: The prompt to display in the UI.

**Argument Types and Body**

- **str**: A simple string argument. The body is the value.
    ```json
    "arg1": {
        "type": "str",
        "value": "value when choosed this arg",
        "prompt": "Prompt"
    }
    ```
- **fmtstr**: A formatted string argument. The body is the format string.
    ```json
    "arg2": {
        "type": "fmtstr",
        "format": "%s",
        "prompt": "Prompt"
    }   
    ```
- **bool**: A boolean argument. The body is the value when the argument is true and false. But this is only supported in V1.0 Pre-release. You can use `choose` to replace it.
    ```json
    "arg3": {
        "type": "bool",
        "true": "value when choosed true",
        "false": "value when choosed false",
        "prompt": "Prompt"
    }
    ```
- **choose**: A selection argument. The body is an array of choices. P.S. This is also supported formatted string argument.
    ```json
    "arg4": {
        "type": "choose",
        "options": ["A", "B", "C"],
        "format": "%s is selected",
        "prompt": "Prompt"
    }
    ```

## Try By Yourself - Build a JSON Configuration for G++

### Problem

In this part, we will create a configuration file for the `g++` compiler.

1. Open your favorite text editor and create a new file named `g++.json`.
2. Add some Basic Information.
3. Add the following arguments into the file: Source File, Output File, CPP Standard, O2 Flag and some other Compile Options.
4. Run the `main.py` script with the `g++.json` file as an argument.

### Answer

Content of `g++.json`:
```json
{
	"title": "Compile CPP",
	"version": 2, 
	"exec": "g++",
	"args": {
		"source": {
			"type": "fmtstr",
			"format": "%s",
            "prompt": "Source File"
		},
		"save": {
			"type": "fmtstr",
			"format": "-o %s",
            "prompt": "Save As"
		},
		"std": {
			"type": "choose",
			"options":["14", "11", "98"],
			"default":"11",
			"format": "-std=c++%s",
            "prompt": "CPP Standard"
		},
		"O2": {
			"type": "str",
			"value": "-O2",
            "prompt": "O2"
		},
        "DisableANSI": {
            "type": "str",
            "value": "-ansi",
			"prompt": "Disable ANSI"
        }
	}
}
```

Run Code:
```sh
python main.py g++.json
```

The output should be like this:
```
Running: g++ ../cpp/bit.cpp -o ../cpp/bit -std=c++11 -O2 -ansi
Command executed with exit code: 0

--------------------------------------------------
```

## More Examples

You can find some examples in the `example` directory.

More example can be found [here](https://github.com/gene-2012/T2G-library).
