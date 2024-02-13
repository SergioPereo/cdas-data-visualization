import pandas as pd
import datetime as date

format_months = {'Enero': 1, 'Febrero': 2, 'Marzo': 3,'Abril': 4, 'Mayo': 5, 'Junio': 6, 'Julio': 7, 'Agosto': 8, 'Septiembre': 9, 'Octubre': 10, 'Noviembre': 11,'Diciembre': 12}
df = pd.read_excel("db_periodistas_asesinados.xlsx")
df['Fecha'] = df['Fecha'].apply(lambda x: date.datetime(int(x.split(" ")[4]), int(format_months[x.split(" ")[2]]), int(x.split(" ")[0])))

print(df)
print(df, df.dtypes,df[df['Fecha']>date.datetime(2014,2,10)])