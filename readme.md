# codesh

## Project Overview

Codesh is a terminal-based code file generator/project that helps developers quickly generate boilerplate code and directory structures for various programming languages.

## Features
- Generates code files for various programming languages
- Customizable templates and structures
- Easy to use from the command line

## Installation

Follow these steps to install codesh:
1. Clone the repository
2. Run the installation script

## Usage

After installation, you can use codesh by running the following command in the terminal:

```bash
codesh [options] <language>
```

## Usage Examples

1. **Backup Files**

   ```sh
   codesh backup --source ~/Documents --destination /backup
   ```

2. **Quickly Compile Projects**

   ```sh
   codesh compile --project ~/projects/myproject
   ```

3. **Environment Cleanup**

   ```sh
   codesh clean --temp-files --log
   ```

## Configuration Options

### General Settings

- **Log Level**
  - Description: Sets the verbosity of the log output.
  - Options: `debug`, `info`, `warn`, `error`
  - Default: `info`

- **Dry Run**
  - Description: Simulate the commands without executing them.
  - Options: `true`, `false`
  - Default: `false`

### Backup Settings

- **Compression**
  - Description: Enable compression for backups.
  - Options: `zip`, `tar`, `none`
  - Default: `zip`

- **Encryption**
  - Description: Protect backups using encryption.
  - Options: `aes256`, `none`
  - Default: `none`

### Compile Settings

- **Optimization Level**
  - Description: Adjust the optimization level of the compilation.
  - Options: `O0`, `O1`, `O2`, `O3`
  - Default: `O2`

- **Target Platform**
  - Description: Specify the target platform for the build.
  - Options: `linux`, `windows`, `macos`
  - Default: `linux`

## Environment Setup

To use codesh, ensure the following prerequisites are met:

1. **Operating System**: Compatible with major operating systems including Linux, Windows, and macOS.

2. **Dependencies**:
   - `bash` 4.0 or higher
   - `rsync` for file operations
   - `gcc` for compilation tasks (optional, required for compile command)

3. **Installation Steps**:
   - Clone the repository:
     ```sh
     git clone https://github.com/username/codesh.git
     ```
   - Navigate into the cloned directory:
     ```sh
     cd codesh
     ```
   - Run the install script:
     ```sh
     ./install.sh
     ```

4. **Environment Variables**:
   - `CODESH_CONFIG`: Path to a custom config file.
   - `CODESH_LOG_DIR`: Directory for log storage.

## Contributing

Contributions are welcome! Please read the contributing guidelines before submitting a pull request.

## License

This project is licensed under the MIT License.
