# ClickData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**click_count** | **int** | Number of clicks on this specific link | 
**target_url** | **str** | The URL that was clicked | 

## Example

```python
from paubox.models.click_data import ClickData

# TODO update the JSON string below
json = "{}"
# create an instance of ClickData from a JSON string
click_data_instance = ClickData.from_json(json)
# print the JSON string representation of the object
print(ClickData.to_json())

# convert the object into a dict
click_data_dict = click_data_instance.to_dict()
# create an instance of ClickData from a dict
click_data_from_dict = ClickData.from_dict(click_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


