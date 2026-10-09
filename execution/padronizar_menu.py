# -*- coding: utf-8 -*-
"""
Padroniza o menu superior do 'Site Final' com base na página inicial (referência):
mesmo logo, mesma posição, mesmos ícones (Lucide) e mesmo visual de "pílulas".
- A página inicial NÃO é alterada (é a referência).
- Mantém por página: o botão ativo e o comportamento de Dados/Desafio (modais/avisos já existentes).
- O CSS do cabeçalho é isolado (prefixo cm-) para não depender do Tailwind de cada página.
"""
import io, re

B = 'Site Final/'
PAGINAS = {
    'clima_em_movimento_o_fen_meno-2.html': 'O Fenômeno',
    'clima_em_movimento_el_ni_no.html': 'El Niño',
    'la_nina_clima_em_movimento.html': 'La Niña',
    'brasil-clima-em-movimento.html': 'Brasil',
}
# rótulo, ícone lucide, arquivo de destino, classe do ícone, cor no hover
ITENS = [
    ('Início', 'home', 'gemini-pagina-inicial.html', '', '#ffffff'),
    ('O Fenômeno', 'waves', 'clima_em_movimento_o_fen_meno-2.html', '', '#ffffff'),
    ('El Niño', 'flame', 'clima_em_movimento_el_ni_no.html', 'cm-ic-orange', '#fb923c'),
    ('La Niña', 'snowflake', 'la_nina_clima_em_movimento.html', 'cm-ic-cyan', '#67e8f9'),
    ('Brasil', 'map-pin', 'brasil-clima-em-movimento.html', '', '#34d399'),
    ('Dados', 'bar-chart-2', None, '', '#ffffff'),
    ('Desafio', 'gamepad-2', None, '', '#ffffff'),
]

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
.cm-header{position:sticky;top:0;z-index:50;display:flex;align-items:center;justify-content:space-between;
  padding:12px 24px;background:rgba(3,8,22,.88);-webkit-backdrop-filter:blur(16px);backdrop-filter:blur(16px);
  border-bottom:1px solid rgba(255,255,255,.08);font-family:'Plus Jakarta Sans',sans-serif;box-sizing:border-box;width:100%}
.cm-header *{box-sizing:border-box}
@media(min-width:1024px){.cm-header{padding:12px 48px}}
.cm-logo{display:flex;align-items:center;gap:12px;cursor:pointer;text-decoration:none}
.cm-logo-ic{width:40px;height:40px;border-radius:9999px;background:rgba(8,145,178,.25);border:1px solid rgba(34,211,238,.4);
  display:flex;align-items:center;justify-content:center;color:#67e8f9;transition:transform .15s}
.cm-logo:hover .cm-logo-ic{transform:scale(1.05)}
.cm-logo-ic i,.cm-logo-ic svg{width:20px;height:20px}
.cm-logo h1{margin:0;font-size:14px;font-weight:800;letter-spacing:.05em;line-height:1;color:#fff}
.cm-logo p{margin:2px 0 0;font-size:10px;font-weight:400;letter-spacing:.025em;color:rgba(103,232,249,.8)}
@media(min-width:640px){.cm-logo h1{font-size:16px}.cm-logo p{font-size:11px}}
.cm-nav{display:none;align-items:center;gap:6px;font-size:12px;font-weight:600}
@media(min-width:1280px){.cm-nav{display:flex}}
.cm-btn{display:flex;align-items:center;gap:6px;padding:6px 14px;border-radius:9999px;border:1px solid transparent;
  background:transparent;color:#cbd5e1;font:inherit;line-height:1rem;cursor:pointer;transition:all .15s}
.cm-btn:hover{background:rgba(30,41,59,.6);color:var(--hv)}
.cm-btn i,.cm-btn svg{width:14px;height:14px;flex-shrink:0}
.cm-ic-orange{color:#fb923c}.cm-ic-cyan{color:#67e8f9}
.cm-btn.cm-active{background:rgba(6,182,212,.2);color:#67e8f9;border-color:rgba(34,211,238,.4)}
.cm-btn.cm-active:hover{color:#67e8f9}
"""

def texto(html):
    t = re.sub(r'<!--.*?-->', '', html, flags=re.S)
    t = re.sub(r'<svg.*?</svg>', '', t, flags=re.S)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = re.sub(r'[^\w\sçãõáéíóúâêôÇÃÕÁÉÍÓÚÂÊÔ]', '', t)
    return re.sub(r'\s+', ' ', t).strip()

def onclick_existente(header, rotulo):
    """Recupera o onclick que o botão (Dados/Desafio) já tinha no menu antigo."""
    nav = re.search(r'<nav\b.*?</nav>', header, re.S)
    if not nav:
        return None
    for m in re.finditer(r'<button\b([^>]*)>(.*?)</button>', nav.group(0), re.S):
        if texto(m.group(2)).endswith(rotulo):
            oc = re.search(r'onclick="([^"]*)"', m.group(1))
            return oc.group(1) if oc else None
    return None

def monta_header(ativo, ocl, extra):
    botoes = []
    for rotulo, ic, destino, cls_ic, hv in ITENS:
        icone = f'<i data-lucide="{ic}"' + (f' class="{cls_ic}"' if cls_ic else '') + '></i>'
        if rotulo == ativo:
            botoes.append(f'      <button class="cm-btn cm-active">{icone} {rotulo}</button>')
            continue
        acao = f"window.location.href='{destino}'" if destino else ocl.get(rotulo)
        attr = f' onclick="{acao}"' if acao else ''
        botoes.append(f'      <button class="cm-btn"{attr} style="--hv:{hv}">{icone} {rotulo}</button>')
    nav = '\n'.join(botoes)
    return f"""<header class="cm-header">
    <style>{CSS}</style>
    <div class="cm-logo" onclick="window.location.href='gemini-pagina-inicial.html'">
      <div class="cm-logo-ic"><i data-lucide="globe"></i></div>
      <div>
        <h1>CLIMA EM MOVIMENTO</h1>
        <p>Quando o oceano muda, o planeta responde.</p>
      </div>
    </div>
    <nav class="cm-nav">
{nav}
    </nav>{extra}
    <script>(function(){{function go(){{lucide.createIcons();}}if(window.lucide){{go();}}else{{var s=document.createElement('script');s.src='https://unpkg.com/lucide@latest';s.onload=go;document.head.appendChild(s);}}}})();</script>
  </header>"""

for arq, ativo in PAGINAS.items():
    p = B + arq
    s = io.open(p, encoding='utf-8', newline='').read()
    m = re.search(r'<header\b.*?</header>', s, re.S)
    assert m, f'header não encontrado em {arq}'
    antigo = m.group(0)
    ocl = {r: onclick_existente(antigo, r) for r in ('Dados', 'Desafio')}
    # Preserva o botão móvel "Alternar Estado" do El Niño (se existir)
    mm = re.search(r'<!-- Mobile quick toggle button -->\s*<div[^>]*>[\s\S]*?</div>', antigo)
    extra = ('\n    ' + mm.group(0)) if mm else ''
    s = s[:m.start()] + monta_header(ativo, ocl, extra) + s[m.end():]
    io.open(p, 'w', encoding='utf-8', newline='').write(s)
    print('ok', arq, ocl)
