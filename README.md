# Utilizando Análise de Dados para Auxiliar Investidores no Mercado Imobiliário

## Business understanding

### Contexto

O mercado imobiliário é uma arena complexa e dinâmica, onde os investidores buscam oportunidades de investimento sólidas
e desejam tomar decisões estratégicas informadas. Identificar as propriedades certas, prever seu desempenho futuro e
calcular os retornos esperados são desafios críticos que os investidores enfrentam. Nesse contexto, a aplicação da
metodologia CRISP-DM (Cross-Industry Standard Process for Data Mining) desempenha um papel fundamental.

### Problema Abordado:

Investidores no mercado imobiliário enfrentam a necessidade de identificar oportunidades de investimento, comparar
várias propriedades e antecipar os retornos potenciais. Para tomar decisões estratégicas eficazes, é essencial contar
com suporte baseado em dados e análises confiáveis.

### Solução Proposta:

A solução proposta envolve a aplicação de modelos preditivos avançados, como regressão e análise de séries temporais,
para prever o valor futuro de imóveis e estimar os potenciais retornos para os investidores. Além disso, por meio de uma
dashboard intuitiva e interativa, oferecemos a capacidade de comparar várias propriedades lado a lado. Essa abordagem
fornece aos investidores uma visão abrangente do mercado imobiliário, permitindo que eles tomem decisões informadas e
estratégicas em seus investimentos.

### Benefícios para os Investidores:

- Identificação mais precisa de oportunidades de investimento.
- Estimativas confiáveis de retornos futuros.
- Comparação fácil de várias propriedades.
- Melhor compreensão do mercado imobiliário.
- Apoio decisivo na tomada de decisões estratégicas.
- Esta solução não apenas aumenta a eficácia das decisões dos investidores, mas também oferece uma vantagem competitiva
  no mercado imobiliário em constante mudança, tornando o processo de investimento mais transparente e orientado por
  dados.

### Objetivo

Treinar um modelo para prever o ROI (retorno sobre investimento) de um imóvel e gerar uma dashboard para analise de
propriedades.

## Data understanding

O dataset foi gerado pelo CHATGPT com as seguintes colunas:

| Coluna                           | Tipo    | Descrição                                                                |
|----------------------------------|---------|--------------------------------------------------------------------------|
| id                               | int64   | Identificador único auto-incrementável                                   |
| Tipo de imóvel                   | object  | Se é casa, apartamento ou condomínio                                     |
| Localização                      | object  | Cidade do imovel (indo de cidade 1 a 10)                                 |
| Coordenadas                      | object  | Pontos geograficos do imovel                                             |
| Número de Quartos                | int64   | Numéro de quartos do imovel                                              |
| Número de Banheiros              | int64   | Numéro de quartos do imovel                                              |
| Área Total (em metros quadrados) | float64 | Área do imovel                                                           |
| Idade da Propriedade             | int64   | Diferença entre ano atual e ano de construção da propriedade             |
| Condição da Propriedade          | object  | Condição atual do propriedade podendo ser: Excelente, Boa, Média ou Ruim |
| Amenidades                       | object  | Se o imovel possui garagem, piscina, jardim, vista panoramica            |
| Preço de Venda Anterior          | int64   | Preço da ultima venda do imovel                                          |
| Data de Venda Anterior           | date    | Data de ultima venda do imovel                                           |
| Histórico de aluguel             | bool    | Se o imovel foi alugado                                                  |
| Valor de aluguel                 | float64 | Valor de aluguel do imóvel                                               |
| Taxa de juros atuais             | float64 | Valor de juros do imóvel                                                 |
| Custos de manutenção anuais      | float64 | Média de gastos com manutenção ao longo dos anos                         |
| Taxas de Condomínio Mensais      | float64 | Taxas atuais a serem pagas ao condominio do imovel                       |
| Impostos sobre a Propriedade     | float64 | Valor gastos com impostos anualmente                                     |
| Histórico de Valorização         | float64 | Valor entre 0.1 a 0.5 com taxa de valorização historica                  |
| Fluxos de Caixa Anuais           | float64 | Possivel retorno em caixa anual                                          |
| Retorno sobre Investimento (ROI) | float64 | Retorno sobre investimento                                               |
| Preço de venda atual             | float64 | Valor de venda do imóvel                                                 |
| Data de Inclusão no Dataset      | date    | Data de inclusão no dataset                                              |
| Fonte dos Dados                  | object  | Origem de dados                                                          |

As informações sobre a propriedade, como idade, condição, amenidades, histórico de venda e aluguel, bem como dados
financeiros relevantes, como taxas de juros, custos de manutenção, impostos podem ser relevantes para o objetivo do
algoritmo.

O ROI foi calculado: 
```python
    roi: float = (0.2 * idade_imovel + 0.4 * preco_anterior + 0.2 * area_total + 0.3 + taxas_juros * 0.2
                  + 0.4 * valor_alugueis + 0.3 * custos_manutencao_anual + 0.1 * impostos_sobre_imovel + 0.1 *
                  taxas_condominio + np.random.normal(0, 2, num_rows))
```


## Data preparation
### Codificação de atributos
Foi necessario utilizar o LabelEncoder para tranformar os atributos não numericos. Segue trecho do codigo
```python
    le = LabelEncoder()
    data_encoded = df.apply(lambda col: le.fit_transform(col) if col.dtype == 'object' else col)
```

### Divisão entre treino e teste
Utilizado 20% para testes e 80% para treinamento dos algoritmos, conforme trecho:

```python
    x_treino, x_teste, y_treino, y_teste = train_test_split(x, y, test_size=0.2, random_state=23)
```

## Modeling
Foi testado dois algoritmos para previsão do ROI, arvores de decisão e regresão linear, sendo a regressão a com maior precisão.

```python
def train_and_evaluate_decision_tree(x_treino_dt: pd.DataFrame, y_treino_dt: pd.Series, x_teste_dt: pd.DataFrame,
                                     y_teste_dt: pd.Series) -> None:
    decision_tree_model = DecisionTreeRegressor()
    decision_tree_model.fit(x_treino_dt, y_treino_dt)

    predicates = decision_tree_model.predict(x_teste_dt)

    score = r2_score(y_teste_dt, predicates)
    print("Decision tree R² Score:", score)


def train_and_evaluate_linear_regression(x_treino_lr: pd.DataFrame, y_treino_lr: pd.Series, x_teste_lr: pd.DataFrame,
                                         y_teste_lr: pd.Series) -> None:
    linear_regression_model = LinearRegression()
    linear_regression_model.fit(x_treino_lr, y_treino_lr)
    score = linear_regression_model.score(x_teste_lr, y_teste_lr)
    print('LinearRegression: ', score)
```

## Evaluation
A saída das funções: 
Decision tree R² Score: 0.9999960273775078
LinearRegression:  0.9999999999878614

## Conclusão
