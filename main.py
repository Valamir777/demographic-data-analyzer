import pandas as pd
# This entrypoint file to be used in development. Start by reading README.md
import demographic_data_analyzer
from unittest import main

# Test your function by calling it here
print(demographic_data_analyzer.bachelorsEducation_percent(pd.read_csv('adult.data.csv')))

# Run unit tests automatically
#main(module='test_module', exit=False)
