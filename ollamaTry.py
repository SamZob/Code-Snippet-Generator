import ollama
import json

stream = ollama.chat(
    model='codellama',
    messages=[{'role': 'user', 'content':'Implement a sum function between two inputs in Python'}]
)

print(stream)