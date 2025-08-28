#!/usr/bin/env python3
"""
Windows printing shim for Melted Civic Node.
Uses win32print / win32api to send ticket files to the default or chosen printer.
"""

import sys
import win32print
import win32api

def print_file(path: str, printer: str | None = None):
    if printer:
        # Temporarily set the default printer
        win32print.SetDefaultPrinter(printer)
    win32api.ShellExecute(0, "print", path, None, ".", 0)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: win_print.py <file> [printer]")
        sys.exit(1)
    f = sys.argv[1]
    p = sys.argv[2] if len(sys.argv) > 2 else None
    print_file(f, p)
