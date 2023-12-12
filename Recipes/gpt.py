import openai
import base64
import os
import json

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

## https://platform.openai.com/docs/guides/images/usage?context=python

# Retrieve the API key from the environment variable
openai_api_key = os.getenv('OPENAI_API_KEY')

if openai_api_key is None:
    raise ValueError("No OpenAI API key found in environment variables")

def gpt4_vision(image: str) -> dict:
    """
    Process an image using GPT-4 Vision model and return the response in a structured format.

    Args:
    image (str): Path to the image file.

    Returns:
    dict: JSON response from GPT-4 Vision model.
    """
    # Convert the image to the format required by GPT-4 (e.g., Base64 encoding)
    with open(image, "rb") as file:
        encoded_image = base64.b64encode(file.read()).decode('utf-8')

    client = openai.OpenAI(api_key = openai_api_key)
    template = '{"recipes": [{"name": "", "ingredients": [], "steps": []}, {"name": "", "ingredients": [], "steps": []}]}'
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"What can I cook with the following image? Your output to the question must be correctly formatted using the template: {template}"},
                    {
                        "image": encoded_image
                    },
                ],
            }
        ],
        max_tokens=500,
    )

    print(response.choices[0].message.content)
    return json.loads(response.choices[0].message.content)


def dalle_3(prompt: str) -> str:
    """
    Generate an image using DALL-E 3 model based on the provided prompt.

    Args:
    prompt (str): The prompt to generate the image.

    Returns:
    str: URL of the generated image.
    """
    client = openai.OpenAI(api_key = openai_api_key)
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1792x1024",
        quality="standard",
        n=1,
        )
    image_url = response.data[0].url
    return image_url