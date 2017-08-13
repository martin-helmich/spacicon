def gauss_limited(prng, mu, sigma, minR=None, maxR=None):
    if minR is None:
        minR = mu - 2 * sigma
    if maxR is None:
        maxR = mu + 2 * sigma

    while True:
        r = prng.gauss(mu, sigma)

        if r >= minR and r <= maxR:
            return r