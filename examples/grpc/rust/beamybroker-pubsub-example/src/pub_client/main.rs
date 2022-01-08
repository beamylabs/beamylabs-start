use std::io::Write;

use lib_helper::{
    beamy_api::base::{
        network_service_client::NetworkServiceClient, signal::Payload::Integer,
        system_service_client::SystemServiceClient, ClientId, NameSpace, PublisherConfig, Signal,
        SignalId, Signals,
    },
    check_license, reload_configuration, upload_folder,
};
use tonic::transport::Channel;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let channel = Channel::from_static("http://localhost:50051")
        .connect()
        .await?;

    let mut system_stub = SystemServiceClient::new(channel.clone());
    let mut network_stub = NetworkServiceClient::new(channel);

    check_license(&mut system_stub).await?;
    upload_folder(&mut system_stub, "configuration").await?;
    reload_configuration(&mut system_stub).await?;

    // Publish 10 messages
    for _ in 0..=10 {
        let client_id = Some(ClientId {
            id: "rusty_publisher".to_string(),
        });

        print!("Enter a value: ");
        std::io::stdout().flush()?;

        // Take input from terminal
        let mut input_string = String::new();
        let _input_result = std::io::stdin().read_line(&mut input_string);

        // try to parse the string into int64, if fail: payload = 0
        let input_as_int: i64 = input_string.trim().parse().unwrap_or(0);

        let signals = generate_signals(input_as_int);
        let publisher_config = PublisherConfig {
            client_id,
            signals,
            frequency: 0,
        };

        let result = network_stub.publish_signals(publisher_config).await?;
        println!("{:#?}", result.metadata());
    }

    Ok(())
}

/// Generate signals that can be published on gRPC
fn generate_signals(input: i64) -> Option<Signals> {
    let namespace = Some(NameSpace {
        name: "VirtualInterface".to_string(),
    });
    let signal_id = Some(SignalId {
        name: "virtual_signal".to_string(),
        namespace,
    });
    let signal_payload = Some(Integer(input));
    let signal = Signal {
        id: signal_id,
        raw: vec![],
        timestamp: 0,
        payload: signal_payload,
    };
    let signals_vec = vec![signal];

    Some(Signals {
        signal: signals_vec,
    })
}
