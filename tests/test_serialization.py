"""Test tessifs serialization capabilities."""

import pytest
from tessif_examples import basic, scientific

from tessif.system_model import AbstractEnergySystem as Aes  # nopep8

basic_creates = [attr for attr in dir(basic) if "create" in attr]


@pytest.mark.parametrize("system_model_name", basic_creates)
def test_basic_es_serialization(system_model_name):
    """Test to and from json serialization."""
    es = getattr(basic, system_model_name)()
    json_stream = es.serialize()
    parsed_es = Aes.deserialize(json_stream)

    for es_attr in es._es_attributes:
        # compare timeframes
        if es_attr == "timeframe":
            assert getattr(es, es_attr).equals(getattr(parsed_es, es_attr))

        # compare global_constraints
        elif es_attr == "global_constraints":
            assert getattr(es, es_attr) == getattr(parsed_es, es_attr)

        # compare components
        else:
            for es_node, pes_node in zip(getattr(es, es_attr), getattr(es, es_attr)):
                for es_attr, pes_attr in zip(
                    es_node.attributes.values(), pes_node.attributes.values()
                ):
                    assert es_attr == pes_attr


scientific_creates = [attr for attr in dir(scientific) if "create" in attr]


@pytest.mark.parametrize("system_model_name", scientific_creates)
def test_scientific_es_serialization(system_model_name):
    """Test to and from json serialization."""
    es = getattr(scientific, system_model_name)()
    json_stream = es.serialize()
    parsed_es = Aes.deserialize(json_stream)

    for es_attr in es._es_attributes:
        # compare timeframes
        if es_attr == "timeframe":
            assert getattr(es, es_attr).equals(getattr(parsed_es, es_attr))

        # compare global_constraints
        elif es_attr == "global_constraints":
            assert getattr(es, es_attr) == getattr(parsed_es, es_attr)

        # compare components
        else:
            for es_node, pes_node in zip(getattr(es, es_attr), getattr(es, es_attr)):
                for es_attr, pes_attr in zip(
                    es_node.attributes.values(), pes_node.attributes.values()
                ):
                    assert es_attr == pes_attr
