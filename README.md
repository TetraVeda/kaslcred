# KASLCred : KERI and ACDC Schema Linker for Credentials
Computes self addressing identifiers (SAIDs) for KERI and ACDC schema parts and links them together by SAID.

## Usage

``` shell
python -m kaslcred [schema_dir] [output_dir] [schema_map_file.json]

# Example:
# Requires having pre-written and pre-copied all of the schema files into ${KASL_HOME}/schemas
export KASL_HOME=${HOME}/.kasl
python -m kaslcred ${KASL_HOME}/schemas ${KASL_HOME}/results ${KASL_HOME}/schemas/schema_map.json
```

## Installation

### Docker

### Manual Local Installation
1. Install Python
2. Install the Rust Toolchain: https://www.rust-lang.org/tools/install\
   This is for the [Blake3](https://github.com/BLAKE3-team/BLAKE3) crypto library built when installing KERI.
3. Install KERI: `pip install keri==0.6.8`
4. Install KASLcred

### Dependencies

KASLCred depends on the following libraries being installed:

Rust toolchain (for Blake3 dependency)

#### Libsodium

The Homebrew installation of Libsodium is not sufficient, or did not work for me. I had to do the following instructions like stated in Libsodium's Gitbook [Installation documentation](https://libsodium.gitbook.io/doc/installation)

Download a tarball of libsodium, preferably the latest stable version, then follow the ritual:
```bash
./configure
make && make check
sudo make install
```


#### [KERIpy](https://github.com/WebOfTrust/keripy) version 1.0.0

```bash
python -m pip install keri=1.0.0
``` 

KERIpy further depends on the following set of dependencies being installed:

#### [Rust](https://www.rust-lang.org/tools/install) v1.60+

This is required for Blake3 dependency in KERI to be able to build.
```bash
# the "-s -- -y" options are for a silent, unattended install. Omit them if you want to configure the install.
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
# Remember to set the PATH variable to include the Cargo binary directory like so:  PATH="$HOME/.cargo/bin:$PATH
```



## Development

Installing from the root repo directory:

``` shell
python3 -m pip install -e ./
```
