use std::{error::Error, fs};

use beamy_api::base::{
    file_upload_request::Data, system_service_client::SystemServiceClient, FileDescription,
    FileUploadRequest,
};
use futures::{stream, Stream};
use sha2::{Digest, Sha256};
use tonic::transport::Channel;
use walkdir::WalkDir;

use crate::beamy_api::base::{Empty, LicenseStatus};

pub mod beamy_api;

/// Generate a sha256 key of the data in the provided file
pub fn get_sha256(path: &str) -> Result<String, Box<dyn Error>> {
    // Read all the data from the file
    let bytes = fs::read(path)?;

    // Create a hasher and add the data from the file to it
    let mut hasher = Sha256::new();
    hasher.update(bytes);

    // Generate the key and make it to a readable String
    let result = format!("{:x}", hasher.finalize());
    Ok(result)
}

/// Generate the file description data in the right order that the beamybroker needs
async fn generate_data(
    path: &str,
    dest_path: String,
    _chunk_size: usize,
    sha256: String,
) -> Result<impl Stream<Item = FileUploadRequest>, Box<dyn Error>> {
    // Read all the data from the file
    let buf = fs::read(path)?;

    // Create a file description with the sha256 key and file destination path
    let fd = Some(Data::FileDescription(FileDescription {
        sha256,
        path: dest_path,
    }));

    let data = Some(Data::Chunk(buf));

    // Create the upload requests with file description and data
    let file_description = FileUploadRequest { data: fd };
    let data = FileUploadRequest { data };

    Ok(stream::iter(vec![file_description, data]))
}

/// Upload file to BeamyBroker
async fn upload_file(
    system_stub: &mut SystemServiceClient<Channel>,
    path: &str,
    dest_path: String,
) -> Result<(), Box<dyn Error>> {
    let sha256 = get_sha256(path)?;
    let chunk_size = 1000000;
    let upload_iterator = generate_data(path, dest_path, chunk_size, sha256).await?;
    let _response = system_stub.upload_file(upload_iterator).await?;

    println!("Uploaded file {}", path);

    Ok(())
}

/// Takes a path to a directory as argument and then walks the directory recursively
///
/// Then we filter out the folders and just keep the files
pub async fn upload_folder(
    system_stub: &mut SystemServiceClient<Channel>,
    path: &str,
) -> Result<(), Box<dyn Error>> {
    for entry in WalkDir::new(path)
        .into_iter()
        .filter_map(|e| {
            if e.is_err() {
                println!("Error when trying to upload folder: {:#?}", e)
            }
            e.ok()
        })
        .filter(|e| e.path().is_file())
    {
        if let Some(entry) = entry.path().to_str() {
            upload_file(system_stub, entry, entry.replace(path, "")).await?;
        }
    }

    Ok(())
}

/// Reload beamybroker configuration
pub async fn reload_configuration(
    system_stub: &mut SystemServiceClient<Channel>,
) -> Result<(), Box<dyn Error>> {
    let _response = system_stub.reload_configuration(Empty {}).await?;
    println!("Reload your configuration");
    Ok(())
}

/// Check BeamyBroker license
pub async fn check_license(
    system_stub: &mut SystemServiceClient<Channel>,
) -> Result<(), Box<dyn Error>> {
    let status = system_stub
        .get_license_info(Empty {})
        .await?
        .into_inner()
        .status();

    println!("Check your license, status is: {:?}", status);

    // Don't continue if the license isn't valid
    assert!(status == LicenseStatus::Valid);
    Ok(())
}
