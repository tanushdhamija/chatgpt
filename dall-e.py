import openai
from config import APIKEY

# set API key
openai.api_key = APIKEY

while True:
    user_prompt = input("\nEnter a prompt to generate image (q to quit): ")

    if user_prompt.lower() == 'q':
        break

    try:
        response = openai.Image.create(
                    prompt=user_prompt,
                    n=1,
                    size="1024x1024"
                    )
        image_url = response['data'][0]['url']
        print(f'\nGo to image: {image_url}')
    except Exception as e:
        print(e)

print("\n-------------------------------------------------------")
print('Exited.')