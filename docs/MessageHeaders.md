# MessageHeaders


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**subject** | **str** |  | 
**var_from** | **str** | Must match the verified domain of your API key. | 
**reply_to** | **str** | Reply-to address; must match a verified domain if different from from. | [optional] 
**list_unsubscribe** | **str** | Insert a List-Unsubscribe header (mailto and/or http). See RFC guidance for syntax.  | [optional] 
**list_unsubscribe_post** | **str** | Used in conjunction with List-Unsubscribe header. | [optional] 
**x_custom_header** | **str** | Example custom header; any custom header may be added with an X- prefix. | [optional] 
**additional_properties** | **str** | Any additional X- prefixed custom header values. | [optional] 

## Example

```python
from paubox.models.message_headers import MessageHeaders

# TODO update the JSON string below
json = "{}"
# create an instance of MessageHeaders from a JSON string
message_headers_instance = MessageHeaders.from_json(json)
# print the JSON string representation of the object
print(MessageHeaders.to_json())

# convert the object into a dict
message_headers_dict = message_headers_instance.to_dict()
# create an instance of MessageHeaders from a dict
message_headers_from_dict = MessageHeaders.from_dict(message_headers_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


