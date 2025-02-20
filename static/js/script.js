function calcularMetodo() {
    let funcion = document.getElementById("funcion").value;
    let metodo = document.getElementById("metodo").value;
    let a = parseFloat(document.getElementById("a").value);
    let b = parseFloat(document.getElementById("b").value);
    let tol = parseFloat(document.getElementById("tol").value);

    if (funcion.trim() === "") {
        Swal.fire({ icon: "error", title: "Error", text: "Por favor, ingresa una función válida." });
        return;
    }
    if (isNaN(a) || isNaN(b) || isNaN(tol)) {
        Swal.fire({ icon: "error", title: "Error", text: "Los valores de a, b y tolerancia deben ser numéricos." });
        return;
    }
    if (a === b) {
        Swal.fire({ icon: "error", title: "Error", text: "Los valores de a y b no pueden ser iguales." });
        return;
    }

    document.getElementById("loading").style.display = "block";

    fetch("/calcular", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ funcion, metodo, a, b, tol })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("loading").style.display = "none";

        if (data.error) {
            let mensajeError = `<b style='color:red;'>${data.error}</b>`;
            if (data.error.includes("El método de falsa posición no es aplicable")) {
                mensajeError += `<br><small>El método de falsa posición requiere que la función cambie de signo en el intervalo [a, b]. Asegúrate de que f(a) y f(b) tengan signos opuestos.</small>`;
            }
            document.getElementById("resultado").innerHTML = mensajeError;
            Swal.fire({ icon: "error", title: "Error de cálculo", html: mensajeError });
            return;
        }

        document.getElementById("resultado").innerHTML = `<b>Raíz encontrada:</b> ${data.raiz.toFixed(6)}`;

        let tablaBody = document.getElementById("tabla").getElementsByTagName("tbody")[0];
        tablaBody.innerHTML = "";
        data.iteraciones.forEach(iter => {
            let row = `<tr>
                <td>${iter.Iteración}</td><td>${iter.a.toFixed(6)}</td>
                <td>${iter.Xr.toFixed(6)}</td><td>${iter.b.toFixed(6)}</td>
                <td>${iter["Error %"] ? iter["Error %"].toFixed(2) + "%" : "-"}</td>
                <td>${iter["F(Xr)"].toFixed(6)}</td>
            </tr>`;
            tablaBody.innerHTML += row;
        });

        let x_vals = data.iteraciones.map(i => i.Xr);
        let y_vals = data.iteraciones.map(i => i["F(Xr)"]);

        Plotly.newPlot("grafica", [{ x: x_vals, y: y_vals, mode: "lines+markers", name: "Iteraciones" }], {
            title: "Convergencia del Método", xaxis: { title: "Xr (Aproximación)" }, yaxis: { title: "F(Xr)", zeroline: true }, responsive: true
        });

        document.getElementById("btnExportarCSV").style.display = "block";
        document.getElementById("btnExportarCSV").onclick = function() {
            exportarResultados("csv", data.iteraciones);
        };

        document.getElementById("btnExportarPDF").style.display = "block";
        document.getElementById("btnExportarPDF").onclick = function() {
            exportarResultados("pdf", data.iteraciones);
        };

        document.getElementById("btnExportarExcel").style.display = "block";
        document.getElementById("btnExportarExcel").onclick = function() {
            exportarResultados("xlsx", data.iteraciones);
        };

        document.getElementById("btnCopiarResultados").style.display = "block";
        document.getElementById("btnCopiarResultados").onclick = function() {
            copiarResultados(data.iteraciones);
        };
    });
}

function exportarResultados(formato, iteraciones) {
    fetch(`/exportar/${formato}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ iteraciones })
    })
    .then(response => response.json())
    .then(data => {
        window.location.href = data.archivo;
    });
}

function copiarResultados(iteraciones) {
    let texto = "Iteración\ta\tXr\tb\tError %\tF(Xr)\n";
    iteraciones.forEach(iter => {
        texto += `${iter.Iteración}\t${iter.a.toFixed(6)}\t${iter.Xr.toFixed(6)}\t${iter.b.toFixed(6)}\t${iter["Error %"].toFixed(2)}%\t${iter["F(Xr)"].toFixed(6)}\n`;
    });
    navigator.clipboard.writeText(texto).then(() => {
        Swal.fire({ icon: "success", title: "Copiado", text: "Los resultados han sido copiados al portapapeles." });
    });
}