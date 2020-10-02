defmodule Base.DiagnosticsRequest do
  @moduledoc false
  use Protobuf, syntax: :proto3

  @type t :: %__MODULE__{
          upLink: Base.SignalId.t() | nil,
          downLink: Base.SignalId.t() | nil,
          serviceId: binary,
          dataIdentifier: binary
        }
  defstruct [:upLink, :downLink, :serviceId, :dataIdentifier]

  field :upLink, 1, type: Base.SignalId
  field :downLink, 2, type: Base.SignalId
  field :serviceId, 3, type: :bytes
  field :dataIdentifier, 4, type: :bytes
end

defmodule Base.DiagnosticsResponse do
  @moduledoc false
  use Protobuf, syntax: :proto3

  @type t :: %__MODULE__{
          raw: binary
        }
  defstruct [:raw]

  field :raw, 5, type: :bytes
end

defmodule Base.DiagnosticsService.Service do
  @moduledoc false
  use GRPC.Service, name: "base.DiagnosticsService"

  rpc :SendDiagnosticsQuery, Base.DiagnosticsRequest, Base.DiagnosticsResponse
end

defmodule Base.DiagnosticsService.Stub do
  @moduledoc false
  use GRPC.Stub, service: Base.DiagnosticsService.Service
end
