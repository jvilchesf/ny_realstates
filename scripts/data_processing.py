"""
NYC Real Estate Data Processing Script
This script downloads, cleans, and processes NYC DOB Job Application Filings data.
"""

import os
import pandas as pd
import polars as pl
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
import requests
from datetime import datetime

# Configuration
DATA_DIR = Path("data")
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
OUTPUT_DIR = Path("output")

# Create directories if they don't exist
for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR, OUTPUT_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Dataset configuration
DATASET_URL = (
    "https://data.cityofnewyork.us/api/views/ic3t-wcy2/rows.csv?accessType=DOWNLOAD"
)
RAW_DATA_FILE = (
    RAW_DATA_DIR
    / f"DOB_Job_Application_Filings_{datetime.now().strftime('%Y%m%d')}.csv"
)
PROCESSED_DATA_FILE = PROCESSED_DATA_DIR / "job_application_filings_output.csv"


def download_data(url: str, output_path: Path) -> None:
    """
    Download the NYC DOB dataset from the Open Data portal.

    Args:
        url: URL to download the dataset from
        output_path: Path where the file will be saved
    """
    print(f"Downloading data from NYC Open Data Portal...")
    print(f"This may take several minutes due to the large file size...")

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get("content-length", 0))
        block_size = 8192
        downloaded = 0

        with open(output_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=block_size):
                if chunk:
                    file.write(chunk)
                    downloaded += len(chunk)
                    if total_size:
                        percent = (downloaded / total_size) * 100
                        print(f"\rProgress: {percent:.1f}%", end="")

        print(f"\n✓ Data downloaded successfully to {output_path}")
    except Exception as e:
        print(f"✗ Error downloading data: {e}")
        raise


def load_data(file_path: Path) -> pl.DataFrame:
    """
    Load the raw CSV data using Polars with proper schema overrides.

    Args:
        file_path: Path to the CSV file

    Returns:
        Polars DataFrame with loaded data
    """
    print(f"Loading data from {file_path}...")

    # Specify schema overrides for problematic columns
    schema_overrides = {"Applicant License #": pl.Utf8}

    try:
        df = pl.read_csv(
            str(file_path),
            schema_overrides=schema_overrides,
            ignore_errors=True,
            null_values=["H65055"],
        )
        print(
            f"✓ Data loaded successfully: {df.shape[0]:,} rows, {df.shape[1]} columns"
        )
        return df
    except Exception as e:
        print(f"✗ Error loading data: {e}")
        raise


def process_data(df: pl.DataFrame) -> pd.DataFrame:
    """
    Process and clean the data, filtering for 2023-2024 approvals.

    Args:
        df: Raw Polars DataFrame

    Returns:
        Processed pandas DataFrame
    """
    print("Processing data...")

    # Convert to pandas for compatibility
    df_pandas = df.to_pandas()

    # Convert 'Approved' column to datetime
    df_pandas["Date_Approved"] = pd.to_datetime(
        df_pandas["Approved"], format="%d/%m/%Y", errors="coerce"
    )

    # Filter for 2023 and 2024
    df_filtered = df_pandas[df_pandas["Date_Approved"].dt.year.isin([2023, 2024])]

    if df_filtered.empty:
        print("⚠ Warning: No data found for years 2023-2024. Check date format.")
        return pd.DataFrame()

    print(f"✓ Filtered data: {len(df_filtered):,} records from 2023-2024")

    # Group and aggregate
    grouped_df = (
        df_filtered.groupby(
            [
                "Borough",
                "Job Type",
                "Job Status",
                "Approved",
                "Job #",
                "Building Type",
                "Pre- Filing Date",
                "BUILDING_CLASS",
                "Job Description",
                "Date_Approved",
                "Fully Paid",
            ]
        )
        .agg(
            {
                "GIS_LATITUDE": "mean",
                "GIS_LONGITUDE": "mean",
                "Initial Cost": "sum",
            }
        )
        .reset_index()
    )

    print(f"✓ Data aggregated: {len(grouped_df):,} unique records")

    return grouped_df


def create_visualizations(df_filtered: pd.DataFrame) -> None:
    """
    Create visualization of job types over time.

    Args:
        df_filtered: Filtered pandas DataFrame
    """
    print("Creating visualizations...")

    columns_of_interest = [
        "Plumbing",
        "Mechanical",
        "Boiler",
        "Fuel Burning",
        "Fuel Storage",
        "Standpipe",
        "Sprinkler",
        "Fire Alarm",
        "Equipment",
        "Fire Suppression",
        "Curb Cut",
        "Other",
    ]

    # Melt the DataFrame to long format
    df_long = df_filtered.melt(
        id_vars=["Date_Approved"],
        value_vars=columns_of_interest,
        var_name="Job_Type",
        value_name="Count",
    )

    # Convert 'X' to 1, everything else to 0
    df_long["Count"] = df_long["Count"].apply(lambda x: 1 if x == "X" else 0)

    # Drop rows with NaN values
    df_long = df_long.dropna(subset=["Count"])

    # Group by month and job type
    df_long["Month_Approved"] = df_long["Date_Approved"].dt.to_period("M")
    monthly_counts = (
        df_long.groupby(["Month_Approved", "Job_Type"])["Count"]
        .sum()
        .unstack(fill_value=0)
    )

    # Create the plot
    fig, ax = plt.subplots(figsize=(14, 8))
    monthly_counts.plot(kind="bar", stacked=True, ax=ax)
    ax.set_title("Quantity of Jobs per Month by Type", fontsize=16, fontweight="bold")
    ax.set_xlabel("Month Approved", fontsize=12)
    ax.set_ylabel("Number of Jobs", fontsize=12)
    ax.legend(title="Job Type", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()

    # Save the plot
    plot_path = OUTPUT_DIR / "jobs_by_month_type.png"
    plt.savefig(plot_path, dpi=300, bbox_inches="tight")
    print(f"✓ Visualization saved to {plot_path}")
    plt.close()


def save_processed_data(df: pd.DataFrame, output_path: Path) -> None:
    """
    Save the processed DataFrame to CSV.

    Args:
        df: Processed pandas DataFrame
        output_path: Path where the CSV will be saved
    """
    print(f"Saving processed data to {output_path}...")
    df.to_csv(output_path, index=False)
    print(f"✓ Processed data saved: {len(df):,} records")


def main():
    """
    Main execution function.
    """
    print("=" * 70)
    print("NYC Real Estate Trends - Data Processing Pipeline")
    print("=" * 70)

    try:
        # Step 1: Download data (skip if file already exists)
        if not RAW_DATA_FILE.exists():
            download_data(DATASET_URL, RAW_DATA_FILE)
        else:
            print(f"✓ Raw data file already exists: {RAW_DATA_FILE}")

        # Step 2: Load data
        df_raw = load_data(RAW_DATA_FILE)

        # Step 3: Process data
        df_processed = process_data(df_raw)

        if df_processed.empty:
            print("✗ No data to process. Exiting.")
            return

        # Step 4: Save processed data
        save_processed_data(df_processed, PROCESSED_DATA_FILE)

        # Step 5: Create visualizations
        # Need to reload the filtered data for visualization
        df_pandas = df_raw.to_pandas()
        df_pandas["Date_Approved"] = pd.to_datetime(
            df_pandas["Approved"], format="%d/%m/%Y", errors="coerce"
        )
        df_filtered = df_pandas[df_pandas["Date_Approved"].dt.year.isin([2023, 2024])]
        create_visualizations(df_filtered)

        print("\n" + "=" * 70)
        print("✓ Pipeline completed successfully!")
        print("=" * 70)
        print(f"\nOutput files:")
        print(f"  - Processed data: {PROCESSED_DATA_FILE}")
        print(f"  - Visualization: {OUTPUT_DIR / 'jobs_by_month_type.png'}")

    except Exception as e:
        print(f"\n✗ Pipeline failed with error: {e}")
        raise


if __name__ == "__main__":
    main()
