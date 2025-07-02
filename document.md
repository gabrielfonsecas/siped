# SIPED - README

## Índice

- [Frontend](#frontend)
- [Backend](#backend)
- [Banco de Dados](#banco-de-dados)
- [Scripts e Validações](#scripts-e-validações)
- [Funcionalidades Gerais](#funcionalidades-gerais)
- [Observações e Perguntas](#observações-e-perguntas)

---

## Frontend

### ✔️ Feito

- Inserido a logo do SIPED na index.
- Ajustado o layout da página de paciente.
- Ajustado o dropdown do header para responsividade.
- Ajustado o alerta dos scripts no cadastro de paciente.
- Ajuste de campos obrigatórios no cadastro de paciente.
- Inserido links para cadastro e visualização de paciente no header.
- Ajustado o botão de salvar/apagar do cadastro de paciente para ficar igual ao de nova consulta.
- Inserido as unidades de medida dos campos de consulta ao visualizar.
- Inserido tipos de valores no cadastro de paciente.
- Ajustado campos de texto para permitir pular linhas (longtext).
- Inserido alerta de cadastro com sucesso (consulta e paciente).
- Inserido SIPED no header.

### 🔜 A Fazer

- Ajustar os HTMLs:
  - `editarPaciente`
  - `confirmarExclusao`
- Ajustar nomes nas listas.html (title do paciente).
- Alterar os titles das páginas.
- Alterar os HTMLs (listas, nova consulta), os nomes estão confusos.
- Ajustar tabulação das divs (nova consulta já está ok).
- Ajustar cadastroPaciente em classe de colunas (ex: `<div class="column is-one-third">`).
- Alterar para textarea os campos dentro de nova consulta.
- Inserir nome em negrito no nova consulta.
- Questionar onde fica o melhor lugar para idade no nova consulta.

---

## Backend

### ✔️ Feito

- Ajustado o relacionamento de paciente e consulta.
- Ajustado para salvar os campos do banco tudo em minúsculo (feito em cadastroPaciente).
- Ajustado os campos que são selecionados do banco para formatar as palavras (primeira letra maiúscula de cada palavra).
- Ajustado sexo e tipo sanguíneo para maiúscula (paciente).
- Ajustado as formatações no campo (atualiza os valores dos campos com os formatos corretos).
- Ajustado os dados de nomes em primeira letra maiúscula de cada palavra (cadastroPaciente).
- Ajustes no banco (feito mais ou menos).
- Data de nascimento está zerando ao editar paciente (feito).
- Idade está com um dia de erro (ajustado a princípio).
- Setar como padrão a data da consulta como dia de hoje (feito).
- Quando altera a data de nascimento buga a idade nas consultas anteriores (feito, porém rever pra garantir).
- Inserir meses e dias na idade de consulta (feito).
- IMC deve ser automático no banco (não está automático, mas para ver é necessário clicar, quando clica vai pro banco).
- Aparecer o IMC.
- Temperatura - exame físico.
- Ao dar enter ele envia o formulário mas não deve (feito).

### 🔜 A Fazer

- Ajustar para CPF não obrigatório do paciente.
- Descobrir qual deve ser a segunda informação na busca do paciente.
- Verificar as views.
- Ajustar nomes no banco (ex: doencaPrevia).
- Erro ao enviar o formulário, está dando como enviado mas não foi. (feito) ajustar apenas os de editarpaciente
- Ver sobre histórico gestacional idades.
- Inserir scripts de validação no editarPaciente.
- Refazer o buscaPaciente e cadastroConsulta baseado no listaConsulta.
- Tentar ajustar o banco para consulta ao invés de novaConsulta.
- Está sendo feito o ajuste do banco de idade, será salvo em meses também (rever isso).
- Alterar para o cálculo da idade referente à data da consulta (não fazer).
- Alterar para o None de consulta quando null.
- Arrumar bug de CPF do paciente null.
- Não pode excluir paciente se houver consulta cadastrada.
- Criar um campo novo de exclusão dentro do banco de paciente para apenas esconder o paciente (não deletar de fato do banco).

---

## Banco de Dados

### ✔️ Feito

- Ajustado o relacionamento de paciente e consulta.
- Ajustes no banco (feito mais ou menos).
- Está sendo feito o ajuste do banco de idade, será salvo em meses também (rever isso).

### 🔜 A Fazer

- Ajustar nomes no banco (ex: doencaPrevia).
- Criar um campo novo de exclusão dentro do banco de paciente para apenas esconder o paciente (não deletar de fato do banco).
- Tentar ajustar o banco para consulta ao invés de novaConsulta.

---

## Scripts e Validações

### ✔️ Feito

- CadastroPaciente: scripts ajustados.
- Consulta: scripts ajustados.

### 🔜 A Fazer

- NovaConsulta: scripts a fazer.
- Inserir scripts de validação no editarPaciente.
- Necessário verificar o script (parece ter repetições).

---

## Funcionalidades Gerais

### ✔️ Feito

- Inserido alerta de cadastro com sucesso (consulta e paciente).
- Inserido SIPED no header.
- Inserido as unidades de medida dos campos de consulta ao visualizar.
- Inserido tipos de valores no cadastro de paciente.
- Ajustado o botão de salvar/apagar do cadastro de paciente para ficar igual ao nova consulta.
- Campos de texto pular linha (longtext).
- IMC deve ser automático no banco (não está automático, mas para ver é necessário clicar, quando clica vai pro banco).
- Aparecer o IMC.
- Temperatura - exame físico.
- Idade está com um dia de erro (ajustado a princípio).
- Setar como padrão a data da consulta como dia de hoje (feito).
- Quando altera a data de nascimento buga a idade nas consultas anteriores (feito, porém rever pra garantir).
- Inserir meses e dias na idade de consulta (feito).
- Ao dar enter ele envia o formulário mas não deve (feito).

### 🔜 A Fazer

- Aparecer a doença e medicação caso tenha no histórico.
- Colocar data consulta em consulta por mais recente.
- Criar uma lógica para medicamento e doença prévia em nova consulta.
- Inserir data de nascimento e CPF no listar-consulta.html.
- Alterar URL para formato: ex: `http://127.0.0.1:8000/nova-consulta/9/`
- Alterar os HTMLs (listas, nova consulta), os nomes estão meio confusos.
- Ajustar nomes nas listas.html (title do paciente).
- Não seria melhor input a estatura no HTML de gráfico e inserir ela no banco? (avaliar)
- Campo para imprimir receita, atestado da consulta (pensar).

---

## Observações e Perguntas

- Há necessidade de mais campos? Algum de extrema importância?
- O que é necessário de ferramenta, como gráfico de crescimento?
- Avaliar se o ajuste do banco de idade (salvar em meses) está adequado.
- Avaliar se o input de estatura no gráfico deve ser inserido no banco.

---

> **Legenda:**  
> ✔️ Feito  
> 🔜 A Fazer



-abertura (fabricio)
-figma
-sistema

limitações:
agenda
cid

encerra comentando sobre o teste

perguntas:
-há necessidade de mais campos? mais algum de extrema importancia?
-o que é necessario de ferramenta, como grafico de crescimento?
-gostaria que fosse clicavel nos nodos dos historicos de crescimento para visualizar



cpf não obrigatório ✔️
rg não obrigatório ✔️
rg do responsável não obrigatório ✔️
endereço não obrigatório ✔️

prematuro, idade cronológica e idade corrigida em consultas ✔️ -ajustar hidden do prematuro
poder editar os remédios/comorbidades?
gráfico para diagnostico de imc - pegar os dados para criança, não de adulto.
adicionar diferentes gráficos
perímetro cefálico na tela ✔️
trocar fundoscopia para teste do reflexo vermelho ✔️
remover a repetição de temperatura ✔️
ela vai mandar alguma tabela? me perdi no meio do dialogo
não precisa voltar para consulta ao clicar na bolinha do gráfico ✔️
campo para classificar o peso, estatura e imc, que eles possam descrever se está bom ou não de acordo com a leitura do gráfico ✔️
ausculta ✔️
colocar classificação de pressão arterial
links externos para os gráficos especiais
historico gestacional apenas na primeira consulta

CDC

usa o programa tazi na clinica
e-sus na prefeitura de não sei aonde


termo de consentimento e questionário