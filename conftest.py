"""
Deixa a pasta do projeto visivel para os testes.

Sem isto, "from braille import ..." so funciona se o pytest for chamado
exatamente da raiz do projeto. Com isto, funciona de qualquer lugar.
"""

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent

if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))
