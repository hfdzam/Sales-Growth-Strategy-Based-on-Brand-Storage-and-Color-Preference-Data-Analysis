# Sales Growth Strategy Based on Brand Storage and Color Preference Data Analysis

## Project Overview

This project analyzes smartphone sales data to uncover market trends related to brand popularity, storage capacities, and color preferences. The goal is to provide actionable insights that help optimize sales strategies, inventory management, and marketing efforts, thereby enhancing customer satisfaction and overall business performance.

## Notebook Purpose
In this notebook, you will:

### Data Collection:
- **Extract data using Airflow and PostgreSQL**: The data is initially stored in PostgreSQL after being extracted using Airflow.
- **Clean and preprocess the data**: The extracted data is then cleaned to remove duplicates, handle missing values, and standardize the data format.
- **Index the cleaned data into Elasticsearch**: After cleaning, the data is indexed into Elasticsearch for further analysis.
- **Validate the results through data quality checks**: Great Expectations (GX) is used for validation to ensure data integrity.

## Tools and Libraries Used:
- **Python**: The core programming language used for scripting and automation.
- **Airflow**: Orchestrates the workflow for data extraction, transformation, and loading.
- **PostgreSQL**: A relational database used to store and retrieve structured data.
- **Elasticsearch**: A distributed search engine used to index and query data.
- **Pandas**: Used for data manipulation and analysis.
- **SQLAlchemy**: ORM library used to manage connections to the PostgreSQL database.
- **Great Expectations (GX)**: Used for data validation to ensure the quality and consistency of the data.

## Docker Setup:
This project utilizes Docker for containerization:
- **Airflow**: Manages the ETL workflow.
- **PostgreSQL**: Serves as the database for storing and managing the data.
- **Elasticsearch**: Facilitates quick search and analysis of large datasets.
- **Kibana**: Provides visualization tools for data stored in Elasticsearch.

## Visualizations:
Visualizations for the insights are provided in PNG format, covering various aspects such as:
- **Brand Performance**
- **Storage Preferences**
- **Color Preferences**
- **Discount Strategies**
- **Sales Target and Goals**

## Conclusion and Business Recommendations
The analysis reveals key insights into market trends that can be used to optimize sales and marketing strategies, improve inventory management, and ultimately enhance customer satisfaction. These insights are critical for making data-driven decisions that align with business goals.

---

For details and to view the script, check out [this Python script](P2M3_hafidz_masruri_DAG.py).

For validation, check out [this Jupyter Notebook](P2M3_hafidz_masruri_GX.ipynb).

## My Kibana Visualization

![Sales Data Visualization](images/intro.png)
![Sales Data Visualization](images/plot01.png)
![Sales Data Visualization](images/plot02.png)
![Sales Data Visualization](images/plot03.png)
![Sales Data Visualization](images/plot04.png)
![Sales Data Visualization](images/plot05.png)
![Sales Data Visualization](images/plot06.png)
![Sales Data Visualization](images/kesimpulan.png)
