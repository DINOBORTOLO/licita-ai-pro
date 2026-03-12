# ESCOLHA O MODO DE OPERAÇÃO

# MODO = "api"          # Apenas APIs (mais rápido, pode falhar)
# MODO = "demo"         # Dados fictícios (para testes)
MODO = "hibrido"      # APIs + Links de busca (recomendado - sempre funciona)

if MODO == "api":
    from fontes import buscar_todas_fontes
elif MODO == "demo":
    from demo_dados import buscar_todas_fontes_demo as buscar_todas_fontes
else:  # hibrido
    from fontes_hibrido import buscar_todas_fontes_hibrido as buscar_todas_fontes