import pandas as pd
from pandas.testing import assert_frame_equal
from src.top_100_apps_details import TopHundredAppsRetriever

t100 = TopHundredAppsRetriever()
# test data reads from cache but without the calculated columns
input_data = pd.read_csv('data/cached_data.csv', usecols=range(44))
output = pd.read_csv('data/cached_data.csv')
test_output = t100._categorise_dataframe(input_data)


# All methods calling the external API are just wrappers around code that
# is already tested, so we just test the categorisation function with cache data
class TestAppsDetails:
    def test_categorise_dataframe_output_type(self):
        assert isinstance(test_output, pd.DataFrame)

    def test_categorise_dataframe_output_accurate(self):
        assert_frame_equal(output, test_output)
