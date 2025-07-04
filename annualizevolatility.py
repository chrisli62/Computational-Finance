def annualize_volatility(r, periods_per_year=12):
	return r.std() * (periods_per_year**0.5)