# ETL off an SQS Queue

### Author: [Yixuan(Lisa) Liang ](mailto:liangyixuan333@gmail.com)

## Overview

This application is designed to efficiently and securely process messages from an AWS SQS queue, transform the data, and then load it into a PostgreSQL database. It masks sensitive fields, ensuring the privacy of the data, and maintains a continuous polling mechanism until the queue is empty.

## Features

- Polls messages from a standard AWS SQS queue in batches of 10 messages per iteration.
- Extracts message body, parses JSON data, and loads into a dataframe.
- Filter data to get the valid messages.
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
   docker-compose --version
   ```

2. **Pull data** to docker

   ```shell
   docker pull fetchdocker/data-takehome-localstack
   docker pull fetchdocker/data-takehome-postgres
   ```

3. **Start Required Services**: Run LocalStack and PostgreSQL containers.

   ```shell
   docker-compose up 
   ```

4. **Read a message from the queue using awslocal**:

   ```
   awslocal sqs receive-message --queue-url http://localhost:4566/000000000000/login-queue
   ```
   Then will get the messages structure like below

   ```json
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
   ```

   

5. **Verify Data**: Open PostgreSQL and check the `user_logins` table.

   ```shell
   psql -d postgres -U postgres -p 5432 -h localhost -W
   postgres=# select * from user_logins; 
   ```

6. **Download GitHub Files**: First,   download the application files from GitHub repository. 
   by visiting the following GitHub link: https://github.com/LIANGYIXUAN3335/ETL-off-an-SQS-Queue.

7. **Open a Command Line Interface**: We should open a command line interface (such as Terminal or Command Prompt) and navigate to the extracted application folder. This can be done using the cd command. For example:

   ```shell
   cd /path/to/ETL-off-an-SQS-Queue
   ```

8. Download all requirement packages

   ```shell
   pip install -r requirements.txt
   ```

9. **Run the Application**: Once inside the application folder, users can run the application entry command provided by you. 

   ```
   python -m src.main
   ```
   ```
   2023-10-09 17:19:47,707 - INFO - Processing : 10 messages
   2023-10-09 17:19:47,709 - INFO - Finished processing all messages.
   2023-10-09 17:19:47,710 - INFO - Messages processed and saved to database.
   2023-10-09 17:19:47,720 - INFO - Deleted message with length: 10 from SQS.
   2023-10-09 17:19:47,731 - INFO - Received 10 messages from SQS. Processing...
   2023-10-09 17:19:47,732 - INFO - Received 10 messages to process.
   2023-10-09 17:19:47,732 - INFO - Starting to process message with ID: 90e8f5f2-a003-44b4-9bba-3fca6a72b35a.
   2023-10-09 17:19:47,732 - INFO - Starting to process message with ID: 69c244a2-bd3a-498d-9063-1a46ac3bccf8.
   2023-10-09 17:19:47,732 - INFO - Starting to process message with ID: d9fb100c-d8eb-45a9-a2c3-3bb73086a3bb.
   2023-10-09 17:19:47,732 - INFO - Starting to process message with ID: 7556d90e-5e2a-4484-b10a-c61bc53b9953.
   2023-10-09 17:19:47,733 - INFO - Starting to process message with ID: 822db50f-7e5d-4725-9bd4-d8e551becbf4.
   2023-10-09 17:19:47,733 - INFO - Starting to process message with ID: b6b3c1c2-214e-4617-9fb1-421b5bd154e1.
   2023-10-09 17:19:47,733 - INFO - Starting to process message with ID: b845598c-3daf-4500-aae3-dae3039cccf1.
   2023-10-09 17:19:47,733 - INFO - Starting to process message with ID: 76502ea4-9e83-46f8-92ff-ca90b2ab0eda.
   2023-10-09 17:19:47,734 - INFO - Starting to process message with ID: c36db7c3-e173-4335-b540-a8134b38252d.
   2023-10-09 17:19:47,734 - INFO - Starting to process message with ID: 4708f899-d1e4-41c5-a784-6193f377e368.
   2023-10-09 17:19:47,734 - INFO - Processing : 10 messages
   2023-10-09 17:19:47,737 - INFO - Finished processing all messages.
   2023-10-09 17:19:47,737 - INFO - Messages processed and saved to database.
   2023-10-09 17:19:47,758 - INFO - Deleted message with length: 10 from SQS.
   2023-10-09 17:19:47,777 - WARNING - No messages received from SQS.
   2023-10-09 17:19:47,777 - INFO - Database connection close
   ```

   

10. **Run the Application**
     ![image-20231009172035340](D:\github\ETL off an SQS Queue\ETL-off-an-SQS-Queue\result)
### Thoughts of design:
1. **Privacy First**: Given the sensitivity of IP and Device IDs, I employed DES hashing to mask these fields. This ensures data privacy while maintaining the uniqueness and consistency of the data.
2. **Reliability**: Messages are deleted from the queue only after successful processing and storage in PostgreSQL, ensuring data integrity.
3. **Continuous Polling**: The system continuously pulls the queue until it's empty, ensuring all messages are processed.

### Assumptions Made:

- Duplicates are allowed, assuming downstream data cleaning processes.
- Valid JSON structure in SQS messages.

### Potential Improvements:

- Use 3DES hashing techniques for PII recovery to improve the security.
- Consider NoSQL storage for JSON data.
- Implement rich data visualization using tools like matplotlib.

## Problems

1. **How would you deploy this application in production?**

   **Thought Process**: Our primary objectives are ensuring high availability, scalability, and security of the application.

   - Utilize **Kubernetes (k8s)** for deploying and orchestrating the Docker containers. Kubernetes provides capabilities such as auto-deployment, rolling updates, integrated storage systems, and service discovery. This ensures our application remains healthy, and auto-scales based on the load.
   - Sensitive information like database connection parameters, API keys, DES key etc., should not be hardcoded or stored in plain text. We can consider using Kubernetes Secrets for storing such sensitive information, ensuring that only authorized pods have access.

2. **What other components would you want to add to make this production-ready?**

   **Thought Process**: An application in production should be stable, secure, and efficiently handle errors.

   - Integrate **AWS Lambda** with **SQS**. Whenever data is pulled from the SQS queue, Lambda can be triggered to process it. This serverless architecture can offer auto-scalability and reduce maintenance overhead.
   
3. **How can this application scale with a growing dataset?**

   - **Monitor SQS with CloudWatch**: Set alarms for high message accumulation.
   - **Use Kubernetes HPA**: Auto-scale pods based on SQS CloudWatch metrics.
   - **Adopt Multi-threaded Processing**: Handle multiple SQS messages concurrently within each pod.
   - **Optimize Processing Logic**: Identify and address processing bottlenecks.
   - **Database Optimizations**: Implement efficient data storage and querying strategies.

4. **How can PII be recovered later on?**

   **Thought Process**: Even if we mask the data, there might be scenarios where we need the original data. Thus, we need a secure and reliable recovery mechanism.

   - 3DES is to encrypt the data before masking, and store this encrypted data in a restricted storage area. When there's a need to recover the original data, only those with the appropriate decryption keys can decipher it.

5. **What are the assumptions you made?**

   - The input data always arrives in the expected format and structure.
   - The database is always accessible, and any connection failures are transient and can be resolved with retry strategies.