# sentiment/coinglass.py

import random

def get_coinglass_data():
    # Simulated liquidation data for now
    sample_data = {
        "BTCUSDT": {
            "long_short_ratio": random.uniform(0.7, 1.5)
        },
        "ETHUSDT": {
            "long_short_ratio": random.uniform(0.7, 1.5)
        },
        "XRPUSDT": {
            "long_short_ratio": random.uniform(0.7, 1.5)
        }
    }
    return sample_data
