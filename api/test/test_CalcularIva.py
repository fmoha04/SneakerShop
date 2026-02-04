import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'web')))

from funciones_auxiliares import calculariva

def test_iva():
    resultado_esperado = 21
    resultado = calculariva(100)
    assert resultado == resultado_esperado
