import argparse
import sys
import os
import pipeline

def main() -> None:
    parser = argparse.ArgumentParser(
        description='Digitaliza documentos escaneados via OCR + NLP.'
    )
    parser.add_argument(
        'arquivo',
        help='Caminho para a imagem (PNG/JPEG) ou PDF escaneado.'
    )
    parser.add_argument(
        '--saida', default='resultados',
        help='Diretório de saída (padrão: resultados/).'
    )
    parser.add_argument(
        '--top', type=int, default=20,
        help='Número de termos mais frequentes (padrão: 20).'
    )
    
    args = parser.parse_args()
    
    if not os.path.isfile(args.arquivo):
        print(f'Erro: arquivo nao encontrado: {args.arquivo}')
        sys.exit(1)
        
    ext = os.path.splitext(args.arquivo)[1].lower()
    if ext not in ('.png', '.jpg', '.jpeg', '.tif', '.tiff', '.pdf'):
        print(f'Erro: formato nao suportado: {ext}')
        print('Formatos aceitos: .png .jpg .jpeg .tif .tiff .pdf')
        sys.exit(1)
        
    print('=' * 56)
    print(' DIGITALIZADOR DE DOCUMENTOS ESCANEADOS')
    print(' OCR (Tesseract) + NLP (spaCy pt_core_news_sm)')
    print('=' * 56)
    print(f' Entrada : {args.arquivo}')
    print(f' Saída   : {args.saida}/')
    print('=' * 56)
    print()
    
    try:
        resultado = pipeline.processar_documento(
            args.arquivo,
            dir_saida=args.saida,
            top_n=args.top,
        )
        pipeline.exibir_resumo(resultado)
    except FileNotFoundError as e:
        print(f'Erro: {e}')
        sys.exit(1)
    except OSError as e:
        print(f'Erro de configuração: {e}')
        sys.exit(1)
    except Exception as e:
        print(f'Erro inesperado: {e}')
        raise

if __name__ == '__main__':
    main()
