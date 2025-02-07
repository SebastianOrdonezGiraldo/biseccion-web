from flask import Flask, request, jsonify, render_template, send_file
import numpy as np
import sympy as sp
import pandas as pd
import os
from fpdf import FPDF

app = Flask(__name__)


def evaluar_funcion(funcion_str, x_val):
    """Convierte la función ingresada en una expresión evaluable."""
    x = sp.Symbol('x')
    try:
        funcion_sympy = sp.sympify(funcion_str)
        funcion_lambda = sp.lambdify(x, funcion_sympy, 'numpy')
        return funcion_lambda(x_val)
    except:
        return None


def biseccion(funcion_str, a, b, tol=1e-6, max_iter=100):
    """Método de bisección con validación de intervalo y almacenamiento de iteraciones."""
    try:
        f = lambda x: evaluar_funcion(funcion_str, x)
        if f(a) is None or f(b) is None:
            return {"error": "La función ingresada no es válida."}
        if f(a) * f(b) >= 0:
            return {"error": "El método de bisección no es aplicable en este intervalo."}

        iteraciones = []
        c = a
        prev_xr = None

        for i in range(1, max_iter + 1):
            c = (a + b) / 2
            if prev_xr is not None and c != 0:
                error = abs((c - prev_xr) / c) * 100
            else:
                error = 0  # Evita NaN cuando prev_xr es None o c es 0

            iteraciones.append([i, a, c, b, error, f(c)])
            prev_xr = c

            if abs(f(c)) < tol or (b - a) / 2 < tol:
                break

            if f(c) * f(a) < 0:
                b = c
            else:
                a = c

        df_iteraciones = pd.DataFrame(iteraciones, columns=["Iteración", "a", "Xr", "b", "Error %", "F(Xr)"])
        return {"raiz": c, "iteraciones": df_iteraciones.to_dict(orient="records")}
    except Exception as e:
        return {"error": str(e)}


def newton_raphson(funcion_str, x0, tol=1e-6, max_iter=100):
    """Método de Newton-Raphson para encontrar raíces."""
    try:
        x = sp.Symbol('x')
        funcion_sympy = sp.sympify(funcion_str)
        derivada = sp.diff(funcion_sympy, x)
        f = sp.lambdify(x, funcion_sympy, 'numpy')
        df = sp.lambdify(x, derivada, 'numpy')

        iteraciones = []
        for i in range(1, max_iter + 1):
            if df(x0) == 0:
                return {"error": "Derivada cero. No se puede aplicar Newton-Raphson."}
            x1 = x0 - f(x0) / df(x0)
            error = abs((x1 - x0) / x1) * 100
            iteraciones.append([i, x0, x1, error, f(x1)])
            if error < tol:
                break
            x0 = x1

        df_iteraciones = pd.DataFrame(iteraciones, columns=["Iteración", "Xn", "Xn+1", "Error %", "F(Xn+1)"])
        return {"raiz": x1, "iteraciones": df_iteraciones.to_dict(orient="records")}
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

    if metodo == "newton":
        resultado = newton_raphson(funcion, a, tol)
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

    return jsonify({"archivo": file_path})


if __name__ == "__main__":
    app.run(debug=True)
