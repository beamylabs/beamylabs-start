# Copyright 2019 Volvo Cars
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# ”License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# “AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

defmodule Car5g do

  use GenServer
  require Logger

  defstruct [
    :signal_pid,
    :recorded_file,
    :name,
    :tcp_connection,
    signal_map: %{}
  ]

  def start_link({name, tcp_server}) do
    state = %__MODULE__{tcp_connection: tcp_server, name: name}
    GenServer.start_link(__MODULE__, state, name: name)
  end

  @send_data false

  @namespace "VirtualCanInterface"
  # @flexray_namespace "Flexray"

  @signals (
    signal1 = Base.SignalId.new(name: "BenchC_a", namespace: Base.NameSpace.new(name: @namespace))
    signal2 = Base.SignalId.new(name: "BenchC_b", namespace: Base.NameSpace.new(name: @namespace))
    signal3 = Base.SignalId.new(name: "BenchC_c_1", namespace: Base.NameSpace.new(name: @namespace))
    # signal4 = Base.SignalId.new(name: "BenchC_c_3", namespace: Base.NameSpace.new(name: @flexray_namespace))
    # signal5 = Base.SignalId.new(name: "BenchC_c_4", namespace: Base.NameSpace.new(name: @flexray_namespace))
    signal6 = Base.SignalId.new(name: "BenchC_c_2", namespace: Base.NameSpace.new(name: @namespace))
    [signal1, signal2, signal3, signal6]
  )

  @intervall_in_ms 100

  def init(state) do
    :ssl.start()
    spawn(__MODULE__, :subscribe_to_signals, [self(), @signals])
    # schedule_work(@intervall_in_ms, :grpc_read)
    schedule_work(@intervall_in_ms, :grpc_subscribe)
    {:ok, state}
  end

  defp schedule_work(intervall_in_ms, func),
    do: Process.send_after(self(), func, intervall_in_ms)

 # speed
 # 0.01 m/s
 # Speed of the RU in direction specified in the “heading” field.
 # acceleration
 # 0.1 m/s²
 # Acceleration of the RU in direction specified in the “heading” field.
 # yaw_rate
 # 0.1 degrees/s
 # Heading change of the road user, where the sign indicates the direction

 # "position":{
 # 	"latitude":<int32>,
 # 	"longitude":<int32>},
 # "position_type":<string>,
 # "heading":<uint16>,
 # "speed":<uint16>,
 # "acceleration":<int16>,
 # "yaw_rate":<int16>,

  def convert_constant() do
    180/:math.pi
  end

  def radpers_todefpers(radians_per_second) do
    radians_per_second * convert_constant() * 10
  end

  def subscribe_to_signals(dest, signals) do
    {:ok, channel} = GRPC.Stub.connect("localhost:50051")
    signalIds = Base.SignalIds.new(signalId: signals)

    Logger.debug "signals #{inspect signals}"
    request = Base.SubscriberConfig.new(clientId: Base.ClientId.new(id: "grpc-client"), signals: signalIds, on_change: false)
    # https://github.com/tony612/grpc-elixir/issues/88
    {:ok, stream} = channel |> Base.NetworkService.Stub.subscribe_to_signals(request, timeout: :infinity)

    Enum.each stream, fn (response) ->
      case response do
          {:ok, %Base.Signals{signal: signals}} ->
            GenServer.cast(dest, {:subscription_arrived, signals})
          {:error, %GRPC.RPCError{message: message, status: status}} ->
            Logger.debug "bang #{inspect message} #{inspect status}"
            subscribe_to_signals(dest, signals)
          general ->
            Logger.debug "inspect general"
            subscribe_to_signals(dest, signals)
      end
    end
  end

  def handle_cast({:subscription_arrived, signals}, state) do
    update_map =
      Enum.reduce(signals, state.signal_map, fn(%Base.Signal{id: %Base.SignalId{name: name}, payload: payload}, acc) ->
        pack_map(name, payload, acc)
      end)

    {:noreply, %__MODULE__{state | signal_map: update_map}}
  end

  defp send_file(channel, file, destination_path, chunksize \\ 4000000, run_when_done \\ fn(file) -> end) do

    {:ok, binary} = File.read(file)
    # {:ok, binary} = {:ok,
    #   <<70, 79, 82, 49, 0, 0, 12, 212, 66, 69, 65, 77, 65, 116, 85, 56, 0, 0, 0, 214,
    #   0, 0, 0, 20, 7, 109, 101, 116, 114, 105>>}

    sha256 = :crypto.hash(:sha256, binary) |> Base.encode16()

    chopped_binary = File.stream!(file, [:binary], chunksize) |> Stream.chunk_every(1) |> Enum.to_list
    chunks = Enum.count(chopped_binary)
    zipped_and_chopped = Enum.zip(1..chunks, chopped_binary)

    file_description = Base.FileDescription.new(sha256: sha256, path: destination_path)

    Enum.reduce(Enum.shuffle(zipped_and_chopped), [], fn({entry, [binary]}, uploaded) ->
      uploaded = [entry-1] ++ uploaded
      file_upload_chunk_request = Base.FileUploadChunkRequest.new(fileDescription: file_description, chunks: chunks, chunkId: (entry-1), chunk: binary, path: destination_path, cancelUpload: false)
      case Enum.count(uploaded) == chunks do
        false ->
          {:ok, %Base.FileUploadResponse{data: {:finished, false}}} = Base.SystemService.Stub.upload_file_chunk(channel, file_upload_chunk_request)
          # assert Enum.sort(transferred) == Enum.sort(uploaded)
          uploaded
        true ->
          {:ok, %Base.FileUploadResponse{data: {:finished, true}}} = Base.SystemService.Stub.upload_file_chunk(channel, file_upload_chunk_request)
          uploaded
      end
    end)

    run_when_done.(file)
  end

  def send_file_helper(file, destination_path, timeout \\ 0) do
    {:ok, channel} = GRPC.Stub.connect("localhost:50051")
    pid = self()
    send_file(channel, file, destination_path, 4000000, fn(file) -> send(pid, :done) end)
    receive do
      :done ->
        :ok
      after
        1_000 -> :error
    end
  end

  def reload_helper() do
    {:ok, channel} = GRPC.Stub.connect("localhost:50051")
    # {:ok, %Base.ReloadMessage{status: {:configuration, configuration}}} = Base.SystemService.Stub.reload_configuration(channel, Base.Empty.new())
    {:ok, %Base.ReloadMessage{} = message} = Base.SystemService.Stub.reload_configuration(channel, Base.Empty.new())
    Logger.debug("reload returned #{inspect message}")
  end

  def pack_map(name, payload, acc) do
    case name do
      "BenchC_a" -> update_map(acc, "speed", extract_payload(payload), &(&1*100))
      "BenchC_b" -> update_map(acc, "acceleration", extract_payload(payload), &(&1*10))
      "BenchC_c_1" -> update_map(acc, "yaw_rate", extract_payload(payload), &radpers_todefpers/1)
      "BenchC_c_3" -> update_map(acc, "position.latitude", extract_payload(payload))
      "BenchC_c_4" -> update_map(acc, "position.longitude", extract_payload(payload))
      "BenchC_c_2" -> update_map(acc, "test_data", extract_payload(payload))
      _ -> acc
    end
  end

  def read_grpc(state) do
    {:ok, channel} = GRPC.Stub.connect("localhost:50051")


    request = Base.SignalIds.new(signal_id: @signals)
    response = Base.NetworkService.Stub.read_signals(channel, request)

    {:ok, %Base.Signals{signal: signals}} = response

    response_map = Enum.reduce(signals, %{}, fn(%Base.Signal{id: %Base.SignalId{name: name}, payload: payload}, acc) ->
      pack_map(name, payload, acc)
    end)

    dispatch_data(response_map, state)
  end

  @default_info (
    %{"type" => "override", "origin" => "can_gateway"}
  )

  def add_timestamp(response_map) do
    Map.put(response_map, "timestamp", System.system_time(:microsecond))
  end

  def dispatch_data(response_map, state) do
    response_map_with_defaults = Map.merge(response_map, @default_info)
    {:ok, encoded_map} = Poison.encode(add_timestamp(response_map_with_defaults))
    Car5g.Client.send_message(state.tcp_connection, encoded_map)
  end

  def update_map(map, name, value, conversion \\ &(&1)) do
    case value do
      :empty -> map
      value -> Map.put(map, name, conversion.(value))
    end
  end

  def extract_payload(payload) do
    case payload do
      {:empty, true} -> :empty
      # this application is not interested in arbitartion.
      {:arbitration} -> :empty
      {:double, value} -> value
      {:integer, value} -> value
    end
  end

  def handle_info(:grpc_read = worker, state) do
    schedule_work(@intervall_in_ms, worker)
    read_grpc(state)
    {:noreply, state}
  end

  def handle_info(:grpc_subscribe = worker, state) do
    schedule_work(@intervall_in_ms, worker)
    dispatch_data(state.signal_map, state)
    {:noreply, state}
  end

  # this is a test url, go visit it on the web, potentially generate your own.
  @url  'http://requestbin.fullcontact.com/znfw38zn'
  def post_data_to_endpoint(body) do
      if (@send_data) do
      # use this to post params.
        {:ok, {{'HTTP/1.1', 200, 'OK'}, headers, _body}} = :httpc.request(:post, {@url, [], 'application/json', String.to_charlist(body)}, [], [])
      end
  end

end
