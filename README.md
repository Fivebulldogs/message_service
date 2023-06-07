# Installation

1. Install `docker` and `docker compose` on your machine

# Setup postgres db

1. Start the database container:
   `docker compose start db`
2. Run `docker compose exec -it db psql -U postgres` to go to the database shell
3. Execute the following in the database shell:

```
CREATE DATABASE messages;
ALTER USER postgres with encrypted password 'messagespassword';
```

# Start web service and migrate database

1. Start the web service: `docker compose start web`
2. To migrate, run `docker compose run --rm web python manage.py migrate`

# Run tests

`docker compose exec -it web python manage.py test`

# API documentation

http://localhost:8000/api/docs

# Post a message

`curl -d '{"recipient": "mybestfriend", "text": "Hello friend!"}' localhost:8000/api/message`

# Fetch messages

`curl localhost:8000/api/messages`

# Fetch new messages only

`curl localhost:8000/api/messages/new`

# Fetch messages by start and stop index

Indexing starts at 0. The message at `stop`is not included in the result.

To fetch the three latest messages use:
`curl localhost:8000/api/messages?start=0&stop=3`

# Delete one or more messages by id

`curl -X "DELETE" "localhost:8000/api/messages?id=1&id=2`
