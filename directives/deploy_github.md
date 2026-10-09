# Diretiva: Deploy do Projeto 'Clima' no GitHub Pages via GitHub Desktop

## Contexto & Memória do Projeto
- **Nome do repositório escolhido:** `clima`
- **Ferramenta de controle de versão do usuário:** GitHub Desktop
- **Pasta de publicação:** `Site Final`
- **URL pública de destino no GitHub Pages:** `https://<seu-usuario>.github.io/clima/`

## Regra Fundamental do GitHub Pages
O GitHub Pages procura obrigatoriamente um arquivo chamado `index.html` na raiz do repositório para ser a página inicial.
- A página inicial atual é `gemini-pagina-inicial.html`.
- Para o deploy no GitHub, deve existir uma cópia idêntica chamada `index.html` na pasta de publicação.
- Todos os links de "Início" apontando para `gemini-pagina-inicial.html` funcionam normalmente, e quem acessar a raiz `https://.../clima/` cairá automaticamente no `index.html`.

## Procedimento Operacional Padrão (Passo a Passo)

1. **Preparação dos Arquivos:**
   - Garantir que `Site Final/index.html` seja uma cópia sincronizada de `gemini-pagina-inicial.html`.
   - Garantir que arquivos de suporte e mídias estejam nos caminhos relativos corretos.

2. **Criação do Repositório no GitHub Desktop:**
   - Abrir o GitHub Desktop.
   - Ir em `File` -> `New Repository...` (ou `Add Existing Repository...` apontando para a pasta onde os arquivos finais estão).
   - Nome: `clima`.
   - Publicar no GitHub (`Publish repository`) desmarcando a opção "Keep this code private" (deve ser público para o GitHub Pages gratuito funcionar).

3. **Ativação do GitHub Pages:**
   - No GitHub (navegador), acessar o repositório `clima`.
   - Ir em `Settings` -> `Pages`.
   - Em `Build and deployment` -> `Branch`: selecionar `main` (ou `master`) e pasta `/ (root)`.
   - Clicar em `Save`.
   - O link público ficará ativo em `https://<seu-usuario>.github.io/clima/`.
