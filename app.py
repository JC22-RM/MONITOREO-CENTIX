
from flask import Flask, render_template, request, redirect
from smartolt import obtener_onus
from datetime import datetime

app = Flask(__name__)


# =====================================================
# FUNCIONES GENERALES
# =====================================================

def tiempo_transcurrido(fecha_texto):

    if not fecha_texto:
        return "Sin dato"

    try:
        fecha = datetime.strptime(
            str(fecha_texto),
            "%Y-%m-%d %H:%M:%S"
        )

        diferencia = datetime.now() - fecha

        if diferencia.total_seconds() < 0:
            return "0 min"

        dias = diferencia.days
        horas = diferencia.seconds // 3600
        minutos = (diferencia.seconds % 3600) // 60

        if dias >= 7:
            return f"{dias // 7} semana(s)"
        elif dias > 0:
            return f"{dias} día(s)"
        elif horas > 0:
            return f"{horas} hora(s)"
        else:
            return f"{minutos} min"

    except (ValueError, TypeError):
        return "Sin dato"


def normalizar_estado(estado):

    estado = str(estado or "").strip().lower()

    equivalencias = {
        "online": "Online",
        "los": "LOS",
        "offline": "Offline",
        "power fail": "Power fail",
        "power_fail": "Power fail"
    }

    return equivalencias.get(estado, estado)


# =====================================================
# DATOS DE DEMOSTRACIÓN
# =====================================================

def obtener_datos_demo():

    incidencias = [
        {
            "olt": "HUAWEI CENTRAL",
            "board": "14",
            "port": "15",
            "zona": "Zona Central",
            "estado": "LOS",
            "cantidad": 15,
            "tiempo": "25 min"
        },
        {
            "olt": "JUAN PABLO II",
            "board": "5",
            "port": "8",
            "zona": "Juan Pablo II",
            "estado": "LOS",
            "cantidad": 3,
            "tiempo": "15 min"
        },
        {
            "olt": "HUAWEI CENTRAL",
            "board": "10",
            "port": "4",
            "zona": "Zona Central",
            "estado": "Power fail",
            "cantidad": 2,
            "tiempo": "30 min"
        },
        {
            "olt": "JUAN PABLO II",
            "board": "7",
            "port": "6",
            "zona": "Juan Pablo II",
            "estado": "Power fail",
            "cantidad": 13,
            "tiempo": "40 min"
        },
        {
            "olt": "HUAWEI CENTRAL",
            "board": "12",
            "port": "3",
            "zona": "Zona Central",
            "estado": "Offline",
            "cantidad": 5,
            "tiempo": "20 min"
        },
        {
            "olt": "JUAN PABLO II",
            "board": "8",
            "port": "2",
            "zona": "Juan Pablo II",
            "estado": "Offline",
            "cantidad": 13,
            "tiempo": "35 min"
        }
    ]

    return {
        "total_onus": 5231,
        "online": 5180,
        "los": 18,
        "power_fail": 15,
        "offline": 18,
        "incidencias": incidencias,
        "olts_con_incidencias": 2,
        "datos_demo": True
    }


# =====================================================
# OBTENER DATOS DE SMARTOLT
# =====================================================

def obtener_datos_monitoreo():

    try:
        onus = obtener_onus()

        if not onus:
            return obtener_datos_demo()

        total_onus = len(onus)

        online = 0
        los = 0
        power_fail = 0
        offline = 0

        grupos = {}

        for onu in onus:

            estado = normalizar_estado(onu.get("status"))

            if estado == "Online":
                online += 1

            elif estado == "LOS":
                los += 1

            elif estado == "Power fail":
                power_fail += 1

            elif estado == "Offline":
                offline += 1

            else:
                continue

            if estado not in ["LOS", "Power fail", "Offline"]:
                continue

            clave = (
                onu.get("olt_id"),
                onu.get("board"),
                onu.get("port"),
                estado
            )

            if clave not in grupos:

                grupos[clave] = {
                    "olt": onu.get("olt_id") or "Sin identificar",
                    "board": onu.get("board") or "Sin dato",
                    "port": onu.get("port") or "Sin dato",
                    "zona": onu.get("zone_id") or "Sin zona",
                    "estado": estado,
                    "cantidad": 0,
                    "tiempo": tiempo_transcurrido(
                        onu.get("last_status_change")
                    )
                }

            grupos[clave]["cantidad"] += 1

        incidencias = sorted(
            grupos.values(),
            key=lambda x: x["cantidad"],
            reverse=True
        )

        olts_con_incidencias = len(set(
            item["olt"]
            for item in incidencias
        ))

        return {
            "total_onus": total_onus,
            "online": online,
            "los": los,
            "power_fail": power_fail,
            "offline": offline,
            "incidencias": incidencias,
            "olts_con_incidencias": olts_con_incidencias,
            "datos_demo": False
        }

    except Exception as error:

        print("Error al consultar SmartOLT:", error)

        return obtener_datos_demo()


# =====================================================
# LOGIN
# =====================================================

@app.route("/")
def login():

    return render_template("login.html")


@app.route("/validar", methods=["POST"])
def validar():

    usuario = request.form.get("usuario")
    password = request.form.get("password")

    if usuario == "admin" and password == "123456":
        return redirect("/dashboard")

    return render_template(
        "login.html",
        error="❌ Usuario o contraseña incorrectos"
    )


# =====================================================
# DASHBOARD
# =====================================================

@app.route("/dashboard")
def dashboard():

    return render_template("dashboard.html")


# =====================================================
# MONITOREO
# =====================================================

@app.route("/monitoreo")
def monitoreo():

    datos = obtener_datos_monitoreo()

    return render_template(
        "monitoreo.html",
        **datos
    )


# =====================================================
# ANÁLISIS DE INCIDENCIAS
# =====================================================

@app.route("/diagnostico")
def diagnostico():

    return render_template("diagnostico.html")


# =====================================================
# HISTORIAL DE INCIDENCIAS
# =====================================================

@app.route("/historial")
def historial():

    registros = [

        {
            "fecha": "30/10/2026",
            "fecha_iso": "2026-10-30",
            "olt": "HUAWEI CENTRAL",
            "zona": "Zona Central",
            "problema": "Router sin conexión",
            "elemento": "Router",
            "solucion": "Reinicio y reconfiguración del equipo",
            "tiempo": 20,
            "estado": "Solucionado"
        },

        {
            "fecha": "30/10/2026",
            "fecha_iso": "2026-10-30",
            "olt": "HUAWEI CENTRAL",
            "zona": "Zona Central",
            "problema": "Caja sin óptico",
            "elemento": "Caja",
            "solucion": "Revisión de conectores y reparación de acometida",
            "tiempo": 45,
            "estado": "Solucionado"
        },

        {
            "fecha": "29/10/2026",
            "fecha_iso": "2026-10-29",
            "olt": "JUAN PABLO II",
            "zona": "Juan Pablo II",
            "problema": "Mufa sin óptico",
            "elemento": "Mufa",
            "solucion": "Revisión y reparación de empalme de fibra",
            "tiempo": 90,
            "estado": "Solucionado"
        },

        {
            "fecha": "29/10/2026",
            "fecha_iso": "2026-10-29",
            "olt": "HUAWEI CENTRAL",
            "zona": "Zona Central",
            "problema": "ONU en LOS",
            "elemento": "ONU",
            "solucion": "Revisión de acometida y reconexión óptica",
            "tiempo": 30,
            "estado": "Solucionado"
        },

        {
            "fecha": "28/10/2026",
            "fecha_iso": "2026-10-28",
            "olt": "JICAMARCA",
            "zona": "Jicamarca",
            "problema": "Power Fail",
            "elemento": "Alimentación eléctrica",
            "solucion": "Restablecimiento de alimentación del equipo",
            "tiempo": 25,
            "estado": "Solucionado"
        },

        {
            "fecha": "28/10/2026",
            "fecha_iso": "2026-10-28",
            "olt": "JUAN PABLO II",
            "zona": "Juan Pablo II",
            "problema": "Router sin conexión",
            "elemento": "Router",
            "solucion": "Pendiente de visita técnica",
            "tiempo": 0,
            "estado": "Pendiente"
        }

    ]

    solucionadas = sum(
        1 for item in registros
        if item["estado"] == "Solucionado"
    )

    tiempos = [
        item["tiempo"]
        for item in registros
        if item["estado"] == "Solucionado"
    ]

    tiempo_promedio = (
        round(sum(tiempos) / len(tiempos))
        if tiempos else 0
    )

    return render_template(
        "historial.html",
        historial=registros,
        solucionadas=solucionadas,
        tiempo_promedio=tiempo_promedio,
        datos_demo=True
    )


# =====================================================
# REPORTES
# =====================================================

@app.route("/reportes")
def reportes():

    datos = obtener_datos_monitoreo()

    return render_template(
        "reportes.html",
        **datos
    )


# =====================================================
# USUARIOS
# =====================================================

@app.route("/usuarios")
def usuarios():

    return render_template("usuarios.html")


# =====================================================
# CONFIGURACIÓN
# =====================================================

@app.route("/configuracion")
def configuracion():

    return render_template("configuracion.html")


# =====================================================
# EJECUCIÓN
# =====================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
