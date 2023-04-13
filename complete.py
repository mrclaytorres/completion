import os
import openai
import pandas as pd
import datetime
import os.path
import time
import csv
import creds
import logging

openai.api_key = creds.OPENAI_API_KEY

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

def completion():

  # User chooses a model
  choose_model = input('1. gpt-4\n2. gpt-3.5-turbo\n3. text-davinci-003\n\nEnter the number that corresponds to the model: ')
  
  time_start = datetime.datetime.now().replace(microsecond=0)
  directory = os.path.dirname(os.path.realpath(__file__))

  topic_list = []
  prompt_list = []
  output_list = []

  with open('terms.csv', encoding='unicode_escape') as f:
    reader = csv.DictReader(f)

    for line in reader:

      row_time_start = datetime.datetime.now().replace(microsecond=0)

      converted_row = convert_row( line )
      # prompt = converted_row['Prompt']
      topic = converted_row['Topic']
      system = converted_row['system']
      user = converted_row['user']

      logging.basicConfig(level=logging.DEBUG, filename='error.log')

      try:
        match choose_model:
          case '1':
            print(f'\nWaiting for a response...\n')
            response = gpt_4(user, system)
          case '2':
            print(f'\nWaiting for a response...\n')
            response = gpt_3_5_turbo(user)
          case '3':
            max_tokens = input('\nTokens to spend (between 1 to 4,097)?\nEnter token: \n')
            print(f'\nWaiting for a response...\n')
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
        pass

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

if __name__ == '__main__':
  completion()
    