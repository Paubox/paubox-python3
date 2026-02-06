# TemplatedMessageHeaders


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**subject** | **str** | Message subject (can include template variables) | 
**var_from** | **str** | Must match the verified domain of your API key. | 
**reply_to** | **str** | Reply-to address; must match a verified domain if different from from. | [optional] 
**list_unsubscribe** | **str** | Insert a List-Unsubscribe header (mailto and/or http). See RFC guidance for syntax.  | [optional] 
**list_unsubscribe_post** | **str** | Used in conjunction with List-Unsubscribe header. | [optional] 
**additional_properties** | **str** | Any additional custom header values. | [optional] 

## Example

```python
from paubox.models.templated_message_headers import TemplatedMessageHeaders

# TODO update the JSON string below
json = "{}"
# create an instance of TemplatedMessageHeaders from a JSON string
templated_message_headers_instance = TemplatedMessageHeaders.from_json(json)
# print the JSON string representation of the object
print(TemplatedMessageHeaders.to_json())

# convert the object into a dict
templated_message_headers_dict = templated_message_headers_instance.to_dict()
# create an instance of TemplatedMessageHeaders from a dict
templated_message_headers_from_dict = TemplatedMessageHeaders.from_dict(templated_message_headers_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


