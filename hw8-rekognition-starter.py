"""
SI 673 - Image Recognition with AWS Rekognition

Help Kelly recover her four missing pet photos!
"""

import boto3

# ==========================================
# Configuration
# ==========================================

BUCKET = "si673-pets-YOUR-ACCOUNT-ID"
PREFIX = "pet/"

s3 = boto3.client("s3", region_name="us-east-1")
rekognition = boto3.client("rekognition", region_name="us-east-1")

answer = []


# ==========================================
# Part 1 - Retrieve Images from S3
# ==========================================

response = s3.list_objects_v2(Bucket=BUCKET, Prefix=PREFIX)

# TODO 1: Loop through the objects returned by S3
# Hint: Look at response["Contents"]


# TODO 2: Extract each image's S3 object key
# Skip objects that aren't JPG, JPEG, or PNG images


# ==========================================
# Part 2 - Analyze Images with Rekognition
# ==========================================

# Example: Analyze a single image using its S3 key.
# Move/adapt this code inside your image-processing loop.

# result = rekognition.detect_labels(
#     Image={
#         "S3Object": {
#             "Bucket": BUCKET,
#             "Name": "pet/example.jpg"
#         }
#     },
#     MaxLabels=10
# )

# TODO 3: Call detect_labels() for each image.
# Examine the labels and confidence scores returned.


# ==========================================
# Part 3 - Identify Kelly's Pets
# ==========================================

# TODO 4: Develop logic to identify likely pet photos.
# Which labels indicate an animal?
# Would confidence thresholds help?


# TODO 5: Add matching filenames to 'answer'.
# Remember: filenames only, not S3 paths.
# Avoid duplicates!


# ==========================================
# Results
# ==========================================

print("Kelly's recovered pet photos:")
print(answer)

assert len(answer) == 4, "Expected four pet photos!"
