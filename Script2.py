import pdfplumber

produtos = []

with pdfplumber.open("5ff238a8-f1dc-4583-9850-57195633a422.pdf") as pdf:
    for pagina in pdf.pages:
        tabelas = pagina.extract_tables()
        for tabela in tabelas:
            # Verifica se a tabela é a de produtos pelo cabeçalho
            if len(tabela) > 0 and tabela[0][0] and "CÓDIGO PRODUTO" in tabela[0][0]:
                for linha in tabela[1:]:  # Pula o cabeçalho
                    if linha[0] and linha[1]:  # Garante que é uma linha válida de produto
                        codigo = linha[0].strip()
                        descricao = linha[1].replace('\n', ' ').strip()
                        
                        partes_valores = linha[6].split() if linha[6] else []
                        quantidade = partes_valores[0] if len(partes_valores) > 0 else None
                        valor_unitario = partes_valores[1] if len(partes_valores) > 1 else None
                        
                        produtos.append({
                            "codigo": codigo,
                            "descricao": descricao,
                            "quantidade": quantidade,
                            "valor_unitario": valor_unitario
                        })

print(f"Total de produtos extraídos: {len(produtos)}")
for p in produtos[:3]:  # Mostra os 3 primeiros para conferência
    print(p)