# Dataset Information

This directory should contain the following datasets:

1. **UNHCR Refugee Statistics** (`United_Nations_Refugee_Data.csv`)
   - Source: UNHCR Refugee Data Finder
   - URL: https://www.kaggle.com/datasets/unitednations/refugee-data
   - Required columns:
     - Year
     - Origin
     - Host_Country
     - Total_Refugees
     - GDP_Host
     - Population_Host
     - Conflict_Intensity

2. **World Bank Migration** (`pop_and_net_migration.csv`)
   - Source: World Bank
   - URL: https://www.kaggle.com/datasets/muhammadaammartufail/population-and-net-migration-dataset-world-bank
   - Required columns:
     - Country: Name of the country.
     - Year: Year of the recorded data.
     - Total Population: The total population of the country.
     - Net Migration: Net migration balance (positive for immigration surplus, negative for emigration surplus).

*Note : This dataset provides a comprehensive look at population and migration trends in five South Asian countries: Afghanistan, Bangladesh, India, Pakistan, and Sri Lanka, covering the years 1960 to 2023. The data is sourced directly from the World Bank API and contains detailed statistics on total population and net migration for each year.*

3. **Global Slavery Index** (`global_slavery_index.csv`)
   - Source: Walk Free Foundation
   - URL: https://www.kaggle.com/datasets/patricklford/modern-slavery?select=Global_Slavery_Index_2023.csv
   - Required columns:
     - Population
     - Country
     - Estimated prevalence of modern slavery per 1,000 population
     - Estimated number of people in modern slavery
     - Region

Please download these datasets and place them in this directory before running the analysis. 