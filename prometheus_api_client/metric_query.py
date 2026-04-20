from collections.abc import Sequence
from typing import Dict,Tuple,Union,Optional
from enum import StrEnum
from functools import reduce
import logging

class LabelQueryOp(StrEnum):
    EQUAL='='
    NOT_EQUAL='!='
    REGEX_EQUAL='=~'
    REGEX_NOT_EQUAL='!~'

LabelQuery=Union[str,Tuple[LabelQueryOp, str]]
MetricLabelQuery = Dict[str,LabelQuery]

def query_to_str(metric_name: str, label_query: Optional[MetricLabelQuery]=None)->str:
    """
    Contruct query string from label query dictionary
    
    :param label_query: (MetricLabelQuery) The label query dictionary. Default is None
    :return: (str) Query string inside brackets
    :raises:
        (ValueError) Raises an exception in case of an invalid label query operator
    """
    if not label_query:
        return metric_name
    def _format_label_query(label_key: str, label: LabelQuery)->str:
        if isinstance(label, Sequence) and not isinstance(label, str):
            if len(label) != 2:
                raise ValueError(f"wrong number of elements in label query with operator: {len(label)} instead of 2")
            label_op=label[0]
            if label_op not in LabelQueryOp:
                raise ValueError(f"unknown label operator: '{label_op}'")
            label_value=label[1]
            return f"{label_key}{label_op}'{label_value}'"
        else:
            return f"{label_key}{LabelQueryOp.EQUAL}'{label}'"
    label_list=[_format_label_query(label_key, label) for label_key, label in label_query.items()]
    return  metric_name + "{" + ",".join(label_list) + "}"
