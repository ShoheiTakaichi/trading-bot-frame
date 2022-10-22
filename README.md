## Requirements

This is for local setting. Install python3 at first.

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

In addition, you should install ccxws individually.
How to install ccxws is written in Dockerfile.


### create requirements.txt

When you add new module, you must update reqirements.txt by following command.

`pip freeze > requirements.txt`




## bot server

```
docker build . -t bot-server --no-cache
docker run -p 8000:8000 -t bot-server
```

`.env` example
```
BOTMODE=GIP
BITFINEX_API={bitfinex_key}
BITFINEX_SECRET={bitfinex_secret_key}
```

PIPELINE!
