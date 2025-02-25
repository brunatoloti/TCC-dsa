# TCC do MBA em Data Science e Analytics da USP/Esalq - Turma 231


## Título

Criação de uma plataforma web em Python para aplicação do PPL da dieta em escolas

## Orientador

André Luis Ramos Sanches

## Resumo

O fornecimento de uma alimentação saudável e nutritiva para crianças e adolescentes 
em idade escolar é muito importante. Por conta disso, existem determinações governamentais 
para garantir que cardápios escolares respeitem as exigências nutricionais para estas faixas 
etárias. Além disso, uma vez que os repasses governamentais para este fim são limitados, 
elaborar cardápios que, além de respeitarem essas exigências, tenham um baixo custo é 
bastante relevante. Neste contexto, o presente trabalho teve como objetivo desenvolver uma 
plataforma web que formule cardápios escolares que garantam as recomendações 
nutricionais dos alunos e que possuam um custo mínimo utilizando a linguagem Python e a 
técnica matemática de programação linear, baseada na teoria de pesquisa operacional. Os 
dados usados foram obtidos a partir da Tabela Brasileira de Composição de Alimentos [TACO] 
e do manual de Planejamento de cardápios para a Alimentação Escolar do Fundo Nacional 
de Desenvolvimento da Educação [FNDE], além de serem usadas informações de preços 
correntes dos alimentos que devem ser informados pelo usuário no momento da utilização da 
aplicação web. Para demonstração do uso, foi realizado um estudo de caso. Como resultado, 
foi obtida uma plataforma web de utilização amigável, descomplicada e que pode contribuir 
com trabalhos futuros nesta área, auxiliando profissionais de pesquisa operacional e 
nutricionistas técnicos escolares. 

## Tecnologias utilizadas

* **Linguagem:** Python
* **Principais bibliotecas:** streamlit, PulP, pandas

## Dados

Adaptados e inseridos em duas planilhas:

* [**Obtidos da Tabela Brasileira de Composição de Alimentos**](https://github.com/brunatoloti/TCC-dsa/blob/main/data/alimentos.xlsx)
* [**Obtidos do manual de Planejamento de cardápios para a Alimentação Escolar**](https://github.com/brunatoloti/TCC-dsa/blob/main/data/alimentos_restricoes.xlsx)

## Passos do desenvolvimento do material e métodos
Uma vez que se quis criar uma plataforma que resolve um problema de pesquisa
operacional, especificamente o problema da dieta, foi necessário fazer uma contextualização teórica e seguir os passos
recomendados pela literatura como representativos de estudos de PO bem-sucedidos.
Esses passos não precisam ser todos seguidos, necessariamente, porém, neste trabalho,
foram. Segundo Hillier e Lieberman (2013), os passos são:
1. Definir o problema de interesse e coletar os dados; 
2. Formular um modelo matemático para representar o problema; 
3. Desenvolver um procedimento computacional a fim de derivar soluções para o 
problema com base no modelo; 
4. Testar o modelo e aprimorá-lo conforme necessário; 
5. Preparar-se para a aplicação contínua do modelo; 
6. Implementá-lo. 

## Manual de utilização da plataforma

[Acessar o manual](https://github.com/brunatoloti/TCC-dsa/blob/main/data/manual_utilizacao.pdf)

## Referências

Belfiore, P.; Fávero, L.P. 2013. Pesquisa operacional para cursos de engenharia. 1 ed. 
Editora Elsevier, Rio de Janeiro, RJ, Brasil. 

Brasil. 2009. Lei n. 11947, de 16 de junho de 2009. Dispõe sobre o atendimento da 
alimentação escolar e do Programa Dinheiro Direto na Escola aos alunos da educação 
básica, altera as Leis nos 10.880, de 9 de junho de 2004, 11.273, de 6 de fevereiro de 2006, 
11.507, de 20 de julho de 2007, revoga dispositivos da Medida Provisória no 2.178-36, de 24 
de agosto de 2001, e a Lei no 8.913, de 12 de julho de 1994, e dá outras providências. 
Diário Oficial da União, Brasília, 17 jun. 2009. Seção 1, p. 2. 

Brasil. 2020. Resolução n.6, de 08 de maio de 2020. Dispõe sobre o atendimento da 
alimentação escolar aos alunos da educação básica no âmbito do Programa Nacional de 
Alimentação Escolar – PNAE. Diário Oficial da União, Brasília, 12 maio 2020. Seção 1, p. 38. 

Danelon, M.A.S.; Danelon, M.S.; Silva, M.V. 2015. Serviços de alimentação destinados ao 
público escolar: análise da convivência do Programa de Alimentação Escolar e das cantinas. 
Revista Segurança Alimentar e Nutricional (Online) 13: 85-94. 

Ferreira, H.G.R.; Alves, R.G.; Mello, S.C.R.P. 2019. O programa nacional de alimentação 
escolar (PNAE): alimentação e aprendizagem. Revista da Seção Judiciária do Rio de 
Janeiro 22: 90-113. 

Fundo Nacional de Desenvolvimento da Educação [FNDE]. 2022. Planejamento de 
cardápios para a Alimentação Escolar. Disponível em: <https://www.gov.br/fnde/pt-br/acesso-a-informacao/acoes-e-programas/programas/pnae/manuais-e-cartilhas/MANUAL_V8.pdf>. Acesso em: 06 mar. 2024. 

Hillier, F.S.; Lieberman, G.J. 2013. Introdução à pesquisa operacional. 9ed. Bookman, Porto 
Alegre, RS, Brasil. 

Ministério da Saúde [MS]. 2014. Guia alimentar para a população brasileira. Disponível em: 
<https://bvsms.saude.gov.br/bvs/publicacoes/guia_alimentar_populacao_brasileira_2ed.pdf>. Acesso em: 24 abr. 2024.

Núcleo de Estudos e Pesquisas em Alimentação [NEPA]. 2011. Tabela Brasileira de 
Composição de Alimentos – TACO. Disponível em: <https://www.cfn.org.br/wp-content/uploads/2017/03/taco_4_edicao_ampliada_e_revisada.pdf>. Acesso em: 06 mar. 2024. 

Oliveira, D.E.; Borges, A.C.A; Silva, V.V. 2020. Uma aplicação do problema da dieta para se 
encontrar o menor custo de refeições diárias para idosos na cidade de Monte Carmelo – MG. Brazilian Journal of Development 6: 36025-36034. 

Reis, M.R.S. 2023. Programação linear e o problema da dieta. Dissertação de Mestrado 
Profissional em Matemática. Universidade Federal de Sergipe, São Cristóvão, SE, Brasil. 

Santos, M.; Sampaio, R.T.; Martins, E.R.; Dias, F.C.; Walker, R.A. 2017. Aplicação da 
programação linear na formulação de uma dieta de custo mínimo: estudo de caso de uma 
empresa de refeições coletivas no estado do Rio de Janeiro. In: XIII Encontro Mineiro de 
Engenharia de Produção - EMEPRO 2017, 2017, Juiz de Fora, MG, Brasil. Anais... p. [...]. 

Sociedade Brasileira de Pediatria [SBP]. 2012. Manual de orientação do departamento de 
nutrologia: alimentação do lactente ao adolescente, alimentação na escola, alimentação 
saudável e vínculo mãe-filho, alimentação saudável e prevenção de doenças, segurança 
alimentar. Disponível em: <https://www.sbp.com.br/fileadmin/user_upload/pdfs/14617a-PDManualNutrologia-Alimentacao.pdf>. Acesso em: 24 abr. 2024. 

Stigler, G.J. 1945. The Cost of Subsistence. Agricultural & Applied Economics Association 
27: 303-314.