import pytest
import os

def test_project_structure():
    """Verifica se os arquivos essenciais existem."""
    assert os.path.exists("main.py")
    assert os.path.exists("src/prospector.py")

def test_database_connection():
    """Verifica se a pasta de dados existe."""
    assert os.path.exists("data")
