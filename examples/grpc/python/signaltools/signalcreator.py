import grpc
import sys

sys.path.append("../../common")
import common_pb2
import network_api_pb2


class SignalCreator:
    def __init__(self, system_stub):
        self._sinfos = {}
        self._virtual = []
        self._networks = {}
        namespaces = []
        conf = system_stub.GetConfiguration(common_pb2.Empty())
        for ninfo in conf.networkInfo:
            namespaces.append(ninfo.namespace)
            if ninfo.type == "virtual":
                self._virtual.append(ninfo.namespace.name)
        for namespace in namespaces:
            res = system_stub.ListSignals(namespace)
            self._addframes(namespace, res)
            for finfo in res.frame:
                self._add(finfo.signalInfo)
                for sinfo in finfo.childInfo:
                    self._add(sinfo)

    def _addframes(self, namespace, res):
        self._networks[namespace.name] = res

    def _add(self, sinfo):
        k = (sinfo.id.namespace.name, sinfo.id.name)
        if k in self._sinfos:
            raise Exception(f"duplicate (namespace,signal): {k}")
        self._sinfos[k] = sinfo.metaData

    def signal(self, name, namespace_name):
        k = (namespace_name, name)
        if (k not in self._sinfos) and (namespace_name not in self._virtual):
            raise Exception(f"signal not declared (namespace, signal): {k}")
        return common_pb2.SignalId(
            name=name, namespace=common_pb2.NameSpace(name=namespace_name)
        )

    def frames(self, namespace_name):
        all_frames = []
        for finfo in self._networks[namespace_name].frame:
            all_frames.append(self.signal(finfo.signalInfo.id.name, namespace_name))
            # all_frames.append(finfo) 
        return all_frames

    def frame_by_signal(self, name, namespace_name):
        for finfo in self._networks[namespace_name].frame:
            for sinfo in finfo.childInfo:
                if sinfo.id.name == name:
                    return self.signal(finfo.signalInfo.id.name, namespace_name)
        raise Exception(f"signal not declared (namespace, signal): {namespace_name} {name}")

    def signals_in_frame(self, name, namespace_name):
        all_signals = []
        frame = None
        for finfo in self._networks[namespace_name].frame:
            if finfo.signalInfo.id.name == name:
                frame = finfo
                for sinfo in finfo.childInfo:
                    all_signals.append(self.signal(sinfo.id.name, namespace_name))
        assert frame != None, f"frame {name} does not exist in namespace {namespace_name}"
        assert all_signals != [], f"frame {name} {namespace_name} does not have childs"
        return all_signals

    def signal_with_payload(self, name, namespace_name, value_pair, allow_malformed = False):
        signal = self.signal(name, namespace_name)

        key, value = value_pair
        types = ["integer", "double", "raw", "arbitration"]
        if key not in types:
            raise Exception(f"type must be one of: {types}")
        if key is "raw" and allow_malformed is False:
            assert len(value)*8 == self._sinfos[(namespace_name, name)].size, f"payload size missmatch, expected {self._sinfos[(namespace_name, name)].size/8} bytes"
        params = {"id": signal, key: value}
        return network_api_pb2.Signal(**params)

        # Above is simlar as this, but parameterised.
        # return network_api_pb2.Signal(
        #     id=signal, value_dict.get_key=value_dict["integer"]
        # )
