# Dexo-Bot
An advanced discord security bot with multi-features and easy to use commands.

# Features
⚙️ **Highly Configureable** - Dexo provides a lot of configuration options to make the bot work as you want.

🔒 **Security** - Dexo provides a lot of security features to protect your server from raids and nukes.

🛠️ **Moderation** - Dexo provides a lot of moderation features to make your server clean and safe.

✅ **Verification** - Dexo provides various options of verification features to make your server secure.

🔥 **High Performance** - Dexo is built with optimization for maintaining and securing high performance.

📚 **Easy to Use** - Dexo is easy to use and has a lot of commands to make your server secure.


# Technologies
- [Python](https://www.python.org/)
- [Nextcord]()
- [MongoDB](https://www.mongodb.com/)

# Installation
1. Clone the repository
```bash
git clone https://github.com/ItsNotAlexy/Dexo-Bot
```
2. Install the dependencies
```bash
pip install -r requirements.txt
```
3. Create a `./config` folder and add a `apiconf.json` file with the following content:
```json
{
    "VT_API_KEY": "YOUR-VIRUSTOTAL-API-KEY",
}
```
4. Create a `./config` folder and add a `botconf.json` file with the following content:
```json
{
    "TOKEN": "YOUR-BOT-TOKEN",
    "DEVELOPERS": [DEVELOPERS-ID],
    "COPYRIGHT": "Created By alexyssh"
}
```
5. Create a `./config` folder and add a `dbconf.json` file with the following content:
```json
{
    "MONGO_URI": "YOUR-MONGO-URI",
    "DB_NAME": "YOUR-DATABASE-NAME",
    "GUILD_CONFIG_COLLECTION_NAME": "YOUR-GUILD-CONFIG-COLLECTION-NAME",
    "USER_CONFIG_COLLECTION_NAME": "YOUR-USER-COLLECTION-NAME",
    "USER_VERIFACTION_COLLECTION_NAME":"YOUR-USER-VERIFACTION-COLLECTION-NAME"
}
```
6. Run the bot
```bash
python main.py
```

# Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


# License
[MIT](https://choosealicense.com/licenses/mit/)


# Contact
- Discord: [alexyssh](https://discord.com/users/697323031919591454)
