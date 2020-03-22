# Telegram and VK helper bots

Telegram and VK bots to help your company communicate with your customers or possible employees.

## How to install


1. First if all you need to create an account and project at [DialogFlow](https://cloud.google.com/dialogflow/docs/quick/setup). At the end of this step you'll get your project_id, save it somewhere.
2. Create an agent in your DialogFlow project - [here](https://cloud.google.com/dialogflow/docs/quick/build-agent), use project_id from previous step during the creation of an agent.
3. Get credentials for your project. Follow the instructions [here](https://cloud.google.com/docs/authentication/getting-started). Save the credentials if some safe place.
4. To use Telegram bot:
    1. You need to register two new bots on [Telegram](https://telegram.org/). Find `@BotFather` bot in your app, type `/newbot`, then follow the instructions of that bot. When you're finished, you'll get your bot api token, which looks like this - `95132391:wP3db3301vnrob33BZdb33KwP3db3F1I`. Create two bots, you'll use one as a helper bot and other as a logging bot.
    2. Then you need to type `\start` in your bots chats.
    3. Go to `@myidbot` in Telegram app and type `\getid` to get your chat_id.
5. To use VK bot:
    1. Create VK Group - [here](https://vk.com/groups_create)
    2. Go to your group's Settings - API, create new API key and allow to send messages on behalf of the group. Save your API key somewhere safe.
6. Deploy.
    1. Locally
        - You need to create `.env` file in directory with this program and put there your dvmn api token, telegram bot tokens and your telegram chat_id. Your can also set long polling timeout and proxy for telegram bot, but its optional. `.env` file should look like this, but with your data instead:
            ```
             TELEGRAM_HELPER_BOT_TOKEN=<YOUR_TELEGRAM_HELPER_BOT_TOKEN>
             TELEGRAM_LOG_BOT_TOKEN=<YOUR_TELEGRAM_LOGGER_BOT_TOKEN>
             TELEGRAM_PROXY_URL=<PROXY_URL>
             TELEGRAM_CHAT_ID=<YOUR_TELEGRAM_CHAT_ID>
             VK_GROUP_TOKEN=<VK_GROUP_API_TOKEN>
             GOOGLE_APPLICATION_CREDENTIALS=<PATH_TO_YOUR_GOOOGLE_CREDS>
             GOOGLE_PROJECT_ID=<YOUR_PROJECT_ID>
            ```
        - Python3 should be already installed. The project was made using `Python 3.6.9`. This version or higher should be fine.
        - Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
            ```
            pip install -r requirements.txt
            ```
    2. Heroku
        - Register on [Heroku](https://www.heroku.com/). Connect your Heroku account to your GitHub account. Fork current repository to your account.
        - Create new app on [Heroku's Apps page](https://dashboard.heroku.com/apps).
        - Go to "Deploy" tab of your app and deploy `master` branch of the forked repository.
        - Go to "Settings" tab of your app and add your api keys and tokens into "Config Vars" section (for vars name reference, see 6.1).
        - To hide your google credentials in heroku follow the instructions [here](https://stackoverflow.com/a/56818296). But use another buildback: `heroku buildpacks:add https://github.com/gerywahyunugraha/heroku-google-application-credentials-buildpack -a "<YOUR_APP_NAME"`


## How to use

1. Locally
    1. To teach your DialogFlow Agent new intents, follow these steps:
        - Create json file with learning information, using following format:
        ```
        {
            "<THEME>": {
                "questions":
                    [
                        "<POSSIBLE_INCOMING_MESSAGE1>",
                        "<POSSIBLE_INCOMING_MESSAGE2>",
                    ],
                "answer": "<YOUR_BOTS_ANSWER_TO_THESE_MESSAGES>",
            },
            ...
        }
        ```
        - Run following command:

        ```$ python3 create_intents.py <PATH_TO_YOUR_JSON_FILE>```
    2. To launch bots use following commands:
    ```
    $ python3 tg_bot.py
    $ python3 vk_bot.py 
    ```
2. Heroku

    Go to "Resources" tab of your app and turn on your bots.
    
Results:

Telegram bot example conversation - [here](https://imgur.com/2FldaX4)
VK bot example conversation - [here](https://imgur.com/jlVzlaW)

## Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
