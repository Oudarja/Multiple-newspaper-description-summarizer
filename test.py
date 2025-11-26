import ollama

response = ollama.chat(
    model="llama3.2:3b",  
    messages=[
        {"role": "system", "content": "You are a helpful AI summarizer. You will summarize the given text and try to keep the length of summarized text as small as possible.That's your work"},
        {"role": "user", "content": "রাজধানী ঢাকায় আজ সোমবার সকালে শীতের হালকা আমেজ আরো কিছুটা অনুভূত হয়েছে। সঙ্গে ছিল হালকা কুয়াশা। রোববার ঢাকার সর্বনিম্ন তাপমাত্রা ছিল ..."}
    ]
)

print(response["message"]["content"])



