# Where Does Your Data Live? Decoding the Modern Data Ecosystem

If you are stepping into the world of data engineering or analytics, you have likely been hit with a wave of storage buzzwords like _data lake_ and _data warehouse_. In this article, we will demystify them and you'll get to understand exactly where your data belongs 


## Database
Imagine you just launched a business. You need a system to record daily operations every time a customer buys a product, updates their password or submits a support ticket. This is the job of a standard Database.
A database is a collection of structured or unstructured data stored in a computer system, managed by a Database Management System (DBMS). Unlike data warehouses, databases are most useful for small, atomic transactions and typically contain only the most up-to-date information, which makes historical queries impossible. Common types include:

* **Relational (SQL) Databases** for structured data as in tables with fixed rows and columns. Examples include Postgresql, MySQL
* **Non-relational (NoSQL) Databases** for unstructured data like JSON (JavaScript Object Notation), documents. Examples include MongoDB

Databases have the following core features:
* **ACID Properties:** To guarantee absolute data integrity during transactions, databases adhere strictly to the ACID framework:
	* **Atomicity:** Database transactions are treated as a single, "all-or-nothing" unit.
	* **Consistency:** Data must seamlessly transition from one valid state to another without breaking the user defined rules.
	* **Isolation:** Multiple transactions can happen concurrently without interfering with one another.
	* **Durability:** Once a transaction is complete, the changes are permanent and irreversible, even if the system crashes.

* **Query Language:** Databases allow users to interact directly with the system using specific languages, most commonly SQL (Structured Query Language). This enables developers and analysts to easily retrieve, filter, aggregate or update information.

* **Indexing:** Think of this like the index at the back of a textbook. Instead of forcing the system to scan an entire table, indexes act as structural shortcuts that allow the database to locate specific data instantly.

* **Normalization:** This is the design practice of breaking down large datasets into smaller, interconnected tables. It eliminates duplicate information, reduces redundancy and keeps the database organized and efficient.  

* **Data Backup and Recovery:** To safeguard against hardware failures, software bugs or unexpected downtime, databases come equipped with robust mechanisms to safely back up and restore data.  

* **Data Modelling:** Designing a database requires a clear structural blueprint. This process moves through three phases:
	* **Conceptual modelling** maps out the high-level data relationships.
	* **Logical modelling** adds the technical details.
	* **Physical modelling** translates that design into the actual working database schema. 

**Use cases for databases**
Databases excel in scenarios that require real-time data handling and high transaction volumes. 
Key use cases include:
* **Real-Time Transaction Processing:** Databases are built to execute immediate operations, such as processing payments at a retail point-of-sale (POS) system or handling financial transfers in banking.  

* **Customer Relationship Management (CRM):** They allow CRM platforms to manage real-time customer orders, interactions and support tickets.  

* **Enterprise Resource Planning (ERP):** Databases power the day-to-day operational software of businesses, managing records for everything from employee payroll to live inventory management.

Databases are perfect for storing records in real-time, but what happens when you want to compare current sales to those from five years ago? Running a massive historical query could cripple your active, database-dependent operations. To remedy this, a separate storage system dedicated to historical data should suffice.


## Data Warehouse

To solve the historical reporting problem, a data warehouse is used. Instead of handling real-time transactions, it stores massive amounts of structured, historical data from multiple sources to help organizations spot long-term trends and make data-driven decisions. It is usually denormalized to prioritize read operations ahead of write operations. These are the key features of a data warehouse:

* **Centralized Data:** Data warehouses consolidate information from multiple systems to give analysts a comprehensive, high-level view of the organization's data.  

* **Time-Variant Data:** Data warehouses retain historical records, allowing businesses to analyze past performance, compare specific time periods, and identify long-term trends.  

* **Denormalized Architecture:** Data is deliberately structured with fewer tables to minimize complex relationships, which drastically speeds up read performance and simplifies heavy analytical queries.  

* **Aggregated Data:** Information is frequently summarized at various levels of detail, enabling analysts to quickly pull high-level overviews or drill down into granular metrics when necessary.  

* **Query Optimization:** To process massive analytical workloads efficiently, warehouses utilize advanced performance techniques such as indexing, data segmentation and materialized views.  

* **BI Integration:** Data warehouses natively support and connect with Business Intelligence (BI) platforms to power interactive dashboards, robust reporting and data visualizations.

### Use cases for data warehouses

Data warehouses are better suited for use cases that involve the analysis and reporting of large datasets. These use cases include:

* **Business Intelligence (BI):** Data warehouses consolidate large volumes of historical data, which is ideal for analytics, reporting and forecasting.
* **Trend analysis and reporting:** Data warehouses are ideal for generating business reports, dashboards and exploring patterns over time.
* **Predictive analytics and data mining:** Data warehouses support advanced analytics that help businesses make data-driven decisions, such as predicting customer behavior or market trends.

Note that data warehouses are not intended to satisfy the transaction and concurrency needs of an application. If an organization determines they will benefit from a data warehouse, they will need a separate database or databases to power their daily operations. Examples of data warehouses include:
* Amazon Redshift.
* Google BigQuery.
* Snowflake.

Data warehouses are incredibly organized, but this rigid structure is a double-edged sword. While it guarantees clean, structured data, it leaves you with a problem, where do you put millions of messy, unstructured website click logs or raw JSON files?

## Data Lake

When data is too large or unstructured for a data warehouse, it gets dumped into a data lake. Here, data from disparate sources is stored in its original, raw format. Due to its storage flexibility, it acts as a playground for data scientists who train machine learning models on the data before it is fully structured. Like data warehouses, data lakes are not intended to satisfy the transaction and concurrency needs of an application. 
Key features of a data lake:

* **Support for diverse formats:** Handles data in formats like JSON and Parquet, accommodating a wide range of use cases.

* **Real-time analytics readiness:** Ideal for machine learning and advanced data science workloads.

* **Horizontal scalability:** Uses cost-efficient storage solutions such as Amazon S3 or Azure Blob Storage, allowing seamless growth with increasing data volumes.

The following are examples of technology that provide flexible and scalable storage for building data lakes:
* AWS S3
* Azure Data Lake Storage Gen2
* Google Cloud Storage

As your hypothetical company grows, your Data Warehouse becomes massive. Now the Marketing team is complaining that it takes them too long to find the specific campaign metrics they need among all the finance, HR and engineering data.

Enter the **Data Mart**.

## Data Mart

A data mart is a specialized, smaller-scale database designed to serve the specific needs of a single business unit such as marketing or finance. Whether as a standalone entity or as a small partition of a larger data warehouse, its primary goal is to filter an organization's massive data pool into a highly focused, manageable repository for quick access.  

**Types of Data Marts**

There are three main types of data marts, categorized by how they source their information and their relationship to a central data warehouse:  

* **Dependent Data Marts:** These are directly partitioned from an enterprise's central data warehouse. Using this top-down approach, the data mart extracts a specific, predefined subset of the primary data whenever a department needs to run an analysis.  

* **Independent Data Marts:** These operate as fully standalone repositories without relying on a central data warehouse. Teams extract, process and store data directly from various internal or external sources.  

* **Hybrid Data Marts:** As the name implies, these blend the two approaches by pulling information from both an existing data warehouse and external operational systems. This provides the speed and structured interface of a top-down approach while maintaining the flexible integration of an independent setup.

Historically, companies had to maintain both a Data Lake (for raw, cheap machine learning storage) and a Data Warehouse (for fast, structured BI reporting). Moving data between the two was expensive.Recently, a new architecture emerged to bridge this gap: the **Data Lakehouse**.

## Data Lakehouse

A data lakehouse is a modern hybrid architecture that combines the massive, cost-effective storage of a data lake with the robust data management capabilities of a warehouse. By bridging the gap between raw data storage and high-speed analytics, a lakehouse can simultaneously support unstructured machine learning workloads and structured Business Intelligence workflows.  

Key Features of a Data Lakehouse:

* **ACID Compliance:** Unlike traditional data lakes, lakehouses guarantee reliable transactions to maintain strict data consistency and integrity.  

* **Flexible Schemas:** They support both "schema-on-write" and "schema-on-read". This gives engineers flexibility when ingesting raw data, while still providing a rigid, reliable structure when analysts need to query it.  

* **Native BI Integration:** Lakehouses connect seamlessly with popular Business Intelligence platforms like Tableau, Power BI, and Looker, making it easy for decision-makers to visualize their data directly from the source.


**Final Thoughts**
There is no single "best" data storage solution, only the right tool for the job. In fact, a robust modern data ecosystem usually relies on these systems working together:

1. Your **Database** captures the live sale.

2. Your **Data Lake** stores the messy, raw website logs of how the customer found you.

3. Your **Data Warehouse** analyzes five years of those sales trends.

4. Your **Data Mart** gives the marketing team instant access to only the metrics they care about.


