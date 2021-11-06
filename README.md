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

# Using pyenv and pipenv

## Pyenv
https://github.com/pyenv/pyenv   

For Mac use brew...
```
brew install pyenv
```

For Linux (rPi) follow these instructions...

Install the Python build dependencies
```
sudo apt-get update; sudo apt-get install make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```

Install pyenv - Check out Pyenv where you want it installed. A good place to choose is $HOME/.pyenv (but you can install it somewhere else):
```
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
```

Optionally, try to compile a dynamic Bash extension to speed up Pyenv. Don't worry if it fails; Pyenv will still work normally:

```
 cd ~/.pyenv && src/configure && make -C src
```

Configure your shell's environment for Pyenv
```
sed -Ei -e '/^([^#]|$)/ {a \
export PYENV_ROOT="$HOME/.pyenv"
a \
export PATH="$PYENV_ROOT/bin:$PATH"
a \
' -e ':a' -e '$!{n;ba};}' ~/.profile
echo 'eval "$(pyenv init --path)"' >>~/.profile

echo 'eval "$(pyenv init -)"' >> ~/.bashrc
```

