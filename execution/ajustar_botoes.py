# Ajustes de botões no Site Final (originais em "site/" permanecem intactos)
import io
base = 'Site Final/'

# --- Página inicial ---
p = base + 'gemini-pagina-inicial.html'
L = io.open(p, encoding='utf-8', newline='').read().split('\n')
# 1) Remove a seção "Cards Temáticos" (Oceano/Atmosfera/Planeta): linhas 194-246 (+ linha em branco 247)
assert 'Cards Tem' in L[193] and L[245].strip() == '</div>', 'trecho inesperado'
del L[193:247]
# 2) Botão COMEÇAR A EXPLORAR -> página O Fenômeno
i = next(k for k, l in enumerate(L) if "navigateTo('page-fenomeno')" in l and 'inline-flex items-center gap-3 px-8' in l)
L[i] = L[i].replace("navigateTo('page-fenomeno')", "window.location.href='clima_em_movimento_o_fen_meno-2.html'")
io.open(p, 'w', encoding='utf-8', newline='').write('\n'.join(L))

# --- Página O Fenômeno ---
p = base + 'clima_em_movimento_o_fen_meno-2.html'
s = io.open(p, encoding='utf-8', newline='').read()
a = """onclick="simulateScenario('nino')" class="inline-flex items-center gap-2.5 px-7 py-3"""
b = """onclick="simulateScenario('nina')" class="inline-flex items-center gap-2.5 px-7 py-3"""
assert s.count(a) == 1 and s.count(b) == 1
s = s.replace(a, a.replace("simulateScenario('nino')", "window.location.href='clima_em_movimento_el_ni_no.html'"))
s = s.replace(b, b.replace("simulateScenario('nina')", "window.location.href='la_nina_clima_em_movimento.html'"))
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
