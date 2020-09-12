- Debe tener instalado python 3.8.5 64 bits en su computador
- Cree un virtual env de python o use el entorno Jarvisenv
	venv <nombre_env>
- Active su entorno virtual.
	source <nombre_env>\Scripts\activate
- Instale los requerimientos a partir de requirements.txt.
	pip install -r requirements.txt
- Instale pyaudio. Pruebe con:
	pip install pyaudio
--Si no funciona, instale pyaudio desde el whl incluido en la carpeta:
	pip install PyAudio-0.2.11-cp38-cp38-win_amd64.whl
- Ejecute el programa
	python index.py
Si usted tiene otra distribución de python:
- Desde un entorno virtual, instale los requerimientos a partir de
  requirements.txt
	pip install -r requirements.txt
- Instale pyaudio. Pruebe con:
	pip install pyaudio
--Si esto no funciona, entre al siguiente link: 
	https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
--Descargue el wheel correspondiente a su distribución de python.
 - Instale el pyaudio a partir de su wheel.
	pip install PyAudio-0.2.11... .whl
 - Ejecute el programa
	python index.py