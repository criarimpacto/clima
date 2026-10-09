# -*- coding: utf-8 -*-
"""
Script cirúrgico para consertar todas as pontas soltas no 'Site Final':
1. Corrigir barra invertida indesejada \' em window.location.href='dados-clima-em-movimento.html' em todas as páginas
2. Na página inicial: padronizar o botão Desafio com um toast amigável ou ação
3. Na página La Niña: trocar o botão "X COMPARAR OS DOIS →" (L1293) para navegar direto para dados-clima-em-movimento.html#bloco-comparador
4. Na página Brasil:
   - Corrigir o botão "VER OS DADOS" (L1255)
   - Corrigir "+ DADOS" (L1062) e "Acessar Gráficos e Séries da Região" (L1120)
   - Vincular os 5 botões de região (NORTE, NORDESTE, CENTRO_OESTE, SUDESTE, SUL) para quando o usuário clicar e quiser ver dados, navegar para dados-clima-em-movimento.html?regiao=...
"""
import io, os, re

base_dir = "Site Final"

# 1. Corrigir \' em todas as páginas
for arq in os.listdir(base_dir):
    if not arq.endswith(".html"):
        continue
    p = os.path.join(base_dir, arq)
    c = io.open(p, "r", encoding="utf-8").read()
    
    # Substituir \'dados-clima-em-movimento.html\' por 'dados-clima-em-movimento.html'
    c_novo = c.replace(r"\'dados-clima-em-movimento.html\'", "'dados-clima-em-movimento.html'")
    c_novo = c_novo.replace(r"\'dados-clima-em-movimento.html#bloco-brasil\'", "'dados-clima-em-movimento.html#bloco-brasil'")
    c_novo = c_novo.replace(r"\'dados-clima-em-movimento.html#bloco-comparador\'", "'dados-clima-em-movimento.html#bloco-comparador'")
    
    if c != c_novo:
        io.open(p, "w", encoding="utf-8").write(c_novo)
        print(f"Barras de escape corrigidas em: {arq}")

# 2. Corrigir La Niña (botão de comparação L1293)
p_nina = os.path.join(base_dir, "la_nina_clima_em_movimento.html")
c_nina = io.open(p_nina, "r", encoding="utf-8").read()
c_nina = c_nina.replace(
    'onclick="openComparisonModal()" class="w-full sm:w-auto px-6 py-4 rounded-2xl bg-gradient-to-r from-cyan-500 to-sky-600',
    'onclick="window.location.href=\'dados-clima-em-movimento.html#bloco-comparador\'" class="w-full sm:w-auto px-6 py-4 rounded-2xl bg-gradient-to-r from-cyan-500 to-sky-600'
)
io.open(p_nina, "w", encoding="utf-8").write(c_nina)
print("La Niña L1293 atualizado!")

# 3. Corrigir Brasil (botoeira e atalhos de dados)
p_br = os.path.join(base_dir, "brasil-clima-em-movimento.html")
c_br = io.open(p_br, "r", encoding="utf-8").read()

# O botão 'VER OS DADOS' no rodapé deve navegar direto
c_br = re.sub(
    r'<button onclick="[^"]*" class="([^"]*font-display[^"]*)">\s*<svg[^>]*>.*?</svg>\s*<span>VER OS DADOS</span>\s*</button>',
    r"""<button onclick="window.location.href='dados-clima-em-movimento.html#bloco-brasil'" class="\1">
          <svg class="w-5 h-5 text-emerald-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
          </svg>
          <span>VER OS DADOS</span>
        </button>""",
    c_br,
    flags=re.DOTALL
)

# Atualizar "+ DADOS" e "Acessar Gráficos e Séries da Região" para navegar com a região ativa
c_br = c_br.replace(
    'onclick="window.location.href=\'dados-clima-em-movimento.html#bloco-brasil\'" title="Ver dados técnicos históricos desta região"',
    'onclick="goToRegionData()" title="Ver dados técnicos históricos desta região"'
)
c_br = c_br.replace(
    'onclick="window.location.href=\'dados-clima-em-movimento.html#bloco-brasil\'" class="w-full mt-4 py-2.5 px-4 rounded-xl',
    'onclick="goToRegionData()" class="w-full mt-4 py-2.5 px-4 rounded-xl'
)

# Adiciona a função auxiliar goToRegionData() no script da página Brasil se não existir
if 'function goToRegionData' not in c_br:
    script_fix = """
    function goToRegionData() {
      const reg = (currentRegionKey || 'SUL').toLowerCase().replace('_', '-');
      window.location.href = 'dados-clima-em-movimento.html?regiao=' + reg + '#bloco-brasil';
    }
    """
    c_br = c_br.replace("</script>", script_fix + "\n  </script>")

io.open(p_br, "w", encoding="utf-8").write(c_br)
print("Brasil atualizado com goToRegionData() e CTA 'VER OS DADOS'!")

# 4. Na página inicial: dar feedback no botão Desafio
p_home = os.path.join(base_dir, "gemini-pagina-inicial.html")
c_home = io.open(p_home, "r", encoding="utf-8").read()
c_home = c_home.replace(
    '<button class="nav-btn flex items-center gap-1.5 px-3.5 py-1.5 rounded-full text-slate-300 hover:text-white hover:bg-slate-800/60 transition">\n        <i data-lucide="gamepad-2" class="w-3.5 h-3.5"></i> Desafio\n      </button>',
    '<button class="nav-btn flex items-center gap-1.5 px-3.5 py-1.5 rounded-full text-slate-300 hover:text-white hover:bg-slate-800/60 transition" onclick="alert(\'O módulo Desafio está sendo construído!\')">\n        <i data-lucide="gamepad-2" class="w-3.5 h-3.5"></i> Desafio\n      </button>'
)
io.open(p_home, "w", encoding="utf-8").write(c_home)
print("Página inicial atualizada!")
