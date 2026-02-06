# BulkSendResponseMessagesInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**source_tracking_id** | **str** |  | [optional] 
**custom_headers** | **Dict[str, str]** |  | [optional] 
**data** | **str** |  | [optional] 

## Example

```python
from paubox.models.bulk_send_response_messages_inner import BulkSendResponseMessagesInner

# TODO update the JSON string below
json = "{}"
# create an instance of BulkSendResponseMessagesInner from a JSON string
bulk_send_response_messages_inner_instance = BulkSendResponseMessagesInner.from_json(json)
# print the JSON string representation of the object
print(BulkSendResponseMessagesInner.to_json())

# convert the object into a dict
bulk_send_response_messages_inner_dict = bulk_send_response_messages_inner_instance.to_dict()
# create an instance of BulkSendResponseMessagesInner from a dict
bulk_send_response_messages_inner_from_dict = BulkSendResponseMessagesInner.from_dict(bulk_send_response_messages_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


