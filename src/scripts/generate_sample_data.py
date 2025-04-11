import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Create data directory if it doesn't exist
os.makedirs('data/raw', exist_ok=True)

# Set random seed for reproducibility
np.random.seed(42)

# Generate providers data
def generate_providers(n=50):
    energy_types = ['wind', 'hydro', 'nuclear']
    providers = {
        'provider_id': range(1, n + 1),
        'provider_name': [f'Provider_{i}' for i in range(1, n + 1)],
        'energy_type': np.random.choice(energy_types, size=n),
        'capacity_mw': np.random.uniform(100, 1000, n).round(2),
        'region': np.random.choice(['North', 'South', 'East', 'West'], size=n),
        'active_since': pd.date_range(start='2020-01-01', periods=n, freq='D')
    }
    return pd.DataFrame(providers)

# Generate customers data
def generate_customers(n=200):
    id_types = ['DNI', 'RUC', 'CE']
    cities = ['Lima', 'Arequipa', 'Trujillo', 'Cusco', 'Piura']
    customers = {
        'customer_id': range(1, n + 1),
        'id_type': np.random.choice(id_types, size=n),
        'id_number': [f'{np.random.randint(10000000, 99999999)}' for _ in range(n)],
        'customer_name': [f'Customer_{i}' for i in range(1, n + 1)],
        'city': np.random.choice(cities, size=n),
        'customer_type': np.random.choice(['residential', 'commercial', 'industrial'], size=n),
        'registration_date': pd.date_range(start='2020-01-01', periods=n, freq='D')
    }
    return pd.DataFrame(customers)

# Generate transactions data
def generate_transactions(n=1000, providers_df=None, customers_df=None):
    transactions = {
        'transaction_id': range(1, n + 1),
        'transaction_date': pd.date_range(start='2023-01-01', periods=n, freq='H'),
        'transaction_type': np.random.choice(['buy', 'sell'], size=n),
        'entity_id': np.random.choice(range(1, 251), size=n),  # Combined providers and customers
        'quantity_kwh': np.random.uniform(100, 10000, n).round(2),
        'price_per_kwh': np.random.uniform(0.05, 0.15, n).round(4),
        'energy_type': np.random.choice(['wind', 'hydro', 'nuclear'], size=n),
        'status': np.random.choice(['completed', 'pending', 'cancelled'], size=n, p=[0.8, 0.15, 0.05])
    }
    
    df = pd.DataFrame(transactions)
    df['total_amount'] = df['quantity_kwh'] * df['price_per_kwh']
    return df

# Generate the data
providers_df = generate_providers()
customers_df = generate_customers()
transactions_df = generate_transactions()

# Save to CSV files with proper timestamps
timestamp = datetime.now().strftime('%Y%m%d')

providers_df.to_csv(f'data/raw/providers_{timestamp}.csv', index=False)
customers_df.to_csv(f'data/raw/customers_{timestamp}.csv', index=False)
transactions_df.to_csv(f'data/raw/transactions_{timestamp}.csv', index=False)

print("Sample data files generated successfully in data/raw/ directory") 