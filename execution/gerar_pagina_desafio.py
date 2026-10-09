# -*- coding: utf-8 -*-
"""
Gera a página 'desafio-clima-em-movimento.html' autônoma em 'Site Final':
- Sorteia 10 perguntas aleatórias:
  * 4 fáceis (sorteadas dentre 25)
  * 4 médias (sorteadas dentre 25)
  * 2 difíceis (sorteadas dentre 10)
- Apresenta uma pergunta por vez, com progresso visual, alternativas interativas
- Feedback explicativo imediato ao responder
- Painel final com pontuação, medalha/classificação conforme o rendimento, resumo dos acertos e botão de 'Jogar Novamente' (com novas perguntas sorteadas)
"""
import io, json

banco_json = io.open("Site Final/banco_questoes.json", "r", encoding="utf-8").read()

html_content = f"""<!DOCTYPE html>
<html lang="pt-BR" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Desafio Científico - Clima em Movimento | Quiz do ENOS</title>
  
  <!-- Fontes -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
  
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>

  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          fontFamily: {{
            sans: ['Plus Jakarta Sans', 'sans-serif'],
            mono: ['JetBrains Mono', 'monospace'],
          }},
          colors: {{
            ocean: {{
              950: '#020713',
              900: '#051024',
              850: '#081734',
              800: '#0d2249',
              700: '#1a4185',
            }}
          }},
          boxShadow: {{
            'glow-cyan': '0 0 25px -2px rgba(6, 182, 212, 0.45)',
            'glow-orange': '0 0 25px -2px rgba(249, 115, 22, 0.45)',
            'glow-emerald': '0 0 25px -2px rgba(16, 185, 129, 0.45)',
            'glow-purple': '0 0 30px -3px rgba(168, 85, 247, 0.45)',
          }}
        }}
      }}
    }}
  </script>

  <style>
    body {{
      background-color: #020713;
      color: #f1f5f9;
      font-family: 'Plus Jakarta Sans', sans-serif;
      overflow-x: hidden;
    }}
    
    /* Header Padronizado */
    .cm-header {{
      position: sticky;
      top: 0;
      z-index: 50;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 12px 24px;
      background: rgba(3,8,22,.88);
      -webkit-backdrop-filter: blur(16px);
      backdrop-filter: blur(16px);
      border-bottom: 1px solid rgba(255,255,255,.08);
      box-sizing: border-box;
      width: 100%;
    }}
    @media(min-width: 1024px) {{
      .cm-header {{ padding: 12px 48px; }}
    }}
    .cm-logo {{
      display: flex;
      align-items: center;
      gap: 12px;
      cursor: pointer;
      text-decoration: none;
    }}
    .cm-logo-ic {{
      width: 40px;
      height: 40px;
      border-radius: 9999px;
      background: rgba(8,145,178,.25);
      border: 1px solid rgba(34,211,238,.4);
      display: flex;
      align-items: center;
      justify-content: center;
      color: #67e8f9;
      transition: transform .15s;
    }}
    .cm-logo:hover .cm-logo-ic {{ transform: scale(1.05); }}
    .cm-logo-ic i, .cm-logo-ic svg {{ width: 20px; height: 20px; }}
    .cm-logo h1 {{
      margin: 0;
      font-size: 14px;
      font-weight: 800;
      letter-spacing: .05em;
      line-height: 1;
      color: #fff;
    }}
    .cm-logo p {{
      margin: 2px 0 0;
      font-size: 10px;
      font-weight: 400;
      letter-spacing: .025em;
      color: rgba(103,232,249,.8);
    }}
    @media(min-width: 640px) {{
      .cm-logo h1 {{ font-size: 16px; }}
      .cm-logo p {{ font-size: 11px; }}
    }}
    .cm-nav {{
      display: none;
      align-items: center;
      gap: 6px;
      font-size: 12px;
      font-weight: 600;
    }}
    @media(min-width: 1280px) {{
      .cm-nav {{ display: flex; }}
    }}
    .cm-btn {{
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 6px 14px;
      border-radius: 9999px;
      border: 1px solid transparent;
      background: transparent;
      color: #cbd5e1;
      font: inherit;
      line-height: 1rem;
      cursor: pointer;
      transition: all .15s;
    }}
    .cm-btn:hover {{
      background: rgba(30,41,59,.6);
      color: var(--hv);
    }}
    .cm-btn i, .cm-btn svg {{ width: 14px; height: 14px; flex-shrink: 0; }}
    .cm-ic-orange {{ color: #fb923c; }}
    .cm-ic-cyan {{ color: #67e8f9; }}
    .cm-btn.cm-active {{
      background: rgba(6,182,212,.2);
      color: #67e8f9;
      border-color: rgba(34,211,238,.4);
    }}
    .cm-btn.cm-active:hover {{ color: #67e8f9; }}

    .glass-panel {{
      background: rgba(5, 16, 36, 0.75);
      backdrop-filter: blur(14px);
      border: 1px solid rgba(26, 65, 133, 0.45);
    }}
    .opt-btn {{
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .opt-btn:hover:not(:disabled) {{
      transform: translateX(4px);
      border-color: rgba(34, 211, 238, 0.6);
      background-color: rgba(8, 23, 52, 0.9);
    }}
  </style>
</head>
<body class="min-h-screen flex flex-col justify-between selection:bg-cyan-500 selection:text-ocean-950">

  <!-- ========================================== -->
  <!-- 1. NAVBAR SUPERIOR PADRONIZADA            -->
  <!-- ========================================== -->
  <header class="cm-header">
    <div class="cm-logo" onclick="window.location.href='gemini-pagina-inicial.html'">
      <div class="cm-logo-ic"><i data-lucide="globe"></i></div>
      <div>
        <h1>CLIMA EM MOVIMENTO</h1>
        <p>Quando o oceano muda, o planeta responde.</p>
      </div>
    </div>
    <nav class="cm-nav">
      <button class="cm-btn" onclick="window.location.href='gemini-pagina-inicial.html'" style="--hv:#ffffff">
        <i data-lucide="home"></i> Início
      </button>
      <button class="cm-btn" onclick="window.location.href='clima_em_movimento_o_fen_meno-2.html'" style="--hv:#ffffff">
        <i data-lucide="waves"></i> O Fenômeno
      </button>
      <button class="cm-btn" onclick="window.location.href='clima_em_movimento_el_ni_no.html'" style="--hv:#fb923c">
        <i data-lucide="flame" class="cm-ic-orange"></i> El Niño
      </button>
      <button class="cm-btn" onclick="window.location.href='la_nina_clima_em_movimento.html'" style="--hv:#67e8f9">
        <i data-lucide="snowflake" class="cm-ic-cyan"></i> La Niña
      </button>
      <button class="cm-btn" onclick="window.location.href='brasil-clima-em-movimento.html'" style="--hv:#34d399">
        <i data-lucide="map-pin"></i> Brasil
      </button>
      <button class="cm-btn" onclick="window.location.href='dados-clima-em-movimento.html'" style="--hv:#ffffff">
        <i data-lucide="bar-chart-2"></i> Dados
      </button>
      <!-- ITEM ATIVO: DESAFIO -->
      <button class="cm-btn cm-active">
        <i data-lucide="gamepad-2"></i> Desafio
      </button>
    </nav>
  </header>

  <!-- ========================================== -->
  <!-- CONTEÚDO PRINCIPAL DO QUIZ                 -->
  <!-- ========================================== -->
  <main class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 pb-20 relative z-10 w-full flex-1">

    <!-- TELA INICIAL: APRESENTAÇÃO DO DESAFIO -->
    <section id="screen-intro" class="text-center py-6">
      <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-cyan-950/60 border border-cyan-500/40 text-cyan-300 text-xs font-semibold uppercase tracking-wider mb-4 shadow-glow-cyan">
        <i data-lucide="award" class="w-4 h-4"></i>
        Desafio Científico Interativo
      </div>
      <h1 class="text-3xl sm:text-5xl font-black text-white tracking-tight">
        TESTE SEUS <span class="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-sky-300 to-blue-500">CONHECIMENTOS</span>
      </h1>
      <p class="text-slate-300 text-sm sm:text-base mt-3 max-w-xl mx-auto leading-relaxed">
        Você responderá a <strong>10 perguntas aleatórias</strong> selecionadas do nosso banco de dados oficial sobre El Niño, La Niña e os impactos no Brasil.
      </p>

      <!-- Grade Informativa dos Níveis -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 max-w-2xl mx-auto my-8">
        <div class="p-4 rounded-2xl bg-ocean-900/80 border border-emerald-500/30 text-left">
          <span class="text-xs font-mono font-bold text-emerald-400 block mb-1 uppercase">🟢 4 Perguntas Fáceis</span>
          <p class="text-[11px] text-slate-300 leading-relaxed">Conceitos fundamentais de oceano, ventos alísios e localização geográfica.</p>
        </div>
        <div class="p-4 rounded-2xl bg-ocean-900/80 border border-amber-500/30 text-left">
          <span class="text-xs font-mono font-bold text-amber-400 block mb-1 uppercase">🟡 4 Perguntas Médias</span>
          <p class="text-[11px] text-slate-300 leading-relaxed">Circulação de Walker, anomalias regionais do Brasil e monitoramento NOAA.</p>
        </div>
        <div class="p-4 rounded-2xl bg-ocean-900/80 border border-purple-500/30 text-left">
          <span class="text-xs font-mono font-bold text-purple-400 block mb-1 uppercase">🟣 2 Perguntas Difíceis</span>
          <p class="text-[11px] text-slate-300 leading-relaxed">Física avançada: ondas Kelvin, termoclina, Modoki e feedback de Bjerknes.</p>
        </div>
      </div>

      <button onclick="iniciarQuiz()" class="px-9 py-4 rounded-2xl bg-gradient-to-r from-cyan-500 via-sky-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-black text-sm uppercase tracking-wider shadow-glow-cyan flex items-center justify-center gap-3 mx-auto transition transform hover:scale-105 active:scale-95">
        <i data-lucide="play" class="w-5 h-5 fill-current"></i>
        <span>INICIAR DESAFIO (10 PERGUNTAS)</span>
      </button>
    </section>

    <!-- TELA DO JOGO: PERGUNTA ATIVA -->
    <section id="screen-quiz" class="hidden">
      <!-- Barra Superior de Status -->
      <div class="flex items-center justify-between mb-4 flex-wrap gap-2">
        <div class="flex items-center gap-3">
          <span class="text-xs font-mono font-bold text-cyan-400 uppercase" id="quiz-step-text">
            Pergunta 1 de 10
          </span>
          <span id="quiz-diff-badge" class="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold uppercase">
            Fácil
          </span>
        </div>
        <div class="flex items-center gap-2 text-xs font-mono text-slate-400">
          <span>Pontuação Atual:</span>
          <span id="quiz-score-live" class="text-emerald-400 font-bold">0 pts</span>
        </div>
      </div>

      <!-- Barra de Progresso Visual -->
      <div class="w-full h-2 rounded-full bg-ocean-950 overflow-hidden border border-ocean-800 mb-6">
        <div id="quiz-progress-bar" class="h-full rounded-full bg-gradient-to-r from-cyan-500 via-sky-400 to-blue-500 transition-all duration-300" style="width: 10%;"></div>
      </div>

      <!-- Card da Pergunta -->
      <div class="glass-panel rounded-3xl p-6 sm:p-8 shadow-2xl mb-6">
        <h2 id="quiz-question-text" class="text-lg sm:text-xl font-bold text-white leading-relaxed mb-6">
          Carregando pergunta...
        </h2>

        <!-- Alternativas -->
        <div id="quiz-options-container" class="space-y-3">
          <!-- Gerado via JavaScript -->
        </div>

        <!-- Caixa de Feedback e Explicação (Após Responder) -->
        <div id="quiz-feedback-box" class="hidden mt-6 p-4 rounded-2xl border text-xs leading-relaxed transition-all">
          <div class="flex items-center gap-2 font-bold mb-1" id="quiz-feedback-title"></div>
          <p id="quiz-feedback-expl" class="text-slate-300"></p>
        </div>

        <!-- Botão Próxima Pergunta -->
        <div class="mt-6 flex justify-end">
          <button id="btn-next-question" onclick="proximaPergunta()" disabled class="px-6 py-3 rounded-xl bg-ocean-800 text-slate-500 font-bold text-xs uppercase tracking-wider transition flex items-center gap-2 cursor-not-allowed">
            <span>Próxima Pergunta</span>
            <i data-lucide="arrow-right" class="w-4 h-4"></i>
          </button>
        </div>
      </div>
    </section>

    <!-- TELA FINAL: RESULTADO E PONTUAÇÃO -->
    <section id="screen-result" class="hidden text-center py-6">
      <div class="glass-panel rounded-3xl p-8 sm:p-12 max-w-2xl mx-auto shadow-2xl">
        
        <div id="result-badge-icon" class="w-20 h-20 rounded-3xl bg-cyan-600/20 border border-cyan-400/40 flex items-center justify-center text-4xl mx-auto mb-4 shadow-glow-cyan">
          🏆
        </div>

        <h2 class="text-2xl sm:text-4xl font-black text-white tracking-tight" id="result-title">
          Parabéns!
        </h2>
        
        <p class="text-slate-300 text-sm mt-2" id="result-subtitle">
          Você concluiu a rodada de 10 perguntas científicas do ENOS.
        </p>

        <!-- Placar -->
        <div class="my-8 p-6 rounded-2xl bg-ocean-950/90 border border-ocean-700/80 max-w-sm mx-auto">
          <div class="text-[11px] font-mono uppercase text-slate-400 font-bold">
            Sua Pontuação Final
          </div>
          <div class="text-5xl font-black text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-emerald-400 my-2 font-mono" id="result-score">
            8 / 10
          </div>
          <div class="text-xs font-semibold text-slate-300" id="result-percentage">
            80% de aproveitamento
          </div>
        </div>

        <!-- Classificação Educacional -->
        <div class="p-4 rounded-xl bg-ocean-900 border border-ocean-800 text-xs text-slate-300 mb-8 max-w-md mx-auto text-left" id="result-comment">
          <!-- Gerado via script -->
        </div>

        <!-- Ações Finais -->
        <div class="flex items-center justify-center gap-4 flex-wrap">
          <button onclick="reiniciarQuiz()" class="px-7 py-3.5 rounded-2xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-bold text-xs uppercase tracking-wider shadow-glow-cyan flex items-center gap-2 transition">
            <i data-lucide="rotate-ccw" class="w-4 h-4"></i> Jogar Novamente (Novo Sorteio)
          </button>
          <button onclick="window.location.href='dados-clima-em-movimento.html'" class="px-7 py-3.5 rounded-2xl bg-ocean-850 hover:bg-ocean-800 border border-ocean-700 text-slate-200 font-bold text-xs uppercase tracking-wider transition flex items-center gap-2">
            <i data-lucide="bar-chart-2" class="w-4 h-4"></i> Rever Dados do Site
          </button>
        </div>

      </div>
    </section>

  </main>

  <!-- RODAPÉ GLOBAL -->
  <footer class="border-t border-ocean-800/80 bg-ocean-950/80 py-6 text-center text-xs text-slate-500">
    <p>Projeto Clima em Movimento • Observatório Educacional Oceano-Atmosfera</p>
  </footer>

  <!-- ========================================== -->
  <!-- LÓGICA DO QUIZ EM JAVASCRIPT               -->
  <!-- ========================================== -->
  <script>
    lucide.createIcons();

    // BANCO COMPLETO DE QUESTÕES (60 Itens)
    const BANCO_QUESTOES = {banco_json};

    // Estado da Partida
    let rodadaAtual = [];
    let indiceAtual = 0;
    let pontuacao = 0;
    let respondeu = false;

    // Função para embaralhar array (Fisher-Yates)
    function shuffleArray(arr) {{
      const a = [...arr];
      for (let i = a.length - 1; i > 0; i--) {{
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
      }}
      return a;
    }}

    // Sorteia exatamente: 4 fáceis, 4 médias e 2 difíceis
    function sortearRodada() {{
      const faceis = BANCO_QUESTOES.filter(q => q.diff === 'facil');
      const medias = BANCO_QUESTOES.filter(q => q.diff === 'media');
      const dificeis = BANCO_QUESTOES.filter(q => q.diff === 'dificil');

      const sortFaceis = shuffleArray(faceis).slice(0, 4);
      const sortMedias = shuffleArray(medias).slice(0, 4);
      const sortDificeis = shuffleArray(dificeis).slice(0, 2);

      // Combina mantendo ordem crescente ou embaralhada
      // Vamos intercalar ou manter progressão didática: Fácil -> Médio -> Difícil
      rodadaAtual = [...sortFaceis, ...sortMedias, ...sortDificeis];
      indiceAtual = 0;
      pontuacao = 0;
    }}

    function iniciarQuiz() {{
      sortearRodada();
      document.getElementById('screen-intro').classList.add('hidden');
      document.getElementById('screen-result').classList.add('hidden');
      document.getElementById('screen-quiz').classList.remove('hidden');
      renderizarPergunta();
    }}

    function reiniciarQuiz() {{
      iniciarQuiz();
    }}

    function renderizarPergunta() {{
      respondeu = false;
      const q = rodadaAtual[indiceAtual];
      if (!q) return;

      // Status
      document.getElementById('quiz-step-text').innerText = `Pergunta ${{indiceAtual + 1}} de ${{rodadaAtual.length}}`;
      document.getElementById('quiz-score-live').innerText = `${{pontuacao}} / ${{indiceAtual}} acertos`;
      document.getElementById('quiz-progress-bar').style.width = `${{((indiceAtual + 1) / rodadaAtual.length) * 100}}%`;

      // Badge de Dificuldade
      const badge = document.getElementById('quiz-diff-badge');
      if (q.diff === 'facil') {{
        badge.innerText = '🟢 Fácil';
        badge.className = 'px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold uppercase bg-emerald-950 text-emerald-400 border border-emerald-500/40';
      }} else if (q.diff === 'media') {{
        badge.innerText = '🟡 Média';
        badge.className = 'px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold uppercase bg-amber-950 text-amber-400 border border-amber-500/40';
      }} else {{
        badge.innerText = '🟣 Difícil';
        badge.className = 'px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold uppercase bg-purple-950 text-purple-400 border border-purple-500/40';
      }}

      // Enunciado
      document.getElementById('quiz-question-text').innerText = q.q;

      // Opções
      const container = document.getElementById('quiz-options-container');
      container.innerHTML = '';

      const letras = ['A', 'B', 'C', 'D'];
      q.opts.forEach((opt, idx) => {{
        const btn = document.createElement('button');
        btn.className = 'opt-btn w-full p-4 rounded-2xl bg-ocean-900/90 border border-ocean-700/80 text-left text-xs sm:text-sm text-slate-200 flex items-center gap-3.5';
        btn.id = `opt-btn-${{idx}}`;
        btn.innerHTML = `
          <span class="w-7 h-7 rounded-xl bg-ocean-800 border border-ocean-600 flex items-center justify-center font-mono font-bold text-xs text-cyan-300 shrink-0">
            ${{letras[idx]}}
          </span>
          <span class="flex-1">${{opt}}</span>
        `;
        btn.onclick = () => selecionarResposta(idx);
        container.appendChild(btn);
      }});

      // Reseta feedback e botão próxima
      document.getElementById('quiz-feedback-box').classList.add('hidden');
      const btnNext = document.getElementById('btn-next-question');
      btnNext.disabled = true;
      btnNext.className = 'px-6 py-3 rounded-xl bg-ocean-800 text-slate-500 font-bold text-xs uppercase tracking-wider transition flex items-center gap-2 cursor-not-allowed';
    }}

    function selecionarResposta(escolha) {{
      if (respondeu) return;
      respondeu = true;

      const q = rodadaAtual[indiceAtual];
      const correta = q.ans;
      const feedbackBox = document.getElementById('quiz-feedback-box');
      const feedbackTitle = document.getElementById('quiz-feedback-title');
      const feedbackExpl = document.getElementById('quiz-feedback-expl');

      // Desabilita botões e colore certo/errado
      for (let i = 0; i < q.opts.length; i++) {{
        const btn = document.getElementById(`opt-btn-${{i}}`);
        btn.disabled = true;
        btn.classList.remove('hover:bg-ocean-800');

        if (i === correta) {{
          btn.className = 'w-full p-4 rounded-2xl bg-emerald-950/90 border-2 border-emerald-400 text-left text-xs sm:text-sm text-emerald-100 flex items-center gap-3.5 shadow-glow-emerald';
        }} else if (i === escolha) {{
          btn.className = 'w-full p-4 rounded-2xl bg-rose-950/80 border-2 border-rose-500 text-left text-xs sm:text-sm text-rose-200 flex items-center gap-3.5';
        }} else {{
          btn.className = 'w-full p-4 rounded-2xl bg-ocean-950/50 border border-ocean-800/40 text-left text-xs sm:text-sm text-slate-500 flex items-center gap-3.5 opacity-60';
        }}
      }}

      if (escolha === correta) {{
        pontuacao++;
        feedbackBox.className = 'mt-6 p-4 rounded-2xl border border-emerald-500/40 bg-emerald-950/40 text-xs leading-relaxed text-emerald-200';
        feedbackTitle.innerHTML = '<span class="text-emerald-400">✅ Resposta Correta!</span>';
      }} else {{
        feedbackBox.className = 'mt-6 p-4 rounded-2xl border border-rose-500/40 bg-rose-950/40 text-xs leading-relaxed text-rose-200';
        feedbackTitle.innerHTML = '<span class="text-rose-400">❌ Resposta Incorreta</span>';
      }}

      feedbackExpl.innerText = q.expl;
      feedbackBox.classList.remove('hidden');

      // Habilita botão próxima
      const btnNext = document.getElementById('btn-next-question');
      btnNext.disabled = false;
      btnNext.className = 'px-6 py-3 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-bold text-xs uppercase tracking-wider transition flex items-center gap-2 cursor-pointer shadow-glow-cyan';
      
      // Atualiza placar live
      document.getElementById('quiz-score-live').innerText = `${{pontuacao}} / ${{indiceAtual + 1}} acertos`;
    }}

    function proximaPergunta() {{
      if (indiceAtual < rodadaAtual.length - 1) {{
        indiceAtual++;
        renderizarPergunta();
      }} else {{
        finalizarQuiz();
      }}
    }}

    function finalizarQuiz() {{
      document.getElementById('screen-quiz').classList.add('hidden');
      document.getElementById('screen-result').classList.remove('hidden');

      const pct = Math.round((pontuacao / rodadaAtual.length) * 100);
      document.getElementById('result-score').innerText = `${{pontuacao}} / ${{rodadaAtual.length}}`;
      document.getElementById('result-percentage').innerText = `${{pct}}% de acertos`;

      const badgeIcon = document.getElementById('result-badge-icon');
      const title = document.getElementById('result-title');
      const subtitle = document.getElementById('result-subtitle');
      const comment = document.getElementById('result-comment');

      if (pontuacao >= 9) {{
        badgeIcon.innerText = '🥇';
        title.innerText = 'Excelente! Mestre do ENOS';
        subtitle.innerText = 'Você demonstrou domínio profundo tanto sobre os fundamentos quanto sobre a física avançada do sistema.';
        comment.innerHTML = '<strong>Avaliação do Observatório:</strong> Seus conhecimentos sobre circulação oceânica, teleconexões e impactos regionais estão no nível de um pesquisador em climatologia.';
      }} else if (pontuacao >= 7) {{
        badgeIcon.innerText = '🥈';
        title.innerText = 'Muito Bom! Conhecimento Sólido';
        subtitle.innerText = 'Você compreende perfeitamente a dinâmica entre o Oceano Pacífico e o clima do Brasil.';
        comment.innerHTML = '<strong>Avaliação do Observatório:</strong> Ótimo desempenho nas questões básicas e intermediárias. Uma revisão sobre as ondas de Kelvin e Bjerknes vai te levar à nota máxima!';
      }} else if (pontuacao >= 5) {{
        badgeIcon.innerText = '🥉';
        title.innerText = 'Bom Desempenho!';
        subtitle.innerText = 'Você captou a essência de como o oceano dita as regras do clima no continente.';
        comment.innerHTML = '<strong>Avaliação do Observatório:</strong> Bom início! Vale a pena revisitar a página de Dados e o Simulador 3D para consolidar as nuances de cada região do Brasil.';
      }} else {{
        badgeIcon.innerText = '📘';
        title.innerText = 'Continue Explorando!';
        subtitle.innerText = 'O sistema climático terrestre é complexo e fascinante.';
        comment.innerHTML = '<strong>Dica de Estudo:</strong> Dê uma olhada nos infográficos de El Niño e La Niña na barra superior e tente novamente. Cada rodada sorteia perguntas inéditas!';
      }}
    }}
  </script>

</body>
</html>
"""

out_file = "Site Final/desafio-clima-em-movimento.html"
with io.open(out_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Página de desafio criada com sucesso em: {out_file}")
