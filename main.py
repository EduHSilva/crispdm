import os

import pandas as pd
import random
import datetime
from ydata_profiling import ProfileReport


def generate_data(path_file: str, num_rows: int) -> None:
    data: pd.DataFrame = pd.DataFrame(columns=[
        'ID da Propriedade', 'Tipo de Imóvel', 'Localização', 'Coordenadas Geográficas',
        'Número de Quartos', 'Número de Banheiros', 'Área Total (em metros quadrados)',
        'Idade da Propriedade', 'Condição da Propriedade', 'Amenidades', 'Preço de Venda Anterior',
        'Data de Venda Anterior', 'Histórico de Aluguel', 'Características do Bairro',
        'Tendências de Mercado', 'Taxas de Juros Atuais', 'Custos de Manutenção Anuais',
        'Taxas de Condomínio Mensais', 'Impostos sobre a Propriedade', 'Histórico de Valorização',
        'Fluxos de Caixa Anuais', 'Retorno sobre Investimento (ROI)', 'Data de Inclusão no Dataset',
        'Fonte dos Dados'
    ])

    for _ in range(num_rows):
        data = data._append({
            'ID da Propriedade': random.randint(1, 10000),
            'Tipo de Imóvel': random.choice(['Casa', 'Apartamento', 'Condomínio']),
            'Localização': f'Cidade {random.randint(1, 10)}',
            'Coordenadas Geográficas': f'({random.uniform(-90, 90)}, {random.uniform(-180, 180)})',
            'Número de Quartos': random.randint(1, 6),
            'Número de Banheiros': random.randint(1, 4),
            'Área Total (em metros quadrados)': random.uniform(50, 300),
            'Idade da Propriedade': random.randint(1, 50),
            'Condição da Propriedade': random.choice(['Excelente', 'Boa', 'Média', 'Ruim']),
            'Amenidades': ', '.join(random.sample(['Piscina', 'Garagem', 'Jardim', 'Vista panorâmica'], 2)),
            'Preço de Venda Anterior': random.randint(50000, 5000000),
            'Data de Venda Anterior': datetime.date(random.randint(1980, 2023), random.randint(1, 12),
                                                    random.randint(1, 28)),
            'Histórico de Aluguel': random.choice(['Sim', 'Não']),
            'Características do Bairro': f'Bairro {random.randint(1, 20)}',
            'Tendências de Mercado': random.choice(['Crescente', 'Estável', 'Decrescente']),
            'Taxas de Juros Atuais': random.uniform(2, 6),
            'Custos de Manutenção Anuais': random.uniform(100, 5000),
            'Taxas de Condomínio Mensais': random.uniform(50, 500),
            'Impostos sobre a Propriedade': random.uniform(500, 5000),
            'Histórico de Valorização': random.uniform(0.1, 0.5),
            'Fluxos de Caixa Anuais': random.uniform(1000, 50000),
            'Retorno sobre Investimento (ROI)': random.uniform(0.05, 0.2),
            'Data de Inclusão no Dataset': datetime.date(random.randint(2010, 2023), random.randint(1, 12),
                                                         random.randint(1, 28)),
            'Fonte dos Dados': random.choice(['Zillow', 'Kaggle', 'Redfin'])
        }, ignore_index=True)

    data.to_csv(path_file, index=False)


if __name__ == '__main__':
    path: str = './data/dataset_imobiliario.csv'
    if not os.path.isfile(path):
        generate_data(path, 20000)

    df: pd.DataFrame = pd.read_csv(path)
    profile = ProfileReport(df, title="Profiling Report")
