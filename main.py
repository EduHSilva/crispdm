import os
import pandas as pd
import numpy as np
import random
import datetime

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from ydata_profiling import ProfileReport
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score


def generate_data(path_file: str, num_rows: int) -> None:
    data: pd.DataFrame = pd.DataFrame(columns=[
        'ID da Propriedade', 'Tipo de Imóvel', 'Localização',
        'Número de Quartos', 'Número de Banheiros', 'Área Total (em metros quadrados)',
        'Idade da Propriedade', 'Condição da Propriedade', 'Amenidades', 'Preço de Venda Anterior',
        'Data de Venda Anterior', 'Histórico de Aluguel', 'Taxas de Juros Atuais', 'Custos de Manutenção Anuais',
        'Taxas de Condomínio Mensais', 'Impostos sobre a Propriedade', 'Histórico de Valorização',
        'Fluxos de Caixa Anuais', 'Retorno sobre Investimento (ROI)', 'Data de Inclusão no Dataset',
        'Fonte dos Dados'
    ])

    idade_imovel: int = np.random.randint(1, 50, num_rows)
    preco_anterior: int = np.random.randint(50000, 5000000, num_rows)
    area_total: float = np.random.uniform(50, 300, num_rows)
    taxas_juros: float = np.random.uniform(2, 6, num_rows)
    valor_alugueis: int = np.random.randint(500, 5000, num_rows)
    custos_manutencao_anual: float = np.random.uniform(100, 5000, num_rows)
    impostos_sobre_imovel: float = np.random.uniform(500, 5000, num_rows)
    taxas_condominio: float = np.random.uniform(50, 500, num_rows)

    roi: float = (0.2 * idade_imovel + 0.4 * preco_anterior + 0.2 * area_total + 0.3 + taxas_juros * 0.2
                  + 0.4 * valor_alugueis + 0.3 * custos_manutencao_anual + 0.1 * impostos_sobre_imovel + 0.1 *
                  taxas_condominio + np.random.normal(0, 2, num_rows))

    for i in range(num_rows):
        id_propriedade: int = i
        print(i)

        data = data.append({
            'ID da Propriedade': id_propriedade,
            'Tipo de Imóvel': random.choice(['Casa', 'Apartamento', 'Condomínio']),
            'Localização': f'Cidade {random.randint(1, 10)}',
            'Número de Quartos': random.randint(1, 6),
            'Número de Banheiros': random.randint(1, 4),
            'Área Total (em metros quadrados)': area_total[i],
            'Idade da Propriedade': idade_imovel[i],
            'Condição da Propriedade': random.choice(['Excelente', 'Boa', 'Média', 'Ruim']),
            'Amenidades': ', '.join(random.sample(['Piscina', 'Garagem', 'Jardim', 'Vista panorâmica'], 2)),
            'Preço de Venda Anterior': preco_anterior[i],
            'Data de Venda Anterior': datetime.date(random.randint(1980, 2023), random.randint(1, 12),
                                                    random.randint(1, 28)),
            'Histórico de Aluguel': random.choice(['Sim', 'Não']),
            'Valor aluguel': valor_alugueis[i],
            'Taxas de Juros Atuais': taxas_juros[i],
            'Custos de Manutenção Anuais': custos_manutencao_anual[i],
            'Taxas de Condomínio Mensais': taxas_condominio[i],
            'Impostos sobre a Propriedade': impostos_sobre_imovel[i],
            'Histórico de Valorização': random.uniform(0.1, 0.5),
            'Fluxos de Caixa Anuais': random.uniform(1000, 50000),
            'Retorno sobre Investimento (ROI)': roi[i],
            'Preço de Venda Atual': random.randint(50000, 5000000),
            'Data de Inclusão no Dataset': datetime.date(random.randint(2010, 2023), random.randint(1, 12),
                                                         random.randint(1, 28)),
            'Fonte dos Dados': random.choice(['Zillow', 'Kaggle', 'Redfin'])
        }, ignore_index=True)

        data.to_csv(path_file, index=False)


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


if __name__ == '__main__':
    path: str = './data/dataset_imobiliario.csv'
    if not os.path.isfile(path):
        generate_data(path, 10000)

    df: pd.DataFrame = pd.read_csv(path)
    profile: ProfileReport = ProfileReport(df, title="Profiling Report")
    profile.to_file("report.html")

    le: LabelEncoder = LabelEncoder()
    data_encoded: pd.DataFrame = df.apply(lambda col: le.fit_transform(col) if col.dtype == 'object' else col)

    y: pd.DataFrame = data_encoded['Retorno sobre Investimento (ROI)']
    x: pd.DataFrame = data_encoded.loc[:, df.columns != 'Retorno sobre Investimento (ROI)']

    x_treino, x_teste, y_treino, y_teste = train_test_split(x, y, test_size=0.2, random_state=23)

    train_and_evaluate_decision_tree(x_treino, y_treino, x_teste, y_teste)

    train_and_evaluate_linear_regression(x_treino, y_treino, x_teste, y_teste)
