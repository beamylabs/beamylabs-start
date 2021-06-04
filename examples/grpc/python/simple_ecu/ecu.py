#!/usr/bin/env python3

import asyncio

import os
import time
import binascii

from grpclib.client import Channel
import sys, getopt

sys.path.append("../common")
from generated_betterproto.base import *
from helper import *


def read_signal(stub, signal):
    """Read signals

    Parameters
    ----------
    stub : NetworkServiceStub
        Object instance of class
    signal : SignalId
        Object instance of class

    Returns
    -------
    Signals
        Object instance of class

    """
    return stub.read_signals(signal_id=[signal])


async def publish_signals(client_id, stub, signals_with_payload):
    """Publish signals

    Parameters
    ----------
    client_id : ClientId
        Object instance of class
    stub : NetworkServiceStub
        Object instance of class
    signals_with_payload : Signal
        Object instance of class

    """
    try:
        await stub.publish_signals(
            client_id=client_id,
            signals=Signals(signal=signals_with_payload),
            frequency=0,
        )
    except Exception as err:
        print(err)


increasing_counter = 0


async def ecu_A(stub, pause):
    """Publishes a value, read other value (published by ecu_B)

    Parameters
    ----------
    stub : NetworkServiceStub
        Object instance of class
    pause : int
        Amount of time to pause, in seconds

    """
    while True:
        global increasing_counter
        namespace = "ecu_A"
        clientId = ClientId(id="id_ecu_A")

        # Publishes value 'counter'
        counter = SignalId(name="counter", namespace=NameSpace(name=namespace))
        counter_with_payload = Signal(id=counter, integer=increasing_counter)
        await publish_signals(clientId, stub, [counter_with_payload])
        print("\necu_A, seed is ", increasing_counter)

        time.sleep(pause)

        # Read the other value 'counter_times_2' and output result
        counter_times_2 = SignalId(
            name="counter_times_2", namespace=NameSpace(name=namespace)
        )
        read_counter_times_2 = await read_signal(stub, counter_times_2)
        print(
            "ecu_A, (result) counter_times_2 is ",
            read_counter_times_2.signal[0].integer,
        )
        increasing_counter = (increasing_counter + 1) % 4


async def ecu_B_read(stub, pause):
    """Read a value published by ecu_A

    Parameters
    ----------
    stub : NetworkServiceStub
        Object instance of class
    pause : int
        Amount of time to pause, in seconds

    """
    while True:
        namespace = "ecu_B"
        client_id = ClientId(id="id_ecu_B")

        # Read value 'counter'
        counter = SignalId(name="counter", namespace=NameSpace(name=namespace))
        read_counter = await read_signal(stub, counter)
        print("ecu_B, (read) counter is ", read_counter.signal[0].integer)

        time.sleep(pause)


async def ecu_B_subscribe(stub):
    """Subscribe to a value published by ecu_A and publish doubled value back to ecu_A

    Parameters
    ----------
    stub : NetworkServiceStub
        Object instance of class

    """
    namespace = "ecu_B"
    client_id = ClientId(id="id_ecu_B")

    # Subscribe to value 'counter'
    counter = SignalId(name="counter", namespace=NameSpace(name=namespace))
    # Publish doubled value as 'counter_times_2'
    try:
        async for subs_counter in stub.subscribe_to_signals(
            client_id=client_id,
            signals=SignalIds(signal_id=[counter]),
            on_change=True,
        ):
            for signal in subs_counter.signal:
                print("ecu_B, (subscribe) counter is ", signal.integer)
                counter_times_2 = SignalId(
                    name="counter_times_2",
                    namespace=NameSpace(name=namespace),
                )
                signal_with_payload = Signal(
                    id=counter_times_2, integer=signal.integer * 2
                )
                await publish_signals(client_id, stub, [signal_with_payload])

    except Exception as err:
        print(err)


def read_on_timer(stub, signals, pause):
    """Simple reading with timer, logs on purpose tabbed with double space

    Parameters
    ----------
    stub : NetworkServiceStub
        Object instance of class
    signals : SignalId
        Object instance of class
    pause : int
        Amount of time to pause, in seconds

    """
    while True:
        read_info = SignalIds(signal_id=signals)
        try:
            response = stub.read_signals(read_info)
            for signal in response.signal:
                print(
                    "  read_on_timer "
                    + signal.id.name
                    + " value "
                    + str(signal.integer)
                )
        except Exception as err:
            print(err)
        time.sleep(pause)


async def main(argv):
    """Main function, checking arguments passed to script, setting up stubs, configuration and starting tasks.

    Parameters
    ----------
    argv : list
        Arguments passed when starting script

    """
    # Checks argument passed to script, ecu.py will use below ip-address if no argument is passed to the script
    ip = "127.0.0.1"
    # Keep this port
    port = "50051"
    try:
        opts, args = getopt.getopt(argv, "h", ["ip="])
    except getopt.GetoptError:
        print("Usage: ecu.py --ip <ip_address>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("Usage: ecu.py --ip <ip_address>")
            sys.exit(2)
        elif opt == "--ip":
            ip = arg

    # Setting up stubs and configuration
    async with Channel(host=ip, port=port) as channel:
        network_stub = NetworkServiceStub(channel)
        system_stub = SystemServiceStub(channel)
        await check_license(system_stub)

        await upload_folder(system_stub, "configuration_udp")
        # upload_folder(system_stub, "configuration_lin")
        # upload_folder(system_stub, "configuration_can")
        await reload_configuration(system_stub)

        # Lists available signals
        configuration = await system_stub.get_configuration()
        for info in configuration.network_info:
            print(
                "signals in namespace ",
                info.namespace.name,
                await system_stub.list_signals(name=info.namespace.name),
            )

        # python3.7+: can use neater create_task() instead of ensure_future()
        ecu_A_task = asyncio.ensure_future(ecu_A(network_stub, 1))
        ecu_B_read_task = asyncio.ensure_future(ecu_B_read(network_stub, 1))
        ecu_B_subscribe_task = asyncio.ensure_future(ecu_B_subscribe(network_stub))

        await ecu_A_task

        # read_signals = [common_pb2.SignalId(name="counter", namespace=common_pb2.NameSpace(name = "ecu_A")), common_pb2.SignalId(name="TestFr06_Child02", namespace=common_pb2.NameSpace(name = "ecu_A"))]
        # ecu_read_on_timer  = Thread(target = read_on_timer, args = (network_stub, read_signals, 10))
        # ecu_read_on_timer.start()


if __name__ == "__main__":
    # python3.7+: may be simplified as: asyncio.run(main(sys.argv[1:]))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(sys.argv[1:]))
