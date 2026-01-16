# MessageReceiptErrorResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**errors** | [**List[ErrorResponseErrorsInner]**](ErrorResponseErrorsInner.md) |  | 
**source_tracking_id** | **str** | The tracking ID for the message | 

## Example

```python
from paubox.models.message_receipt_error_response import MessageReceiptErrorResponse

# TODO update the JSON string below
json = "{}"
# create an instance of MessageReceiptErrorResponse from a JSON string
message_receipt_error_response_instance = MessageReceiptErrorResponse.from_json(json)
# print the JSON string representation of the object
print(MessageReceiptErrorResponse.to_json())

# convert the object into a dict
message_receipt_error_response_dict = message_receipt_error_response_instance.to_dict()
# create an instance of MessageReceiptErrorResponse from a dict
message_receipt_error_response_from_dict = MessageReceiptErrorResponse.from_dict(message_receipt_error_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


