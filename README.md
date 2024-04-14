# TRANSPORT_PLANNING_NEW

This is newer version of original Transport planning project ([link](https://github.com/StefanGlova/transport-planning)). It is re-built from scratch, using knowledge and algorithms from the original. It is built on Test Driver Developement principle, where I write failing test first, then code to make test passed, then re-factor and another failing test, etc. It also uses OOP, coparing with declarative approach in the original.

## Modules

The project is made of modules where each module is reponsible for a part of the project.

## 1. Data processing module

This module is design to take file path as parameter and optional parameter 'diamiter' and create object from GeneralFileParser class. When calling parse method, it returns dataset python list containing dictionary object for each line, where key is header of original file and value of line is value.

**Example Input**

```
|'Customer Name' |'Customer Postcode' |'SKU'  |'Qty' |'Vehicle Type' |'Due Date'  |
|'Bob'           |'N9 9LA'            |'SKU1' |'100' |'trailer'      |'2023-11-10'|
```

**Example Output**

```
parsed_data = [
    {
        "Customer Name": "Bob",
        "Customer Postcode": "N9 9LA",
        "SKU": "SKU1",
        "Qty": "100",
        "Vehicle Type": "trailer",
        "Due Date": "2023-11-10",
    }
]
```

The other class of data processing module is specific for content of file, ensuring that all infomation for further algoritm are correct:

### a ProcessInventory class

The object created from this class takes one paramenter - parsed_data, which is outcome of GeneralFileParser class when calling parse method.

The method in this class is parse_inventory, and it returns python dictionary with SKU as key and quantity as value. It checks that parsed_data have correct fields and both are of correct type - it must have SKU as string and Qty as number which cannot be negative.

It is general practice that one SKU may be stored in multiple different locations in real warehouse, so when calling parse_inventory method, the returned dictionary add values together for each SKU to ensure each SKU is in the outcome only once.

It raises custom created Errors for following reasons:

1. WrongKeyError - if any dictionary in parsed_data list has either missing key, or got an extra key or any of the keys is wrong - different than expected. It raises this error also, if parsed_data is empty list.

2. WrongValueTypeError - if 'Qty' field contain value which cannot be converted to number.

3. WrongNumericRange - if 'Qty' field is negative number

**Example Input**

```
parsed_data = [
    {
        "SKU": "SKU1",
        "Qty": "15",
    },
    {
        "SKU": "SKU2",
        "Qty": "0",
    },
    {
        "SKU": "SKU1",
        "Qty": "5",
    },
]
```

**Example Output**

```
orderbook = {
    "SKU1": 20,
    "SKU2": 0
}
```

### b ProcessOrderbook class

Similar to ProcessInventory, this one takes prased_data as an input, and checks if all fields are correct. The fields must be 'Customer Name' as string, 'Customer Postcode' as string, 'SKU' as string, 'Qty' as number which cannot be negative, 'Vehicle Type' as string, which should be either 'trailer' or 'rigid' and if it is different it let process further, but allocate any different in outcome to 'ERROR' list for further inventigation and finally 'Due Date' which is of date format.

When parse_orderbook method is called, it iterates through input list for every line, check for vehicle type and split lines into three categories - 'trailer', 'rigid' and 'ERROR'.

It raises customer created Errors for following reasons:

1. WrongKeyError - if any dictionary in parsed_data list has either missing key, or got an extra key or any of the keys is wrong - different than expected. It raises this error also, if parsed_data is empty list.

2. WrongValueTypeError - if 'Qty' field contain value which cannot be converted to number; or if 'Due Date' contain value which cannot be converted to date using datetime module.

3. WrongNumericRange - if 'Qty' field is negative number

**Example Input**

```
parsed_data = [
    {
        "Customer Name": "Alice",
        "Customer Postcode": "E1W 2RG",
        "SKU": "SKU123",
        "Qty": "57",
        "Vehicle Type": "trailer",
        "Due Date": "2024-04-10",
    },
    {
        "Customer Name": "Bob",
        "Customer Postcode": "N9 9LA",
        "SKU": "SKU456",
        "Qty": "1000",
        "Vehicle Type": "trailer",
        "Due Date": "2023-11-10",
    }
]
```

**Example Output**

```
orderbook = {
    "trailer": [
        {
            "Customer Name": "Alice",
            "Customer Postcode": "E1W 2RG",
            "SKU": "SKU123",
            "Qty": "57",
            "Due Date": "2024-04-10",
        },
        {
            "Customer Name": "Bob",
            "Customer Postcode": "N9 9LA",
            "SKU": "SKU456",
            "Qty": "1000",
            "Due Date": "2023-11-10",
        }
    ],
    "rigid": []
}
```

### c ProcessPostcode class

Similar to both, ProcessOrderbook class and ProcessInventory class, thsi one takes parsed_data as an input, and checks if all fields are correct. the fileds must be 'Postcode' as string, 'Latitude' as decimal number between -90 and +90; and 'Longitude' as decimal number between -180 and +180.

When parse_postcode method is successfully run, it return dictionary object with Postcodes as keys and for each postcode as value are 2 other dictionaries - latitude and its value and longitude and its value.

It raises customer created Errors for following reasons:

1. WrongKeyError - if any dictionary in parsed_data list has either missing key or got an extra key or any of the keys is wrong - different than expected. It raises this error also, if parsed_data is empty list.

2. WrongValueTypeError - if 'Latitude' or 'Longitude' does not have numeric values.

3. WrongNumericRange - if 'Latitude' is not in range of -90 and +90, or if 'Lontitude' is not in range of -180 and +180.

**Example Input**

```
parsed_data = [
    {
        "Postcode": "ABC",
        "Latitude": "1.123456",
        "Longitude": "50.123456"
    },
    {
        "Latitude": "1.987654",
        "Postcode": "EFG",
        "Longitude": "50.654987"
    },
]
```

**Example Output**

```
postcodes = {
    "ABC": {
        "Latitude": "1.123456",
        "Longitude": "50.123456"
    },
    "EFG": {
        "Latitude": "1.987654",
        "Longitude": "50.654987"
    }
}

```
