# DynamicTemplateListResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**templates** | [**List[DynamicTemplateResponse]**](DynamicTemplateResponse.md) |  | [optional] 

## Example

```python
from paubox.models.dynamic_template_list_response import DynamicTemplateListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of DynamicTemplateListResponse from a JSON string
dynamic_template_list_response_instance = DynamicTemplateListResponse.from_json(json)
# print the JSON string representation of the object
print(DynamicTemplateListResponse.to_json())

# convert the object into a dict
dynamic_template_list_response_dict = dynamic_template_list_response_instance.to_dict()
# create an instance of DynamicTemplateListResponse from a dict
dynamic_template_list_response_from_dict = DynamicTemplateListResponse.from_dict(dynamic_template_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


