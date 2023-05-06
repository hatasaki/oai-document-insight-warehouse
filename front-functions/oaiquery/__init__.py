import logging
import azure.functions as func
import json
import openai
import os
import time

def main(req: func.HttpRequest, docs: func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Get text and filenames from request body
    req_body = req.get_json()
    question = req_body.get('text')
    filenames = req_body.get('filenames')

    # OpenAIのAPIキーを環境変数から取得
    openai.api_key = os.environ["OPENAI_API_KEY"]
    if os.environ.get("OPENAI_API_TYPE") == "azure":
        logging.info("Use Azure")
        openai.api_base = os.environ["AZURE_OPENAI_API_BASE"]
        openai.api_type = os.environ["OPENAI_API_TYPE"]
        openai.api_version = os.environ["AZURE_OPENAI_API_VERSION"]
    else:
        logging.info("Use open_ai")
        openai.api_type = "open_ai"

    # filenamesのfile毎にdocsからcontentを取得
    text = ''
    for filename in filenames:
        for doc in docs:
            if doc['id'] == filename:
                text += "filename=" + filename + " content=" + doc['content'] + '\n'

    # OpenAIのAPIを呼び出すパラメータを設定
    params = {
            "messages": [
                {"role": "system", "content": "次の内容に基づき解答を作成する\n" + text},
                {"role": "user", "content": question}
                ],
            "temperature" :0.7,
            #"max_tokens": 1024,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0
    }
    if os.environ.get("OPENAI_API_TYPE") == "azure":
        params["engine"] = os.environ["AZURE_OPENAI_MODEL_DEPLOY"]
    else:
        params["model"] = os.environ["OPENAI_MODEL"]

    #openaiのapiを呼び出し
    try:
        response = openai.ChatCompletion.create(**params)
        answer = response["choices"][0]["message"]['content']
    except Exception as e:
        error_message = e.json_body['error']['message']
        answer = "エラーが発生しました " + error_message

    return func.HttpResponse(body=json.dumps({"answer": answer}), mimetype='application/json')
