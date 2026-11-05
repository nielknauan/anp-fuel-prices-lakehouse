"""Configuração central do pipeline (caminhos e fontes)."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

ANP_BASE_URL = (
    "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/shpc/dsas/ca"
)

# Mapeamento das colunas originais da ANP -> snake_case
COLUMN_MAP = {
    "Regiao - Sigla": "regiao_sigla",
    "Estado - Sigla": "uf",
    "Municipio": "municipio",
    "Revenda": "revenda",
    "CNPJ da Revenda": "cnpj_revenda",
    "Nome da Rua": "logradouro",
    "Numero Rua": "numero",
    "Complemento": "complemento",
    "Bairro": "bairro",
    "Cep": "cep",
    "Produto": "produto",
    "Data da Coleta": "data_coleta",
    "Valor de Venda": "valor_venda",
    "Valor de Compra": "valor_compra",
    "Unidade de Medida": "unidade_medida",
    "Bandeira": "bandeira",
}

# Faixa plausível de preço (R$) usada na regra de qualidade
PRICE_MIN = 0.5
PRICE_MAX = 30.0


@dataclass(frozen=True)
class Paths:
    root: Path

    @property
    def landing(self) -> Path:
        return self.root / "landing"

    @property
    def bronze(self) -> Path:
        return self.root / "bronze" / "precos_combustiveis"

    @property
    def silver(self) -> Path:
        return self.root / "silver" / "precos_combustiveis"

    @property
    def quarantine(self) -> Path:
        return self.root / "silver" / "precos_combustiveis_quarentena"


def get_paths() -> Paths:
    return Paths(Path(os.getenv("LAKEHOUSE_ROOT", "lakehouse")).resolve())
