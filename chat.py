from openai import OpenAI
from config import APIKEY

# set API key
client = OpenAI(api_key=APIKEY)

# model to use
model="gpt-3.5-turbo"

# store message history to pass each time to the model
message_history = []

# count no. of tokens, prompts per chat/session
tokens = 0
prompts = 0

# set AI behavior at the start
behavior = input(f"\nEnter the kind of behavior for the AI (press enter to skip)\n(e.g. You are a helpful assistant who answers sarcastically): ") \
                or "You are a helpful assistant"
message_history.append({"role": "system", "content": behavior})

print()
for i in range(10):
    print(".")
print("Starting chat...")
print("-------------------------------------------------------")

while True:

    user_message = input(f"{prompts+1}) User (press Q/q to quit): ")
    prompts += 1

    if user_message.lower() == 'q':
        break

    message_history.append({"role": "user", "content": user_message})

    try:
        completion = client.chat.completions.create(
                    model=model,
                    messages=message_history
                    )
        response = completion["choices"][0]["message"]["content"]
        message_history.append({"role": "assistant", "content": response})
        tokens += completion['usage']['total_tokens']

        # print finish_reason
        finish_reason = completion['choices'][0]['finish_reason']
       # if finish_reason == 'stop':
            # API returned complete model output
            #print(f"Returned complete response.")
        if finish_reason == 'length':
            # Incomplete model output due to max_tokens parameter or token limit
            print("Incomplete response (max tokens reached)")
        elif finish_reason == 'content_filter':
            # Omitted content due to a flag from our content filters
            print("Content flagged. Skipping response..")
        elif finish_reason == 'null':
            # API response still in progress or incomplete
            print("Response still in progress/incomplete.")
        

        print(f"\nChatGPT: {response}\n\n")

    except Exception as e:
        print(f'\nNOTE: {e}')
        break


print("-------------------------------------------------------")
print("Exited.")
print(f"Total no. of tokens used in chat session ({prompts-1} {'prompt' if prompts-1 == 1 else 'prompts'}): {tokens}")
print("-------------------------------------------------------")
