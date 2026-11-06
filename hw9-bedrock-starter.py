import json
import boto3

bedrock = boto3.client("bedrock-runtime")
MODEL_ID = "us.amazon.nova-lite-v1:0"


def lambda_handler(event, context):
    qs = event.get("queryStringParameters") or {}
    prompt = qs.get("prompt", "Tell me a fun fact about Michigan")

    # Invoke model via bedrock
    resp = bedrock.converse(
        modelId=MODEL_ID,
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"maxTokens": 300, "temperature": 0.7},
    )

    # Extract response text & format response
    answer = resp["output"]["message"]["content"][0]["text"]
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"prompt": prompt, "answer": answer}),
    }
