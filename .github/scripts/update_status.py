"""Membaca folder modul di repo dan memperbarui tabel status di README.md."""
import re
from pathlib import Path

MIN_FILES = 3
DONE, NOT_DONE = "Selesai", "Belum"

MODULES = [
    (1, "Pengantar Mikrokontroler"),
    (2, "Sensor dan Aktuator Motor"),
    (3, "Komunikasi Serial dan Interfacing"),
    (4, "Interrupt, Timer, Watchdog, dan Multitasking"),
    (5, "Pemrosesan Data dan Dasar Sistem Kontrol"),
]

START, END = "<!-- STATUS:START -->", "<!-- STATUS:END -->"
ROOT = Path(__file__).resolve().parents[2]


def find_module_dir(n: int) -> Path | None:
    """Cari folder 'Modul_1', 'Modul _1', 'modul1', dst. (tidak peduli huruf/spasi/underscore)."""
    pattern = re.compile(rf"^modul[\s_]*{n}$", re.IGNORECASE)
    for p in ROOT.iterdir():
        if p.is_dir() and pattern.match(p.name):
            return p
    return None


def status(module_dir: Path | None, kind: str) -> str:
    count = 0
    if module_dir is not None:
        count = sum(
            1 for p in module_dir.rglob("*.pdf")
            if p.is_file() and p.name.upper().startswith(f"{kind}_")
        )
    label = DONE if count >= MIN_FILES else NOT_DONE
    return f"{label}({min(count, MIN_FILES)}/{MIN_FILES})"


def build_table() -> str:
    rows = [
        "| Modul | Topik | LS | LA |",
        "|-------|-------|--------|-------|",
    ]
    for n, topik in MODULES:
        d = find_module_dir(n)
        rows.append(f"| Modul {n} | {topik} | {status(d, 'LS')} | {status(d, 'LA')} |")
    return "\n".join(rows)


def main() -> None:
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    if START not in text or END not in text:
        raise SystemExit(f"Penanda {START} dan {END} tidak ditemukan di README.md")

    before, rest = text.split(START, 1)
    _, after = rest.split(END, 1)
    new_text = f"{before}{START}\n{build_table()}\n{END}{after}"

    if new_text != text:
        readme.write_text(new_text, encoding="utf-8")
        print("README.md diperbarui")
    else:
        print("Tidak ada perubahan")


if __name__ == "__main__":
    main()
