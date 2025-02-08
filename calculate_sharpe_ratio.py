def calculate_sharpe_ratios(data):
    for fund in data:
        # Assuming the API provides 'returns' and 'risk_free_rate' for each fund
        returns = fund['returns']
        risk_free_rate = fund['risk_free_rate']
        standard_deviation = fund['standard_deviation']

        # Calculate the Sharpe ratio
        sharpe_ratio = (returns - risk_free_rate) / standard_deviation
        fund['sharpe_ratio'] = sharpe_ratio

    return data
