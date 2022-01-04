# Rust gRPC signal-broker example

This project is intended to be a basic example of how to use the subscribe/publish functions with beamybroker.

## Setup

1. Download and install Rust https://www.rust-lang.org/
2. Choose an IDE that you prefer to use. (If you just want to try it out,
   you can skip this part and just use the terminal)

The cargo build system will download and install all necessary dependencies that are declared in Cargo.toml

The signal-broker namespace I'm using in this example is <b>VirtualInterface</b>

## Add Protofiles

Don't forget to add the latest up to date .proto files from here https://github.com/beamylabs/beamylabs-start/tree/master/proto_files and put them in the protos folder

## How to use

From terminal use these commands below

```zsh
# Run as subscriber
cargo run --bin sub_client

# Run as publisher
cargo run --bin pub_client
```
