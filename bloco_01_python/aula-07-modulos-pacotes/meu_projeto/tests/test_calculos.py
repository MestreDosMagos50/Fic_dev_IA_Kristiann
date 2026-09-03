import pytest
from analise import media, validar_notas
from analise.calculos import mediana

def test_media_simples():
    assert media([6.0, 8.0, 10.0]) == 8.0

def test_media_lista_com_um_elemento():
    assert media([7.5]) == 7.5

def test_media_lista_vazia_lanca_excecao():
    with pytest.raises(ValueError):
        media([])

def test_mediana_lista_impar():
    assert mediana([3.0, 7.0, 9.0]) == 7.0

def test_validar_notas_remove_invalidas():
    resultado = validar_notas([5.0, -1.0, 11.0, 8.0])
    assert resultado == [5.0, 8.0]
