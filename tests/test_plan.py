import pytest
from json import JSONDecodeError
from tfplanconverter.plan import Plan


@pytest.fixture()
def plan():
    return Plan()


def test_jsonload(tmp_path_factory, plan):

    ### IF file not found
    with pytest.raises(FileNotFoundError) as e:
        plan.jsonload("fakeplan.plan")

    ### IF content is not valid
    with pytest.raises(JSONDecodeError) as e:
        with (tmp_path_factory.mktemp("data") / "jsondecodeerror.json") as fp:
            fp.write_text("test")
            plan.jsonload(fp.absolute())

    ### IF content is valid
    with (tmp_path_factory.mktemp("data") / "ok.json") as fp:
        fp.write_text('{"ciao": "test"}')
        res = plan.jsonload(fp.absolute())
        assert res == {"ciao": "test"}


def test_getplannedchild(plan):
    inputDataNotValid = {
        "planned_values": {"root_module": {"keynotvalid": [{"resources": [{}]}]}}
    }
    inputDataRecursive = {
        "planned_values": {
            "root_module": {"child_modules": [{"child_modules": [{"resources": [{}]}]}]}
        }
    }

    with pytest.raises(KeyError) as e:
        plan.setRes(inputDataNotValid)
        plan.getplannedchild()

    plan.setRes(inputDataRecursive)
    assert plan.getplannedchild() == [{"resources": [{}]}]


def test_generate_dictionary_for_resource(plan):

    ### IF is EMPTY
    res = [{"resources": []}]
    assert plan.generate_dictionary_for_resource(res) == {}

    ### IF resource structure is incomplete
    res = [{"resources": [{"index": "t"}]}]
    with pytest.raises(KeyError) as e:
        plan.generate_dictionary_for_resource(res)

    ### IF resource structure is correctly
    res = [
        {
            "resources": [
                {"type": "aws_security_group", "index": "test1", "values": {}},
                {
                    "type": "aws_security_group_rule",
                    "index": "test1_rule2",
                    "values": {},
                },
            ]
        }
    ]
    result = plan.generate_dictionary_for_resource(res)
    assert result == {"test1": [{"name": "test1_rule2"}]}


def test_getchangedchild(plan):

    res = {
        "resource_changes": [
            {
                "type": "aws_security_group",
                "index": "test1",
                "change": {"actions": ["create"]},
            }
        ]
    }
    result = plan.getchangedchild(res)
    assert result == False

    res = {
        "resource_changes": [
            {
                "type": "aws_security_group",
                "index": "test1",
                "change": {"actions": ["update"]},
            },
            {
                "type": "aws_security_group",
                "index": "test2",
                "change": {"actions": ["update"]},
            },
            {
                "type": "aws_security_group",
                "index": "test3",
                "change": {"actions": ["update"]},
            },
        ]
    }
    result = plan.getchangedchild(res)
    assert result == True

    res = {
        "resource_changes": [
            {
                "type": "aws_security_group",
                "index": "test1",
                "change": {"actions": ["update"]},
            },
            {"type": "aws_vpc", "index": "test2", "change": {"actions": ["create"]}},
            {"type": "aws_vpc", "index": "test3", "change": {"actions": ["create"]}},
        ]
    }
    result = plan.getchangedchild(res)
    assert result == True

    res = {
        "resource_changes": [
            {
                "type": "aws_security_group",
                "index": "test1",
                "change": {"actions": ["create"]},
            },
            {"type": "aws_vpc", "index": "test2", "change": {"actions": ["update"]}},
            {"type": "aws_vpc", "index": "test3", "change": {"actions": ["update"]}},
        ]
    }
    result = plan.getchangedchild(res)
    assert result == False


def test_getchangedchildlist(plan):

    dict = {
        "default1": [
            {
                "name": "default1_egress_1",
                "cidr_blocks": ["10.0.0.0/8"],
                "description": "None",
                "from_port": "0",
                "ipv6_cidr_blocks": "None",
                "prefix_list_ids": "None",
                "protocol": "-1",
                "to_port": "0",
                "type": "egress",
            },
            {
                "name": "default1_ingress_1",
                "cidr_blocks": ["10.0.0.0/8"],
                "description": "None",
                "from_port": "443",
                "ipv6_cidr_blocks": "None",
                "prefix_list_ids": "None",
                "protocol": "tcp",
                "to_port": "443",
                "type": "ingress",
            },
            {
                "name": "default1_ingress_2",
                "cidr_blocks": ["10.0.0.0/8"],
                "description": "None",
                "from_port": "8080",
                "ipv6_cidr_blocks": "None",
                "prefix_list_ids": "None",
                "protocol": "tcp",
                "to_port": "8080",
                "type": "ingress",
            },
        ]
    }
    res = [
        {
            "type": "aws_security_group",
            "index": "default1",
            "change": {"actions": ["create"]},
        },
        {"type": "aws_vpc", "index": "test2", "change": {"actions": ["update"]}},
        {"type": "aws_vpc", "index": "test3", "change": {"actions": ["update"]}},
    ]

    attended = {
        "default1": [
            {"action": ["create"]},
            {
                "name": "default1_egress_1",
                "cidr_blocks": ["10.0.0.0/8"],
                "description": "None",
                "from_port": "0",
                "ipv6_cidr_blocks": "None",
                "prefix_list_ids": "None",
                "protocol": "-1",
                "to_port": "0",
                "type": "egress",
            },
            {
                "name": "default1_ingress_1",
                "cidr_blocks": ["10.0.0.0/8"],
                "description": "None",
                "from_port": "443",
                "ipv6_cidr_blocks": "None",
                "prefix_list_ids": "None",
                "protocol": "tcp",
                "to_port": "443",
                "type": "ingress",
            },
            {
                "name": "default1_ingress_2",
                "cidr_blocks": ["10.0.0.0/8"],
                "description": "None",
                "from_port": "8080",
                "ipv6_cidr_blocks": "None",
                "prefix_list_ids": "None",
                "protocol": "tcp",
                "to_port": "8080",
                "type": "ingress",
            },
        ]
    }
    assert plan.getchangedchildlist(dict, res) == attended

    res = [
        {
            "type": "aws_security_group",
            "index": "default1",
        }
    ]
    with pytest.raises(KeyError) as e:
        plan.getchangedchildlist(dict, res)


# def test_extractDictionary(plan):
#     plan.jsonload()
#     plan.extractDictionary("yes")


def test_extractDictionary(plan):
    res = {
        "planned_values": {
            "root_module": {"child_modules": [{"child_modules": [{"resources": [{}]}]}]}
        },
        "resource_changes": [
            {
                "type": "aws_security_group",
                "index": "test1",
                "change": {"actions": ["create"]},
            },
            {"type": "aws_vpc", "index": "test2", "change": {"actions": ["update"]}},
            {"type": "aws_vpc", "index": "test3", "change": {"actions": ["update"]}},
        ],
    }
    plan.setRes(res)
    assert plan.extractDictionary("yes") == False

    res = {
        "planned_values": {
            "root_module": {"child_modules": [{"child_modules": [{"resources": [{}]}]}]}
        }
    }
    with pytest.raises(KeyError) as e:
        plan.setRes(res)
        plan.extractDictionary("no") == 0

    res = {
        "planned_values": {
            "root_module": {
                "child_modules": [
                    {
                        "child_modules": [
                            {
                                "resources": [
                                    {
                                        "type": "aws_vpc",
                                        "index": "vpc_test",
                                        "values": {},
                                    },
                                    {
                                        "type": "aws_vpc",
                                        "index": "vpc_test2",
                                        "values": {},
                                    },
                                ]
                            }
                        ]
                    }
                ]
            }
        }
    }
    plan.setRes(res)
    assert plan.extractDictionary("no") == "No Resources"

    # import filecmp
    plan.jsonload("tests/templates/plan_test.plan")
    result = plan.extractDictionary("no")
    attended = {
        "default1": [
            {"action": ["create"]},
            {
                "name": "default1_egress_1",
                "cidr_blocks": ["10.0.0.0/8"],
                "description": None,
                "from_port": 0,
                "ipv6_cidr_blocks": None,
                "prefix_list_ids": None,
                "protocol": "-1",
                "self": False,
                "to_port": 0,
                "type": "egress",
            },
            {
                "name": "default1_ingress_1",
                "cidr_blocks": ["10.0.0.0/8"],
                "description": None,
                "from_port": 443,
                "ipv6_cidr_blocks": None,
                "prefix_list_ids": None,
                "protocol": "tcp",
                "self": False,
                "to_port": 443,
                "type": "ingress",
            },
            {
                "name": "default1_ingress_2",
                "cidr_blocks": ["10.0.0.0/8"],
                "description": None,
                "from_port": 8080,
                "ipv6_cidr_blocks": None,
                "prefix_list_ids": None,
                "protocol": "tcp",
                "self": False,
                "to_port": 8080,
                "type": "ingress",
            },
        ],
        "lambda": [
            {"action": ["create"]},
            {
                "name": "lambda_egress_1",
                "cidr_blocks": ["10.0.0.0/8"],
                "description": None,
                "from_port": 0,
                "ipv6_cidr_blocks": None,
                "prefix_list_ids": None,
                "protocol": "-1",
                "self": False,
                "to_port": 0,
                "type": "egress",
            },
            {
                "name": "lambda_ingress_1",
                "cidr_blocks": ["10.0.0.0/8"],
                "description": None,
                "from_port": 443,
                "ipv6_cidr_blocks": None,
                "prefix_list_ids": None,
                "protocol": "tcp",
                "self": False,
                "to_port": 443,
                "type": "ingress",
            },
            {
                "name": "lambda_ingress_2",
                "cidr_blocks": ["10.0.0.0/8"],
                "description": None,
                "from_port": 8080,
                "ipv6_cidr_blocks": None,
                "prefix_list_ids": None,
                "protocol": "tcp",
                "self": False,
                "to_port": 8080,
                "type": "ingress",
            },
        ],
    }

    assert attended == result


def test_getRes(plan):
    res = {
        "planned_values": {
            "root_module": {"child_modules": [{"child_modules": [{"resources": [{}]}]}]}
        }
    }
    plan.setRes(res)
    assert plan.getRes() == res
