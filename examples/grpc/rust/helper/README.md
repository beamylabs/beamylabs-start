A helper-lib that generates code from .proto-files and also have functions to check license / upload configuration.

## Generate .proto files
In the [build.rs](build.rs) file. It takes all the .proto-files inside the [proto](proto) folder, and generate rust code. The output dir is set to [beamy_api](src/beamy_api)

## Functions
For now, you have these functions implemented

* check_license
* upload_folder
* reload_configuration