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

def completion():

  time_start = datetime.datetime.now().replace(microsecond=0)
  directory = os.path.dirname(os.path.realpath(__file__))
  
  topic_list = []
  prompt_list = []
  output_list = []

  with open('terms.csv') as f:
    reader = csv.DictReader(f)

    for line in reader:

      converted_row = convert_row( line )
      # prompt = converted_row['Prompt']
      topic = converted_row['Topic']
      system = converted_row['system']
      user = converted_row['user']

      print(f'\n{user}\n')

      logging.basicConfig(level=logging.DEBUG, filename='error.log')

      try:

        response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
          ]
        )

        print(f'{response.choices[0].message.content}\n')
        print(f'Tokens used: {response.usage.total_tokens}\n')
        
        topic_list.append(topic)
        prompt_list.append(user)
        output_list.append(response.choices[0].message.content)
      
      except:
        print(f'An error occured while working on: {user}\n')
        topic_list.append(topic)
        prompt_list.append(user)
        output_list.append('Unexpected error occured')
        logging.exception("Oops:")
        pass
  
  time_end = datetime.datetime.now().replace(microsecond=0)
  runtime = time_end - time_start
  print(f"Script runtime: {runtime}.\n")

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
    