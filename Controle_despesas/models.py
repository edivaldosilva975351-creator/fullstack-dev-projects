from dataclasses import dataclass
from datetime import date

@dataclass
class Transaction:
    id: int | None
    valor: float
    categoria: str
    data: str  # formato YYYY-MM-DD
    tipo: str  # 'despesa' ou 'receita'
    descricao: str | None