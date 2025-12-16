"""
Sentinel Mock Data Generator
=============================
Generates synthetic financial datasets with intentional anomalies for QA testing.

Author: Data Engineering Team
Purpose: Portfolio Demonstration - Automated Data Integrity Protocol
"""

import csv
import os
from datetime import datetime, timedelta


def generate_sales_log():
    """
    Creates sales_log.csv with internal billing records.
    Includes TXN-1005 (missing payment scenario).
    """
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    sales_records = [
        ['txn_id', 'client', 'billed_amount', 'timestamp'],
        ['TXN-1001', 'Acme Corp', 12000, '2025-12-01 09:15:00'],
        ['TXN-1002', 'GlobalTech Inc', 8500, '2025-12-02 11:30:00'],
        ['TXN-1003', 'Beta Industries', 5000, '2025-12-03 14:20:00'],  # ANOMALY: Variance
        ['TXN-1004', 'Omega Solutions', 15000, '2025-12-04 10:45:00'],
        ['TXN-1005', 'Phantom LLC', 7200, '2025-12-05 16:00:00'],  # ANOMALY: Missing in Bank
        ['TXN-1006', 'Delta Enterprises', 9800, '2025-12-06 13:10:00'],
        ['TXN-1007', 'Epsilon Group', 11500, '2025-12-07 08:50:00'],
        ['TXN-1008', 'Control Co', 6000, '2025-12-08 15:30:00'],  # CONTROL: Perfect Match
        ['TXN-1009', 'Zenith Partners', 13200, '2025-12-09 12:00:00'],
        ['TXN-1010', 'Vortex Systems', 10500, '2025-12-10 17:20:00']
    ]
    
    filepath = os.path.join(data_dir, 'sales_log.csv')
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(sales_records)
    
    print(f"✓ Generated: {filepath}")
    return filepath


def generate_bank_feed():
    """
    Creates bank_feed.csv with external payment confirmations.
    Excludes TXN-1005 and introduces variance in TXN-1003.
    """
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    bank_records = [
        ['txn_id', 'bank_ref', 'received_amount', 'settled_date'],
        ['TXN-1001', 'BNK-REF-A001', 12000, '2025-12-01'],
        ['TXN-1002', 'BNK-REF-A002', 8500, '2025-12-02'],
        ['TXN-1003', 'BNK-REF-A003', 4500, '2025-12-03'],  # ANOMALY: $500 short
        ['TXN-1004', 'BNK-REF-A004', 15000, '2025-12-04'],
        # TXN-1005 MISSING HERE - Simulates unpaid invoice
        ['TXN-1006', 'BNK-REF-A006', 9800, '2025-12-06'],
        ['TXN-1007', 'BNK-REF-A007', 11500, '2025-12-07'],
        ['TXN-1008', 'BNK-REF-A008', 6000, '2025-12-08'],  # CONTROL: Perfect
        ['TXN-1009', 'BNK-REF-A009', 13200, '2025-12-09'],
        ['TXN-1010', 'BNK-REF-A010', 10500, '2025-12-10']
    ]
    
    filepath = os.path.join(data_dir, 'bank_feed.csv')
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(bank_records)
    
    print(f"✓ Generated: {filepath}")
    return filepath


if __name__ == '__main__':
    print("\n" + "="*60)
    print("SENTINEL DATA GENERATOR | Initializing Mock Datasets")
    print("="*60 + "\n")
    
    sales_path = generate_sales_log()
    bank_path = generate_bank_feed()
    
    print("\n" + "-"*60)
    print("ANOMALY INJECTION SUMMARY:")
    print("-"*60)
    print("• TXN-1005: Missing Payment (Sales exists, Bank missing)")
    print("• TXN-1003: Revenue Leakage ($5000 billed → $4500 received)")
    print("• TXN-1008: Control Group (Perfect match)")
    print("-"*60)
    print("\n✓ Mock data generation complete. Ready for Sentinel analysis.\n")
