import ollama

def generate_summarization(news_portal, content):
    try:
        # Call the model
        response = ollama.chat(
        model="llama3.2:3b",
         messages=[
        {
            "role": "system",
            "content": ("Summarize the article into a clear and concise paragraph while preserving the full context. "
            "Ignore all timestamps, author names, editors, publisher info, footers, advertisements, contact details, and publishing dates. "
            "Do not include unrelated information or your own opinions.")
        },
        {
            "role": "user",
            "content": content
        }
    ]
    )

        # Get summarized text
        # Correct access for Ollama SDK
        summary_text = response["message"]["content"]

        # Add news portal info and separator
        summary_text = f"{news_portal}\n{summary_text}\n==========\n"

        # Save to output.txt (append mode)
        with open("output.txt", "a", encoding="utf-8") as f:
            f.write(content)
            f.write("\n-----------------\n")
            f.write(summary_text)

        print("Summary saved to output.txt")
        return summary_text

    except Exception as e:
        print(f"Error generating summary: {e}")
        return f"{news_portal}\nN/A\n==========\n"
