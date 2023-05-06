import logging
import azure.functions as func
import openai
import os
import time


def main(documents: func.DocumentList, outputDocument: func.Out[func.Document]):
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
    # 環境変数OPENAI_SYSTEMに設定した文章を取得
    system_content = os.environ["OPENAI_SYSTEM"]

    # documentsに含まれるドキュメントを順にOpenAIのAPIを呼び出して結果を取得
    for doc in documents:
        print("triggered filename: ", doc["id"])
        # ドキュメントがopenaiフィールドを持っている場合は処理をスキップ
        if "openai" in doc:
            if doc["openai"] != "":
                print("skip filename: ", doc["id"])
                continue
        print("create openai for filename: ", doc["id"])
        # ドキュメントの内容を取得
        content = doc["content"]
        # OpenAIのAPIを呼び出すパラメータを設定
        params = {
                "messages": [
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": content}
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
        # OpenAIのAPIを呼び出して結果を取得
        for i in range(3):
            try:
                response = openai.ChatCompletion.create(**params)
                break
            except Exception as e:
                error_message = e.json_body['error']['message']
                logging.error('Error(try' + str(i) + '): ' + error_message)
                if e.http_status != 429: break
                time.sleep(30)
        # OpenAIのAPIの結果から文章を取得
        text = response["choices"][0]["message"]['content']
        print("openai: ", text)
        # ドキュメントの内容にOpenAIのAPIの結果を追記
        doc["openai"] = text
        outputDocument.set(doc)
