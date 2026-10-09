# -*- coding: utf-8 -*-
"""
Limpeza do 'Site Final' (originais em 'site/' intactos):
 1) Remove as funções de download (sem botões que as acionem) de Fenômeno, Brasil e La Niña.
 2) Remove da página inicial a seção oculta 'page-fenomeno' + o JS do simulador e a função navigateTo.
 3) Botão 'Início' da página inicial passa a apontar para o próprio arquivo.
"""
import io, re

def ler(p):
    return io.open(p, encoding='utf-8', newline='').read()

def gravar(p, s):
    io.open(p, 'w', encoding='utf-8', newline='').write(s)

def remover(s, padrao, nome):
    """Remove 1 ocorrência do padrão; falha se não achar (evita edição silenciosa errada)."""
    novo, n = re.subn(padrao, '', s, count=1)
    assert n == 1, f'padrão não encontrado: {nome}'
    return novo

B = 'Site Final/'

# ---------- 1) Funções de download ----------
p = B + 'clima_em_movimento_o_fen_meno-2.html'
s = ler(p)
s = remover(s, r'\r?\n    function downloadCodeFile\(\) \{[\s\S]*?\r?\n    \}(?=\r?\n  </script>)', 'downloadCodeFile')
gravar(p, s)

p = B + 'brasil-clima-em-movimento.html'
s = ler(p)
s = remover(s, r'    /\* Download direto de 1 clique do código HTML \*/\r?\n    function downloadHTMLFile\(\) \{[\s\S]*?\r?\n    \}\r?\n\r?\n(?=    let toastTimer;)', 'downloadHTMLFile')
gravar(p, s)

p = B + 'la_nina_clima_em_movimento.html'
s = ler(p)
s = remover(s, r'    /\* =+\r?\n       SCRIPT DE DOWNLOAD DIRETO[\s\S]*?function downloadHtmlFile\(\) \{[\s\S]*?\r?\n    \}\r?\n\r?\n(?=    window\.onload)', 'downloadHtmlFile')
gravar(p, s)

# ---------- 2 e 3) Página inicial ----------
p = B + 'gemini-pagina-inicial.html'
s = ler(p)

# 3) Botão Início aponta para o próprio arquivo
a = '''<button id="nav-home" onclick="navigateTo('page-home')"'''
assert s.count(a) == 1
s = s.replace(a, '''<button id="nav-home" onclick="window.location.href='gemini-pagina-inicial.html'"''')

# 2a) Seção oculta page-fenomeno (inclui o cabeçalho de comentário que a antecede)
s = remover(s, r'  <!-- =+ -->\r?\n  <!-- 3\. PÁGINA 2: O FENÔMENO[\s\S]*?<section id="page-fenomeno"[\s\S]*?</section>\r?\n\r?\n', 'section page-fenomeno')

# 2b) Função navigateTo (não é mais usada)
s = remover(s, r'    // Roteamento SPA entre telas\r?\n    function navigateTo\(pageId\) \{[\s\S]*?\r?\n    \}\r?\n\r?\n', 'navigateTo')

# 2c) JS do simulador: do comentário "Lógica do Simulador" até o fim do script
s = remover(s, r'    // =+\r?\n    // Lógica do Simulador Oceanográfico \(Página 2\)[\s\S]*?(?=  </script>)', 'JS simulador')

# Sanidade: nada de referências quebradas
for ref in ['navigateTo', 'page-fenomeno', 'slider-nin', 'simulateElNinoDirect', 'resetSim']:
    assert ref not in s, f'referência restante: {ref}'
gravar(p, s)
print('ok')
