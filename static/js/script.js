function calcularBiseccion() {
    let funcion = document.getElementById("funcion").value;
    let metodo = document.getElementById("metodo").value;
    let a = document.getElementById("a").value;
    let b = document.getElementById("b").value;
    let tol = document.getElementById("tol").value;

    if (funcion.trim() === "") {
        alert("Por favor, ingresa una función válida.");
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
            document.getElementById("resultado").innerHTML = `<b style='color:red;'>${data.error}</b>`;
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

        Plotly.newPlot("grafica", [{ x: x_vals, y: y_vals, mode: "lines+markers", name: "Iteraciones" }], { title: "Convergencia de Bisección" });

        document.getElementById("btnExportarCSV").style.display = "block";
        document.getElementById("btnExportarCSV").onclick = function() {
            exportarResultados("csv", data.iteraciones);
        };

        document.getElementById("btnExportarPDF").style.display = "block";
        document.getElementById("btnExportarPDF").onclick = function() {
            exportarResultados("pdf", data.iteraciones);
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
