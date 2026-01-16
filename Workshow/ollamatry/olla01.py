import ollama

response = ollama.chat(model='my-translate-model', messages=[
    {'role': 'user', 'content': '請翻譯：今天天氣很好。'}
])
print(response['message']['content'])