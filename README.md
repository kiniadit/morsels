USAGE INSTRUCTIONS
-------------------

1. `pip install requirements.txt`
2. Create a **.env** file by copying empty variables in **.env_delete**. Delete **.env_delete**. Fill in environment variables.
3. Load fixtures with `manage.py loaddata *<fixture_name>*`
4. Make sure you have valid Twilio API account credentials and a verified caller id.
5. Start a **ngrok** server and input the hostanme into your **.env** file.
3. Make, run migrations and start Django server.
