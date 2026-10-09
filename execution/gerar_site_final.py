# Gera a pasta "Site Final" copiando as páginas de "site/" e ajustando APENAS os links do menu superior.
# Os arquivos originais não são alterados.
import re, os, shutil, sys
sys.stdout.reconfigure(encoding='utf-8')

ORIGEM = 'site'
DESTINO = 'Site Final'

# Mapa: rótulo do menu -> arquivo de destino
DESTINOS = {
    'Início': 'gemini-pagina-inicial.html',
    'O Fenômeno': 'clima_em_movimento_o_fen_meno-2.html',
    'El Niño': 'clima_em_movimento_el_ni_no.html',
    'La Niña': 'la_nina_clima_em_movimento.html',
    'Brasil': 'brasil-clima-em-movimento.html',
}
# Página ativa de cada arquivo (o botão correspondente não é alterado)
ATIVA = {v: k for k, v in DESTINOS.items()}

os.makedirs(DESTINO, exist_ok=True)

def processa_nav(nav, arquivo):
    """Troca o onclick dos botões de navegação entre páginas."""
    def troca_botao(m):
        botao = m.group(0)
        texto = re.sub(r'<!--.*?-->', '', botao, flags=re.S)
        texto = re.sub(r'<svg.*?</svg>', '', texto, flags=re.S)
        texto = re.sub(r'<[^>]+>', ' ', texto)
        texto = re.sub(r'[^\w\sçãõáéíóúâêôÇÃÕÁÉÍÓÚÂÊÔ]', '', texto)  # remove emoji
        texto = re.sub(r'\s+', ' ', texto).strip()
        # identifica o rótulo
        rotulo = next((r for r in DESTINOS if texto.endswith(r)), None)
        if rotulo is None or ATIVA.get(arquivo) == rotulo:
            return botao  # Dados/Desafio/Sobre ou página atual: não mexe
        link = f"window.location.href='{DESTINOS[rotulo]}'"
        abre = re.match(r'<button\b[^>]*>', botao).group(0)
        if 'onclick="' in abre:
            nova = re.sub(r'onclick="[^"]*"', f'onclick="{link}"', abre, count=1)
        else:
            nova = abre[:-1] + f' onclick="{link}">'
        return nova + botao[len(abre):]
    return re.sub(r'<button\b.*?</button>', troca_botao, nav, flags=re.S)

for arq in DESTINOS.values():
    with open(os.path.join(ORIGEM, arq), encoding='utf-8', newline='') as f:
        s = f.read()
    m = re.search(r'<nav\b.*?</nav>', s, re.S)
    novo = s[:m.start()] + processa_nav(m.group(0), arq) + s[m.end():]
    with open(os.path.join(DESTINO, arq), 'w', encoding='utf-8', newline='') as f:
        f.write(novo)
    print('OK', arq)
