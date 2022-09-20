import re
import os
import openai
from time import time,sleep
from random import seed,choice
from uuid import uuid4


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


openai.api_key = open_file('openaiapikey.txt')


def gpt3_completion(prompt, engine='text-davinci-002', temp=0.0, top_p=1.0, tokens=2000, freq_pen=0.0, pres_pen=0.0, stop=['asdfasdf', 'asdasdf']):
    max_retry = 5
    retry = 0
    prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()  # force it to fix any unicode errors
    while True:
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop)
            text = response['choices'][0]['text'].strip()
            #text = re.sub('\s+', ' ', text)
            filename = '%s_gpt3.txt' % time()
            save_file('gpt3_logs/%s' % filename, prompt + '\n\n==========\n\n' + text)
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % oops
            print('Error communicating with OpenAI:', oops)
            sleep(1)


def run_prompt(filename, story):
    prompt = open_file(filename).replace('<<STORY>>', story)
    return gpt3_completion(prompt)


if __name__ == '__main__':
    files = os.listdir('synopses/')
    for file in files:
        if os.path.exists('plots/%s' % file):
            print('Skipping:', file)
            continue
        story = open_file('synopses/%s' % file)
        print('\n\nSTORY:', story)
        prompt = open_file('prompt_outline.txt').replace('<<STORY>>', story)
        plot = gpt3_completion(prompt)
        print('\n\nPLOT:', plot)
        save_file('plots/%s' % file, descr)