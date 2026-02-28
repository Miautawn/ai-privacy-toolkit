import pandas as pd


def calculate_disclosure_risk(generalized_data: pd.DataFrame) -> float:
    """Calculates the identity disclosure risk of the generalized dataset.
    Based on the metric from Xu et al. (2007): sum(1 / freq(r)) over all records.

    The "disclosure risk" defined in the original paper calculates
    how unique each record is on average and hence, how easy is it to disclose an individual.

    It is rather similar to k-similarity or anonimity-set in the purpose.

    Arguments:
        generalized_data (pd.DataFrame): The generalized dataset for which to calculate the disclosure risk.

    Returns:
        float: disclosure risk score.
        The lower it is (0), the more abstract and similar each datapoints are to each other.
        If it's high (1), then each datapoint is completely unique
    """

    if generalized_data.empty:
        return 0.0

    # Group by all columns to find the frequency of each exact record combination
    # dropna=False ensures we don't accidentally drop rows with missing/generalized values
    unique_combinations = generalized_data.groupby(
        generalized_data.columns.tolist(), dropna=False
    ).size()

    # The sum of 1/freq(r) for all records mathematically simplifies to the number of unique records.
    total_records = len(generalized_data)
    risk = len(unique_combinations) / total_records

    return risk
