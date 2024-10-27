---
title: Car Predict
emoji: 🐠
colorFrom: red
colorTo: gray
sdk: docker
pinned: false
license: mit
---

## Car Predict
Using Machine Learning to predict Vehicle prices in Colombia.

## Run locally
Please create your virtual environment before, for example
```bash
python3 -m venv myenv
source myenv/bin/activate
```
Set root as Pythonpath and install requirements
```bash
export PYTHONPATH=$PWD

pip install requirements_dev.txt
```
## This project use DVC :stars:
```bash
dvc init
dvc repro #to run experiment with config
```
run many experiments
```bash
sh run_experiments.sh
```
#  :zap: API
## :whale: Docker
```bash
docker compose build
docker compose up
```

## DVC command notes

DVC exp remove -A
dvc queue remove --all

dvc queue log -expid-

dvc exp apply --expid


