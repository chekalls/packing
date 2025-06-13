FROM python:3.11-slim

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    python3-tk \
    x11-apps \
    build-essential \
    libglib2.0-0 \
    libxrender1 \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Installer les bibliothèques Python
RUN pip install --no-cache-dir \
    matplotlib \
    pandas \
    numpy

# Créer un répertoire de travail
WORKDIR /app

# Copier le script Python
COPY Packing.py .

# Lancer l'application
# CMD ["python", "Packing.py"]
