# BlobTrigger - Python

The `BlobTrigger` makes it incredibly easy to react to new Blobs inside of Azure Blob Storage. This sample demonstrates a simple use case of processing data from a given Blob using Python.

## How it works

For a `BlobTrigger` to work, you provide a path which dictates where the blobs are located inside your container, and can also help restrict the types of blobs you wish to return. For instance, you can set the path to `samples/{name}.png` to restrict the trigger to only the samples path and only blobs with ".png" at the end of their name.

## Learn more

Documentation

local.settings.json needs to include the following:

{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "DefaultEndpointsProtocol=https;AccountName=__name__;AccountKey=__key__;EndpointSuffix=core.windows.net",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "CosmosDBEndpoint": "__primary_endpoint__",
    "PREDICTION_ENDPOINT": "__prediction_endpoint__",
    "PREDICTION_KEY": "__prediction_key__",
    "PREDICTION_PROJECT_ID": "__project_id__",
    "PREDICTION_PUBLISHED_NAME": "__iteration_published_name__"
  }
}

Azure Portal: the Azure Function parameters need to define these keys with the same values than your local.settings.json:

    PREDICTION_ENDPOINT
    PREDICTION_KEY
    PREDICTION_PROJECT_ID
    PREDICTION_PUBLISHED_NAME

It also needs to define the following connection string of type 'Custom' for Cosmos:

    connectionStringSetting