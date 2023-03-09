import openai
from config import APIKEY

# set API key
openai.api_key = APIKEY

# model to use
model="gpt-3.5-turbo"

tokens_session = 0

while True:

    user_message = input("\nAsk your question (or type 'exit' to quit): ")
    if user_message.lower() == 'exit':
        break
    
    try:
        response = openai.ChatCompletion.create(
                    model=model,
                    messages=[{"role": "user", "content": user_message}]
                    )
        
        # total tokens used
        input_tokens = response['usage']['prompt_tokens']
        output_tokens = response['usage']['completion_tokens']
        tokens_used = input_tokens + output_tokens # or tokens_used = response['usage']['total_tokens']
        tokens_session += tokens_used

        # print finish_reason
        finish_reason = response['choices'][0]['finish_reason']
        if finish_reason == 'stop':
            # API returned complete model output
            print(f"Returned complete response.")
        elif finish_reason == 'length':
            # Incomplete model output due to max_tokens parameter or token limit
            print("Incomplete response (max tokens reached)")
        elif finish_reason == 'content_filter':
            # Omitted content due to a flag from our content filters
            print("Content flagged. Skipping response..")
        elif finish_reason == 'null':
            # API response still in progress or incomplete
            print("Response still in progress/incomplete.")
        
        # print ChatGPT response
        print(f"ChatGPT: {response['choices'][0]['message']['content']}")
        print(f"Tokens used: {tokens_used} ({input_tokens} + {output_tokens})")
    
    except Exception as e:
        print(e)
        break


print("-------------------------------------------------------")
print("Exited.")
print(f"Total no. of tokens used in session: {tokens_session}")
print("-------------------------------------------------------")