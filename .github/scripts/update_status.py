"""Membaca folder modul di repo dan memperbarui tabel status di README.md."""
from pathlib import Path

# ---- Pengaturan (sesuaikan dengan struktur repo) ----
MIN_FILES = 4                          # jumlah file minimum agar status menjadi "Selesai"
FOLDER_PATTERN = "modul{n}/{kind}"     # mis. modul1/LS dan modul1/LA
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


def status(folder: Path) -> str:
    if not folder.is_dir():
        return NOT_DONE
    files = [p for p in folder.rglob("*") if p.is_file() and p.name != ".gitkeep"]
    return DONE if len(files) >= MIN_FILES else NOT_DONE


def build_table() -> str:
    rows = [
        "| Modul | Topik | LS | LA |",
        "|-------|-------|--------|-------|",
    ]
    for n, topik in MODULES:
        ls = status(ROOT / FOLDER_PATTERN.format(n=n, kind="LS"))
        la = status(ROOT / FOLDER_PATTERN.format(n=n, kind="LA"))
        rows.append(f"| Modul {n} | {topik} | {ls} | {la} |")
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
