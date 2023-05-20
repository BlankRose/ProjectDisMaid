<h1 align='center'>
	🎀 <b>Project DisMaid</b> 🎀<br>
	<i style='font-size:120%;'>Just a regular Discord bot</i>
</h1>
<p align='center'>
	<img alt="Top Language" src="https://img.shields.io/static/v1?label=Language&message=Python&color=important&style=plastic"/>
	<img alt="Code Size" src="https://img.shields.io/github/languages/code-size/BlankRose/ProjectDisMaid?label=Code+Size&color=informational&style=plastic"/>
	<img alt="Last Commit" src="https://img.shields.io/github/last-commit/BlankRose/ProjectDisMaid?label=Last+Commit&color=critical&style=plastic"/>
</p>

# 📗 About the Project :

This is a python project where I try to make a discord bot basically<br>
Of course, its far from being the best bot out there but it is a project I made to test my skills on Python

Just a silly maid mouse for all of your needs~<br>
This project was made to come with as many features as you could see on many bots while being fully free to use, without any paywalls or any voting requirements.<br>
It is of course open-source as it also could serve as a quick reference for those who wanna start up a new bot on their own or if anyone wanna improve it overall.

# ⭐️ Support :

Pull requests are opens and accepted!<br>
Along with any kind of support~ 😊

If you wanna try it by yourself, here's some useful links:
 - [My discord server (Starlands)](https://discord.gg/pPvPtBWrcp)
 - [Bot's invite link (RoseMaid)](https://discord.com/api/oauth2/authorize?client_id=820667068814065694&permissions=8&scope=bot)

# 🛠 Configuration :

It will requierds a <i>"configs.json"</i> file in order to work which will contains the following entries:
- `token`: Token used to connect your bot
  - STRING (**Mandatory**)
  - Can be found in [discord's developers portal](https://discord.com/developers/)
- `maxLogs`: Amount of logs saved, currently generated excluded
  - INTEGER (**Default:** 5)
  - -1 for keeping everything
- `local`: True for locally saved data, False for server stored data
  - BOOLEAN (**Mandatory**)
- `database`: Name of the database (for server) or directory (for local)
  - STRING (**Mandatory**)
- `database-ip`: IP to the server where is located database
  - STRING (**Default:** '127.0.0.1')
- `database-port`: Port to the server
  - INTEGER (**Default:** 3306)
- `database-user`: User to use for database
  - STRING (**Default:** 'root')
- `database-pass`: Password for given user
  - STRING (**Default:** '')
- `database-retry`: How many tries to connect to database before exiting
  - INTEGER (**Default:** 5)
  - -1 for infinite retries
- `database-time`: Delay between two tries (in seconds)
  - INTEGER (**Default:** 5)
- `autoSave`: Should it automatly saves (will still save upon exit)
  - BOOLEAN (**Default:** True)
- `autoSave-time`: Delay between two saves (in seconds)
  - INTEGER (**Default:** 600)
- `localizations`: Folder where is stored bot's localizations
  - STRING (**Mandatory**)