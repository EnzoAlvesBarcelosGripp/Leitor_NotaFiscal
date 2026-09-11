from script import processar_nota

# Executa a extração
df_nota = processar_nota("5ff238a8-f1dc-4583-9850-57195633a422.pdf")

# Salva em .csv configurado para o padrão do Excel
df_nota.to_csv("produtos_extraidos.csv", sep=";", encoding="utf-8-sig", index=False)