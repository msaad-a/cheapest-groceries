
import pandas as pd

nofrills = pd.read_csv("nofrills_product_prices.csv")
nofrills['store'] = ['nofrills'] * nofrills.shape[0]

metro = pd.read_csv("metro_product_prices.csv")
metro['store'] = ['metro'] * metro.shape[0]

longos = pd.read_csv("longos_product_prices.csv")
longos['store'] = ['longos'] * longos.shape[0]


all_stores = pd.concat([nofrills, metro, longos], ignore_index=True)
all_stores['product'] = all_stores['product'].apply(lambda x: x.replace('"', ''))
all_stores.to_csv('all_product_prices.csv')