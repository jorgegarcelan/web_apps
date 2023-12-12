# Recipe Realm Web App 🌐

Welcome to the Recipe Realm, the ultimate web application for discovering, creating, and sharing your favorite cooking recipes.

## Setup Instructions 🚀

Before running the application, follow these setup instructions to get started.

### OpenAI API Key Setup

Create a `.env` file in the Recipes directory with the OpenAI API key contents that were sent via email. This file is crucial for the application to function properly.

### Virtual Environment

Set up a virtual environment to manage the project's dependencies.

#### Creation:
```python3 -m venv venv```

#### Activation:
For Windows Command Prompt:
```venv\Scripts\activate```

For Linux/macOS:
```source venv/bin/activate```

#### Install all dependencies:
```pip install -r requirements.txt```

### Database Configuration 💻
The __init__.py file includes configuration settings for both SQLite and MySQL. Adjust these settings according to your database preferences:
- For a simple setup or testing, SQLite is recommended.
- For a production environment, MySQL or another robust database system is advisable.

If the database has not been initialized yet:
``` 
python init_database.py
```
Execute the following command to insert default data:
``` 
python insert_data.py
```
Execute the following command to start the Flask development server:
``` 
flask --debug --app=Recipes run 
```

## ADDITIONAL FUNCTIONALITIES ⚙️

- **Remove photos**: A user is able to remove a photo that was previously uploaded by him/he. This functionality is accesible in the recipe view under "Your Pictures" tab, as well as in your profile view under "Photos".

- **Explore Recipes**: We have created a view where you can browse recipes according to some filters.

- **Chef Assistant**: Powered by GPT4-V, we have use the OpenAI api to use this large language vision model to add an interesting functionality to our app. You are able to submit a photo of your fridge, food or raw ingredients and the model will process it and make recipe suggestions (2).

- **User Data**: Users are the key to any app. Therefore, we have decided to add more fields so we have more unique and personal profiles. In this sense, we have added:
    - *Username that starts with "@" just like Twitter/X*: At the moment of signing up JS code will add this special character to your username at real-tine.
    - *Bio*: A user will be able to write whatever makes him/her a unique Chef.
    - *Sign Up Date*: We'll also add when the user signed up, so people could see the experience of the chef in the platform.

- **Recipe Data**: Recipes will be more useful when more info is available. Therefore, we have added different fields that will make a recipe more unique:
    - *Type of Food*: It refers to the cuisine of such food (italian, asian, spanish...)
    - *Category of Food*: There are certain foods that are commonly eaten in the breakfast and not in the dinner. That's the reason why we think for users it's important to differentiate between categories of food, so they choose the recipe that best fits in each time of the day!

- **About Us**: We want to get to know our chefs and the recipes they create, so we think that they will also want to get to know us! This section explains who are we, our mission, what we offer and future steps...

## ADDITIONAL INFORMATION ℹ️

Following with the recent popularity of AI, we have used ChatGPT for the name and logo of our web, creating the data for the database and the photos for the recipes.

## 👥 Authors

- [@PabloGradolph](https://github.com/PabloGradolph)
- [@jorgegarcelan](https://github.com/jorgegarcelan)


![Logo](https://upload.wikimedia.org/wikipedia/commons/4/47/Acronimo_y_nombre_uc3m.png)
