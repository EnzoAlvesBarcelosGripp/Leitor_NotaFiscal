import pdfplumber
import re
import pandas as pd

def processar_nota(caminho_pdf):
    # 1. Extrai texto e tabelas do PDF
    with pdfplumber.open(caminho_pdf) as pdf:
        full_text = '\n'.join([page.extract_text() for page in pdf.pages])
        
        # 2. Campos fora da tabela (Regex)
        match_emissao = re.search(r"EMISS.O:\s*(\d{2}/\d{2}/\d{4})", full_text)
        data_emissao = match_emissao.group(1) if match_emissao else None

        match_pedido = re.search(r"PEDIDO\(S\):\s*(\d+)", full_text)
        numero_pedido = match_pedido.group(1) if match_pedido else None

        match_destinatario = re.search(r"DESTINAT.RIO:\s*(.*?)\s*(- \d+ -)", full_text)
        razao_social = match_destinatario.group(1) if match_destinatario else None

        match_desconto = re.search(r"DESCONTO.*?\n\s*[\d\.,]+\s+[\d\.,]+\s+([\d\.,]+)", full_text)
        valor_desconto = match_desconto.group(1) if match_desconto else None

        # 3. Extração dos produtos das tabelas
        produtos = []
        for pagina in pdf.pages:
            tabelas = pagina.extract_tables()
            for tabela in tabelas:
                if len(tabela) > 0 and tabela[0][0] and "CÓDIGO PRODUTO" in tabela[0][0]:
                    for linha in tabela[1:]:
                        if linha[0] and linha[1]:
                            # Separa quantidade e valor unitário com Regex seguro
                            quantidade = None
                            valor_unitario = None
                            
                            if linha[6]:
                                match_valores = re.search(r"(\d+,\d{4})\s*([\d\.]+,\d+)", linha[6])
                                if match_valores:
                                    quantidade = match_valores.group(1)
                                    valor_unitario = match_valores.group(2)
                            
                            produtos.append({
                                "Razão Social": razao_social,
                                "Data Emissão": data_emissao,
                                "Número Pedido": numero_pedido,
                                "Desconto": valor_desconto,
                                "Código": linha[0].strip(),
                                "Descrição": linha[1].replace('\n', ' ').strip(),
                                "Quantidade": quantidade,
                                "Valor Unitário": valor_unitario
                            })
                            
    return pd.DataFrame(produtos)