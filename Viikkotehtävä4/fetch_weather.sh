#!/bin/bash
cd /home/ubuntu/linux_administrator/linux_viikkotehtava4

VENV_DIR="venv"

# Luo virtuaaliympäristö, jos ei vielä ole
if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv $VENV_DIR
fi

# Aktivoi venv
source $VENV_DIR/bin/activate

# Asenna kirjastot
pip install --upgrade pip
pip install -r requirements.txt

# Aja sääskripti
python fetch_weather.py
