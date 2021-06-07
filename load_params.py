import yaml

def getParams():
    with open("params.yaml", "rb") as f:
        conf = yaml.load(f.read(), Loader= yaml.FullLoader)
    return conf
