# UNIVERSIDADE DO MINHO
### Escola de Engenharia
### Engenharia Biomédica 1º Semestre 2ºAno

## Sistema de Consulta e Análise de Publicações Científicas
### Algoritmos e Técnicas de Programação

**Docentes orientadores:**
- Luís Filipe Cunha
- José Carlos Ramalho

**Realizado por:**
- Beatriz Carvalho Figueiras (A102463)
- Carlos Manuel Filipe Carvalho Araújo(A107187)
- Paulo Cristiano Fernandes Taveira(A103086)

## 1. INTRODUÇÃO

No âmbito da Unidade Curricular de Algoritmos e Técnicas de Programação, da Licenciatura de Engenharia Biomédica da Escola de Engenharia da Universidade do Minho, 2º ano, 1º semestre, ano letivo 2024/2025, foi proposto aos alunos a elaboração de um trabalho, em sistema Python, que permitisse criar, atualizar e analisar publicações científicas. 
Este trabalho tem como objetivo aprofundar o que foi lecionado.
A metodologia deste trabalho consistiu em pesquisas na internet, bem como, materiais fornecidos pelos docentes orientadores e ferramentas do Python.
Neste trabalho, começamos por apresentar uma breve introdução à estrutura geral do programa. De seguida, enumeramos algumas informações sobre o funcionamento tanto da Interface de linha de comando (CLI) como da Interface gráfica. Terminamos com uma reflexão crítica sobre o que foi mencionado anteriormente.

## 2. Estrutura do programa

Utilizou-se a linguagem Python para escrever/desenvolver o nosso programa, em conjunto com módulos como o FreeSimpleGUI (para o desenvolvimento da interface gráfica), datetime (para formatação e gerenciamento de datas), do ficheiro json (como base de dados), matplotlib.pyplot (para a realização dos gráficos), os (para a captação de endereço dos ficheiros para evitar erros no procedimento), PrettyTables (para a realização e apresentação de tabelas no terminal) e Colorama (para atribuir cor ao texto no terminal). 
Na pasta “app” temos 4 ficheiros: 
   • fun.py - onde se encontram todas as funções backend para o programa; 
   • graph.py - onde se encontra a interface gráfica e algumas das funções relacionadas à mesma; 
   • main.py - quando se corre este ficheiro no terminal, a interação com o programa  começa, através da interface gráfica; 
   • cli.py - para correr a linha de comando que permite interagir com o programa através da linha. 

### 2.1 FUNCIONAMENTO DO FUN

1. **`from collections import Counter`**
   - **Objetivo**: O `Counter` é uma subclasse de dicionário especializada em contar elementos em iteráveis. Foi útil para calcular a frequência de datas, autores e palavras-chave nas publicações.
2. **`import json`**
   - **Objetivo**: O módulo `json` é necessário para trabalhar com dados no formato JSON.
3. **`import tkinter as tk`**
   - **Objetivo**: Importa a biblioteca principal do tkinter, que é usada para criar janelas, botões, textos e outros elementos visuais num programa.
4. **`from tkinter import filedialog`**
   - **Objetivo**: Importa o módulo filedialog, que é usado para abrir janelas específicas que permitem ao usuário selecionar arquivos ou pastas no sistema.
5. **`import matplotlib.pyplot as plt`**
   - **Objetivo**: O módulo pyplot da biblioteca Matplotlib, é uma ferramenta que permite para criar gráficos e visualizações em Python.
O ficheiro fun contem enumeras funções que são chamadas pelas interfaces. Está organizado, primeiramente, com funções comuns às duas interfaces e depois com as da interface da linha de comando, seguida das da interface gráfica. Na apresentação do funcionamento de cada interface é explicado suncintamente o modo de atuar de algumas destas funções. 

### 2.2 FUNCIONAMENTO DA INTERFACE DA LINHA DE COMANDO (CLI)

#### Explicação dos módulos

1. **`from fun import *`***
   - **Objetivo**: Permite acessar funções presentes no fun.py que serão necessárias para esta interface.

2. **`import calendar`***
   - **Objetivo**: O módulo fornece funções relacionadas a calendários, ou seja, como criar e manipular meses e anos.

3. **`from datetime import datetime`**
   - **Objetivo**: O módulo `datetime` permite realizar operações com dados e horas atuais.

4. **`from colorama import Fore`**
   - **Objetivo**: O módulo `colorama` facilita o uso de cores no terminal. `Fore` permite definir cores para o texto no terminal.

#### 2.2.1 Importação Inicial

O comando 1 designa a variável "filepath" como sendo o resultado da função file() (que se encontra no fun), que abre uma janela que permite selecionar um arquivo json de entre os vários documentos do user. Posteriormente, à variável data é atribuida a função importar(filepath), que acessa ao conteudo do arquivo e verifica a sua estrutura, chamando as funções verifcestrutura(item) e verifcautores(autores). Se o conteudo respeitar o formato, o user pode escolher se pretende trabalhar com o arquivo que importou, se pretende salvar o conteudo deste para um novo arquivo e trabalhar deste último ou se pretende adicionar o conteudo do primeiro arquivo ao fim de outro arquivo já existente.
Caso o user comece por selecionar outra opção sem ser 1, 9, 0 ou " ", é feito um print a indicar para iniciar com o comando 1.

#### 2.2.2 Criar Publicação

O comando 2 chama a função `createPub`, que permite adicionar uma nova publicação ao arquivo/ficheiro. O utilizador fornece os dados necessários, e o código valida os campos obrigatórios (título e pelo menos 1 autor), verificando também se a data está no formato válido. Caso contrário, o sistema solicita a inserção correta. No final, a nova publicação é imediatamente guardada no ficheiro.

#### 2.2.3 Consultar Publicação

O comando 3 atribui à variável filtered_data a função tabfilterpt(data), que através de uma filtragem de 5 categorias relevantes, é apresentada uma tabela com toda a informação que se enquandre nos filtros. Posteriormente, o user introduz o número do ID da publicação que pretende ver com maior detalhe, chamando a função conspub(filterID, filtered_data) e é apresentada uma nova tabela só com os dados dessa publicação.

#### 2.2.4 Consultar Publicações

O comando 4 é semelhante ao 3, distinguindo-os o facto de poder consultar mais ID.

#### 2.2.5 Eliminar Publicações

O comando 5 é de igual forma semelhante ao comando 3. Contudo, substitui a função conspub pela DelPub, que permite eliminar a uma publicação pelo input do seu ID. Ainda nesta função é garantido que os ID são reordenados, não havendo saltos entre eles.

#### 2.2.6 Relatórios

O comando 6 começa por pedir ao user para escolher qual relatório pretende visualizar. Dentro dos disponíveis estão: 1- Distribuição de publicações por ano; 2-Número de publicações por autor e 3-Distribuição de palavras-chave pela sua frequência. Os resultados são exibidos no terminal com o auxílio das seguintes funções: `relPubAnoster`, `relPubAutor` e `relKeywords`. Se o user introduzir o comando "-", retoma ao menu anterior (lista()).

#### 2.2.7 Listar Autores

Ao utilizar o comando 7, a função `autores` lista no sistema todos os autores por ordem alfabética

#### 2.2.8 Atualizar publicação

No comando 8, a estrutura do código é igual à do 3, sendo apenas chamada a função updatePubs(pub) imediatamente a seguir à função conspub. Na função updatePubs é possível alterar os dados das 5 categorias, nomeadamente: data de publicação, resumo, palavras-chave, autores e afiliações. Esta função termina quando o user introduz "n" para não alterar mais nenhuma publicação.

#### 2.2.9 Ajuda

Com o comando 9, é chamada a função helpUser(), que lista todos os comandos disponíveis e a função correspondente de cada um. Caso o utilizador pressione "Enter" no menu principal sem escrever nada, o sistema imprime uma mensagem informando que, se precisar de ajuda, pode utilizar o comando 9.

#### 2.10 Sair do Programa

Com o comando 0, é encerrada consulta com a mensagem "Saiu do programa" 

### 2.3 Funcionamento da Interface Gráfica

1. **`from FreeSimpleGUI as sg`***
   - **Objetivo**: Permite criar interfaces gráficas simples, com definições de layout e ações baseadas em eventos, como clicar em botões.

#### 2.3.1 wprincipal()

Esta é, como o próprio nome indica, a janela principal da interface, constituída por 6 botões: 
   • Help - abre uma janela reduzida, a whelp() , que contêm listado o propósito dos 4 botões centrais;
   • Sair - fecha a janela;
   • Importar - abre a janela wficheirogui();
   • Consultar - abre a janela wconsultar(data, filepath);
   • Listar Autores - abre a janela wlistar(data);
   • Relatórios - abre a janela wrelatorios(data).
Se o user começar por selecionar os botões **Consultar**, **Listar Autores** e **Relatórios**, é adicionada uma linha de texto vermelha à janela principal a indicar: "Ainda não selecionou um ficheiro". Por outro lado, se começar por **Importar** e a importação for bem sucedida é adicionada uma linha verde: "Ficheiro importado com sucesso!", se for mal sucedida é uma linha vermelha: "Erro ao importar ficheiro!".

#### 2.3.2 wficheirogui()

Nesta janela, existe apenas um botão - **Browse** - que, semelhante ao cli, atribui à variável filepath função file(), abrindo a pasta de arquivos do user, mas à variável data atribui a função importargui(filepath), que apenas salva o ficheiro e utiliza o seu conteudo.
É retomado à wprincipal o filepath e a data, que nada mais é do que uma cópia do conteudo do ficheiro.

#### 2.3.3 wconsultar()

Esta é a janela mais complexa da interface. Antes mesmo do layout, o formato do data é simplificado e transformado no formato de publicações, através da função publicacoesc(data).
O layout da janela é formado por um título, 4 botões: 2 superiores (**Filtrar** e **Limpar filtros**) e dois inferiores (**Sair** e **Atualizar**), uma tabela e uma linha de texto informativa. 
A tabela possui 5 colunas: "Título", "Autores", "Afiliações", "Data de publicação" e "Palavras-chave". Se o user clicar sobre as headings: "Título", "Autores", e "Data de publicação" o conteudo da tabela será ordenado consoante a heading selecionada. Isto é possível através do evento == ('-TABELA-', '+CLICKED+', (-1, 0)), mais especificamente, '-TABELA-' identifica o elemento do layout, '+CLICKED+' indica o tipo de evento (clicar) e o (-1, 0) representa as coordenadas (linha, coluna), aqui usamos linha igual a -1 pois os headins não fazem parte das linhas do conteudo da tabela. Para a ordenação são chamadas as funções: ordpubtitulo(publicacoes,ori), ordpubnome(publicacoes,ori) e ordpubdata(publicacoes,ori).
O botão **Filtrar** abre a janela wFilterPub(publicacoes), que através do preenchimento de pelo menos um dos inputs, filtra pelas publicações que se enquadram, retomando à janela anterior com apenas as publicações filtradas na tabela.
O botão **Limpar filtros** volta a formatar o data em publicacoes e a tabela volta a ter as publicações iniciais.
O botão **Atualizar** usa exatamente o mesmo código que o **Limpar filtros**, contudo, é utilizando quando se retoma da janela wPublicacao(), pois o data já é diferente em algum aspeto e a tabela não atualiza de imediato.
Por fim, o evento '-TABELA-' and values['-TABELA-']!=[], seleciona uma linha da tabela que não seja vazia e atribui os seus valores/conteudo à variável linha_selec, que se existir fornece a informação da linha_selec em publicacoes à variável pub. Esta última variável entra na chamada da janela  wPublicacao(pub, data, filepath, publicacoes).

#### 2.3.4 wPublicacao()

Nesta janela, o layout inicia com 3 botões: **Apagar Publicação**, **Criar Publicação** e **Editar Publicação**, por baixo deste estão vários títulos, textos dentro de retângulos simples e textos dentro de blocos com barras que deslizam, que permitem mostrar toda a informação detalhada da publicação selecionada. Ainda no layout, há o botão **Fechar** para fechar a janela.
Ao selecionar o botão **Apagar Publicação** é aberta a janela wConfirmacao(), estilo popup, com uma pergunta - "Tem a certeza que quer eliminar a publicação?" - e dois botões, sim ou não. Se a opção for sim, é chamada a função deletepubgui(pub, data, filepath), que compara o ID da publicação selecionada com os ID do data e elimina o que for correspondente. De seguida, o filepath é atualizado com o novo data e o data volta a sofrer a transformação para publicacoes, retomando este ultimo para a janela wconsultar com o fechar automático da janela wPublicacao().
Por outro lado, se o botão selecionado for **Criar Publicação** é aberta a janela criarPub(data, filepath). Nesta janela, o user preenche os espaços consoante o seu interesse para criar uma nova publicação. Esta é, posteriormente, transformada na estrutura do data, o filepath é atualizado e data volta a transformar-se em publicacoes.
Por fim, se o botão selecionado for o **Editar Publicação** é aberta a janela editarpublicacao(pub, data, filepath, original_id=pub['ID']). O layout é semelhante ao  wPublicacao() mas mais simplificado, sendo possivel alterar o conteudo dentro de cada quadrado. Nesta janela são chamadas duas funções process_authors(pub) e format_authors(authors). Apesar da informação ser alterada no data, no filepath e em publicacoes, a parte dos nomes, afiliações e orcid é apagada e não conseguimos detetar o problema.

#### 2.3.5 wrelatorios()

Nesta janela existem 6 botões centrais mais o botão sair. Nos botões centrais temos: 'Distribuição de publicações por ano', 'Distribuição de publicações por mês', 'Número de publicações por autor', 'Distribuição de publicações de um autor por anos', 'Distribuição de palavras-chave pela sua frequência' e 'Distribuição de palavras-chave mais frequente por ano.' Consouante o botão central selecionado é chamada a função wpubano(data), wpubmes(data), wpubsautor(data), wpubautorano(data), wpubskeyword(data) e wkeyfreano(data), respetivamente. 

##### 2.3.5.1 wpubano(data)

Esta janela chama, por sua vez, a função relPubAnosgui(data), que permite criar um gráfico de pontos ligados relativamente ao número de publicações por cada ano, usando o Counter()para a contagem das publicações e pyplot para gerar o gráfico.

##### 2.3.5.2  wpubmes(data)

Nesta janela o user introduz o ano que pretende visualizar a distribuição de publicações por mês e chama a função distribPubPorMesgui(data, ano), semelhante à relPubAnosgui(data).

##### 2.3.5.3  wpubsautor(data)

Esta janela chama a função relPubAutorgui(data, top_n=20), que cria uma lista de dicionários, sendo os nomes dos autores as chaves e o número de publicações os valores. Esta lista é organizada e seleciona o top 20 autores com mais publicações, para gerar um gráfico de barras.

##### 2.3.5.4  wpubautorano(data)

Nesta janela o user introduz o nome do autor, é aberto um popup com a lista de autores que façam correspondência parcial ao input do user, de seguida este seleciona o que pretende e é chamada a função PubAutoPorAnogui(data, autor) para gerar o gráfico de distribuição de publicações por anos.

##### 2.3.5.5  wpubskeyword(data)

Esta janela é muito semelhante à wpubsautor(data), chamando a função relkeywordsgui(data, top_n=20). As palavras mais frequentes apresentadas correspondem a caracteres, apesar de que na função relkeywordsgui(data, top_n=20) ocorre uma filtragem para que isso não aconteça.

##### 2.3.5.6  wkeyfreano(data)

Esta janela chama a função keyfreano(data), contudo o gráfico gerado fica em branco.

#### 2.3.6 wlistar(data)

Esta janela não está operacional, mas decidimos desenvolver pelo menos o seu layout. No código são apresentadas algumas funções ao clicar nos botões, no entanto estas dão erro.

## 3. Conclusão

A criação deste sistema de consulta e análise de publicações científicas em Python, irá permitir ao utilizador desta ferramenta, criar, atualizar e analisar publicações. Ou seja, com base num dataset de publicações, o sistema possibilitar a pesquisa de artigos usando filtros relevantes, tais como a data de publicação, as palavras-chave, autores, etc. E ainda será possível, gerar relatórios (mostrando gráficos ilustrativos com estatísticas) detalhados para a análise de métricas dos artigos e dos seus autores.
O desenvolvimento deste projeto, permitiu alargar em grande escala os nossos conhecimentos sobre esta disciplina e testar a nossa capacidade lógica e criativa.

## 4. Webgrafia

https://www.w3schools.com/ 