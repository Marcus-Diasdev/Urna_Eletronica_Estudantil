# Urna Eletrônica Estudantil 🗳️

Um sistema desktop completo desenvolvido em Python para simular o processo de votação eleitoral em ambientes estudantis. Ideal para eleições de representantes de turma, grêmios estudantis e projetos pedagógicos sobre democracia.

Este projeto foi construído para ser portátil, rodando perfeitamente a partir de pendrives, com armazenamento local e interface gráfica intuitiva.

---

## ✨ Funcionalidades

*   **Painel de Administração:** Gerenciamento completo de eleições e candidatos.
*   **Votação em Tela Cheia:** Interface imersiva e bloqueada para os alunos, com botões grandes, fotos dos candidatos e suporte a voto em Branco/Nulo.
*   **Segurança:** Proteção por senha padrão para encerrar votações, ver resultados e excluir dados, evitando que alunos fechem o sistema acidentalmente.
*   **Áudio Autêntico:** Reproduz o som clássico de confirmação da urna ao registrar o voto.
*   **Tratamento de Empates:** Detecta automaticamente empates no primeiro lugar e gera, com um clique, uma nova eleição de 2º Turno apenas com os candidatos empatados.
*   **Portabilidade:** Sistema de cópia automática de imagens para a pasta local, garantindo que o programa funcione em qualquer computador ou pendrive.
*   **Banco de Dados Embutido:** Utiliza SQLite3, dispensando instalações de servidores.

---

## 📖 Manual de Uso (Passo a Passo)

O projeto possui dados fictícios (candidatos Flavio e Ana) para facilitar os testes logo após baixar.

### 1. Acesso ao Painel Admin
Ao abrir o programa, você verá a tela de Administração. 
> **⚠️ IMPORTANTE:** A senha padrão do sistema para todas as ações restritas (encerrar urna, ver resultados, excluir) é **`admin123`**.

### 2. Gerenciando Eleições e Alunos
*   Clique em **+ Criar Nova Votação** para abrir um novo pleito.
*   Na tela de gerenciamento, clique em **Adicionar Aluno** para cadastrar candidatos. O sistema pedirá o nome e abrirá uma janela para selecionar a foto. A foto será automaticamente copiada para a pasta interna de segurança do programa.

### 3. Iniciando a Votação
*   Clique em **▶ Iniciar Urna**. O painel desaparecerá e a Urna assumirá a tela em modo imersivo (Tela Cheia).
*   Os alunos votam clicando no cartão do candidato. O voto é confirmado com o som clássico da urna.
*   **Para fechar a Urna:** Pressione a tecla `ESC` ou tente fechar a janela (Alt+F4). O sistema exigirá a senha de administrador para encerrar e voltar ao menu.

### 4. Apuração e Resultados
*   No painel Admin, clique em **📊 Ver Resultados**.
*   O sistema exibirá a lista ordenada com barra de rolagem (suportando dezenas de alunos), destacando o vencedor com um troféu (🏆) e a miniatura da foto.
*   **Segundo Turno:** Se houver empate exato na primeira colocação, aparecerá no rodapé o botão **Criar Eleição de 2º Turno**, que duplica a votação automaticamente apenas com os empatados.

---

## 🚀 Como Executar o Projeto (Código Fonte)

### Pré-requisitos

Certifique-se de ter o **Python 3.x** instalado. Instale as dependências:

```bash
pip install Pillow pygame
```

### Rodando o código

Clone este repositório:

```bash
git clone [https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git](https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git)
```

# Urna Eletrônica Estudantil 🗳️

Um sistema desktop completo desenvolvido em Python para simular o processo de votação eleitoral em ambientes estudantis. Ideal para eleições de representantes de turma, grêmios estudantis e projetos pedagógicos sobre democracia.

Este projeto foi construído para ser portátil, rodando perfeitamente a partir de pendrives, com armazenamento local e interface gráfica intuitiva. O executável (`.exe`) já está incluso nos arquivos do projeto para facilitar o uso imediato!

---

## ✨ Funcionalidades

*   **Painel de Administração:** Gerenciamento completo de eleições e candidatos.
*   **Votação em Tela Cheia:** Interface imersiva e bloqueada para os alunos, com botões grandes, fotos dos candidatos e suporte a voto em Branco/Nulo.
*   **Segurança:** Proteção por senha padrão para encerrar votações, ver resultados e excluir dados, evitando que alunos fechem o sistema acidentalmente.
*   **Áudio Autêntico:** Reproduz o som clássico de confirmação da urna ao registrar o voto.
*   **Tratamento de Empates:** Detecta automaticamente empates no primeiro lugar e gera, com um clique, uma nova eleição de 2º Turno apenas com os candidatos empatados.
*   **Portabilidade:** Sistema de cópia automática de imagens para a pasta local, garantindo que o programa funcione em qualquer computador ou pendrive.
*   **Banco de Dados Embutido:** Utiliza SQLite3, dispensando instalações de servidores.

---

## 📖 Manual de Uso (Passo a Passo)

O projeto possui dados fictícios (candidatos Flavio e Ana) para facilitar os testes logo após baixar.

### 1. Acesso ao Painel Admin
Ao abrir o programa (rodando o `.exe` ou o script em Python), você verá a tela de Administração. 
> **⚠️ IMPORTANTE:** A senha padrão do sistema para todas as ações restritas (encerrar urna, ver resultados, excluir) é **`admin123`**.

### 2. Gerenciando Eleições e Alunos
*   Clique em **+ Criar Nova Votação** para abrir um novo pleito.
*   Na tela de gerenciamento, clique em **Adicionar Aluno** para cadastrar candidatos. O sistema pedirá o nome e abrirá uma janela para selecionar a foto. A foto será automaticamente copiada para a pasta interna de segurança do programa.

### 3. Iniciando a Votação
*   Clique em **▶ Iniciar Urna**. O painel desaparecerá e a Urna assumirá a tela em modo imersivo (Tela Cheia).
*   Os alunos votam clicando no cartão do candidato. O voto é confirmado com o som clássico da urna.
*   **Para fechar a Urna:** Pressione a tecla `ESC` ou tente fechar a janela (Alt+F4). O sistema exigirá a senha de administrador para encerrar e voltar ao menu.

### 4. Apuração e Resultados
*   No painel Admin, clique em **📊 Ver Resultados**.
*   O sistema exibirá a lista ordenada com barra de rolagem (suportando dezenas de alunos), destacando o vencedor com um troféu (🏆) e a miniatura da foto.
*   **Segundo Turno:** Se houver empate exato na primeira colocação, aparecerá no rodapé o botão **Criar Eleição de 2º Turno**, que duplica a votação automaticamente apenas com os empatados.

---

## 🚀 Como Executar o Projeto

Você tem duas formas de rodar este projeto: usando o executável já pronto ou rodando diretamente o código-fonte em Python.

### Opção A: Usando o Executável (Mais Fácil)
Basta baixar os arquivos do repositório, extrair a pasta e dar um duplo clique no arquivo **`Eleição_ex.exe`**. Não é necessário instalar nada!

### Opção B: Rodando o Código Fonte (Para Desenvolvedores)
Certifique-se de ter o **Python 3.x** instalado. 

1. Clone este repositório:
   ```bash
   git clone [https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git](https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git)
```

Instale as dependências:

```bash
pip install Pillow pygame
```

Execute o arquivo principal:

```bash
python Eleição_ex.py
```

## 🛠️ Guia para Gerar um Novo Executável (.exe)

Como o projeto já inclui um `.exe`, este passo só é necessário se você modificar o código (`.py`) e quiser gerar uma nova versão compilada.

1. Instale o PyInstaller no terminal:
   ```bash
   pip install pyinstaller
   ```

2. Gere o executável (esse comando oculta a tela preta de terminal e empacota tudo):
   ```bash
   pyinstaller --noconsole --onefile Eleição_ex.py
   ```

3. O novo arquivo '.exe' será gerado dentro da pasta 'dist'. Substitua o antigo por este novo.

## 💾 Guia de Portabilidade (Usando no Pendrive)

Para que o sistema funcione perfeitamente em pendrives ou em outros computadores (sem perder as fotos cadastradas e os sons), a estrutura da pasta não pode ser separada. Mantenha os arquivos juntos exatamente como baixados do repositório:

📁 `Pasta_Do_Projeto/`
┣ 📁 `fotos_salvas/` *(Pasta criada automaticamente onde as fotos ficam salvas)*
┣ 🎵 `confirma-urna.mp3` *(Arquivo de áudio do voto)*
┣ 📜 `Eleição_ex.exe` *(O programa executável)*
┣ 📜 `Eleição_ex.py` *(Código-fonte)*
┣ 📜 `Eleição_ex.spec` *(Arquivo de configuração do PyInstaller)*
┣ 🖼️ `logo-sagrado-1024x597.png` *(Logo da urna)*
┗ 📜 `urna_escolar.db` *(Banco de dados com os votos)*

Copie a pasta inteira (com todos esses arquivos dentro) para o seu pendrive.

---

## 🖥️ Como Criar um Atalho no Desktop

Se você for usar o sistema fixo no computador da escola e quiser um ícone na Área de Trabalho:

1. Clique com o botão direito no arquivo `Eleição_ex.exe`.
2. Vá em **Enviar para** > **Área de trabalho (criar atalho)**.
3. No seu Desktop, clique com o botão direito no atalho recém-criado e vá em **Propriedades**.
4. Certifique-se de que o campo **"Iniciar em"** contém o caminho exato da pasta original onde estão os arquivos do projeto (ex: `C:\UrnaEstudantil`).
5. Clique em **OK**. Pronto!
