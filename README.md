# relatos-consumidores
Esse repositório guarda os códigos usados no projeto final de graduação "Modelagem e Construção de uma Base Pública de Relatos de Consumidores", que pode ser encontrado em: https://linktr.ee/biamsarmento

Este trabalho aborda o desenvolvimento de uma base pública de dados estruturados a partir de relatos de consumidores extraídos do site Consumidor.gov.br. A motivação principal está na necessidade de fornecer acesso fácil e automatizado a dados públicos que, muitas vezes, são disponibilizados de forma desestruturada e de difícil manipulação, limitando sua utilização por pesquisadores e profissionais. Para superar esses desafios, foi empregada uma abordagem baseada em técnicas de web scraping, associada a metodologias de modelagem de banco de dados, processos ETL (Extração, Transformação e Carga), e análise de dados com machine learning.

Os códigos estão separados da seguinte forma: 

1) web_scraping.py é o código principal no qual inserimos as datas desejadas para extração.
2) O código functions.py contem as funções utilizadas para a coleta de dados via web scrapping, utilizando BeautifulSoup.
3) O código database.py salva os dados no banco MySQL, que deve ser previamente configurado.
4) O código randomForest.py processa os dados da base, que devem ser salvos no formato JSON, e fornece algumas estatísticas. Ele tenta acertar a nota (de 1 a 5) que o usuário vai escolher para avaliar o atendimento, baseando-se no status e no comentário do relato. O algoritmo usado é o Random Forest.

Espero que esses códigos possam ajudar pesquisadores e cientistas que desejam extrair dados públicos de forma eficiente e automática. :)