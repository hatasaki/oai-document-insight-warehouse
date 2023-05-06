# Azure OpenAI Documents Search App - Document Insight Warehouse

This repo is Document Insight Warehouse project to extract and utilize important documents quickly from a variety of accumulated documents with Azure AI and App services.

## Architecture
- FrontEnd
 - User access Single Page App on Static Web Apps
 - Search docs by keywords with Doc search API
 - Query on docs with Doc query API (utilizing ChatGPT for the docs)
- Document Insight Warehouse
 - Docs stored in DB with ChatGPT created summarize on key points
- Triggers
 - Copy docs in OneDrive to blob
 - Extract texts of docs by recognizing forms of the docs (ex. PDF to text)
 - Summarize docs by ChatGPT with pre-defined system prompt

![Document Insight Warehouse System Diagram](img/DIWHsystemdiagram.png)

## Technology stack

* Javascript
* Azure Static Web Apps
* Python
* Azure Functions
* Azure Cosmos DB
* Azure OpenAI
* Auzre Logic Apps
* Azure Blob Storage
* Azure Form Recognizer

## How to use source codes in this repo

TBD

## Contributing

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.