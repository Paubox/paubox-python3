# DeliveryStatus


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**delivery_status** | **str** | The delivery status of the message | 
**delivery_time** | **str** | The time when the message was delivered (if applicable) | [optional] 
**opened_status** | **str** | Whether the message was opened (single recipient only) | [optional] 
**opened_time** | **str** | The time when the message was first opened (single recipient only) | [optional] 

## Example

```python
from paubox.models.delivery_status import DeliveryStatus

# TODO update the JSON string below
json = "{}"
# create an instance of DeliveryStatus from a JSON string
delivery_status_instance = DeliveryStatus.from_json(json)
# print the JSON string representation of the object
print(DeliveryStatus.to_json())

# convert the object into a dict
delivery_status_dict = delivery_status_instance.to_dict()
# create an instance of DeliveryStatus from a dict
delivery_status_from_dict = DeliveryStatus.from_dict(delivery_status_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


