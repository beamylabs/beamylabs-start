defmodule Base.SenderInfo do
  @moduledoc false
  use Protobuf, syntax: :proto3

  @type t :: %__MODULE__{
          clientId: Base.ClientId.t() | nil,
          value: Base.Value.t() | nil,
          frequency: integer
        }
  defstruct [:clientId, :value, :frequency]

  field :clientId, 1, type: Base.ClientId
  field :value, 2, type: Base.Value
  field :frequency, 3, type: :int32
end

defmodule Base.SubscriberRequest do
  @moduledoc false
  use Protobuf, syntax: :proto3

  @type t :: %__MODULE__{
          clientId: Base.ClientId.t() | nil,
          onChange: boolean
        }
  defstruct [:clientId, :onChange]

  field :clientId, 1, type: Base.ClientId
  field :onChange, 2, type: :bool
end

defmodule Base.Value do
  @moduledoc false
  use Protobuf, syntax: :proto3

  @type t :: %__MODULE__{
          payload: integer
        }
  defstruct [:payload]

  field :payload, 1, type: :int32
end

defmodule Base.FunctionalService.Service do
  @moduledoc false
  use GRPC.Service, name: "base.FunctionalService"

  rpc :OpenPassWindow, Base.ClientId, Base.Empty
  rpc :ClosePassWindow, Base.ClientId, Base.Empty
  rpc :SetFanSpeed, Base.SenderInfo, Base.Empty
  rpc :SubscribeToFanSpeed, Base.SubscriberRequest, stream(Base.Value)
end

defmodule Base.FunctionalService.Stub do
  @moduledoc false
  use GRPC.Stub, service: Base.FunctionalService.Service
end
