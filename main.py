# TODO
import pandas as pd
from thefuzz import fuzz
from thefuzz import process

df = pd.read_csv('all_product_prices.csv')
df = df.drop_duplicates()
product_names = df['product']

#print(product_names.head())
prod_list = product_names.to_list()

#print(type(product_names))

search_term = input("What product do you want to buy?\n")
#search_term = search.lower()

matches = process.extract(search_term, prod_list, limit = 200, scorer = fuzz.partial_token_sort_ratio)

search_results = []
for match in matches:
    if match[1] >= 80:
        search_results.append(match[0])

prod_results = []
for prod in search_results:
    prod_info = df.loc[df['product'] == prod]
    product = prod_info['product'].to_list()
    price = prod_info['price'].to_list()
    store = prod_info['store'].to_list()
    prod_tuple = (product[0], price[0], store[0])
    prod_results.append(prod_tuple)

#print(prod_results)
def merge_sort(lst):
    if len(lst) == 1:
        return lst
    elif len(lst) == 2:
        if lst[0][1] > lst[1][1]:
            lst[0], lst[1] = lst[1], lst[0]
        return lst
    
    left = lst[:len(lst)//2]
    right = lst[len(lst)//2:]

    merge_sort(left)
    merge_sort(right)

    lst = merge(lst, left, right)

    return lst

def merge(arr, left, right):
    i = 0
    j = 0
    k = 0
    while i < len(arr):
        if j >= len(left):
            arr[i] = right[k]
            k += 1
        elif k >= len(right):
            arr[i] = left[j]
            j+=1
        elif left[j][1] > right[k][1]:
            arr[i] = right[k]
            k += 1
        elif left[j][1] <= right[k][1]:
            arr[i] = left[j]
            j += 1 
        i += 1
    return arr
sorted = merge_sort(prod_results)

print("\nHere are the cheapest items matching your search:\n")

i = 1
for prod in sorted[:20]:
    print(f'{i}. {prod[0]} priced at ${prod[1]}, from {prod[2]}.')
    i+=1
