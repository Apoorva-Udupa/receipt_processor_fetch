# Receipt Processor Challenge

This repository holds my **Python-Flask** code for a take-home exam from **Fetch Rewards**. The application runs a server that has  **two API endpoints**:

1. **POST** `/receipts/process`  
   - Accepts a JSON “receipt” object.  
   - Takes the receipt json and then applies the point calculation on the receipt, and returns a JSON response containing a unique **`id`**.  

2. **GET** `/receipts/{id}/points`  
   - Returns the total points associated with the specified `id`.  
   - Returns **404** if the `id` does not exist in the dictionary of id-points pairs.
     

## Project Structure
- **`app.py`** — This file is within receipt_processor folder. This has the code for both GET and POST methods with points calculation. 
- **`requirements.txt`** — Lists Python dependencies needed. Flask is needed to run this code. 
- **`Dockerfile`** — Includes a docker file to build and run the application.  
- **`README.md`** — discusses details of the project.

## Docker Instructions
 1. Build the Docker Image
From the **root** directory (where the DockerFile is located), run:

```bash
 docker build -f DockerFile -t receipt-processor .
```
 2. Run the Container
```bash
 docker run -d -p 5000:5000 --name my-receipt-app receipt-processor
```
 3. Verify the Container is running
```bash
 docker ps
```
Check and test the POST and GET methods and verify points calculation. I used POSTMAN to check the POST and GET methods defined in app.py

 4. Stop the Container
```bash
 docker stop my-receipt-app
```

## Testing with Postman
Below are **step-by-step** instructions to test the Receipt Processor endpoints in **Postman** using a sample JSON receipt:

1. **Open Postman** and **create** a new request.
2. **Set** the request **method** to **POST**.
3. **Enter** the URL where the application is running with /receipts/process
4. Go to the **Body** tab:
    - Select **raw**.
    - Choose **JSON** in the dropdown (ensuring the `Content-Type` header is `application/json`).
5. **Paste** the following sample JSON receipt for testing the endpoint:
   ```json
   {
    "retailer": "Walgreens",
    "purchaseDate": "2022-01-02",
    "purchaseTime": "08:13",
    "total": "2.65",
    "items": [
        {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
        {"shortDescription": "Dasani", "price": "1.40"}
    ]
   }
6. Click Send to submit the request. You should get a 200 OK response with a JSON body like:
   ```json
   { "id": "some-uuid-value" }
7. Copy the returned "uuid" from the response.
8. Create another request in Postman, set the request **method** to **GET**. In the URL paste the copied uuid here: **`url/<copied-id>/points`**
9. You should be get a response of points calculated.
