"""Landing: baixa os arquivos semestrais da ANP (CSV ou ZIP) para a camada landing."""
from __future__ import annotations

import io
import logging
import shutil
import urllib.request
import zipfile
from pathlib import Path

from .config import ANP_BASE_URL

log = logging.getLogger(__name__)


def download_semester(semester: str, landing_dir: Path) -> Path:
    """Baixa um semestre (ex: '2024-01') e devolve o caminho do CSV na landing.

    A ANP publica semestres antigos como .csv e os recentes como .zip,
    então o download tenta os dois formatos.
    """
    landing_dir.mkdir(parents=True, exist_ok=True)
    target = landing_dir / f"ca-{semester}.csv"
    if target.exists():
        log.info("landing: %s já existe, pulando download", target.name)
        return target

    for ext in ("zip", "csv"):
        url = f"{ANP_BASE_URL}/ca-{semester}.{ext}"
        try:
            log.info("landing: baixando %s", url)
            with urllib.request.urlopen(url, timeout=120) as resp:
                payload = resp.read()
        except Exception as exc:  # noqa: BLE001
            log.warning("landing: falha em %s (%s)", url, exc)
            continue

        if ext == "zip":
            with zipfile.ZipFile(io.BytesIO(payload)) as zf:
                csv_name = next(n for n in zf.namelist() if n.lower().endswith(".csv"))
                with zf.open(csv_name) as src, open(target, "wb") as dst:
                    shutil.copyfileobj(src, dst)
        else:
            target.write_bytes(payload)
        return target

    raise RuntimeError(f"Não foi possível baixar o semestre {semester}")


def copy_sample(sample_file: Path, landing_dir: Path) -> Path:
    """Copia o arquivo de amostra versionado no repo para a landing (modo offline/CI)."""
    landing_dir.mkdir(parents=True, exist_ok=True)
    target = landing_dir / sample_file.name
    shutil.copy(sample_file, target)
    return target
