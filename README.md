# core LLM

<p align="center">
  <img src="https://raw.githubusercontent.com/SAWARATSUKI/ServiceLogos/main/Python/Python.png" alt="Python" width="200" />
</p>

This repository's purpose is to enhance LLM's capabilities in reading comprehension and key point extraction.

## Usage

clone the repository

```bash
git clone https://github.com/hibana2077/core-LLM.git
```

cd into the repository

```bash
cd core-LLM
```

### Data generation

To generate data for training, cd into the data_generation directory

```bash
cd data
```

set up config file

```bash
vim ./config.yaml
```

run the data generation script

```bash
sudo docker build -t data_generation . -v $(pwd):/app
```

check the generated data

```bash
cat data.csv
```

### Training

TBW

## License

![MIT](https://img.shields.io/badge/license-MIT-green)