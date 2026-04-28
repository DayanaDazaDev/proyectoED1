# tests/test_bitwise.py
"""Pruebas unitarias para validar la lógica ADT antes de la entrega."""
import sys, os, json

# Ajuste de ruta para importar desde la raíz del proyecto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from estructuras.bitwise_logic import CalculadoraBitwise

def ejecutar_pruebas():
    ruta_json = os.path.join("datos", "pruebas.json")
    with open(ruta_json, "r", encoding="utf-8") as f:
        casos = json.load(f)
    
    aprobados = 0
    print("🧪 Ejecutando pruebas unitarias...")
    for c in casos:
        try:
            res = CalculadoraBitwise.calcular(c["a"], c["b"], c["op"])
            assert res["resultado"] == c["esperado"], (
                f"Falla en {c['op']}({c['a']}, {c['b']}): "
                f"esperado {c['esperado']}, obtenido {res['resultado']}"
            )
            print(f"  ✅ {c['op']}({c['a']}, {c['b']}) -> {res['resultado']}")
            aprobados += 1
        except Exception as e:
            print(f"  ❌ {c['op']}({c['a']}, {c['b']}) -> {e}")
    
    print(f"\n📊 Resultados: {aprobados}/{len(casos)} pruebas pasaron correctamente.")
    if aprobados == len(casos):
        print("🎉 ¡Listo para entrega! La lógica es robusta.")
    return aprobados == len(casos)

if __name__ == "__main__":
    ejecutar_pruebas()
    