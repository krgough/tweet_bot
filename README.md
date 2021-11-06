# Twitter bot to tweet room temperature
TMP75b sensor connected to I2C bus on rPi.  
Setup to tweet to a given twitter account - you must have a developer account with a registered app and the following keys
setup as environment variables.

```
# Consumer API Keys - Can be used wih oauth2 for read only access
CONSUMER_API_KEY
CONSUMER_API_SECRET

# User access tokens - required for write access
ACCESS_TOKEN
ACCESS_TOKEN_SECRET
```
