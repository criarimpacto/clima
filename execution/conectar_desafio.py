# -*- coding: utf-8 -*-
"""
Conecta todos os botões 'Desafio' de todas as páginas em 'Site Final'
para abrirem diretamente 'desafio-clima-em-movimento.html'.
"""
import io, os, re

base_dir = "Site Final"
paginas = [
    "gemini-pagina-inicial.html",
    "clima_em_movimento_o_fen_meno-2.html",
    "clima_em_movimento_el_ni_no.html",
    "la_nina_clima_em_movimento.html",
    "brasil-clima-em-movimento.html",
    "dados-clima-em-movimento.html"
]

for arq in paginas:
    p = os.path.join(base_dir, arq)
    c = io.open(p, "r", encoding="utf-8").read()

    # 1. No menu superior padronizado:
    # <button class="cm-btn" onclick="..." style="--hv:#ffffff"><i data-lucide="gamepad-2"></i> Desafio</button>
    c = re.sub(
        r'<button class="cm-btn"[^>]*style="--hv:#ffffff">\s*<i data-lucide="gamepad-2"></i>\s*Desafio\s*</button>',
        r'<button class="cm-btn" onclick="window.location.href=\'desafio-clima-em-movimento.html\'" style="--hv:#ffffff"><i data-lucide="gamepad-2"></i> Desafio</button>',
        c
    )

    # 2. Na gemini-pagina-inicial.html:
    c = re.sub(
        r'<button class="nav-btn flex items-center gap-1\.5 px-3\.5 py-1\.5 rounded-full text-slate-300 hover:text-white hover:bg-slate-800/60 transition"[^>]*>\s*<i data-lucide="gamepad-2" class="w-3\.5 h-3\.5"></i>\s*Desafio\s*</button>',
        r'<button class="nav-btn flex items-center gap-1.5 px-3.5 py-1.5 rounded-full text-slate-300 hover:text-white hover:bg-slate-800/60 transition" onclick="window.location.href=\'desafio-clima-em-movimento.html\'">\n        <i data-lucide="gamepad-2" class="w-3.5 h-3.5"></i> Desafio\n      </button>',
        c
    )

    # 3. Na página Brasil: CTA 'TESTAR MEU CONHECIMENTO'
    if arq == "brasil-clima-em-movimento.html":
        c = c.replace(
            '<button onclick="openQuizModal()" class="w-full sm:w-auto px-8 py-4 rounded-2xl bg-ocean-900',
            '<button onclick="window.location.href=\'desafio-clima-em-movimento.html\'" class="w-full sm:w-auto px-8 py-4 rounded-2xl bg-ocean-900'
        )

    # 4. Na página Dados: botão 'Desafio' no menu que chamava showDesafioToast()
    if arq == "dados-clima-em-movimento.html":
        c = c.replace(
            '<button class="cm-btn" onclick="showDesafioToast()" style="--hv:#ffffff">\n        <i data-lucide="gamepad-2"></i> Desafio\n      </button>',
            '<button class="cm-btn" onclick="window.location.href=\'desafio-clima-em-movimento.html\'" style="--hv:#ffffff">\n        <i data-lucide="gamepad-2"></i> Desafio\n      </button>'
        )

    io.open(p, "w", encoding="utf-8").write(c)
    print(f"Desafio linkado com sucesso em: {arq}")

print("Todos os botões de Desafio foram linkados para desafio-clima-em-movimento.html!")
