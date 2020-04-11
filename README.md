# smart-tv-bulb

The goal of this app is to turn on TV lights at sunset in case that TV is turned
on at the time. Procedure is accomplished by 2 scripts
* `tv_light_cron.py` - checks for sunset and creates/modifies record in `cron`.
The script should be executed every day (from `cron`).
* `tv_light_action.py` - checks for status of smartthings TV. If the TV is
switched on then the lights are switch on too by their APIs.

## Installation

Clone the repository:
```
git clone https://github.com/blsho/smart-tv-bulb.git
```

Create venv:
```
python3 -m venv venv
```

Install `requirements.txt` to venv:
```
source venv/bin/activate
pip install -r requirements.txt
```

Install cronjob:
```
0 12 * * * $DIR/smart-tv-bulb/venv/bin/python $DIR/smart-tv-bulb/tv_light_cron.py > /dev/null 2>&1 # Checks for sunset
```

## Configuring

Create file `config.py` in project root directory with following attributes:
- `token` - Token from [SmartThings](https://account.smartthings.com/tokens)
- `light_url` - URL of light API
- `light_ids` - List of light IDs
- `location` - Dictionary of `lat` and `lng` of location for sunset.
