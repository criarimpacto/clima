# -*- coding: utf-8 -*-
"""
Aplica todas as correções solicitadas pelo usuário estritamente na pasta 'Site Final':
1. Botão 'MAS O QUE CAUSA TUDO ISSO?' (gemini-pagina-inicial.html) aponta para 'clima_em_movimento_o_fen_meno-2.html'
2. Remove o botão 'Sobre' do menu de navegação de todas as páginas onde existia
3. Em El Niño:
   - CTA 'VER LA NIÑA' navega para 'la_nina_clima_em_movimento.html'
   - CTA 'VER IMPACTOS NO BRASIL' navega para 'brasil-clima-em-movimento.html'
4. Em La Niña:
   - CTA 'VER EL NIÑO' navega para 'clima_em_movimento_el_ni_no.html'
   - CTA 'IR PARA O BRASIL' navega para 'brasil-clima-em-movimento.html'
   - Botão 'Ir para El Niño →' dentro do modal de comparação navega para 'clima_em_movimento_el_ni_no.html'
5. Logo 'CLIMA EM MOVIMENTO' aponta para 'gemini-pagina-inicial.html' em todas as páginas
6. Remove todos os botões de baixar HTML em todas as páginas
7. Avisos da legenda do mapa em brasil-clima-em-movimento.html transformados em apenas efeito hover sem onclick
"""

import io
import re
import os

base_dir = "Site Final"

# ==========================================
# 1. gemini-pagina-inicial.html
# ==========================================
p_home = os.path.join(base_dir, "gemini-pagina-inicial.html")
with io.open(p_home, "r", encoding="utf-8") as f:
    c_home = f.read()

# 1.1 Botão 'MAS O QUE CAUSA TUDO ISSO?' aponta para clima_em_movimento_o_fen_meno-2.html
c_home = c_home.replace(
    """<button onclick="navigateTo('page-fenomeno')" class="inline-flex flex-col items-center gap-2 group text-slate-400 hover:text-cyan-300 transition">""",
    """<button onclick="window.location.href='clima_em_movimento_o_fen_meno-2.html'" class="inline-flex flex-col items-center gap-2 group text-slate-400 hover:text-cyan-300 transition">"""
)

# 1.2 Logo CLIMA EM MOVIMENTO aponta para gemini-pagina-inicial.html
c_home = c_home.replace(
    """<div onclick="navigateTo('page-home')" class="flex items-center gap-3 cursor-pointer group">""",
    """<div onclick="window.location.href='gemini-pagina-inicial.html'" class="flex items-center gap-3 cursor-pointer group">"""
)

# 1.3 Remover botão 'Sobre' do menu
# Procurar pelo bloco do botão Sobre dentro do <nav>
c_home = re.sub(
    r'<button class="nav-btn flex items-center gap-1\.5 px-3\.5 py-1\.5 rounded-full text-slate-300 hover:text-white hover:bg-slate-800/60 transition">\s*<i data-lucide="info" class="w-3\.5 h-3\.5"></i>\s*Sobre\s*</button>',
    '',
    c_home
)

with io.open(p_home, "w", encoding="utf-8") as f:
    f.write(c_home)
print("gemini-pagina-inicial.html atualizado!")


# ==========================================
# 2. clima_em_movimento_o_fen_meno-2.html
# ==========================================
p_fen = os.path.join(base_dir, "clima_em_movimento_o_fen_meno-2.html")
with io.open(p_fen, "r", encoding="utf-8") as f:
    c_fen = f.read()

# 2.1 Logo CLIMA EM MOVIMENTO aponta para gemini-pagina-inicial.html
# Linha 169: <div class="flex items-center gap-3 select-none">
c_fen = c_fen.replace(
    """<div class="flex items-center gap-3 select-none">""",
    """<div onclick="window.location.href='gemini-pagina-inicial.html'" class="flex items-center gap-3 select-none cursor-pointer group">"""
)

# 2.2 Remover botão 'Sobre' do menu
c_fen = re.sub(
    r'<button onclick="openModal\(\'sobre\'\)" class="flex items-center gap-1\.5 px-3\.5 py-1\.5 rounded-full text-slate-300 hover:text-white hover:bg-slate-800/60 transition">\s*<i data-lucide="info" class="w-3\.5 h-3\.5"></i>\s*Sobre\s*</button>',
    '',
    c_fen
)

# 2.3 Remover botão baixar index.html
c_fen = re.sub(
    r'<!-- Botão de Download do index\.html para o Antigravity -->\s*<div class="flex items-center gap-2">\s*<button onclick="downloadCodeFile\(\)"[^>]*>.*?</button>\s*</div>',
    '',
    c_fen,
    flags=re.DOTALL
)

with io.open(p_fen, "w", encoding="utf-8") as f:
    f.write(c_fen)
print("clima_em_movimento_o_fen_meno-2.html atualizado!")


# ==========================================
# 3. clima_em_movimento_el_ni_no.html
# ==========================================
p_nino = os.path.join(base_dir, "clima_em_movimento_el_ni_no.html")
with io.open(p_nino, "r", encoding="utf-8") as f:
    c_nino = f.read()

# 3.1 Logo CLIMA EM MOVIMENTO aponta para gemini-pagina-inicial.html
c_nino = re.sub(
    r'<a href="#" class="flex items-center gap-3\.5 group">',
    r'<a href="gemini-pagina-inicial.html" class="flex items-center gap-3.5 group">',
    c_nino,
    count=1
)

# 3.2 Remover botão 'Sobre' do menu
c_nino = re.sub(
    r'<button onclick="openModal\(\'sobre\'\)" class="px-3\.5 py-2 rounded-lg text-xs font-medium text-slate-300 hover:text-white hover:bg-ocean-850 flex items-center gap-1\.5 transition">\s*<svg.*?</svg>\s*Sobre\s*</button>',
    '',
    c_nino,
    flags=re.DOTALL
)

# 3.3 CTA 1: VER LA NIÑA navega para la_nina_clima_em_movimento.html
c_nino = re.sub(
    r'<!-- CTA 1: VER LA NIÑA -->\s*<button\s+onclick="[^"]*"\s+class="([^"]*)"',
    r"""<!-- CTA 1: VER LA NIÑA -->\n        <button \n          onclick="window.location.href='la_nina_clima_em_movimento.html'" \n          class="\1\"""",
    c_nino
)

# 3.4 CTA 2: VER IMPACTOS NO BRASIL navega para brasil-clima-em-movimento.html
c_nino = re.sub(
    r'<!-- CTA 2: VER IMPACTOS NO BRASIL -->\s*<button\s+onclick="openBrazilModal\(\)"\s+class="([^"]*)"',
    r"""<!-- CTA 2: VER IMPACTOS NO BRASIL -->\n        <button \n          onclick="window.location.href='brasil-clima-em-movimento.html'" \n          class="\1\"""",
    c_nino
)

with io.open(p_nino, "w", encoding="utf-8") as f:
    f.write(c_nino)
print("clima_em_movimento_el_ni_no.html atualizado!")


# ==========================================
# 4. la_nina_clima_em_movimento.html
# ==========================================
p_nina = os.path.join(base_dir, "la_nina_clima_em_movimento.html")
with io.open(p_nina, "r", encoding="utf-8") as f:
    c_nina = f.read()

# 4.1 Logo CLIMA EM MOVIMENTO aponta para gemini-pagina-inicial.html
c_nina = re.sub(
    r'<a href="#" class="flex items-center gap-3\.5 group">',
    r'<a href="gemini-pagina-inicial.html" class="flex items-center gap-3.5 group">',
    c_nina,
    count=1
)

# 4.2 Remover botão 'Sobre' do menu
c_nina = re.sub(
    r'<!-- Sobre Item -->\s*<button onclick="openModal\(\'sobre\'\)" class="px-3 py-2 rounded-lg text-xs font-medium text-slate-300 hover:text-white hover:bg-ocean-850 flex items-center gap-1\.5 transition">\s*<svg.*?</svg>\s*Sobre\s*</button>',
    '',
    c_nina,
    flags=re.DOTALL
)

# 4.3 Remover botão baixar site (.html) da navbar
c_nina = re.sub(
    r'<!-- Direct Download Action in Navbar -->\s*<div class="flex items-center gap-3">\s*<button onclick="downloadHtmlFile\(\)" id="btn-navbar-download"[^>]*>.*?</button>\s*</div>',
    '',
    c_nina,
    flags=re.DOTALL
)

# 4.4 Remover botão flutuante de download (FAB)
c_nina = re.sub(
    r'<!-- Botão Flutuante de Download Destacado \(FAB\) -->\s*<aside class="fixed bottom-6 left-6 z-40">\s*<button onclick="downloadHtmlFile\(\)" id="btn-floating-download"[^>]*>.*?</button>\s*</aside>',
    '',
    c_nina,
    flags=re.DOTALL
)

# 4.5 CTA rodapé: Botão 1: VER EL NIÑO navega para clima_em_movimento_el_ni_no.html
c_nina = re.sub(
    r'<!-- Botão 1: VER EL NIÑO \(Laranja\) -->\s*<button onclick="navigateToElNino\(\)"',
    r"""<!-- Botão 1: VER EL NIÑO (Laranja) -->\n        <button onclick="window.location.href='clima_em_movimento_el_ni_no.html'\"""",
    c_nina
)

# 4.6 CTA rodapé: Botão 3: IR PARA O BRASIL navega para brasil-clima-em-movimento.html
c_nina = re.sub(
    r'<!-- Botão 3: IR PARA O BRASIL \(Verde\) -->\s*<button onclick="openBrazilModal\(\)"',
    r"""<!-- Botão 3: IR PARA O BRASIL (Verde) -->\n        <button onclick="window.location.href='brasil-clima-em-movimento.html'\"""",
    c_nina
)

# 4.7 Botão 'Ir para El Niño →' dentro do modal openComparisonModal
c_nina = c_nina.replace(
    """<button onclick="navigateToElNino()" class="px-4 py-2 rounded-xl bg-orange-600/30 border border-orange-500 text-orange-200 text-xs font-bold hover:bg-orange-600 hover:text-white transition">""",
    """<button onclick="window.location.href='clima_em_movimento_el_ni_no.html'" class="px-4 py-2 rounded-xl bg-orange-600/30 border border-orange-500 text-orange-200 text-xs font-bold hover:bg-orange-600 hover:text-white transition">"""
)

with io.open(p_nina, "w", encoding="utf-8") as f:
    f.write(c_nina)
print("la_nina_clima_em_movimento.html atualizado!")


# ==========================================
# 5. brasil-clima-em-movimento.html
# ==========================================
p_br = os.path.join(base_dir, "brasil-clima-em-movimento.html")
with io.open(p_br, "r", encoding="utf-8") as f:
    c_br = f.read()

# 5.1 Logo CLIMA EM MOVIMENTO aponta para gemini-pagina-inicial.html
c_br = re.sub(
    r'<a href="#" class="flex items-center gap-3\.5 group shrink-0">',
    r'<a href="gemini-pagina-inicial.html" class="flex items-center gap-3.5 group shrink-0">',
    c_br,
    count=1
)

# 5.2 Remover botão baixar código HTML da navbar
c_br = re.sub(
    r'<!-- Botão Download de 1 Clique -->\s*<button onclick="downloadHTMLFile\(\)"[^>]*>.*?</button>',
    '',
    c_br,
    flags=re.DOTALL
)

# 5.3 Avisos da legenda do mapa: remover onclick e deixar apenas efeito mouse hover
c_br = c_br.replace(
    """<div class="flex items-center gap-1.5 text-cyan-400 cursor-pointer hover:text-cyan-300 transition" onclick="showInfoToast('Pacífico: Anomalia térmica nas águas equatoriais (TSM)')">""",
    """<div class="flex items-center gap-1.5 text-cyan-400 hover:text-cyan-300 hover:scale-105 transition-all duration-200 select-none cursor-default" title="Pacífico: Anomalia térmica nas águas equatoriais (TSM)">"""
)

c_br = c_br.replace(
    """<div class="flex items-center gap-1.5 text-sky-400 cursor-pointer hover:text-sky-300 transition" onclick="showInfoToast('Atmosfera: Modificação dos ventos alísios e circulação de Walker')">""",
    """<div class="flex items-center gap-1.5 text-sky-400 hover:text-sky-300 hover:scale-105 transition-all duration-200 select-none cursor-default" title="Atmosfera: Modificação dos ventos alísios e circulação de Walker">"""
)

c_br = c_br.replace(
    """<div class="flex items-center gap-1.5 text-emerald-400 font-bold cursor-pointer hover:text-emerald-300 transition" onclick="showInfoToast('Brasil: Redistribuição de chuvas e temperaturas regionais')">""",
    """<div class="flex items-center gap-1.5 text-emerald-400 font-bold hover:text-emerald-300 hover:scale-105 transition-all duration-200 select-none cursor-default" title="Brasil: Redistribuição de chuvas e temperaturas regionais">"""
)

with io.open(p_br, "w", encoding="utf-8") as f:
    f.write(c_br)
print("brasil-clima-em-movimento.html atualizado!")
