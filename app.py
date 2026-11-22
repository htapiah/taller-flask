# -*- coding: utf-8 -*-
"""
Evaluación Nª 3: Programacion Web
Alumno: Héctor Enrique Tapia Huaiquil
"""
from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)

# Registros guardados en memoria (se pierden al apagar el servidor)
registros = []


# ---------------------------------------------------------------
# FUNCIONES DE APOYO (EJERCICIOS 1 al 6 )
# ---------------------------------------------------------------
def calcular_promedio(nota1, nota2, nota3):
    """Devuelve el promedio de las tres notas con un decimal."""
    return round((nota1 + nota2 + nota3) / 3, 1)


def definir_estado(promedio, asistencia):
    """Aprobado solo si promedio >= 40 y asistencia >= 75."""
    if promedio >= 40 and asistencia >= 75:
        return "APROBADO"
    return "REPROBADO"


def contar_letras(nombre):
    """Cuenta solo las letras del nombre (sin espacios)."""
    return len([c for c in nombre if c.isalpha()])


def nombre_mas_largo(nombres):
    """Devuelve (nombre, cantidad) del nombre con más letras."""
    mayor = max(nombres, key=contar_letras)
    return mayor, contar_letras(mayor)


# ---------------------------------------------------------------
# RUTAS
# ---------------------------------------------------------------
@app.route("/")
def index():
    """Página principal: menú con dos botones."""
    return render_template("index.html")


@app.route("/inicio")
def inicio():
    """Redirección hacia la página principal."""
    return redirect(url_for("index"))


@app.route("/ejercicio1", methods=["GET", "POST"])
def ejercicio1():
    """Formulario de notas: GET muestra el formulario, POST lo procesa."""
    if request.method == "GET":
        return render_template("ejercicio1.html")

    try:
        nota1 = float(request.form["nota1"])
        nota2 = float(request.form["nota2"])
        nota3 = float(request.form["nota3"])
        asistencia = float(request.form["asistencia"])
    except (KeyError, ValueError):
        # Si faltan datos o no son números, se aborta la conexión
        abort(400)

    notas_validas = all(10 <= n <= 70 for n in (nota1, nota2, nota3))
    if not notas_validas or not 0 <= asistencia <= 100:
        return render_template(
            "ejercicio1.html",
            error="Las notas deben estar entre 10 y 70 y la asistencia entre 0 y 100.",
        )

    promedio = calcular_promedio(nota1, nota2, nota3)
    estado = definir_estado(promedio, asistencia)
    registros.append({"ejercicio": "Ejercicio 1",
                      "detalle": f"Promedio {promedio} con asistencia {asistencia:g}%",
                      "resultado": estado})
    return render_template("ejercicio1.html", promedio=promedio, estado=estado)


@app.route("/ejercicio2", methods=["GET", "POST"])
def ejercicio2():
    """Formulario de nombres: muestra el nombre con más letras."""
    if request.method == "GET":
        return render_template("ejercicio2.html")

    nombres = [request.form.get(f"nombre{i}", "").strip() for i in (1, 2, 3)]
    if "" in nombres:
        abort(400)

    if len({n.lower() for n in nombres}) < 3:
        return render_template("ejercicio2.html",
                               error="Los 3 nombres deben ser diferentes.")

    mayor, cantidad = nombre_mas_largo(nombres)
    registros.append({"ejercicio": "Ejercicio 2",
                      "detalle": ", ".join(nombres),
                      "resultado": f"{mayor} ({cantidad} caracteres)"})
    return render_template("ejercicio2.html", mayor=mayor, cantidad=cantidad)


@app.route("/registros")
def ver_registros():
    """Lista todos los registros guardados en memoria."""
    return render_template("registros.html", registros=registros)


@app.route("/registros/<int:numero>")
def ver_registro(numero):
    """Ruta con parámetro por URL: muestra un solo registro."""
    if numero < 1 or numero > len(registros):
        abort(404)
    return render_template("registros.html", registros=[registros[numero - 1]],
                           numero=numero)


@app.errorhandler(404)
def no_encontrado(_error):
    return render_template("error.html", codigo=404,
                           mensaje="La página o el registro no existe."), 404


@app.errorhandler(400)
def solicitud_incorrecta(_error):
    return render_template("error.html", codigo=400,
                           mensaje="Los datos enviados no son válidos."), 400


if __name__ == "__main__":
    app.run(debug=True)