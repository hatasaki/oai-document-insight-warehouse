import logging
import azure.functions as func
import json
import urllib.parse

def main(req: func.HttpRequest, docs: func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    keyword = req.params.get('keyword')
    if keyword:
        # URLエンコードされているのでデコードする
        keyword = urllib.parse.unquote(keyword)
    else:
        keyword = ''

    results = []
    for doc in docs:
        if 'openai' not in doc:
            continue
        if keyword.lower() in doc['openai'].lower() \
            or keyword.lower() in doc['content'].lower() \
                or keyword.lower() in doc['id'].lower() \
                    or keyword == '*' or keyword == '':
            results.append({"id": doc["id"], "content": doc["content"], "openai": doc["openai"]})

    return func.HttpResponse(body=json.dumps(results), mimetype='application/json')
