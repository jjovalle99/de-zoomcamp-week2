if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

def camel_to_snake(name):
    import re
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.lower()


@transformer
def transform(data, *args, **kwargs):
    data = data[(data['passenger_count'] > 0) & (data['trip_distance'] > 0)]
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date

    old_columns = data.columns
    data.columns = [camel_to_snake(col) for col in data.columns]

    print(f'Unique values for `vendor_id`: {sorted(data.vendor_id.unique().tolist())}')
    print(f'Columns renamed: {len(set(old_columns).difference(set(data.columns)))}')
    return data


@test
def test_output(output, *args) -> None:
    assert 'vendor_id' in output.columns, 'vendor_id not in columns'
    assert (output['passenger_count'] > 0).all(), 'There are rows with passenger_count <= 0' 
    assert (output['trip_distance'] > 0).all(), 'There are rows with trip_distance <= 0'
    assert output is not None, 'The output is undefined'
