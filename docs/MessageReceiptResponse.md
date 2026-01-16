# MessageReceiptResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**source_tracking_id** | **str** | The tracking ID for the message | 
**data** | [**MessageReceiptResponseData**](MessageReceiptResponseData.md) |  | 

## Example

```python
from paubox.models.message_receipt_response import MessageReceiptResponse

# TODO update the JSON string below
json = "{}"
# create an instance of MessageReceiptResponse from a JSON string
message_receipt_response_instance = MessageReceiptResponse.from_json(json)
# print the JSON string representation of the object
print(MessageReceiptResponse.to_json())

# convert the object into a dict
message_receipt_response_dict = message_receipt_response_instance.to_dict()
# create an instance of MessageReceiptResponse from a dict
message_receipt_response_from_dict = MessageReceiptResponse.from_dict(message_receipt_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


