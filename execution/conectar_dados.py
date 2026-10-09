# -*- coding: utf-8 -*-
"""
Conecta todos os botões 'Dados' e atalhos de região ao novo arquivo 'dados-clima-em-movimento.html'
em todas as páginas do Site Final.
"""
import io
import re
import os

base_dir = "Site Final"
paginas = [
    "gemini-pagina-inicial.html",
    "clima_em_movimento_o_fen_meno-2.html",
    "clima_em_movimento_el_ni_no.html",
    "la_nina_clima_em_movimento.html",
    "brasil-clima-em-movimento.html"
]

# 1. Atualizar o menu de navegação de todas as páginas para o botão Dados apontar para dados-clima-em-movimento.html
for arq in paginas:
    p = os.path.join(base_dir, arq)
    with io.open(p, "r", encoding="utf-8") as f:
        c = f.read()
    
    # Substituir no botão Dados do menu padronizado
    # Casos:
    # <button class="cm-btn" onclick="..." style="--hv:#ffffff"><i data-lucide="bar-chart-2"></i> Dados</button>
    # ou na gemini-pagina-inicial:
    # <button class="nav-btn flex items-center gap-1.5 px-3.5 py-1.5 rounded-full text-slate-300 hover:text-white hover:bg-slate-800/60 transition"><i data-lucide="bar-chart-2" class="w-3.5 h-3.5"></i> Dados</button>
    
    # Na gemini-pagina-inicial:
    c = re.sub(
        r'<button class="nav-btn flex items-center gap-1\.5 px-3\.5 py-1\.5 rounded-full text-slate-300 hover:text-white hover:bg-slate-800/60 transition">\s*<i data-lucide="bar-chart-2" class="w-3\.5 h-3\.5"></i>\s*Dados\s*</button>',
        r'<button class="nav-btn flex items-center gap-1.5 px-3.5 py-1.5 rounded-full text-slate-300 hover:text-white hover:bg-slate-800/60 transition" onclick="window.location.href=\'dados-clima-em-movimento.html\'">\n        <i data-lucide="bar-chart-2" class="w-3.5 h-3.5"></i> Dados\n      </button>',
        c
    )
    
    # No header padronizado das outras páginas:
    c = re.sub(
        r'<button class="cm-btn"[^>]*style="--hv:#ffffff">\s*<i data-lucide="bar-chart-2"></i>\s*Dados\s*</button>',
        r'<button class="cm-btn" onclick="window.location.href=\'dados-clima-em-movimento.html\'" style="--hv:#ffffff"><i data-lucide="bar-chart-2"></i> Dados</button>',
        c
    )

    with io.open(p, "w", encoding="utf-8") as f:
        f.write(c)
    print(f"Menu Dados atualizado em {arq}")

# 2. Conectar os botões especiais nas páginas específicas:
# 2.1 La Niña: botão 'X COMPARAR OS DOIS →'
p_nina = os.path.join(base_dir, "la_nina_clima_em_movimento.html")
with io.open(p_nina, "r", encoding="utf-8") as f:
    c_nina = f.read()

# Substituir onclick="openComparisonModal()" pelo link da página de Dados
c_nina = c_nina.replace(
    """<button onclick="openComparisonModal()" class="w-full sm:w-auto px-7 py-3.5 rounded-2xl bg-gradient-to-r from-cyan-600 via-sky-600 to-blue-700 hover:from-cyan-500 hover:to-sky-500 text-white font-bold text-sm tracking-wider uppercase shadow-glow-ice flex items-center justify-center gap-3 transition-all transform hover:-translate-y-0.5 active:translate-y-0">""",
    """<button onclick="window.location.href='dados-clima-em-movimento.html#bloco-comparador'" class="w-full sm:w-auto px-7 py-3.5 rounded-2xl bg-gradient-to-r from-cyan-600 via-sky-600 to-blue-700 hover:from-cyan-500 hover:to-sky-500 text-white font-bold text-sm tracking-wider uppercase shadow-glow-ice flex items-center justify-center gap-3 transition-all transform hover:-translate-y-0.5 active:translate-y-0">"""
)

with io.open(p_nina, "w", encoding="utf-8") as f:
    f.write(c_nina)
print("Botão Comparar em La Niña atualizado!")

# 2.2 Brasil: botão 'VER OS DADOS' ou modal de dados
p_br = os.path.join(base_dir, "brasil-clima-em-movimento.html")
with io.open(p_br, "r", encoding="utf-8") as f:
    c_br = f.read()

# Se houver botão de ver dados ou similar:
c_br = re.sub(
    r'onclick="openDataModal\([^)]*\)"',
    r'onclick="window.location.href=\'dados-clima-em-movimento.html#bloco-brasil\'"',
    c_br
)

with io.open(p_br, "w", encoding="utf-8") as f:
    f.write(c_br)
print("Botões de Dados em Brasil atualizados!")
