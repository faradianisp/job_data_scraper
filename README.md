## Data Pipeline & ETL Process

In this phase, I transitioned from simple data collection to building a robust **ETL (Extract, Transform, Load)** pipeline. The goal was to automate the flow of scraped data from a local CSV file into a structured **SQL Server (SSMS)** database.

### The Workflow
`Web Scraping (JobStreet)` ➡️ `Raw CSV` ➡️ `Python Transformation (Regex)` ➡️ `SQL Server Database`

### Key Technical Challenges & Solutions

* **Data Cleaning with Regex (Transform):**
    The raw salary data was highly inconsistent (e.g., *"Rp 7.000.000 – Rp 8.000.000"*, mixed with different thousand separators and invisible characters). I implemented a **Regular Expression (Regex)** logic in Python to:
    * Strip currency symbols and non-numeric characters.
    * Identify and split salary ranges into dedicated `Min_Salary` and `Max_Salary` columns.
    * Ensure data types are numeric (`FLOAT/DECIMAL`) for future analytical queries.

* **Database Integration (Load):**
    I automated the database connection and table creation using `SQLAlchemy` and `pyodbc`. By using the `if_exists='replace'` logic, I ensured the database stays synchronized with the latest scraping results with a single click.

* **Infrastructure Troubleshooting:**
    Encountered and resolved **SSL Security Error 18** during the local SQL Server connection. I managed this by fine-tuning the connection string attributes (`TrustServerCertificate=yes`) and ensuring the correct **ODBC Driver 17** was utilized.

### 🧰 Tech Stack
* **Language:** Python 3.x
* **Libraries:** Pandas (Data Manipulation), SQLAlchemy (ORM), pyodbc (Database Driver), Re (Regular Expressions)
* **Database:** Microsoft SQL Server Management Studio (SSMS)

---
*Next Step: SQL Data Analysis & Insights Generation*