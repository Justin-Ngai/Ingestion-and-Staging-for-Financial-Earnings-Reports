import json
import boto3
import urllib3

# Configuration
SECRET_ARN = "arn:aws:secretsmanager:us-east-1:629904435132:secret:dev/alpha_vantage-wbLVgz"
S3_BUCKET = "raw-us-east-1-jngai-dev"
BASE_URL = "https://www.alphavantage.co/query"

# Clients
http = urllib3.PoolManager()
s3 = boto3.client("s3")
secrets = boto3.client("secretsmanager")

def lambda_handler(event, context):
    # Expects: {"symbol": "AAPL", "year_quarter": "2024Q1"}
    symbol = event.get("symbol", "").upper()
    year_quarter = event.get("year_quarter", "")
    
    if not symbol or not year_quarter:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "Provide 'symbol' and 'year_quarter' (e.g. 2024Q1)"
            })
        }
    
    # Get API key
    res = secrets.get_secret_value(SecretId=SECRET_ARN)
    api_key = json.loads(res["SecretString"])["FreeApiKey"]
    
    # Alpha Vantage expects quarter as a single field (e.g. 2024Q1)
    params = {
        "function": "EARNINGS_CALL_TRANSCRIPT",
        "symbol": symbol,
        "quarter": year_quarter,
        "apikey": api_key
    }
    url = BASE_URL + "?" + "&".join(f"{k}={v}" for k, v in params.items())
    print(f"Request URL: {url}")
    
    try:
        raw_res = http.request("GET", url)
        data = json.loads(raw_res.data.decode("utf-8"))
        
        # Handle API-side errors
        if any(k in data for k in ["Note", "Error Message", "Information"]):
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "error": "Alpha Vantage API error",
                    "details": data
                })
            }
        
        # Prepare JSON content
        json_content = json.dumps(data)
        
        # Define S3 keys for both locations
        target_key = f"alpha_vantage/earnings_call_transcripts/{symbol}/target/transcript.json"
        historic_key = f"alpha_vantage/earnings_call_transcripts/{symbol}/historic/{year_quarter}.json"
        
        # Save to target folder (always overwrites)
        s3.put_object(
            Bucket=S3_BUCKET,
            Key=target_key,
            Body=json_content,
            ContentType="application/json"
        )
        print(f"Saved to target: {target_key}")
        
        # Save to historic folder (overwrites if same quarter exists)
        s3.put_object(
            Bucket=S3_BUCKET,
            Key=historic_key,
            Body=json_content,
            ContentType="application/json"
        )
        print(f"Saved to historic: {historic_key}")
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Files saved successfully",
                "symbol": symbol,
                "quarter": year_quarter,
                "target_key": target_key,
                "historic_key": historic_key
            })
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
