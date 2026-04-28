# estructuras/bitwise_logic.py
"""
ADT CalculadoraBitwise
Implementación orientada a la enseñanza de operaciones a nivel de bits.
Sigue los principios de la Unidad II: encapsulamiento, validación explícita y separación de responsabilidades.
"""
from typing import Optional, Dict, Any

class CalculadoraBitwise:
    """Clase que expone operaciones bitwise con validación y visualización educativa."""
    
    OPERACIONES = {
        "AND": lambda a, b: a & b,
        "OR":  lambda a, b: a | b,
        "XOR": lambda a, b: a ^ b,
        "NOT": lambda a, _: ~a,
        "LSL": lambda a, b: a << b,
        "LSR": lambda a, b: a >> b
    }

    @classmethod
    def calcular(cls, a: int, b: Optional[int], operacion: str) -> Dict[str, Any]:
        """Ejecuta la operación bitwise y retorna un diccionario estructurado."""
        operacion = operacion.upper()
        if operacion not in cls.OPERACIONES:
            raise ValueError(f"Operación '{operacion}' no soportada. Use: {', '.join(cls.OPERACIONES.keys())}")

        # Validación de aridad según tipo de operación
        if operacion == "NOT":
            if b is not None:
                raise ValueError("NOT es unaria. El campo B debe quedar vacío.")
            resultado = ~a
        elif operacion in ("LSL", "LSR"):
            if b is None:
                raise ValueError("Desplazamientos requieren un segundo número (cantidad de bits).")
            if b < 0:
                raise ValueError("La cantidad de bits para desplazar no puede ser negativa.")
            resultado = a << b if operacion == "LSL" else a >> b
        else:
            if b is None:
                raise ValueError(f"{operacion} requiere dos operandos. Complete el campo B.")
            resultado = cls.OPERACIONES[operacion](a, b)

        # Valor añadido: ajuste dinámico del ancho de bits para visualización limpia
        max_val = max(abs(a), abs(b) if b is not None else 0, abs(resultado))
        bits = 8 if max_val < 128 else 16 if max_val < 32768 else 32
        mascara = (1 << bits) - 1

        return {
            "operacion": operacion,
            "a": a,
            "b": b,
            "resultado": resultado,
            "binario_completo": bin(resultado),
            "visualizacion": {
                "bits": bits,
                "a_bin": format(a & mascara, f"0{bits}b"),
                "b_bin": format((b & mascara) if b is not None else 0, f"0{bits}b"),
                "res_bin": format(resultado & mascara, f"0{bits}b")
            }
        }
