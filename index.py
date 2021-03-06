from flask import Flask, render_template, request, redirect, url_for, flash
import threading
import voice_interact as vi
import calendar_func as cf
import pdfToText as pdfFunc

app = Flask(__name__)

app.secret_key = "mysecretkey"

actividades_inicio = ["Qué desea hacer", "Ver su calendario", "Leer pdf", "Ver mapa", "conversar"]
actividades_calendario = ["Qué desea hacer", "Escuchar sus eventos de un día o mes", "Crear un nuevo evento"]
actividades_mapa = ["Puede ver su ubicación", "Puede buscar algo cercano","Puede buscar como llegar a un destino"]
url = ['https://www.google.com/maps/embed/v1/search?key=AIzaSyAWoYcJvFqk76P_YE6CUvSp3FXnDuibPf8&q=mi+ubicacion&zoom=15']
primera_vez = [True]*5

def actividades(pagina):
    if pagina == "conversa":
        vi.engine_speak("Presione el botón del medio para iniciar una conversación")
    else:
        if pagina == "mapa":
            vi.engine_speak("Usted se encuentra en algún lugar cerca de aquí")
        if pagina == "calendario":
            vi.engine_speak("Aquí le muestro sus actividades programadas para esta semana")
        introduccion = vi.record_audio("¿Necesitas ayuda?")
        if "sí" in introduccion:
            respuesta = vi.record_audio(f"¿Conoces mis funciones para {pagina}?")
            if "sí" in respuesta:
                vi.engine_speak("Presione el botón del medio para decirme que desea hacer")
            elif "no" in respuesta:
                if pagina == "inicio":
                    for text in actividades_inicio:
                        vi.engine_speak(text)
                elif pagina == "calendario":
                    for text in actividades_calendario:
                        vi.engine_speak(text)
                elif pagina == "mapa":
                    for text in actividades_mapa:
                        vi.engine_speak(text)
                vi.engine_speak("Presione el botón del medio para decirme que desea hacer")
        elif "no" in introduccion:
            vi.engine_speak("Si necesitas algo, puedes presionar el botón del medio para llamarme.")

@app.route('/calendario/acciones')
def funciones_calendario():
    service = cf.google_authentication()
    respuesta = vi.record_audio("Lo escucho")
    if ("escuchar" in respuesta) or ("dime" in respuesta) or ("digas" in respuesta):
        day = "".join(respuesta.split("eventos")[1:])
        date = cf.get_date(day)
        events = cf.get_events(date,service)
        if not events:
            vi.engine_speak(f"No tienes eventos {day}.")
        else:
            if len(events) == 1:
                vi.engine_speak(f"Tienes un evento {day}")
            else:
                vi.engine_speak(f"Tienes {len(events)} eventos {day}")
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                start_time = str(start.split("T")[1].split("-")[0])
                if int(start_time.split(":")[0]) < 12:
                    start_time = start_time + "a m"
                else:
                    start_time = str(int(start_time.split(":")[0])-12) + ":" + start_time.split(":")[1]
                    start_time = start_time + "p m"
                vi.engine_speak(event['summary'] + "a las " + start_time)
    elif ("añadir" in respuesta) or ("crear" in respuesta):
        day = "".join(respuesta.split("evento")[1:])
        print(day)
        datetime = cf.get_date(day)
        print(datetime)
        summary = vi.record_audio("¿cuál es el título del evento?")
        location = vi.record_audio("¿En qué lugar?")
        description = vi.record_audio("¿cuál es la descripción del evento?")
        hora_inicio = vi.record_audio("¿A qué hora inicia?")
        inicio = cf.get_hour(hora_inicio)
        hora_fin = vi.record_audio("¿A qué hora termina?")
        fin = cf.get_hour(hora_fin)
        cf.create_event(service,summary,location, description,datetime,inicio,fin)
        vi.engine_speak("¡Evento creado satisfactoriamente!")
    return redirect(url_for('calendario'))

@app.route('/mapa/acciones')
def funciones_mapa():
    respuesta = vi.record_audio("¿Qué quieres que haga?")
    if "llegar" in respuesta:
        respuesta = vi.record_audio("Direccion de partida")
        origin = "+".join(respuesta.split())
        respuesta = vi.record_audio("Direccion de destino")
        destiny = "+".join(respuesta.split())
        url_ubicacion = f"https://www.google.com/maps/embed/v1/directions?key=AIzaSyAWoYcJvFqk76P_YE6CUvSp3FXnDuibPf8&origin={origin}&destination={destiny}&avoid=tolls|highways"
        url.pop()
        url.append(url_ubicacion)
        vi.engine_speak("En el mapa se muestra la ruta solicitada")
    elif "busca" in respuesta:
        q = "+".join(respuesta.split()[1:])
        url_buscar = f"https://www.google.com/maps/embed/v1/search?key=AIzaSyAWoYcJvFqk76P_YE6CUvSp3FXnDuibPf8&q={q}"
        url.pop()
        url.append(url_buscar)
        vi.engine_speak("En el mapa se muestra lo que solicitó")
    return redirect(url_for('mapa'))

@app.route('/conversa/conversando')
def conversando():
    while 1:
        user_input=""
        user_input=vi.record_audio("")
        vi.respond(user_input)
        if ("adiós" in user_input) or ("salir" in user_input) or ("apagar" in user_input) or ("adiós" in user_input) or ("hasta pronto" in user_input) or ("chau" in user_input) or ("hasta luego" in user_input):
            break
    return redirect(url_for('conversar'))

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
        return redirect(url_for('conversar'))

@app.route('/')
def Index():
    if primera_vez[0]: 
        t = threading.Thread(target=actividades, args = ["inicio"])
        t.start()
    primera_vez[0] = False
    return render_template('index.html')

@app.route('/calendario')
def calendario():
    if primera_vez[1]: 
        t = threading.Thread(target=actividades, args=["calendario"])
        t.start()
    primera_vez[1] = False
    return render_template('calendar.html')

@app.route('/archivos')
def archivo(methods=['GET', 'POST']):
    #if primera_vez[2]: 
    return render_template('pdf.html')

@app.route('/mapa')
def mapa():
    if primera_vez[3]: 
        t = threading.Thread(target=actividades, args=["mapa"])
        t.start()
    primera_vez[3] = False
    return render_template('mapa.html',iframe_url=url[0])    

@app.route('/conversa')
def conversar():
    if primera_vez[4]: 
        t = threading.Thread(target=actividades, args=["conversa"])
        t.start()
    primera_vez[4] = False
    return render_template('conversa.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    pdf = request.form['pdf_loc']
    if pdf:
        path = f'static\{pdf}'
        pdfFunc.readLines(path,0,1)
        return redirect(url_for('archivo'))
    else:
        return redirect(url_for('archivo'))

if __name__ == '__main__':
    app.run()