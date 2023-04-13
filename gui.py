# gui.py
from pathlib import Path
import PySimpleGUI as sg
import os
import openai
import pandas as pd
import datetime
import os.path
import time
import csv
import creds
import logging

# Convert rows into ascii
def convert_row( row ):
  row_dict = {}
  for key, value in row.items():
    keyAscii = key.encode('ascii', 'ignore' ).decode()
    valueAscii = value.encode('ascii','ignore').decode()
    row_dict[ keyAscii ] = valueAscii
  return row_dict

# Use gpt-4 model
def gpt_4(user, system):

  response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
      {"role": "system", "content": system},
      {"role": "user", "content": user}
    ]
  )
  return response

# Use gpt-3.5-turbo model
def gpt_3_5_turbo(user):

  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "user", "content": user}
    ]
  )
  return response

# Use gpt-3.5 model
def text_davinci_003(user, max_tokens):

  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=user,
    max_tokens=max_tokens,
    temperature=0
  )
  return response

def main():
  # 1st tab elements
  input_file_column = [
    [ sg.T("Choose your model:"), 
      sg.Button("gpt-4"), 
      sg.Button("gpt-3.5-turbo"), 
      sg.Button("text-davinci-003")
    ],
    [sg.T("")],
    [sg.T("Choose your CSV input file (Headers: Topic, Prompt, System, User)")],
    [sg.Text("Choose a file: "), sg.Input(), sg.FileBrowse(key="-IN-")], 
    [sg.Button("Save")]
  ]

  run_application_text = [
    [sg.T("")],
    [sg.T("Run the Completion application:")]
  ]

  run_button = [
    [sg.Button("Run", bind_return_key=True)]
  ]

  # Window to show the process log
  log_column = [
      [sg.Multiline(size=(110, 30), echo_stdout_stderr=True, reroute_stdout=True, autoscroll=True, background_color='black', text_color='white', key='-MLINE-')]
  ]

  # 2nd tab elements
  openai_api_key = [
    [sg.T("")],
    [sg.T("Get your OpenAI API Key here: https://platform.openai.com/docs/api-reference",  enable_events=True,)],
    [sg.T("Your OpenAI API Key: "), sg.Input(key="-API_KEY-", password_char='*')],
  ]

  # ----- 1st Tab Layout -----
  layout1 = [
    [
      sg.Column(input_file_column),
      sg.VSeperator(),
      sg.Column(log_column) 
    ],
    [
      sg.HSeparator(pad=(10,0))
    ],
    [
      sg.Column(run_application_text, justification='center')
    ],
    [
      sg.Column(run_button, justification='center')
    ]
  ]

  # ----- 2nd Tab Layout -----
  layout2 = [
    [
      sg.Column(openai_api_key)
    ]
  ]

  # Create tab group
  tabgrp = [
    [
      sg.TabGroup(
        [
          [
            sg.Tab('App Options', layout1, tooltip='App Options', border_width =10, element_justification= 'center'),
            sg.Tab('OpenAI Options', layout2, tooltip='OpenAI Options', border_width =10, element_justification= 'center')
          ]
        ]
      )
    ]
  ]

  window = sg.Window("Completion App", tabgrp)

  # Initialized variables
  choose_model = ''
  input_filename = ''

  while True:
    event, values = window.read()
    
    if event in (sg.WIN_CLOSED, 'Exit'):
      break
    
    elif event == "Save":
      input_filename = values["-IN-"]

      if input_filename and Path(input_filename).is_file():
        old_directory = Path(input_filename).parent
        directory = sg.popup_get_folder("", no_window=True)

        if directory and Path(directory).is_dir():
          if Path(directory) != old_directory:
            new_path = Path(directory).joinpath(Path(input_filename).name)
            Path(input_filename).replace(new_path)
            input_filename = str(new_path)
            print(f'\nInput filepath: {input_filename}')
            window.Refresh()

    elif event == 'gpt-4':
      choose_model = '1'
      print(f'\nNow using gpt-4 model\n')
      window.Refresh()
      window['gpt-4'].update(disabled=True)
      window['gpt-3.5-turbo'].update(disabled=True)
      window['text-davinci-003'].update(disabled=True)
    
    elif event == 'gpt-3.5-turbo':
      choose_model = '2'
      print(f'\nNow using gpt-3.5-turbo model\n')
      window.Refresh()
      window['gpt-4'].update(disabled=True)
      window['gpt-3.5-turbo'].update(disabled=True)
      window['text-davinci-003'].update(disabled=True)

    elif event == 'text-davinci-003':
      choose_model = '3'
      print(f'\nNow using text-davinci-003 model\n')
      window.Refresh()
      window['gpt-4'].update(disabled=True)
      window['gpt-3.5-turbo'].update(disabled=True)
      window['text-davinci-003'].update(disabled=True)

    elif event == 'Run':

      # Assign the API Key
      openai.api_key = values["-API_KEY-"]

      # If user forgot to choose a model
      if choose_model == '':
        choose_model = '1'
        print(f'\nYou did not choose a model, defaulting to gpt-4.\n')
        window.Refresh()
        window['gpt-4'].update(disabled=True)
        window['gpt-3.5-turbo'].update(disabled=True)
        window['text-davinci-003'].update(disabled=True)
      
      window['Run'].update(disabled=True)
      # User chooses a model
      # choose_model = input('1. gpt-4\n2. gpt-3.5-turbo\n3. text-davinci-003\n\nEnter the number that corresponds to the model: ')
      
      time_start = datetime.datetime.now().replace(microsecond=0)
      directory = os.path.dirname(os.path.realpath(__file__))

      topic_list = []
      prompt_list = []
      output_list = []

      with open(input_filename, encoding='unicode_escape') as f:
        reader = csv.DictReader(f)

        for line in reader:

          row_time_start = datetime.datetime.now().replace(microsecond=0)

          converted_row = convert_row( line )
          # prompt = converted_row['Prompt']
          topic = converted_row['Topic']
          system = converted_row['System']
          user = converted_row['User']

          logging.basicConfig(level=logging.DEBUG, filename='error.log')

          try:
            match choose_model:
              case '1':
                print(f'\nWaiting for a response...\n')
                window.Refresh()
                response = gpt_4(user, system)
              case '2':
                print(f'\nWaiting for a response...\n')
                window.Refresh()
                response = gpt_3_5_turbo(user)
              case '3':
                max_tokens = input('\nTokens to spend (between 1 to 4,097)?\nEnter token: \n')
                print(f'\nWaiting for a response...\n')
                window.Refresh()
                response = text_davinci_003(user, int(max_tokens))

            print(f'{response.choices[0].message.content}\n')
            print(f'Usage: Prompt tokens: {response.usage.prompt_tokens}, Completion tokens: {response.usage.completion_tokens}, Total tokens: {response.usage.total_tokens}\n')

            topic_list.append(topic)
            prompt_list.append(user)
            output_list.append(response.choices[0].message.content)

            row_time_end = datetime.datetime.now().replace(microsecond=0)
            row_run_time = row_time_end - row_time_start
            print(f"Row runtime: {row_run_time}.\n")
            print(f'______________________________\n')
            window.Refresh()
          
          except:
            print(f'An error occured while working on: {user}\n')
            topic_list.append(topic)
            prompt_list.append(user)
            output_list.append('Unexpected error occured')
            logging.exception("Oops:")
            
            row_time_end = datetime.datetime.now().replace(microsecond=0)
            row_run_time = row_time_end - row_time_start
            print(f"Row runtime: {row_run_time}.\n")
            print(f'______________________________\n')
            window.Refresh()
            pass

          window.Refresh()

      # Save output to a CSV file
      now = datetime.datetime.now().strftime('%Y%m%d-%Hh%M')
      print('Saving to a CSV file...\n')
      print(f'Topic: {len(topic_list)}, Prompt: {len(prompt_list)}, Output: {len(output_list)}\n')
      data = {"Topic": topic_list, "Prompt": prompt_list, "Output": output_list}
      df = pd.DataFrame.from_dict(data, orient='index')
      df = df.transpose()

      filename = f"completion{ now }.csv"

      print(f'{filename} saved sucessfully.\n')

      file_path = os.path.join(directory,'csvfiles/', filename)
      df.to_csv(file_path)

      time_end = datetime.datetime.now().replace(microsecond=0)
      runtime = time_end - time_start
      print(f"Script runtime: {runtime}.\n")
      window.Refresh()

      # Enable all button after run
      window['Run'].update(disabled=False)
      window['gpt-4'].update(disabled=False)
      window['gpt-3.5-turbo'].update(disabled=False)
      window['text-davinci-003'].update(disabled=False)

  window.close()

if __name__ == '__main__':
  main()