# SingleSendRequestData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | [**Message**](Message.md) |  | 
**override_open_tracking** | **bool** | Set to true to enable open tracking for this message. | [optional] 
**override_link_tracking** | **bool** | Set to true to enable click tracking for this message (up to 1000 links). | [optional] 
**unsubscribe_url** | **str** | URL to redirect unsubscribe requests for unsubscribe tracking. | [optional] 

## Example

```python
from paubox.models.single_send_request_data import SingleSendRequestData

# TODO update the JSON string below
json = "{}"
# create an instance of SingleSendRequestData from a JSON string
single_send_request_data_instance = SingleSendRequestData.from_json(json)
# print the JSON string representation of the object
print(SingleSendRequestData.to_json())

# convert the object into a dict
single_send_request_data_dict = single_send_request_data_instance.to_dict()
# create an instance of SingleSendRequestData from a dict
single_send_request_data_from_dict = SingleSendRequestData.from_dict(single_send_request_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


