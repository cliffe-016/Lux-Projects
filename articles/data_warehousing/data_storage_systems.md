## Data Warehouse

A data warehouse is a system that stores highly structured information from various sources. They typically store historical data from one or more systems for analysis, Business Intelligence and reporting. It is usually denormalized to prioritize read operations ahead of write operations. You might be wondering, _Is a data warehouse a database?_ Yes, in simple terms, a data warehouse is a giant database that is optimized for analytics. These are the keys features of a data warehouse:

* **Centralized data:** Data from various sources are centralized in a data warehouse giving analysts a high-level view of the organization's data, this helps them to conduct in-depth analyses and generate insights.
* **Time-variant data:**  Data warehouses preserve previous data records enabling users to track past performance, make comparisons and spot long-term trends.
* **Denormalized data:** Without organized data, querying data becomes much easier and performance is optimized for analytical activities requiring complex joins and aggregations.
* **Aggregated Data:** A data warehouse frequently aggregates data at various granularities. This enables analysts to deep down into more niche data as necessary and get summarized data quickly for high-level conclusions.
* **Query Performance Optimisation:** To increase query speed and efficiency, data warehouses use a variety of performance optimisation techniques, including indexing, segmentation and materialized views. These improvements make it possible for lengthy analytical queries to be processed quickly.
* **BI Integration support:** Business intelligence solutions all function in conjunction with data warehouses to produce insightful reports, dashboards and visualizations.

### Use cases for data warehouses

Data warehouses are better suited for use cases that involve the analysis and reporting of large datasets. These use cases include:

* **Business Intelligence (BI):** Data warehouses consolidate large volumes of historical data, which is ideal for analytics, reporting and forecasting.
* **Trend analysis and reporting:** Data warehouses are ideal for generating business reports, dashboards and exploring patterns over time.
* **Predictive analytics and data mining:** Data warehouses support advanced analytics that help businesses make data-driven decisions, such as predicting customer behavior or market trends.

Note that data warehouses are not intended to satisfy the transaction and concurrency needs of an application. If an organization determines they will benefit from a data warehouse, they will need a separate database or databases to power their daily operations. Examples of data warehouses include:
* Amazon Redshift.
* Google BigQuery.
* Snowflake.

## Database
A database is a collection of structured or unstructured data stored in a computer system, managed by a Database Management System (DBMS). Unlike data warehouses, Databases are most useful for small, atomic transactions and typically contain only the most up-to-date information, which makes historical queries impossible. Common types include:

* **Relational (SQL) Databases** for structured data as in tables with fixed rows and columns. Examples include Postgresql, MySQL
* **Non-relational (NoSQL) Databases** for unstructured data like JSON (JavaScript Object Notation), documents. Examples include MongoDB

Databases have the following features:
**ACID properties:** To guarantee data integrity throughout transactions, databases follow the ACID (Atomicity, Consistency, Isolation, Durability) criteria. Atomicity ensures that transactions are treated as indivisible units, consistency ensures that data changes from one valid state to another, isolation avoids interactions between concurrent transactions, and durability ensures that changes made to data after a transaction has been updated and are irreversible.
**Query Language:** Users can interact with the data by using query languages offered by databases, such as SQL (Structured Query Language). To meet different needs queries are used to retrieve, filter, aggregate, or update data.
**Indexing:** Indexes help databases to retrieve data more quickly. Data structures called indexes enable quick access to particular rows of data by avoiding the requirement for full-table scans when running queries.
**Normalization:** The practice of organizing data in relational databases to reduce redundancy and enhance data integrity is known as normalization. This process includes decomposing the data into smaller, related tables and creating connections between them.
**Data Backup and Recovery:** Databases provide mechanisms for data backup and recovery to protect against data loss caused by any kind of failures, down times, software bugs, or other unanticipated events.
**Data Modeling:** Making a conceptual, logical, and physical data model is part of database design. A logical model depicts the data in more detail, a physical model transforms the logical model into the real database schema, and a conceptual model specifies the high-level structure of data and relationships.

**Use cases for databases**
Databases excel in scenarios that require real-time data handling and high transaction volumes. 
Key use cases include:
* **Transaction processing:** Databases are designed to manage transactions in real time, such as in retail point-of-sale (POS) systems or financial transactions in banking.
* **Customer Relationship Management (CRM):** CRM manages real-time customer data, such as orders, interactions, and support tickets.
* **Enterprise Resource Planning (ERP):** Databases play a key role in operational systems, managing everything from procurement and payroll to inventory management.


## Data Lake
A data lake is a repository of data from disparate sources that is stored in its original, raw format. They store huge amounts of data in a variety of formats (csv, json etc) and act as sort of a "dumping site" for data. Like data warehouses, data lakes are not intended to satisfy the transaction and concurrency needs of an application. 
Key features of a data lake:
* **Support for diverse formats:** Handles data in formats like JSON, Avro, and Parquet, accommodating a wide range of use cases.
* **Real-time analytics readiness:** Ideal for machine learning and advanced data science workloads.
* **Horizontal scalability:** Uses cost-efficient storage solutions such as Amazon S3 or Azure Blob Storage, allowing seamless growth with increasing data volumes.

The following are examples of technology that provide flexible and scalable storage for building data lakes:
* AWS S3
* Azure Data Lake Storage Gen2
* Google Cloud Storage

## Data Mart
A data mart is a database that is oriented toward storing information of a particular type or for a particular set of users within an organization: for example, marketing, sales, finance, or human resources. Data marts may be their own entity, or they may be a smaller partition as part of a larger data warehouse. In either case, the goal is to pare down an organization’s data into a more manageable size, usually less than 100 gigabytes.

**Types of data marts**
There are three types of data marts that differ based on their relationship to the data warehouse and the respective data sources of each system:
* **Dependent data marts** are partitioned segments within an enterprise data warehouse. This top-down approach begins with the storage of all business data in one central location. The newly created data marts extract a defined subset of the primary data whenever required for analysis.
* **Independent data marts** act as a standalone system that doesn't rely on a data warehouse. Analysts can extract data on a particular subject or business process from internal or external data sources, process it, and then store it in a data mart repository until the team needs it.
* **Hybrid data marts** combine data from existing data warehouses and other operational sources. This unified approach leverages the speed and user-friendly interface of a top-down approach and also offers the enterprise-level integration of the independent method.

## Data Lakehouse
A data lakehouse merges the cost-efficiency of a data lake with the data management capabilities of a warehouse. It supports both structured and unstructured data while enabling advanced machine learning and business intelligence workflows. This architecture is designed to bridge the gap between raw data storage and performance-oriented analytics.
Key features of a data lakehouse:
* **ACID compliance:** Ensures reliable transactions, maintaining data integrity and data consistency.
* **Schema-on-write and schema-on-read:** Provides flexibility during data ingestion and robust structure during analysis.
* **Integration with BI tools:** Works seamlessly with platforms like Tableau, Power BI, and Looker, enhancing usability for decision-makers.
