# Completion App

Completion is an application powered by OpenAI. The purpose of this project is to automate text completion with a bulk input. Check out [ChatGPT and OpenAI documentaion](https://platform.openai.com/docs/introduction).

## Command Line Version

### Dependency
Install dependency  
`$pip install -r requirements.txt`

### Input File
The application accepts a CSV file as an input with the following required column headers: `Topic`, `Prompt`, `User`, `System`.

`Topic` - The topic of the information that you want to generate.  
`Prompt` - This is the command you want to feed to the AI.  
`User` - Same as the Prompt, this is required especially when you use the `gpt-4` model.  
`System` - The parameter you feed to the AI, telling it what is its role (same as context).

### Output
CSV file output are generated and are saved on a folder called `csvfiles`. You have to manually create this in the root directory of the application.

### OpenAI API Key

Create your `creds.py` in the root folder and have a variable:  
`OPENAI_API_KEY = '<YOUR API KEY HERE>'`  

Please visit [OpenAI](https://platform.openai.com/) to get your API Key.

### Run the Application
`$python complete.py`  

When you run the application in the command line, it will ask for your desired OpenAI model (_just use the appropriate number_), if you want to use `gpt-4` model, make sure your account has `gpt-4` enabled. As of this writing, gpt-4 is invite-only.

## GUI Version
I created a GUI version of this application. If you want to test it on the fly just run the `gui.py` file.  

If you want an executable application, you can use any Python packages that converts Python code into an executable file. I have great success with PyInstall.  

To learn more about how to use PyInstaller, check out Using [PyInstaller to Easily Distribute Python Applications](https://realpython.com/pyinstaller-python/).

## How to use the GUI version

The application is very straight-forward.  

1. Supply your OpenAI API Key in the `OpenAI Options` tab.
2. Select your model. If you did not choose a model, the application will default to `gpt-4`.
3. Choose your input CSV file using the Browse button. (_Please refer to the `Input File` section_)
4. Run the application using the `Run` button.

_Note: The application will show `Not Responding` when you run the application. Don't close it and let it run._