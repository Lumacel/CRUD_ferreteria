import json

with open(r"registro_ventas\\ventas.json", "r+", encoding='utf-8-sig') as file:
        data = json.load(file)
        for i, elemento in enumerate(data):
            if int(elemento["numeracion"])== 2:
                data[i]["estado"]= False if data[i]["estado"] else True
                print(elemento)
                break

