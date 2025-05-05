# risk/position_sizer.py

def calculate_position_size(capital, confidence, volatility):
    """
    Smart dynamic position sizing:
    - High confidence = larger size
    - Low volatility = larger size
    - If volatility high, reduce size
    """
    base_size = capital * 0.02  # 2% of account per trade (default risk)

    # Boost for high confidence
    if confidence > 0.6:
        base_size *= 1.5
    elif confidence < 0.3:
        base_size *= 0.5

    # Adjust for volatility
    if volatility > 0.5:
        base_size *= 0.7
    elif volatility < 0.2:
        base_size *= 1.2

    # Never exceed 5% of total capital
    max_risk_size = capital * 0.05
    final_size = min(base_size, max_risk_size)

    return round(final_size, 2)
