import os
from project import get_command_and_device, get_device_dict
from netbot import NetBot


# set environment variables for logging into devices
os.environ["NTWK_USERNAME"] = "tester"
os.environ["NTWK_PASSWORD"] = "testerpw"


def test_get_device_dict_rt1():
    # Existing device
    assert get_device_dict("rt1") == {
        "host": "vios-rt1.jm",
        "device_type": "cisco_ios",
        "username": "tester",
        "password": "testerpw",
    }


def test_get_device_dict_rt2():
    # Existing device
    assert get_device_dict("rt2") == {
        "host": "vios-rt2.jm",
        "device_type": "cisco_ios",
        "username": "tester",
        "password": "testerpw",
    }


def test_get_device_dict_rt3():
    # Non-existent device
    assert get_device_dict("rt3") == None


def test_get_command_and_device_invalid():
    # string is missing " device=" delimiter
    assert get_command_and_device("netbot get interface device rt1") == (None, None)


def test_get_command_and_device_invalid():
    # device does not exist
    assert get_command_and_device("netbot get interface device=rt3") == (
        "netbot get interface",
        None,
    )


def test_get_command_and_device_rt1():
    assert get_command_and_device("netbot get interface device=rt1") == (
        "netbot get interface",
        {
            "host": "vios-rt1.jm",
            "device_type": "cisco_ios",
            "username": "tester",
            "password": "testerpw",
        },
    )


def test_get_command_and_device_rt2():
    assert get_command_and_device("netbot get interface device=rt2") == (
        "netbot get interface",
        {
            "host": "vios-rt2.jm",
            "device_type": "cisco_ios",
            "username": "tester",
            "password": "testerpw",
        },
    )


def test_netbot_command_interface():
    netbot = NetBot(
        "netbot get interface info",
        {
            "host": "vios-rt2.jm",
            "device_type": "cisco_ios",
            "username": "tester",
            "password": "testerpw",
        },
    )

    assert (
        netbot.get_output()[:60]
        == "Interface                  IP-Address      OK? Method Status"
    )


def test_netbot_command_route():
    netbot = NetBot(
        "netbot get routes",
        {
            "host": "vios-rt2.jm",
            "device_type": "cisco_ios",
            "username": "tester",
            "password": "testerpw",
        },
    )

    assert netbot.get_output()[:22] == "Gateway of last resort"


def test_netbot_invalid_command():
    netbot = NetBot(
        "netbot foo",
        {
            "host": "vios-rt2.jm",
            "device_type": "cisco_ios",
            "username": "tester",
            "password": "testerpw",
        },
    )

    assert netbot.get_output() == (
        f"Command 'netbot foo' is invalid or currently unsupported."
        "Say `netbot help` for list of valid commands."
    )


def test_netbot_invalid_device():
    netbot = NetBot(
        "netbot get routes",
        {
            "host": "192.168.128.244",
            "device_type": "cisco_ios",
            "username": "tester",
            "password": "testerpw",
        },
    )

    assert netbot.get_output() == (
        f"There was a problem connecting to 192.168.128.244\n\n"
    )
