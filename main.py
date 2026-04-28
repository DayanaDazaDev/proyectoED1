# main.py
"""Punto de entrada principal. Flask + Persistencia JSON + UI moderna."""
import json
from pathlib import Path
from datetime import datetime
from flask import Flask, request, render_template_string, jsonify
from estructuras.bitwise_logic import CalculadoraBitwise

app = Flask(__name__)
HISTORIAL_PATH = Path(__file__).parent / "datos" / "historial.json"

def cargar_historial():
    if HISTORIAL_PATH.exists():
        with open(HISTORIAL_PATH, "r", encoding="utf-8") as f:
            try: return json.load(f)
            except: return []
    return []

def guardar_en_historial(a, b, op, resultado):
    historial = cargar_historial()
    registro = {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "a": a, "b": b, "op": op, "resultado": resultado
    }
    historial.insert(0, registro)
    if len(historial) > 50: historial = historial[:50]
    with open(HISTORIAL_PATH, "w", encoding="utf-8") as f:
        json.dump(historial, f, indent=2, ensure_ascii=False)
    return True

@app.route("/api/historial")
def api_historial():
    return jsonify(cargar_historial())

@app.route("/api/historial/limpiar", methods=["POST"])
def limpiar_historial():
    with open(HISTORIAL_PATH, "w", encoding="utf-8") as f:
        json.dump([], f)
    return jsonify({"status": "ok"})

PLANTILLA = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Calculadora Bitwise</title>
<style>
  :root { --bg: #f8fafc; --card: #ffffff; --primary: #2563eb; --text: #0f172a; --muted: #64748b; }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: system-ui, sans-serif; background: var(--bg); color: var(--text); padding: 2rem; }
  .container { max-width: 680px; margin: 0 auto; }
  .card { background: var(--card); padding: 1.8rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
  h2 { margin-bottom: 1.2rem; }
  label { display: block; font-weight: 500; margin: 0.8rem 0 0.3rem; }
  input, select, button { width: 100%; padding: 0.7rem; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 0.95rem; margin-bottom: 0.5rem; }
  button { background: var(--primary); color: white; border: none; cursor: pointer; }
  button:hover { background: #1d4ed8; }
  .resultado { background: #eff6ff; border-left: 4px solid var(--primary); padding: 1rem; margin-top: 1.2rem; border-radius: 0 8px 8px 0; }
  table { width: 100%; border-collapse: collapse; margin-top: 0.8rem; font-family: monospace; }
  th, td { border: 1px solid #e2e8f0; padding: 0.5rem; text-align: center; }
  code { background: #f1f5f9; padding: 0.15rem 0.4rem; border-radius: 4px; }
  
  .btn-historial { position: fixed; top: 20px; right: 20px; background: var(--primary); color: white; border-radius: 50%; width: 48px; height: 48px; display: flex; align-items: center; justify-content: center; cursor: pointer; box-shadow: 0 4px 12px rgba(37,99,235,0.3); z-index: 100; font-size: 1.2rem; border: none; }
  .historial-panel { position: fixed; top: 0; right: -400px; width: 360px; height: 100vh; background: white; box-shadow: -6px 0 16px rgba(0,0,0,0.1); transition: right 0.3s ease; z-index: 99; padding: 1.5rem; overflow-y: auto; }
  .historial-panel.activo { right: 0; }
  .panel-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; padding-bottom: 0.8rem; border-bottom: 2px solid #e2e8f0; }
  .btn-limpiar { background: #ef4444; width: auto; padding: 0.4rem 0.8rem; font-size: 0.8rem; margin: 0; }
  .historial-item { background: #f8fafc; border-left: 3px solid var(--primary); padding: 0.8rem; margin-bottom: 0.6rem; border-radius: 0 6px 6px 0; cursor: pointer; transition: all 0.2s; }
  .historial-item:hover { background: #e0f2fe; transform: translateX(-4px); }
  .historial-item strong { color: var(--primary); }
  .overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.3); opacity: 0; pointer-events: none; transition: opacity 0.3s; z-index: 98; }
  .overlay.activo { opacity: 1; pointer-events: all; }
</style>
</head>
<body>
  <div class="overlay" id="overlay" onclick="togglePanel()"></div>
  <button class="btn-historial" onclick="togglePanel()" title="Historial">🕒</button>
  
  <div class="historial-panel" id="panel">
    <div class="panel-header">
      <h3>📜 Operaciones Recientes</h3>
      <button class="btn-limpiar" onclick="limpiarHistorial()">Limpiar</button>
    </div>
    <div id="lista-historial"><p style="color:#64748b; text-align:center; margin-top:20px;">Cargando...</p></div>
  </div>

  <div class="container">
    <div class="card">
      <h2>🧮 Calculadora de Operaciones Bitwise</h2>
      {% if error %}<div style="background:#fee2e2; color:#b91c1c; padding:0.8rem; border-radius:6px; margin-bottom:1rem;">⚠️ {{ error }}</div>{% endif %}
      <form method="POST">
        <label>Número A:</label>
        <input type="number" name="a" value="{{ request.form.get('a', '') }}" required>
        <label>Número B <small>(vacío para NOT)</small>:</label>
        <input type="number" name="b" value="{{ request.form.get('b', '') }}">
        <label>Operación:</label>
        <select name="operacion">
          {% for op in ['AND','OR','XOR','NOT','LSL','LSR'] %}
            <option value="{{ op }}" {% if request.form.get('operacion')==op %}selected{% endif %}>{{ op }}</option>
          {% endfor %}
        </select>
        <button type="submit" style="margin-top:1rem;">Calcular</button>
      </form>
      {% if resultado %}
      <div class="resultado">
        <h3>✅ Resultado</h3>
        <p><strong>Operación:</strong> {{ resultado.operacion }} | <strong>Decimal:</strong> {{ resultado.resultado }}</p>
        <p><strong>Binario:</strong> <code>{{ resultado.binario_completo }}</code></p>
        <h4 style="margin-top:0.8rem;">🔍 Visualización ({{ resultado.visualizacion.bits }} bits)</h4>
        <table>
          <tr><th>Entrada</th><th>Representación Binaria</th></tr>
          <tr><td>A ({{ resultado.a }})</td><td>{{ resultado.visualizacion.a_bin }}</td></tr>
          {% if resultado.visualizacion.b_bin is not none %}
          <tr><td>B ({{ resultado.b }})</td><td>{{ resultado.visualizacion.b_bin }}</td></tr>
          {% endif %}
          <tr><td><strong>Resultado</strong></td><td><strong>{{ resultado.visualizacion.res_bin }}</strong></td></tr>
        </table>
      </div>
      {% endif %}
    </div>
  </div>

  <script>
    function togglePanel() {
      document.getElementById('panel').classList.toggle('activo');
      document.getElementById('overlay').classList.toggle('activo');
      if(document.getElementById('panel').classList.contains('activo')) {
        cargarHistorial();
      }
    }
    
    function cargarHistorial() {
      fetch('/api/historial')
        .then(r => r.json())
        .then(data => {
          var c = document.getElementById('lista-historial');
          if (data.length === 0) { 
            c.innerHTML = '<p style="color:#64748b; text-align:center; margin-top:20px;">Sin operaciones aún</p>'; 
            return; 
          }
          var html = '';
          for(var i=0; i<data.length; i++) {
            var h = data[i];
            var bVal = h.b !== null ? h.b : '—';
            html += '<div class="historial-item" data-index="' + i + '">';
            html += '<strong>' + h.timestamp + '</strong><br>';
            html += h.a + ' ' + h.op + ' ' + bVal + ' = <strong>' + h.resultado + '</strong>';
            html += '</div>';
          }
          c.innerHTML = html;
          
          // Agregar event listeners
          document.querySelectorAll('.historial-item').forEach(function(item) {
            item.addEventListener('click', function() {
              var idx = parseInt(this.getAttribute('data-index'));
              cargarOperacion(idx);
            });
          });
        })
        .catch(err => {
          document.getElementById('lista-historial').innerHTML = '<p style="color:#ef4444; text-align:center;">Error al cargar</p>';
        });
    }
    
    function cargarOperacion(index) {
      fetch('/api/historial')
        .then(r => r.json())
        .then(data => {
          var h = data[index];
          document.querySelector('input[name="a"]').value = h.a;
          document.querySelector('input[name="b"]').value = h.b !== null ? h.b : '';
          document.querySelector('select[name="operacion"]').value = h.op;
          togglePanel();
          document.querySelector('.container').scrollIntoView({behavior: 'smooth', block: 'center'});
          var form = document.querySelector('form');
          form.style.boxShadow = '0 0 0 3px rgba(37,99,235,0.3)';
          setTimeout(function() { form.style.boxShadow = 'none'; }, 1000);
        });
    }
    
    function limpiarHistorial() {
      fetch('/api/historial/limpiar', {method: 'POST'})
        .then(() => cargarHistorial());
    }
  </script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    resultado, error = None, None
    if request.method == "POST":
        try:
            a = int(request.form["a"])
            b_raw = request.form.get("b", "").strip()
            b = int(b_raw) if b_raw else None
            op = request.form["operacion"]
            resultado = CalculadoraBitwise.calcular(a, b, op)
            guardar_en_historial(a, b, op, resultado["resultado"])
        except ValueError as e:
            error = f"Error de validación: {e}"
        except Exception as e:
            error = f"Error inesperado: {e}"
    return render_template_string(PLANTILLA, resultado=resultado, error=error)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
