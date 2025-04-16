# AI-chatbot

How to install project locally:

1. Launch PyCharm (Don't open any project, stay at starting page).
2. Click "Clone repository"
3. In URL field copy https://github.com/IgorPuchacz/AI-chatbot
4. Click "Clone".
5. Open terminal (left-down corner of pycharm)
6. `pip install -r requirements.txt`
7. `rasa train`
8. Register account at https://console.twilio.com/

How to launch installed project:

1. Open 2 tabs in terminal
2. `rasa run actions`
3. `rasa shell` to make a conversation or `rasa shell nlu` to test just the intentions recognition

How to launch installed project with whatsapp connection (not finished)

1. Open 4 tabs in terminal and run 4 commands as following
2. "rasa run actions"
3. "rasa run --enable-api"
4. "python twilio_webhook.py"
5. "ngrok http 5000" and then copy the address "https://xxx-xxx.ngrok-free.app"
6. In twilio website go to Messaging > Try it out > Whatsapp > Sandbox settings
7. Start a new conversation on whatsapp with number ""
8. In "when message comes in" paste the "https://xxx-xxx.ngrok-free.app" and add "/webhooks/twilio/webhook" after the address. The whole field should look like "https://xxx-xxx.ngrok-free.app/webhooks/twilio/webhook"
9. Click save
10. Talk with AI bot :)