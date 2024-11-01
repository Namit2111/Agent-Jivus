import json
def load_data_from_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data


if __name__ == "__main__":
    print(load_data_from_json(file_path="./data/productDetails.json"))
    