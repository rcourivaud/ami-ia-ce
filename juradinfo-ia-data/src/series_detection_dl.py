from transformers import pipeline

param = db.initialize()


## Loading Data
def load_data(db_param):
    engine = db_param['engine']
    connection = engine.connect()

    df = pd.read_sql("SELECT request_id, titre, num_serie  FROM test_requetes_meta_data", con=connection)
    df = df[df['num_serie'].notna()]
    return df

nlp = pipeline("zero-shot-classification")
df_series = pd.read_sql('SELECT DISTINCT num_serie FROM test_requetes_meta_data', con=engine.connect())
df_series = df_series[df_series.num_serie != ""]
lst_series = list(df_series.num_serie)

df_sequences = load_data(param)
lst_sequences = list(df_sequences.titre)

hypothesis_template = 'The classe of this request is {}.'

result = nlp(lst_sequences, lst_series, hypothesis_template=hypothesis_template)



