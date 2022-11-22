import pytest
from tfplanconverter.converter import *


@pytest.fixture()
def converter():
    return Converter()


def test_read_template(tmp_path_factory, converter):

    with pytest.raises(jinja2.exceptions.TemplateNotFound) as e:
        converter.read_template({}, "faketemplate.html.j2")

    with pytest.raises(jinja2.exceptions.TemplateSyntaxError) as exc:
        with (tmp_path_factory.mktemp("data") / "file.html.j2") as fp:
            fp.write_text("{% endfor %}")
            converter.read_template({}, fp.absolute())

    with (tmp_path_factory.mktemp("data") / "test.html") as fp:
        fp.write_text("<div>\n</div>")
        assert (
            converter.read_template({}, "tests/templates/template.html.j2")
            == fp.read_text()
        )


def test_writefile(tmp_path_factory, converter):

    with (tmp_path_factory.mktemp("data") / "content-error.html") as fp:
        content = "<html><head></head><body></body></html>"
        converter.write_file(content, fp.absolute())

        got = fp.read_text()
        assert got == "<html><head></head><body></body></html>"


def test_convertTxt(converter):

    dict = {
        "default1": [
            {
                "name": "default1_egress_1",
                "cidr_blocks": ["10.0.0.0/8"],
                "description": "None",
                "from_port": 0,
                "ipv6_cidr_blocks": "None",
                "prefix_list_ids": "None",
                "protocol": "-1",
                "to_port": 0,
                "type": "egress",
            }
        ]
    }
    with pytest.raises(Exception):
        converter.convertTxt(dict, "tests/templates/template.html.j2")

    dict = {
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
    wfile = converter.convertTxt(dict, "templates/templateText.txt.j2")
    with open("tests/templates/testoutputmyfile.txt", "r") as file1, open(
        wfile, "r"
    ) as file2:
        file1_lines = file1.readlines()
        file2_lines = file2.readlines()

        for i in range(len(file1_lines)):
            assert file2_lines[i].strip() == file1_lines[i].strip()


def test_convertHtml(converter):

    dict = {
        "default1": [
            {
                "name": "default1_egress_1",
                "cidr_blocks": ["10.0.0.0/8"],
                "description": "None",
                "from_port": 0,
                "ipv6_cidr_blocks": "None",
                "prefix_list_ids": "None",
                "protocol": "-1",
                "to_port": 0,
                "type": "egress",
            }
        ]
    }
    with pytest.raises(Exception):
        converter.convertHtml(dict, "tests/templates/templateText.txt.j2")

    dict = {
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

    wfile = converter.convertHtml(dict, "templates/templateHtml.html.j2")
    with open("tests/templates/testoutputmyfile.html", "r") as file1, open(
        wfile, "r"
    ) as file2:
        file1_lines = file1.readlines()
        file2_lines = file2.readlines()

        for i in range(len(file1_lines)):
            assert file2_lines[i].strip() == file1_lines[i].strip()
