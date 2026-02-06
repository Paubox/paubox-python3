# BulkSendResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**messages** | [**List[BulkSendResponseMessagesInner]**](BulkSendResponseMessagesInner.md) |  | [optional] 

## Example

```python
from paubox.models.bulk_send_response import BulkSendResponse

# TODO update the JSON string below
json = "{}"
# create an instance of BulkSendResponse from a JSON string
bulk_send_response_instance = BulkSendResponse.from_json(json)
# print the JSON string representation of the object
print(BulkSendResponse.to_json())

# convert the object into a dict
bulk_send_response_dict = bulk_send_response_instance.to_dict()
# create an instance of BulkSendResponse from a dict
bulk_send_response_from_dict = BulkSendResponse.from_dict(bulk_send_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


