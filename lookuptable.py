import requests

# make a GET request to the API
response = requests.get("http://localhost:5000/products")
data = response.json()

# Extract the product names from the response
product_names = list(data.keys())

yml_output = f'version: "3.1"\n' \
             f'nlu:\n' \
             f'  - lookup: product\n' \
             f'    examples: |\n'

for product in product_names:
    yml_output += f'      - {product}\n'

# Write output to file
with open('data/productlookup.yml', 'w') as f:
    f.write(yml_output)

# yml_dict = {
#     'version': '3.1',
#     'nlu': {
#         'lookup': 'product',
#         'examples':     [f'{p}' for p in product_names]
#     }
# }

# # Dump YAML data to file
# with open('data/productlookup.yml', 'w') as f:
#     yaml.dump(yml_dict, f, sort_keys=False)

# Construct the YAML data structure
# yaml_data = {
#     "version": "3.1",
#     "nlu": [
#         {
#             "lookup": "product",
#             "examples": "- " + "\n- ".join(product_names)
#         }
#     ]
# }

# # dump the YAML data to a file
# with open("data/productlookup.yml", "w") as f:
#     yaml.dump(yaml_data, f)
