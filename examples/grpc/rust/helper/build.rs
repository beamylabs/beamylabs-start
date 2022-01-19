fn main() -> Result<(), Box<dyn std::error::Error>> {
    tonic_build::configure()
        .build_server(false)
        .out_dir("src/beamy_api")
        .compile(
            &[
                "protos/common.proto",
                "protos/diagnostics_api.proto",
                "protos/functional_api.proto",
                "protos/network_api.proto",
                "protos/system_api.proto",
                "protos/traffic_api.proto",
            ],
            &["protos"],
        )?;

    Ok(())
}
