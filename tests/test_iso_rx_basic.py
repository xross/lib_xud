# Copyright 2016-2025 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.
import pytest

from conftest import PARAMS, test_RunUsbSession  # noqa F401
from usb_session import UsbSession
from usb_transaction import UsbTransaction


@pytest.fixture
def test_session(ep, address, bus_speed):

    start_length = 10
    end_length = start_length + 4

    session = UsbSession(
        bus_speed=bus_speed, run_enumeration=False, device_address=address
    )

    interTransactionDelay = 25  # Fail at 24

    for pktLength in range(start_length, end_length + 1):
        session.add_event(
            UsbTransaction(
                session,
                deviceAddress=address,
                endpointNumber=ep,
                endpointType="ISO",
                transType="OUT",
                dataLength=pktLength,
                interEventDelay=interTransactionDelay,
            )
        )

    return session
