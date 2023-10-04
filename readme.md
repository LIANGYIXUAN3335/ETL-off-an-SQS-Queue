# ETL off an SQS Queue

### Author: [Yixuan(Lisa) Liang ](mailto:liangyixuan333@gmail.com)

## Overview

This application is designed to efficiently and securely process messages from an AWS SQS queue, transform the data, and then load it into a PostgreSQL database. It masks sensitive fields, ensuring the privacy of the data, and maintains a continuous polling mechanism until the queue is empty.

## Features

- Polls messages from a standard AWS SQS queue in batches of 10 messages per iteration.
- Extracts message body, parses JSON data, and loads into a dataframe.
- Masks IP and Device ID fields using SHA256 hashing.
- Stores the processed data in the `user_logins` table in PostgreSQL.
- Deletes processed messages from the queue.

## How to Run

### Pre-requisites:

- Docker
- PostgreSQL

### Execution Steps:

1. **Setup Dependencies**: Ensure `docker-compose` is installed.

   ```
   bashCopy code
   docker-compose --version
   ```

2. **Start Required Services**: Run LocalStack and PostgreSQL containers.

   ```
   bashCopy code
   docker-compose up --detach
   ```

3. **Build & Run Data Pipeline**:

   ```
   bashCopy codedocker build -t debanjalisaha/fetch_data_pipeline .
   docker run debanjalisaha/fetch_data_pipeline
   ```
{
    "Messages": [
        {
            "MessageId": "1a8c0722-fd55-49c0-9d63-b88d066c902d",
            "ReceiptHandle": "ZmZmNTNhYTctMDJjMS00YzQ0LTljZTAtYjdiODY2MGExMzM3IGFybjphd3M6c3FzOnVzLWVhc3QtMTowMDAwMDAwMDAwMDA6bG9naW4tcXVldWUgMWE4YzA3MjItZmQ1NS00OWMwLTlkNjMtYjg4ZDA2NmM5MDJkIDE2OTYyODc2ODAuMTE0NDAxNg==",
            "MD5OfBody": "e4f1de8c099c0acd7cb05ba9e790ac02",
            "Body": "{\"user_id\": \"424cdd21-063a-43a7-b91b-7ca1a833afae\", \"app_version\": \"2.3.0\", \"device_type\": \"android\", \"ip\": \"199.172.111.135\", \"locale\": \"RU\", \"device_id\": \"593-47-5928\"}"
        }
    ]
}
4. **Verify Data**: Open PostgreSQL and check the `user_logins` table.

   ```
   bashCopy codepsql -d postgres -U postgres -p 5432 -h localhost -W
   postgres=# select * from user_logins; 
   ```
## Thought Process

### Design Considerations:

1. **Batch Processing**: To optimize performance, we process messages in batches. This reduces the number of calls to the SQS service.
2. **Privacy First**: Given the sensitivity of IP and Device IDs, we employed SHA256 hashing to mask these fields. This ensures data privacy while maintaining the uniqueness and consistency of the data.
3. **Reliability**: Messages are deleted from the queue only after successful processing and storage in PostgreSQL, ensuring data integrity.
4. **Continuous Polling**: The system continuously polls the queue until it's empty, ensuring all messages are processed.

### Assumptions Made:

- Device ID and IP fields are never null.
- Duplicates are allowed, assuming downstream data cleaning processes.
- Valid JSON structure in SQS messages.
- Pre-existing table schema in PostgreSQL.
- SHA256 as an acceptable masking technique.
- Properly configured Docker test images.

### Potential Improvements:

- Integrate with Airflow for better pipeline orchestration.
- Use reversible hashing or token-based techniques for PII recovery.
- Consider NoSQL storage for JSON data.
- Implement rich data visualization using tools like PowerBI or Splunk.

## Problems

1. **How would you deploy this application in production?**

   **Thought Process**: Our primary objectives are ensuring high availability, scalability, and security of the application.

   - Utilize **Kubernetes (k8s)** for deploying and orchestrating the Docker containers. Kubernetes provides capabilities such as auto-deployment, rolling updates, integrated storage systems, and service discovery. This ensures our application remains healthy, and auto-scales based on the load.
   - Sensitive information like database connection parameters, API keys, etc., should not be hardcoded or stored in plain text. We can consider using Kubernetes Secrets for storing such sensitive information, ensuring that only authorized pods have access.

2. **What other components would you want to add to make this production-ready?**

   **Thought Process**: An application in production should be stable, secure, and efficiently handle errors.

   - Integrate **AWS Lambda** with **SQS**. Whenever data is pulled from the SQS queue, Lambda can be triggered to process it. This serverless architecture can offer auto-scalability and reduce maintenance overhead.
   - To enhance the application's performance further, we can incorporate Redis as a caching layer to cache frequently accessed data and reduce redundant database queries.

3. **How can this application scale with a growing dataset?**

   **Thought Process**: As the data grows, we need to ensure that the system's response time doesn't degrade significantly while maintaining data consistency.

   - Leverage the Horizontal Pod Autoscaling (HPA) feature of **Kubernetes**. With this, if the CPU or memory utilization goes beyond a specified threshold, the number of Pods can be increased automatically to cater to more traffic.
   - Use **Amazon Kinesis** for stream processing of data. As the volume of data increases, Kinesis can offer real-time data stream processing, and in conjunction with Lambda, can ensure real-time processing of data.

4. **How can PII be recovered later on?**

   **Thought Process**: Even if we mask the data, there might be scenarios where we need the original data. Thus, we need a secure and reliable recovery mechanism.

   - A viable approach is to encrypt the data before masking, and store this encrypted data in a restricted storage area. When there's a need to recover the original data, only those with the appropriate decryption keys can decipher it.

5. **What are the assumptions you made?**

   - The input data always arrives in the expected format and structure.
   - The Kubernetes cluster is correctly configured, including network policies, storage, logging, and monitoring.
   - The database is always accessible, and any connection failures are transient and can be resolved with retry strategies.