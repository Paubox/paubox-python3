# BulkSendRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**BulkSendRequestData**](BulkSendRequestData.md) |  | 

## Example

```python
from paubox.models.bulk_send_request import BulkSendRequest

# TODO update the JSON string below
json = "{}"
# create an instance of BulkSendRequest from a JSON string
bulk_send_request_instance = BulkSendRequest.from_json(json)
# print the JSON string representation of the object
print(BulkSendRequest.to_json())

# convert the object into a dict
bulk_send_request_dict = bulk_send_request_instance.to_dict()
# create an instance of BulkSendRequest from a dict
bulk_send_request_from_dict = BulkSendRequest.from_dict(bulk_send_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


