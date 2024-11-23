import pandas as pd
from typing import Optional
import csv


def clean_data(severity_csv: csv, export_csv:bool=False, export_name: Optional[str]=None) -> pd.DataFrame:
    """
    Reads csv file and sorts vulnerabilities by their severity -> prioritizes vulnerabilities
    
    :param csv severity_csv: csv file containing vulnerability analysis of a web
    :param bool export_csv: determines if the file will get exported or just saved locally
    :return pd.Dataframe: Dataframe containing cleaned and sorted data
    """
    
    # Variable initialization
    sort_vals = {
        "critical":4,
        "high":3,
        "medium":2,
        "low":1,
        "unknown":0
        }
    df = pd.read_csv(severity_csv)
    
    # Sorting data based on severity
    df['Severity'] = pd.Categorical(
        df['Severity'],
        categories=sort_vals.keys(),
        ordered=True
        )
    df.sort_values(
        'Severity',
        ascending=True,
        inplace=True,
        kind='stable'
        )
    
    # Exporting to csv
    if export_csv:
        df.to_csv(f'{export_name}.csv', sep=',',index=False, encoding= 'utf-8')
        
    return df

