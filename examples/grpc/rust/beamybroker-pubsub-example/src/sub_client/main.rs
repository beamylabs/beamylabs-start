use beamy_broker_client_example::beamy_api::base::network_service_client::NetworkServiceClient;
use beamy_broker_client_example::beamy_api::base::{
    ClientId, NameSpace, SignalId, SignalIds, SubscriberConfig,
};
use tonic::transport::Channel;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let channel = Channel::from_static("http://localhost:50051")
        .connect()
        .await?;
    let mut client = NetworkServiceClient::new(channel);

    let client_id = Some(ClientId {
        id: "rusty_subscriber".to_string(),
    });

    let signals = generate_signal_ids("VirtualInterface", &["virtual_signal"]);

    let subscriber_config = SubscriberConfig {
        client_id,
        signals,
        on_change: true,
    };

    let mut result = client
        .subscribe_to_signals(subscriber_config)
        .await?
        .into_inner();

    // Read message from stream and print it out
    while let Some(next_message) = result.message().await? {
        println!("Received {:#?}", next_message.signal);
    }

    Ok(())
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
