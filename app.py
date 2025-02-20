from flask import Flask, request, jsonify, render_template, send_file
import numpy as np
import sympy as sp
import pandas as pd
import os
from fpdf import FPDF

app = Flask(__name__)


def evaluar_funcion(funcion_str, x_val):
    x = sp.Symbol('x')
    try:
        funcion_sympy = sp.sympify(funcion_str)
        funcion_lambda = sp.lambdify(x, funcion_sympy, 'numpy')
        return funcion_lambda(x_val)
    except:
        return None


def falsa_posicion(funcion_str, a, b, tol=1e-6, max_iter=100):
    try:
        f = lambda x: evaluar_funcion(funcion_str, x)
        if f(a) is None or f(b) is None:
            return {"error": "La función ingresada no es válida."}
        if f(a) * f(b) >= 0:
            return {"error": "El método de falsa posición no es aplicable en este intervalo. Asegúrate de que f(a) y f(b) tengan signos opuestos."}

        iteraciones = []
        xr = a
        prev_xr = None

        for i in range(1, max_iter + 1):
            xr = (a * f(b) - b * f(a)) / (f(b) - f(a))
            if prev_xr is not None and xr != 0:
                error = abs((xr - prev_xr) / xr) * 100
            else:
                error = 0

            iteraciones.append([i, a, xr, b, error, f(xr)])
            prev_xr = xr

            if abs(f(xr)) < tol:
                break

            if f(xr) * f(a) < 0:
                b = xr
            else:
                a = xr

        df_iteraciones = pd.DataFrame(iteraciones, columns=["Iteración", "a", "Xr", "b", "Error %", "F(Xr)"])
        return {"raiz": xr, "iteraciones": df_iteraciones.to_dict(orient="records")}
    except Exception as e:
        return {"error": str(e)}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/calcular", methods=["POST"])
def calcular():
    data = request.get_json()
    funcion = data.get("funcion")
    metodo = data.get("metodo", "biseccion")
    a = float(data.get("a"))
    b = float(data.get("b"))
    tol = float(data.get("tol"))

    if a == b:
        return jsonify({"error": "Los valores de a y b no pueden ser iguales."})

    if metodo == "newton":
        resultado = newton_raphson(funcion, a, tol)
    elif metodo == "falsa_posicion":
        resultado = falsa_posicion(funcion, a, b, tol)
    else:
        resultado = biseccion(funcion, a, b, tol)

    return jsonify(resultado)


@app.route("/exportar/<formato>", methods=["POST"])
def exportar(formato):
    data = request.get_json()
    df = pd.DataFrame(data["iteraciones"])
    file_path = f"static/resultados.{formato}"

    if formato == "csv":
        df.to_csv(file_path, index=False, sep=";", encoding="utf-8-sig")
    elif formato == "pdf":
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, "Resultados del Método Numérico", ln=True, align='C')
        pdf.ln(10)
        for col in df.columns:
            pdf.cell(40, 10, col, border=1)
        pdf.ln()
        for _, row in df.iterrows():
            for value in row:
                pdf.cell(40, 10, str(value), border=1)
            pdf.ln()
        pdf.output(file_path)
    elif formato == "xlsx":
        df.to_excel(file_path, index=False)

    return jsonify({"archivo": file_path})


if __name__ == "__main__":
    app.run(debug=True)
