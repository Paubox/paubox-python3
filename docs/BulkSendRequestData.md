# BulkSendRequestData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**messages** | [**List[Message]**](Message.md) | Recommended 50 or fewer per request. | 

## Example

```python
from paubox.models.bulk_send_request_data import BulkSendRequestData

# TODO update the JSON string below
json = "{}"
# create an instance of BulkSendRequestData from a JSON string
bulk_send_request_data_instance = BulkSendRequestData.from_json(json)
# print the JSON string representation of the object
print(BulkSendRequestData.to_json())

# convert the object into a dict
bulk_send_request_data_dict = bulk_send_request_data_instance.to_dict()
# create an instance of BulkSendRequestData from a dict
bulk_send_request_data_from_dict = BulkSendRequestData.from_dict(bulk_send_request_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


