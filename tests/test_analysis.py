import pandas as pd
from tradeassistant.analysis import Analysis


def test_analysis_compute():
    df = pd.DataFrame({
        'close': [1,2,3,4,5,6,7,8,9,10],
        'high': [1,2,3,4,5,6,7,8,9,10],
        'low': [0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5],
    })
    result = Analysis('AAPL', df).compute()
    assert 'signal' in result
    assert result['symbol'] == 'AAPL'
