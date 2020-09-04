from flask import Flask, render_template, request, redirect, url_for, flash, copy_current_request_context
import concurrent.futures
import threading
import voice_interact as vi

app = Flask(__name__)

app.secret_key = "mysecretkey"

inicio = ["Qué desea hacer", "Ver su calendario", "Leer pdf", "Ver su ubicación", "conversar"]

def actividades():
    for text in inicio:
        vi.engine_speak(text)

@app.route('/acciones')
def acciones():
    respuesta = vi.record_audio("Lo escucho")
    if "calendario" in respuesta:
        return redirect(url_for('calendario'))
    elif ("pdf" in respuesta) or ("archivo" in respuesta):
        return redirect(url_for('archivo'))
    elif ("mapa" in respuesta) or ("ubicación" in respuesta):
        return redirect(url_for('mapa'))
    else:
        return redirect(url_for('conversar', input = respuesta))

@app.route('/')
def Index(): 
    t = threading.Thread(target=actividades)
    t.start()      
    return render_template('index.html')

@app.route('/conversa/<input>')
def conversar(input):
    t = threading.Thread(target=vi.respond,args=[input])
    t.start()
    return render_template('conversa.html')


if __name__ == '__main__':
    app.run(debug=False)