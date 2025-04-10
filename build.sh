#!/usr/bin/env bash
# Forzar instalación exacta de Python 3.10.13 y dependencias

echo "🔧 Instalar Python 3.10.13..."
pyenv install 3.10.13
pyenv global 3.10.13

echo "📦 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt
