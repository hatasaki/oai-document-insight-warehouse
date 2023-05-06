import logging
import azure.functions as func
import json
import time
import os
import requests
import mimetypes

def main(myblob: func.InputStream, outputDocument: func.Out[func.Document]):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")

    filename = myblob.name.split('/')[1]

    # This is the call to the Form Recognizer endpoint
    endpoint = os.environ.get('FORM_EP')
    apim_key = os.environ.get('FORM_KEY')
    post_url = endpoint + "/formrecognizer/documentModels/prebuilt-read:analyze?api-version=2022-08-31"
    source = myblob.read()

    print(post_url)

    headers = {
    # Request headers
    'Content-Type': mimetypes.guess_type(filename)[0], #'application/pdf',
    'Ocp-Apim-Subscription-Key': apim_key,
    }

    text1=os.path.basename(myblob.name)

    resp = requests.post(url=post_url, data=source, headers=headers)

    if resp.status_code != 202:
        print("POST analyze failed:\n%s" % resp.text)
        quit()
    print("POST analyze succeeded:\n%s" % resp.headers)
    get_url = resp.headers["operation-location"]

    wait_sec = 25

    time.sleep(wait_sec)
    # The layout API is async therefore the wait statement

    resp = requests.get(url=get_url, headers={"Ocp-Apim-Subscription-Key": apim_key})

    resp_json = json.loads(resp.text)

    status = resp_json["status"]

    if status == "succeeded":
        print("POST Layout Analysis succeeded:\n%s")
        results = resp_json
    else:
        print("GET Layout results failed:\n%s")
        quit()

    results = resp_json

    content = results["analyzeResult"]["content"]

    doc = {'id': filename, 'content': content}

    outputDocument.set(func.Document.from_json(json.dumps(doc)))
    
