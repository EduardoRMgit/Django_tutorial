import boto3


def textract_ine(img):

    s3BucketName = "phototest420"
    client = boto3.client(
        'textract',
        aws_access_key_id='AKIA5F5MJTKYM33K4YWS',
        aws_secret_access_key='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',
        region_name='us-east-1'
    )

    response = client.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': 'phototest420',
                'Name': img
            }
        }
    )
    textract = []
    for item in response["Blocks"]:
        if item["BlockType"] == "WORD":
            textract.append(item["Text"])

    return validate_ine(textract)


def validate_ine(extract):
    strings = [
        "INSTITUTO",
        "ELECTORAL",
        "CLAVE",
        "FECHA",
        "NACIMIENTO",
        "ESTADO",
        "DOMICILIO",
        "REGISTRO"
    ]

    nacional = "NACIONAL"
    federal = "FEDERAL"

    matched_strings = []

    if "FEDERAL" in extract:
        strings.append(federal)

    if "NACIONAL" in extract:
        strings.append(nacional)

    for item in extract:
        if item in strings:
            matched_strings.append(item)

    matched_count = len(matched_strings)
    total_count = len(strings)
    percentage = (matched_count / total_count) * 100
    if percentage >= 70:
        return True, extract


def textract_ine_reverso(img):
    s3BucketName = "phototest420"
    client = boto3.client(
        'textract',
        aws_access_key_id='AKIA5F5MJTKYM33K4YWS',
        aws_secret_access_key='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',
        region_name='us-east-1'
    )

    response = client.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': 'phototest420',
                'Name': img
            }
        }
    )
    textract_reverso = []
    for item in response["Blocks"]:
        if item["BlockType"] == "WORD":
            textract_reverso.append(item["Text"])

    textract_reverso = [string.replace("<", " ") if "<" in string else string
        for string in textract_reverso]
    print(textract_reverso[-1])
    print(textract_reverso[-2])

    return validate_ine_reverso(textract_reverso)


def validate_ine_reverso(extract_reverso):
    strings = [
        "EXTRAORDINARIAS",
        "ELECTORAL",
    ]

    nacional = "NACIONAL"
    federal = "FEDERAL"
    matched_strings = []

    if "FEDERAL" in extract_reverso:
        strings.append(federal)

    if "NACIONAL" in extract_reverso:
        strings.append(nacional)

    for item in extract_reverso:
        if item in strings:
            matched_strings.append(item)

    matched_count = len(matched_strings)
    total_count = len(strings)
    percentage = (matched_count / total_count) * 100
    return extract_reverso
