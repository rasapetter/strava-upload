# strava-upload

Upload recorded runs and rides to your Strava account.

## Requirements

* Your own Strava API application, register on [http://www.strava.com/developers](http://www.strava.com/developers).

* [requests](http://docs.python-requests.org/en/latest/)

## How to upload an activity file

Firstly, fetch an access token using `access.py`. Provide your API application's `client_id` and `secret_key`.

```
python access.py --client_id <YOUR_CLIENT_ID> --secret_key <YOUR_SECRET_KEY>
```

Upload an activity file using `strava.py` and the access token from the previous step.

```
python strava.py <ACCESS_TOKEN> <FILE>
```
