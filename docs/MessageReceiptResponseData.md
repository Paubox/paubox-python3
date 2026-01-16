# MessageReceiptResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | [**MessageReceiptResponseDataMessage**](MessageReceiptResponseDataMessage.md) |  | 

## Example

```python
from paubox.models.message_receipt_response_data import MessageReceiptResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of MessageReceiptResponseData from a JSON string
message_receipt_response_data_instance = MessageReceiptResponseData.from_json(json)
# print the JSON string representation of the object
print(MessageReceiptResponseData.to_json())

# convert the object into a dict
message_receipt_response_data_dict = message_receipt_response_data_instance.to_dict()
# create an instance of MessageReceiptResponseData from a dict
message_receipt_response_data_from_dict = MessageReceiptResponseData.from_dict(message_receipt_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


