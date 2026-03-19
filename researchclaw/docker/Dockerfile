# ResearchClaw experiment sandbox — GPU-enabled, isolated environment.
# Build: docker build -t researchclaw/experiment:latest researchclaw/docker/
FROM nvidia/cuda:13.0.1-cudnn-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends \
        python3.10 python3.10-dev python3.10-venv python3-pip \
        gcc g++ cmake make gfortran \
        libopenblas-dev liblapack-dev \
        git curl ca-certificates \
        iptables iproute2 \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1 \
    && python3 -m pip install --upgrade pip setuptools wheel \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Core ML/scientific Python stack
RUN python3 -m pip install \
        https://github.com/kentstone84/PyTorch-2.10.0a0-for-Linux-/releases/download/v2.10.0a0/torch-2.10.0a0-cp310-cp310-linux_x86_64.whl \
    && python3 -m pip install --no-deps \
        https://download-r2.pytorch.org/whl/cu124/torchvision-0.21.0%2Bcu124-cp310-cp310-linux_x86_64.whl \
        https://download-r2.pytorch.org/whl/cu124/torchaudio-2.6.0%2Bcu124-cp310-cp310-linux_x86_64.whl \
    && python3 -m pip install \
        numpy scipy scikit-learn pandas matplotlib seaborn \
        tqdm gymnasium networkx torchdiffeq PyYAML \
    && python3 -m pip install "gymnasium[mujoco]" mujoco

# Extended ML ecosystem — vision, metrics, utilities
RUN python3 -m pip install \
        einops Pillow \
        h5py tensorboard albumentations kornia

# LLM / Transformer training stack
RUN python3 -m pip install \
        transformers>=4.46.0 \
        datasets>=3.0.0 \
        accelerate>=1.0.0 \
        peft>=0.13.0 \
        trl>=0.12.0 \
        bitsandbytes>=0.44.0 \
        sentencepiece protobuf tokenizers safetensors \
        evaluate rouge-score

# Pre-cache standard datasets for offline use (failures are non-fatal — flaky upstream mirrors)
RUN mkdir -p /opt/datasets && \
    python3 -c "import torchvision; torchvision.datasets.CIFAR10(root='/opt/datasets', train=True, download=True); torchvision.datasets.CIFAR10(root='/opt/datasets', train=False, download=True)" || true && \
    python3 -c "import torchvision; torchvision.datasets.CIFAR100(root='/opt/datasets', train=True, download=True); torchvision.datasets.CIFAR100(root='/opt/datasets', train=False, download=True)" || true && \
    python3 -c "import torchvision; torchvision.datasets.FashionMNIST(root='/opt/datasets', train=True, download=True); torchvision.datasets.FashionMNIST(root='/opt/datasets', train=False, download=True)" || true && \
    python3 -c "import torchvision; torchvision.datasets.MNIST(root='/opt/datasets', train=True, download=True); torchvision.datasets.MNIST(root='/opt/datasets', train=False, download=True)" || true && \
    python3 -c "import torchvision; torchvision.datasets.STL10(root='/opt/datasets', split='train', download=True); torchvision.datasets.STL10(root='/opt/datasets', split='test', download=True)" || true && \
    python3 -c "import torchvision; torchvision.datasets.SVHN(root='/opt/datasets', split='train', download=True); torchvision.datasets.SVHN(root='/opt/datasets', split='test', download=True)" || true && \
    chmod -R a+r /opt/datasets

# Non-root user for security
RUN groupadd -r researcher && useradd -r -g researcher -m -s /bin/bash researcher
WORKDIR /workspace
RUN chown researcher:researcher /workspace

# Entrypoint script — three-phase execution (pip install → setup → experiment)
COPY entrypoint.sh /usr/local/bin/rc-entrypoint.sh
RUN chmod +x /usr/local/bin/rc-entrypoint.sh

USER researcher

# Default: run entrypoint wrapper with main.py as the experiment script
ENTRYPOINT ["/usr/local/bin/rc-entrypoint.sh"]
CMD ["main.py"]
