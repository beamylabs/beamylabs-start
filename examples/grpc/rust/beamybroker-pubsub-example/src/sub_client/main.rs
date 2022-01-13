use tonic::transport::Channel;

use lib_helper::{
    beamy_api::base::{
        network_service_client::NetworkServiceClient, system_service_client::SystemServiceClient,
        ClientId, NameSpace, SignalId, SignalIds, SubscriberConfig,
    },
    check_license, reload_configuration, upload_folder,
};
use std::{thread, time};

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

    let client_id = Some(ClientId {
        id: "rusty_subscriber".to_string(),
    });

    let signals = generate_signal_ids("VirtualInterface", &["virtual_signal"]);

    let subscriber_config = SubscriberConfig {
        client_id,
        signals,
        on_change: true,
    };

    // Read message from stream and print it out
    loop {
        let mut result = network_stub
            .subscribe_to_signals(subscriber_config.clone())
            .await?
            .into_inner();

        while let Some(next_message) = result.message().await? {
            println!("Received {:#?}", next_message.signal);
        }

        {
            println!("Subscription dropped, retrying");
            let duration = time::Duration::from_secs(1);
            thread::sleep(duration);
        }
    }
}

/// generate signal ids for subscribe config
fn generate_signal_ids(namespace: &str, signals: &[&str]) -> Option<SignalIds> {
    let generate_namespace = |namespace: &str| {
        Some(NameSpace {
            name: namespace.to_string(),
        })
    };

    let signal_id = signals
        .iter()
        .map(|name| SignalId {
            name: name.to_string(),
            namespace: generate_namespace(namespace),
        })
        .collect::<Vec<SignalId>>();

    Some(SignalIds { signal_id })
}
