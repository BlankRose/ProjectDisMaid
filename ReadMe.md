# NOTICE

This is just a simple docker deployement starting point and exemple.

For more complex deployements, you might consider improving to your likings depending on your needs.

You will need to adjust the following for first usage:
 - Create a `.env` file with the two ENVIRONEMENTS variables:
    - MYSQL_ROOT_PASSWORD
    - MYSQL_DATABASE
 - Modify `app/configs.json` file where you will insert:
    - Your bot's token (can be found on discord's developper portal)
    - Database's password (same as MYSQL_ROOT_PASSWORD)
    - MySQL's database name (same as MYSQL_DATABASE)
