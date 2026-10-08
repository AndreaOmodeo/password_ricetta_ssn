#!/usr/bin/env python3
"""Find a five-digit numeric password for an encrypted PDF."""

import argparse
import io
from pathlib import Path

import pikepdf


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Try every five-digit numeric password against an encrypted PDF."
    )
    parser.add_argument(
        "pdf",
        nargs="?",
        type=Path,
        help="PDF to test (defaults to the PDF alongside this script)",
    )
    args = parser.parse_args()

    if not args.pdf.is_file():
        parser.error(f"PDF file not found: {args.pdf}")

    pdf_data = args.pdf.read_bytes()
    try:
        with pikepdf.open(io.BytesIO(pdf_data), password="") as pdf:
            if not pdf.is_encrypted:
                print(f"PDF is not encrypted: {args.pdf}")
                return 0
            print("PDF accepts an empty password; no five-digit search needed.")
            return 0
    except pikepdf.PasswordError:
        pass

    for number in range(100_000):
        password = f"{number:05d}"
        print(f"Trying password: {password}", end="\r", flush=True)
        try:
            with pikepdf.open(io.BytesIO(pdf_data), password=password):
                print(f"Password found: {password}.")
                return 0
        except pikepdf.PasswordError:
            if number and number % 10_000 == 0:
                print(f"Tried {number:,} passwords...")

    print("No five-digit numeric password found (searched 00000 through 99999).")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
