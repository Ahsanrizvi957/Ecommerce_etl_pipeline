# E-commerce ETL Pipeline

An end-to-end ETL pipeline built using **Python, Pandas, SQLAlchemy, and PostgreSQL** to extract, clean, and load e-commerce data.

## Project Overview

The pipeline processes six raw CSV datasets, performs data cleaning and transformation using Pandas, and loads the processed data into PostgreSQL.

It also includes audit logging to track loading status, row counts, execution time, and errors.

## Tech Stack

- Python
- Pandas
- SQLAlchemy
- PostgreSQL

## How to Run

**1. Clone the repository**

```bash
git clone https://github.com/Ahsanrizvi957/Ecommerce_etl_pipeline.git
cd Ecommerce_etl_pipeline
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install pandas sqlalchemy psycopg2-binary python-dotenv
```

**4. Configure database connection**

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/database_name
```

Replace the credentials with your PostgreSQL details. Create the required database and `stagging` schema before running the pipeline.

**5. Run the pipeline**

```bash
python src/main.py
```

## Key Features

- Extracts data from six CSV files.
- Cleans and transforms data using Pandas.
- Loads processed data into PostgreSQL.
- Uses full-refresh loading strategy.
- Maintains ETL audit logs for monitoring execution.

