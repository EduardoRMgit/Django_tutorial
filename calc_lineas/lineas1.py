#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import numpy as np
import sys

# Para medir el tiempo de ejecucion
t_start = pd.datetime.now()

# Importamos las lineas de unos txt y ponemos formato
data = pd.DataFrame()

lim_percs = np.array([0.1, 0.15])

for i in range(1, len(sys.argv)):
    arg = sys.argv[i]
    if ".txt" in arg or ".csv" in arg:
        datai = pd.read_csv(arg)
        data = pd.concat([data, datai]).fillna(0)
    elif "_" in arg:
        try:
            percs = np.array(arg.split("_")).astype(np.int)
        except Exception:
            raise "The percentages must be integers given like 10_15"

        lim_percs = [percs[0]/100., percs[1]/100.]
    else:
        date_p = arg

data.FECHA = pd.to_datetime(data.FECHA)
data.EXTERNAL_ID = data.EXTERNAL_ID.astype("category")

# Obtenemos fechas desde la cual se hacen los calculos
# El 2do parametro puede tomar los siguientes valores
# nada : Toma la fecha de hoy
# "max" : toma la fecha como el maximo mes en lineas_test
# "<mes>-<año>": Empezar en el mes año. con dos digitos para mes y
# los ultimos dos para año
if 'date_p' in locals():
    if date_p == "max":
        date_now = np.max(data.FECHA)
        date_now = date_now + pd.tseries.offsets.MonthBegin(1)
    else:
        date_now = pd.datetime(int(date_p[-2:])+2000, int(date_p[:2]), 1)
else:
    date_now = pd.datetime.now() + pd.tseries.offsets.MonthEnd(-1)

month_now = date_now.month
year_now = date_now.year
data["MES"] = data.FECHA.apply(lambda x: x.month)
data["ANO"] = data.FECHA.apply(lambda x: x.year)

months_hist = 12
months_min_hist = 10
print("Imported data")
# Se hace un agrupamiento multiindex por usuario y meses
# La verdad esta medio malo porque hace agrupaciones de meses que no existen
# por cubrir todo los meses que existen en todos los años
has_numero = 'NUMERO_MOVIL' in data
g_mes = data.groupby(["EXTERNAL_ID", "ANO", "MES"])

if has_numero:
    users = g_mes.agg(
            MONTO=pd.NamedAgg(column='MONTO', aggfunc=np.mean),
            MES_ANO=pd.NamedAgg(column='FECHA',
                                aggfunc=lambda x: pd.datetime(np.min(x).year,
                                                              np.min(x).month,
                                                              1)
                                ),
           NUMERO_MOVIL=pd.NamedAgg(column='NUMERO_MOVIL',
                                    aggfunc=lambda x: x.iloc[0]
                                    )
        )
else:
    users = g_mes.agg(
            MONTO=pd.NamedAgg(column='MONTO', aggfunc=np.mean),
            MES_ANO=pd.NamedAgg(column='FECHA',
                                aggfunc=lambda x: pd.datetime(np.min(x).year,
                                                              np.min(x).month,
                                                              1)
                                )
        )

print("Grouped data")
# Obtenemos los usuarios para iterar sobre ellos y hacemos el machote de la
# tabla que se regresa
multiind = users.index.to_frame()

user_names = users.index.get_level_values(level=0).astype("category").categories
users.to_csv("users.csv", index=True)

dtypes = np.dtype([
          ('Numero', int),
          ('Usuario', int),
          ])
datatypes = np.empty(0, dtype=dtypes)
user_stats = pd.DataFrame(datatypes)

# Para escribr un porcentaje
perc_size = np.size(user_names)
if(perc_size > 100):
    perc_step = perc_size // 20
    perc_adv = 5
    perc_mult = 20
else:
    perc_step = 1
    perc_adv = 100./perc_size
    perc_mult = 1
print("0%")

for i in range(0, perc_size):

    if((i) % perc_step == 0):
        print(int(perc_adv*((i+1)//perc_step)), "%")

    user = user_names[i]
    user_loc = users.loc[user]

    # Ver si el mes anterior hubo depositos
    year_temp = year_now - 1 if month_now == 1 else year_now
    month_temp = 12 if month_now == 1 else month_now - 1
    prev_month = user_loc[user_loc.MES_ANO == pd.datetime(year_temp,
                                                          month_temp, 1)]

    ult_mes = False
    if((np.size(prev_month) != 0)):
        if((not np.isnan(prev_month.MONTO[0])) and prev_month.MONTO[0] != 0):
            ult_mes = True

    # Ver si months_min_hist de months_hist anteriores tiene depositos
    mod_months = (month_now-months_hist) % 12
    focus_date = date_now + pd.tseries.offsets.MonthEnd(-13)
    last_months = user_loc[user_loc.MES_ANO >= focus_date]

    # Gather the months in which it is active, meaning that it is not nan or 0
    m_inds = np.logical_not(np.isnan(last_months.MONTO.values))
    m_inds2 = last_months.MONTO.values > 0
    m_inds3 = np.logical_and(m_inds, m_inds2)

    active_months_num = np.sum(m_inds3)

    n_meses = False
    if(active_months_num >= months_min_hist):
        n_meses = True
    # Si no cumple las dos anteriores no se le da credito
    user_stats.loc[i, 'n_meses'] = n_meses
    user_stats.loc[i, 'ult_mes'] = ult_mes
    if((n_meses & ult_mes)):
        user_stats.loc[i, 'Credito_Aceptado'] = True
    else:
        user_stats.loc[i, 'Credito_Aceptado'] = False

    # Añadimos al usuario
    user_stats.loc[i, 'Usuario'] = user
    # Poner el NUMERO_MOVIL
    if has_numero:
        movil_inds = np.logical_not(np.isnan(user_loc.NUMERO_MOVIL.values))
        user_stats.loc[i, 'Numero'] = int(user_loc.NUMERO_MOVIL[movil_inds][0])

    # El promedio contando los 0
    miss0 = 12 - len(last_months.MONTO.values)
    montos_0 = np.concatenate((last_months.MONTO.values, np.zeros(miss0)))
    prom = np.mean(montos_0)
    # prom = np.mean(last_months.MONTO.values)

    user_stats.loc[i, 'Promedio'] = int(np.round(prom))
    user_stats.loc[i, 'Pro*0.2'] = int(np.round(prom*0.2))
    user_stats.loc[i, 'Prom*0.2_Redondo'] = int(np.round(prom*0.2,
                                                         decimals=-2))
    # Maximo y minimo
    user_stats.loc[i, 'Max'] = round(np.max(montos_0))
    user_stats.loc[i, 'Min'] = round(np.min(montos_0))

    # Stdev ddof es para que la saque como excel, que divide entre n
    # no entre n-1
    std = np.std(montos_0, ddof=1)
    user_stats.loc[i, 'StDev'] = round(std)

    # Es lim_perc[0]% o perc[1]% default 10 o 15%
    var_string = "es" + str(int(lim_percs[0]*100)) + "%" + "no"\
                 + str(int(lim_percs[1]*100)) + "%"
    if std >= prom/2:
        lim_cred = int(np.ceil(prom*lim_percs[0]))
        user_stats.loc[i, var_string] = True
    else:
        user_stats.loc[i, var_string] = False
        lim_cred = int(np.ceil(prom*lim_percs[1]))

    lim_cred = np.round(lim_cred/50)*50
    user_stats.loc[i, 'Limite_Cred'] = lim_cred

if has_numero:
    user_stats.Numero = user_stats.Numero.astype(int)

user_stats.Usuario = user_stats.Usuario.astype(int)

# Columnas de promedio mensual
date_now = pd.Timestamp.fromtimestamp(date_now.timestamp())
min_date = np.min(data.FECHA)
max_date = np.max(data.FECHA)
months = (date_now.to_period('M') - min_date.to_period('M')).n

for i in range(0, months+1):
    if i == 0:
        date = min_date
    else:
        date = min_date + pd.tseries.offsets.MonthBegin(i)

    date_str = str(date.month) + "-" + str(date.year)[2:]
    inds = (multiind.MES == date.month) & (multiind.ANO == date.year)

    if len(users[inds].MONTO.values) == 0:
        user_stats[date_str] = np.nan
    else:
        user_stats[date_str] = np.round(users[inds].MONTO.values)

user_stats
user_stats.to_csv("detalle.csv", index=False)

#
# El archivo de multiplos de 50
#
user_local = user_stats.loc[user_stats.Credito_Aceptado.values, :]
montos = np.unique(user_local.Limite_Cred)
df_multiplos = pd.DataFrame({'Cantidad': 0, 'Monto': montos, 'Importe': 0})

for i in range(0, np.size(montos)):
    # El numero de veces que aparece el multiplo de 50

    tamano = np.size(user_local.Limite_Cred[user_local.Limite_Cred == montos[i]])
    df_multiplos.iloc[i, 0] = tamano

    # El importe total
    df_multiplos.iloc[i, 2] = tamano*montos[i]


df_multiplos.loc[perc_size, :] = [np.sum(df_multiplos.iloc[:, 0]),
                                  np.sum(df_multiplos.iloc[:, 1]),
                                  np.sum(df_multiplos.iloc[:, 2])]


df_multiplos['Usrs_verificados'] = np.nan
df_multiplos.iloc[0, 3] = np.size(user_names)

info_tot = (np.repeat(str("          "), df_multiplos.shape[0]))
info_tot[-1] = "Total: "
info_tot
df_multiplos.insert(0, ' ', info_tot)
df_multiplos.to_csv("multiplos.csv", index=False)

#
# Los límites de credito resumidos
#
user_lc = user_local.iloc[:, [1, 10]]
user_lc.to_csv("limite_cred.csv", index=False)

print("# de users: ", perc_size)

t_fin = pd.datetime.now()
t_diff = t_fin - t_start
print("Tiempo de ejecucion")
print(t_diff)
