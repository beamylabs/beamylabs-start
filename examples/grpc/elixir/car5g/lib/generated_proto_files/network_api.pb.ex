defmodule Base.SubscriberConfig do
  @moduledoc false
  use Protobuf, syntax: :proto3

  @type t :: %__MODULE__{
          clientId: Base.ClientId.t() | nil,
          signals: Base.SignalIds.t() | nil,
          onChange: boolean
        }
  defstruct [:clientId, :signals, :onChange]

  field :clientId, 1, type: Base.ClientId
  field :signals, 2, type: Base.SignalIds
  field :onChange, 3, type: :bool
end

defmodule Base.SignalIds do
  @moduledoc false
  use Protobuf, syntax: :proto3

  @type t :: %__MODULE__{
          signalId: [Base.SignalId.t()]
        }
  defstruct [:signalId]

  field :signalId, 1, repeated: true, type: Base.SignalId
end

defmodule Base.Signals do
  @moduledoc false
  use Protobuf, syntax: :proto3

  @type t :: %__MODULE__{
          signal: [Base.Signal.t()]
        }
  defstruct [:signal]

  field :signal, 1, repeated: true, type: Base.Signal
end

defmodule Base.PublisherConfig do
  @moduledoc false
  use Protobuf, syntax: :proto3

  @type t :: %__MODULE__{
          signals: Base.Signals.t() | nil,
          clientId: Base.ClientId.t() | nil,
          frequency: integer
        }
  defstruct [:signals, :clientId, :frequency]

  field :signals, 1, type: Base.Signals
  field :clientId, 2, type: Base.ClientId
  field :frequency, 3, type: :int32
end

defmodule Base.Signal do
  @moduledoc false
  use Protobuf, syntax: :proto3

  @type t :: %__MODULE__{
          payload: {atom, any},
          id: Base.SignalId.t() | nil,
          raw: binary,
          timestamp: integer
        }
  defstruct [:payload, :id, :raw, :timestamp]

  oneof :payload, 0
  field :id, 1, type: Base.SignalId
  field :integer, 2, type: :int64, oneof: 0
  field :double, 3, type: :double, oneof: 0
  field :arbitration, 4, type: :bool, oneof: 0
  field :empty, 6, type: :bool, oneof: 0
  field :raw, 5, type: :bytes
  field :timestamp, 7, type: :int64
end

defmodule Base.NetworkService.Service do
  @moduledoc false
  use GRPC.Service, name: "base.NetworkService"

  rpc :SubscribeToSignals, Base.SubscriberConfig, stream(Base.Signals)
  rpc :PublishSignals, Base.PublisherConfig, Base.Empty
  rpc :ReadSignals, Base.SignalIds, Base.Signals
end

defmodule Base.NetworkService.Stub do
  @moduledoc false
  use GRPC.Stub, service: Base.NetworkService.Service
end
