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
Rust toolchain (for Blake3 dependency)
Libsodium
KERI


## Development
Building

``` shell
python3 -m build

python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps kaslcred
```
