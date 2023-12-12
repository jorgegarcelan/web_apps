from Recipes.gpt import dalle_3
from pathlib import Path
from Recipes import db, create_app
import pandas as pd
from PIL import Image
from io import BytesIO
import requests
import time


## https://platform.openai.com/docs/guides/images/usage?context=python

app = create_app()

def generate_photos():
    with app.app_context():
        photos = pd.read_csv('data/photos.csv', sep=";")
        recipes = pd.read_csv('data/recipes.csv', sep=";")

        for photo_id, row in photos.iterrows():
            photo_id+=1
            row = row.to_dict()
            recipe_idx = row['recipe_id'] - 1
            file_extension = row['file_extension']
            print(f"{photo_id=}")
            print(f"{row=}")
            print(f"{recipe_idx=}")
            title = recipes.loc[recipe_idx, 'title']
            print(f"{title=}")
            description = recipes.loc[recipe_idx, 'description']
            print(f"{description=}")
            print("-"*20)

            # Generate image
            info = "I NEED to test how the tool works with extremely simple prompts. DO NOT add any detail, just use it AS-IS. DO NOT add any text. DO NOT make a cartoon-like image"
            prompt = f"{info}. Create a realistic photo for a recipe. The title is {title} and description is {description}."
            generated_image_url = dalle_3(prompt)
            

            # Save the file
            response = requests.get(generated_image_url)

            # Ensure the request was successful
            if response.status_code == 200:
                # Open the image and save it
                image = Image.open(BytesIO(response.content))
                path = Path(f"Recipes/static/photos/recipes/photo-{photo_id}.{file_extension}")
                image.save(path)
            else:
                print("Failed to download the image")
            
            # Wait for a certain amount of time before making the next request
            time.sleep(15)  # Waits for 15 seconds


if __name__ == '__main__':
    generate_photos()
