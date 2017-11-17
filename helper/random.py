from random import Random
from typing import Optional

def gauss_limited(prng: Random,
                  mu: float, 
                  sigma: float, 
                  minR: Optional[float] = None, 
                  maxR: Optional[float] = None) -> float:
    if minR is None:
        minR = mu - 2 * sigma
    if maxR is None:
        maxR = mu + 2 * sigma

    while True:
        r = prng.gauss(mu, sigma)

        if r >= minR and r <= maxR:
            return r