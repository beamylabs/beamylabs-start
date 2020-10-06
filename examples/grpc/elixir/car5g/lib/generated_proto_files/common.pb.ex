defmodule Base.Empty do
  @moduledoc false
  use Protobuf, syntax: :proto3

  @type t :: %__MODULE__{}
  defstruct []
end

defmodule Base.ClientId do
  @moduledoc false
  use Protobuf, syntax: :proto3

  @type t :: %__MODULE__{
          id: String.t()
        }
  defstruct [:id]

  field :id, 1, type: :string
end

defmodule Base.SignalId do
  @moduledoc false
  use Protobuf, syntax: :proto3

  @type t :: %__MODULE__{
          name: String.t(),
          namespace: Base.NameSpace.t() | nil
        }
  defstruct [:name, :namespace]

  field :name, 1, type: :string
  field :namespace, 2, type: Base.NameSpace
end

defmodule Base.SignalInfo do
  @moduledoc false
  use Protobuf, syntax: :proto3

  @type t :: %__MODULE__{
          id: Base.SignalId.t() | nil,
          metaData: Base.MetaData.t() | nil
        }
  defstruct [:id, :metaData]

  field :id, 1, type: Base.SignalId
  field :metaData, 2, type: Base.MetaData
end

defmodule Base.MetaData do
  @moduledoc false
  use Protobuf, syntax: :proto3

  @type t :: %__MODULE__{
          description: String.t(),
          max: integer,
          min: integer,
          unit: String.t(),
          size: integer,
          isRaw: boolean
        }
  defstruct [:description, :max, :min, :unit, :size, :isRaw]

  field :description, 4, type: :string
  field :max, 5, type: :int32
  field :min, 6, type: :int32
  field :unit, 7, type: :string
  field :size, 8, type: :int32
  field :isRaw, 9, type: :bool
end

defmodule Base.NameSpace do
  @moduledoc false
  use Protobuf, syntax: :proto3

  @type t :: %__MODULE__{
          name: String.t()
        }
  defstruct [:name]

  field :name, 1, type: :string
end

defmodule Base.NetworkInfo do
  @moduledoc false
  use Protobuf, syntax: :proto3

  @type t :: %__MODULE__{
          namespace: Base.NameSpace.t() | nil,
          type: String.t(),
          description: String.t()
        }
  defstruct [:namespace, :type, :description]

  field :namespace, 1, type: Base.NameSpace
  field :type, 2, type: :string
  field :description, 3, type: :string
end

defmodule Base.FrameInfo do
  @moduledoc false
  use Protobuf, syntax: :proto3

  @type t :: %__MODULE__{
          signalInfo: Base.SignalInfo.t() | nil,
          childInfo: [Base.SignalInfo.t()]
        }
  defstruct [:signalInfo, :childInfo]

  field :signalInfo, 1, type: Base.SignalInfo
  field :childInfo, 2, repeated: true, type: Base.SignalInfo
end

defmodule Base.Frames do
  @moduledoc false
  use Protobuf, syntax: :proto3

  @type t :: %__MODULE__{
          frame: [Base.FrameInfo.t()]
        }
  defstruct [:frame]

  field :frame, 1, repeated: true, type: Base.FrameInfo
end
