import grpc
import sys

sys.path.append("../../common")
import common_pb2
import network_api_pb2


class SignalCreator:
    def __init__(self, system_stub):
        self._sinfos = {}
        self._virtual = []
        namespaces = []
        conf = system_stub.GetConfiguration(common_pb2.Empty())
        for ninfo in conf.networkInfo:
            namespaces.append(ninfo.namespace)
            if ninfo.type == "virtual":
                self._virtual.append(ninfo.namespace.name)
        for namespace in namespaces:
            res = system_stub.ListSignals(namespace)
            for finfo in res.frame:
                self._add(finfo.signalInfo)
                for sinfo in finfo.childInfo:
                    self._add(sinfo)

    def _add(self, sinfo):
        k = (sinfo.id.namespace.name, sinfo.id.name)
        if k in self._sinfos:
            raise Exception(f"duplicate (namespace,signal): {k}")
        self._sinfos[k] = True

    def signal(self, name, namespace):
        k = (namespace, name)
        if (k not in self._sinfos) and (namespace not in self._virtual):
            raise Exception(f"signal not declared (namespace, signal): {k}")
        return common_pb2.SignalId(
            name=name, namespace=common_pb2.NameSpace(name=namespace)
        )

    def signal_with_payload(self, name, namespace, value_pair):
        signal = self.signal(name, namespace)

        key, value = value_pair
        types = ["integer", "double", "raw", "arbitration"]
        if key not in types:
            raise Exception(f"type must be one of: {types}")
        params = {"id": signal, key: value}
        return network_api_pb2.Signal(**params)

        # Above is simlar as this, but parameterised.
        # return network_api_pb2.Signal(
        #     id=signal, value_dict.get_key=value_dict["integer"]
        # )
