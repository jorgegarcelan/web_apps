import openai
import base64
import os

# Retrieve the API key from the environment variable
openai_api_key = os.getenv('OPENAI_API_KEY')

if openai_api_key is None:
    raise ValueError("No OpenAI API key found in environment variables")

def gpt4_vision(image):

    # Convert the image to the format required by GPT-4 (e.g., Base64 encoding)
    with open(image, "rb") as file:
        encoded_image = base64.b64encode(file.read()).decode('utf-8')

    client = openai.OpenAI(api_key = openai_api_key)

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What can I cook with the following image?"},
                    {
                        "image": encoded_image
                    },
                ],
            }
        ],
        max_tokens=300,
    )

    print(response.choices[0].message.content)
    return response.choices[0].message.content


gpt4_vision("C:/Users/jorge/Desktop/UNI/4-CUARTO/4-1-WEB APPS/PROJECT/web_apps/Recipes/static/imgs/5cf5dad1-4634-468e-a04c-11f2ed72cd85--Fridge_Rocky_Luten.png")