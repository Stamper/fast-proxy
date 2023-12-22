import yaml

import config


def build_pools_set():
    pools = {}
    with open(config.BASE_ROOT / "pools.yaml", "r") as f:
        pool_config = yaml.safe_load(f)
        for k, v in pool_config.items():
            pools[k] = []
            for h in v:
                pools[k] += [(h["scheme"], h["host"], h["port"])] * h["weight"]
    return pools
