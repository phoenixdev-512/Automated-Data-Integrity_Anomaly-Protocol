"""
SENTINEL: Automated Data Integrity Protocol
============================================
Financial reconciliation engine for detecting payment discrepancies.

Core Functions:
- Missing Payment Detection (Left Join Analysis)
- Revenue Variance Identification (Amount Mismatch)
- Forensic Audit Report Generation

Author: Data Engineering Team
Target: WeWork BI Intern Portfolio
"""

import pandas as pd
import logging
import os
from datetime import datetime


# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

def setup_logger():
    """
    Configures enterprise-grade logging system.
    Format: Timestamp | Module | Severity | Message
    """
    log_format = '%(asctime)s | [SENTINEL-CORE] | %(levelname)s | %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(log_format, date_format))
    
    # Root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(console_handler)
    
    return logger


# ============================================================================
# DATA INGESTION MODULE
# ============================================================================

def load_datasets():
    """
    Loads sales and bank datasets into memory.
    Returns: (sales_df, bank_df) or (None, None) on failure
    """
    logger = logging.getLogger()
    
    try:
        base_path = os.path.join(os.path.dirname(__file__), '..')
        sales_path = os.path.join(base_path, 'data', 'sales_log.csv')
        bank_path = os.path.join(base_path, 'data', 'bank_feed.csv')
        
        logger.info("Initiating data ingestion protocol...")
        
        sales_df = pd.read_csv(sales_path)
        logger.info(f"✓ Sales Log: {len(sales_df)} records loaded")
        
        bank_df = pd.read_csv(bank_path)
        logger.info(f"✓ Bank Feed: {len(bank_df)} records loaded")
        
        return sales_df, bank_df
    
    except FileNotFoundError as e:
        logger.critical(f"Data source unavailable: {e}")
        logger.critical("Execute generate_mock_data.py first")
        return None, None
    
    except Exception as e:
        logger.critical(f"Ingestion failure: {e}")
        return None, None


# ============================================================================
# RECONCILIATION ENGINE
# ============================================================================

def detect_anomalies(sales_df, bank_df):
    """
    Performs left join to identify:
    1. Missing Payments (txn_id in Sales but not in Bank)
    2. Revenue Variance (billed_amount != received_amount)
    
    Returns: (missing_payments, variance_records)
    """
    logger = logging.getLogger()
    logger.info("Executing reconciliation algorithm...")
    
    # Left join: Keep all sales records
    merged = pd.merge(
        sales_df,
        bank_df,
        on='txn_id',
        how='left',
        suffixes=('_sales', '_bank')
    )
    
    # DETECTION 1: Missing Payments
    missing_payments = merged[merged['bank_ref'].isna()].copy()
    
    if not missing_payments.empty:
        logger.critical(f"⚠ ALERT: {len(missing_payments)} MISSING PAYMENT(S) DETECTED")
        for _, row in missing_payments.iterrows():
            logger.critical(
                f"   → {row['txn_id']} | Client: {row['client']} | "
                f"Billed: ${row['billed_amount']:,.2f} | STATUS: UNPAID"
            )
    else:
        logger.info("✓ No missing payments detected")
    
    # DETECTION 2: Revenue Variance
    matched_records = merged[merged['bank_ref'].notna()].copy()
    matched_records['variance'] = matched_records['billed_amount'] - matched_records['received_amount']
    variance_records = matched_records[matched_records['variance'] != 0].copy()
    
    if not variance_records.empty:
        logger.warning(f"⚠ ALERT: {len(variance_records)} AMOUNT VARIANCE(S) DETECTED")
        for _, row in variance_records.iterrows():
            variance = row['variance']
            logger.warning(
                f"   → {row['txn_id']} | Billed: ${row['billed_amount']:,.2f} | "
                f"Received: ${row['received_amount']:,.2f} | VARIANCE: ${variance:+,.2f}"
            )
    else:
        logger.info("✓ No amount variances detected")
    
    # DETECTION 3: Perfect Matches (Control Validation)
    perfect_matches = matched_records[matched_records['variance'] == 0]
    logger.info(f"✓ {len(perfect_matches)} transaction(s) reconciled successfully")
    
    return missing_payments, variance_records


# ============================================================================
# FORENSIC REPORT GENERATOR
# ============================================================================

def generate_forensic_report(sales_df, missing_payments, variance_records):
    """
    Writes detailed audit findings to a system log file.
    Output: audit_reports/FORENSIC_REPORT.txt
    """
    logger = logging.getLogger()
    
    report_dir = os.path.join(os.path.dirname(__file__), '..', 'audit_reports')
    os.makedirs(report_dir, exist_ok=True)
    
    report_path = os.path.join(report_dir, 'FORENSIC_REPORT.txt')
    
    with open(report_path, 'w') as f:
        # Header
        f.write("="*80 + "\n")
        f.write("SENTINEL FORENSIC AUDIT REPORT\n")
        f.write("Automated Data Integrity Protocol - Version 1.0\n")
        f.write("="*80 + "\n")
        f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Transactions Analyzed: {len(sales_df)}\n")
        f.write("="*80 + "\n\n")
        
        # Section 1: Missing Payments
        f.write("[CRITICAL FINDINGS] - MISSING PAYMENTS\n")
        f.write("-"*80 + "\n")
        if not missing_payments.empty:
            f.write(f"Status: {len(missing_payments)} UNPAID TRANSACTION(S) IDENTIFIED\n\n")
            for _, row in missing_payments.iterrows():
                f.write(f"Transaction ID: {row['txn_id']}\n")
                f.write(f"Client: {row['client']}\n")
                f.write(f"Billed Amount: ${row['billed_amount']:,.2f}\n")
                f.write(f"Billing Date: {row['timestamp']}\n")
                f.write(f"Bank Confirmation: NOT FOUND\n")
                f.write(f"Risk Level: HIGH - Potential Revenue Loss\n")
                f.write("-"*80 + "\n")
        else:
            f.write("Status: ALL PAYMENTS ACCOUNTED FOR ✓\n")
            f.write("-"*80 + "\n")
        
        f.write("\n")
        
        # Section 2: Revenue Variance
        f.write("[WARNING FINDINGS] - AMOUNT DISCREPANCIES\n")
        f.write("-"*80 + "\n")
        if not variance_records.empty:
            f.write(f"Status: {len(variance_records)} VARIANCE(S) DETECTED\n\n")
            for _, row in variance_records.iterrows():
                variance = row['variance']
                f.write(f"Transaction ID: {row['txn_id']}\n")
                f.write(f"Client: {row['client']}\n")
                f.write(f"Billed Amount: ${row['billed_amount']:,.2f}\n")
                f.write(f"Received Amount: ${row['received_amount']:,.2f}\n")
                f.write(f"Variance: ${variance:+,.2f}\n")
                f.write(f"Risk Level: MEDIUM - Revenue Leakage\n")
                f.write("-"*80 + "\n")
        else:
            f.write("Status: NO AMOUNT DISCREPANCIES FOUND ✓\n")
            f.write("-"*80 + "\n")
        
        f.write("\n")
        
        # Section 3: Executive Summary
        f.write("[EXECUTIVE SUMMARY]\n")
        f.write("-"*80 + "\n")
        total_issues = len(missing_payments) + len(variance_records)
        f.write(f"Total Issues Identified: {total_issues}\n")
        f.write(f"  • Critical (Missing Payments): {len(missing_payments)}\n")
        f.write(f"  • Warnings (Variance): {len(variance_records)}\n")
        
        if not missing_payments.empty:
            total_unpaid = missing_payments['billed_amount'].sum()
            f.write(f"\nPotential Revenue at Risk: ${total_unpaid:,.2f}\n")
        
        if not variance_records.empty:
            total_leakage = variance_records['variance'].sum()
            f.write(f"Revenue Leakage Detected: ${total_leakage:+,.2f}\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("END OF REPORT\n")
        f.write("="*80 + "\n")
    
    logger.info(f"✓ Forensic report written: {report_path}")
    return report_path


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Primary execution pipeline.
    """
    logger = setup_logger()
    
    print("\n" + "="*80)
    print("SENTINEL: AUTOMATED DATA INTEGRITY PROTOCOL")
    print("="*80 + "\n")
    
    logger.info("System initialization complete")
    logger.info("Commencing financial reconciliation sequence...")
    
    # Step 1: Data Loading
    sales_df, bank_df = load_datasets()
    if sales_df is None or bank_df is None:
        logger.critical("ABORT: Cannot proceed without valid datasets")
        return
    
    # Step 2: Anomaly Detection
    logger.info("-" * 80)
    missing_payments, variance_records = detect_anomalies(sales_df, bank_df)
    
    # Step 3: Report Generation
    logger.info("-" * 80)
    logger.info("Generating forensic audit report...")
    report_path = generate_forensic_report(sales_df, missing_payments, variance_records)
    
    # Final Status
    logger.info("-" * 80)
    total_issues = len(missing_payments) + len(variance_records)
    
    if total_issues == 0:
        logger.info("✓ AUDIT COMPLETE: All transactions reconciled successfully")
    else:
        logger.warning(f"⚠ AUDIT COMPLETE: {total_issues} issue(s) require attention")
        logger.warning(f"Review report: {report_path}")
    
    print("\n" + "="*80)
    print("SENTINEL PROTOCOL TERMINATED")
    print("="*80 + "\n")


if __name__ == '__main__':
    main()
