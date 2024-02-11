import json
import abstract
from openai import OpenAI
client = OpenAI()

role = """
You are an AI whose greatest strength is taking a complex technical abstract 
and summarizing it in a concise and descriptive manner such that no important details are lost
from the original text. The best in the world, actually.

Given a series of titles and their abstracts separated by ### , return a list of JSON objects
each with 3 fields:
    - the article's title
    - the article's timestamp (the full thing! be sure to include both date *and* time)
    - your generated summary

Ensure that this response is a valid JSON file with token-conserving formatting.

Here's an example:

This is the Title of the First Paper
Right here is the first publishing date
This is the abstract. Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

###

This is the Title of the Second Paper
Right here is the second publishing date
This is the second abstract. Notice the separator token above. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
"""

abstract.get_papers()

with open('prompt.json', 'r') as f:
    prompt_json = json.loads(f.read())

prompt = ''
for paper in prompt_json:
    prompt += paper['title']
    prompt += '\n'

    prompt += paper['published_date']
    prompt += '\n'

    prompt += paper['abstract']
    prompt += '\n\n'

    prompt += '###'
    prompt += '\n\n'

response = client.chat.completions.create(
    model='gpt-4-1106-preview',
    messages=[
        { 'role': 'system', 'content': role },
        { 'role': 'user', 'content': prompt }
    ]
)

content = response.choices[0].message.content

with open('response.json', 'w') as f:
    f.write(content)

print('usage:')
print(f"  - Completion tokens: {response.usage.completion_tokens}\n")
print(f"  - Total tokens: {response.usage.total_tokens}\n")
