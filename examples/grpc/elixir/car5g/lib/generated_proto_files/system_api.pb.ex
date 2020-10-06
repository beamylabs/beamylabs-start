defmodule Base.Configuration do
  @moduledoc false
  use Protobuf, syntax: :proto3

  @type t :: %__MODULE__{
          networkInfo: [Base.NetworkInfo.t()],
          interfacesJson: binary,
          licenseEndDate: String.t(),
          publicAddress: String.t()
        }
  defstruct [:networkInfo, :interfacesJson, :licenseEndDate, :publicAddress]

  field :networkInfo, 1, repeated: true, type: Base.NetworkInfo
  field :interfacesJson, 2, type: :bytes
  field :licenseEndDate, 3, type: :string
  field :publicAddress, 4, type: :string
end

defmodule Base.ReloadMessage do
  @moduledoc false
  use Protobuf, syntax: :proto3

  @type t :: %__MODULE__{
          status: {atom, any}
        }
  defstruct [:status]

  oneof :status, 0
  field :configuration, 1, type: Base.Configuration, oneof: 0
  field :errorMessage, 2, type: :string, oneof: 0
end

defmodule Base.FileDescription do
  @moduledoc false
  use Protobuf, syntax: :proto3

  @type t :: %__MODULE__{
          sha256: String.t(),
          path: String.t()
        }
  defstruct [:sha256, :path]

  field :sha256, 1, type: :string
  field :path, 2, type: :string
end

defmodule Base.FileUploadRequest do
  @moduledoc false
  use Protobuf, syntax: :proto3

  @type t :: %__MODULE__{
          data: {atom, any}
        }
  defstruct [:data]

  oneof :data, 0
  field :fileDescription, 1, type: Base.FileDescription, oneof: 0
  field :chunk, 2, type: :bytes, oneof: 0
end

defmodule Base.FileUploadChunkRequest do
  @moduledoc false
  use Protobuf, syntax: :proto3

  @type t :: %__MODULE__{
          fileDescription: Base.FileDescription.t() | nil,
          chunks: non_neg_integer,
          chunkId: non_neg_integer,
          chunk: binary,
          cancelUpload: boolean,
          uploadTimeout: non_neg_integer
        }
  defstruct [:fileDescription, :chunks, :chunkId, :chunk, :cancelUpload, :uploadTimeout]

  field :fileDescription, 1, type: Base.FileDescription
  field :chunks, 2, type: :uint32
  field :chunkId, 3, type: :uint32
  field :chunk, 4, type: :bytes
  field :cancelUpload, 5, type: :bool
  field :uploadTimeout, 6, type: :uint32
end

defmodule Base.FileUploadResponse do
  @moduledoc false
  use Protobuf, syntax: :proto3

  @type t :: %__MODULE__{
          data: {atom, any}
        }
  defstruct [:data]

  oneof :data, 0
  field :finished, 1, type: :bool, oneof: 0
  field :cancelled, 2, type: :bool, oneof: 0
  field :errorMessage, 3, type: :string, oneof: 0
end

defmodule Base.SystemService.Service do
  @moduledoc false
  use GRPC.Service, name: "base.SystemService"

  rpc :GetConfiguration, Base.Empty, Base.Configuration
  rpc :ListSignals, Base.NameSpace, Base.Frames
  rpc :UploadFileChunk, Base.FileUploadChunkRequest, Base.FileUploadResponse
  rpc :UploadFile, stream(Base.FileUploadRequest), Base.FileUploadResponse
  rpc :ReloadConfiguration, Base.Empty, Base.ReloadMessage
end

defmodule Base.SystemService.Stub do
  @moduledoc false
  use GRPC.Stub, service: Base.SystemService.Service
end
