#!/usr/bin/env python3
"""
Script para executar o jogo Rally-X Clone.
"""
import sys
import os

# Adiciona src ao path
src_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "src")
sys.path.insert(0, src_path)

from rallyx_clone.app import main

if __name__ == "__main__":
    main()
