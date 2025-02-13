import os
import re


def validate(data_dict, validators):
    errors = []
    if data_dict is None or validators is None:
        errors.append("Invalid input data")
        return errors

    for key in validators:
        if key not in data_dict:
            errors.append(f"Missing key: {key}")
        else:
            for method in validators[key]:
                if not method(data_dict[key]):
                    errors.append(f"Invalid value for key: {key}")
    return errors
