def annualize_returns(r, periods_per_year=12):
	compounded_growth = (1+r).prod()
	n_periods = r.shape[0]
	return compounded_growth**(periods_per_year / n_periods) - 1