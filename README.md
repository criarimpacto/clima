# Clima em Movimento 🌊☀️🌧️

Plataforma educacional interativa sobre os fenômenos oceano-atmosféricos **El Niño** e **La Niña**, abordando causas, mecanismos globais e impactos climáticos específicos no Brasil.

🌐 **Acesse online:** [https://criarimpacto.github.io/clima/](https://criarimpacto.github.io/clima/)

---

## 📂 Estrutura do Repositório

### 🌐 Páginas do Site (HTML, CSS & JS)
O site foi construído de forma modular com animações, gráficos vetoriais (SVG) e interatividade nativa, sem necessidade de dependências pesadas de backend:

* `index.html` e `gemini-pagina-inicial.html`: Página inicial com visão geral do ecossistema e navegação imersiva.
* `clima_em_movimento_o_fen_meno-2.html`: Explicação do acoplamento oceano-atmosfera e circulação de Walker.
* `clima_em_movimento_el_ni_no.html`: Dinâmica do El Niño (aquecimento das águas no Pacífico equatorial).
* `la_nina_clima_em_movimento.html`: Dinâmica da La Niña (resfriamento anômalo e ventos alísios intensos).
* `brasil-clima-em-movimento.html`: Mapa interativo do Brasil com impactos regionais (Norte, Nordeste, Centro-Oeste, Sudeste e Sul).
* `dados-clima-em-movimento.html`: Central de monitoramento com métricas dos índices ONI, SOI e anomalias térmicas.
* `desafio-clima-em-movimento.html`: Quiz interativo com suporte a filtros de dificuldade, explicação pedagógica e placar.
* `banco_questoes.json`: Base estruturada contendo 100 questões divididas por nível e temática.

---

### ⚙️ Scripts de Automação e Manutenção (`execution/`)
Scripts Python determinísticos utilizados na geração, padronização e manutenção do projeto:

* `gerar_questoes.py`: Gera e valida o arquivo `banco_questoes.json` com perguntas categorizadas.
* `gerar_pagina_desafio.py`: Monta a interface do quiz com carregamento dinâmico e validação de respostas.
* `padronizar_menu.py`: Atualiza e sincroniza os menus de navegação em todas as páginas HTML.
* `ajustar_botoes.py`: Sincroniza cores, efeitos de hover e estados dos botões de ação rápida.
* `conectar_dados.py` / `conectar_desafio.py`: Garante os links cruzados e navegação contínua entre as páginas.
* `aplicar_ajustes_completos.py`: Executa a bateria de ajustes de tipografia, responsividade e layout.

---

### 📋 Diretivas e Documentação (`directives/` e `docs/`)
* `directives/deploy_github.md`: Guia passo a passo de publicação no GitHub Pages.
* `docs/descricoes/`: Roteiros conceituais e detalhamentos de conteúdo utilizados na elaboração das páginas.

---

## 🚀 Como Executar ou Fazer Ajustes Locais

1. **Clonar o repositório:**
   ```bash
   git clone https://github.com/criarimpacto/clima.git
   cd clima
   ```

2. **Visualizar o site localmente:**
   Basta abrir qualquer arquivo `.html` (como `index.html`) no navegador ou iniciar um servidor local:
   ```bash
   python -m http.server 8000
   ```
   E acessar `http://localhost:8000`.

3. **Modificar conteúdos ou questões:**
   * Para alterar perguntas do desafio, edite diretamente o arquivo `banco_questoes.json`.
   * Para reprocessar páginas ou menus em lote, execute os scripts correspondentes na pasta `execution/`.
