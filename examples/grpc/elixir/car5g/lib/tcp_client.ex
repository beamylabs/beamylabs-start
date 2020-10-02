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

defmodule Car5g.Client do

  use GenServer
  require Logger

  defmodule State, do: defstruct [
    :addr,
    :port,
    :socket,
    :signal_pid,
    reconnect_intervall: 4_000,
    buffer_message: "",
    name: ""
  ]

  # CLIENT

  def send_message(pid, message) do
    GenServer.cast(pid, {:send_message, message})
  end

  def start_link({name, signal_pid, addr, port}),
    do: GenServer.start_link(__MODULE__, {
      name, signal_pid,
      addr, port,
    }, name: name)


  def init({name, signal_pid, addr, port}) do
    state = %State{addr: addr, port: port, name: name, signal_pid: signal_pid, buffer_message: ""}
    # connect(self)
    Process.send(self(), {:connect}, [:noconnect])
    {:ok, state}
  end


  def handle_info({:connect}, state) do
    case :gen_tcp.connect(state.addr, state.port, [:binary, reuseaddr: true]) do
      {:ok, socket} ->
        Logger.info "Successfully connected to flexray node on ip #{inspect state.addr}, port #{inspect state.port}"
        {:noreply, %State{state | socket: socket}}
      _ ->
        Logger.info "Failed to connect to server node in ip #{inspect state.addr}, port #{inspect state.port}"
        # retry
        Process.send_after(self(), {:connect}, state.reconnect_intervall)
        {:noreply, %State{state | socket: nil}}
    end
  end

  def handle_info({:tcp_closed, _socket}, state) do
    Process.send(self(), {:connect}, [:noconnect])
  end

  def disconnect(pid) do
    GenServer.cast(pid, {:disconnect})
  end

  defp now(), do: System.system_time(:microsecond)

  defp dispatch_payload(state, sid, cycle, payload) do
    GenServer.cast(state.signal_pid, {:raw_flexray_frame, {sid, cycle}, payload, state.name, now()})
  end

  # this is where we get messages which we dispatch to the web client (socket)
  def handle_info({:tcp, _port, message}, state) do
    Logger.debug "recieved message from server, message is #{inspect message}"
    {:noreply, state}
  end

  def handle_cast({:send_message, message}, state) do

    Logger.debug "#{inspect (message  <> "\n")}"
    if (state.socket != nil) do
      response = :gen_tcp.send(state.socket, String.to_charlist(message  <> "\n"))
      Logger.debug "Sending to server #{inspect response}"
    end

    {:noreply, state}
  end

end
