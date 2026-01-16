# DynamicTemplateResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Template ID | [optional] 
**name** | **str** | Template name | [optional] 
**body** | **str** | Template content (Handlebars) | [optional] 
**created_at** | **datetime** | Template creation timestamp | [optional] 
**updated_at** | **datetime** | Template last update timestamp | [optional] 

## Example

```python
from paubox.models.dynamic_template_response import DynamicTemplateResponse

# TODO update the JSON string below
json = "{}"
# create an instance of DynamicTemplateResponse from a JSON string
dynamic_template_response_instance = DynamicTemplateResponse.from_json(json)
# print the JSON string representation of the object
print(DynamicTemplateResponse.to_json())

# convert the object into a dict
dynamic_template_response_dict = dynamic_template_response_instance.to_dict()
# create an instance of DynamicTemplateResponse from a dict
dynamic_template_response_from_dict = DynamicTemplateResponse.from_dict(dynamic_template_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


