# SHH
Shanghai Habitat

# Requirement
Python 3

# Depolyment
```
virtualenv ~/SHH
source ~/SHH/bin/activate

git clone https://github.com/songanyi/SHH && cd SSH

pip install -r requirements.txt

python SHH/manage.py makemigrations
python SHH/manage.py migrate

# Start servser
python SHH/manage.py runserver
```