from setuptools import setup, find_packages

setup(
    name="ai-happy",
    version="1.0.0",
    description="Deep Reason AI metacognition engine for brand licensing and hardware embedding",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn>=0.24.0",
        "pydantic>=2.5.0",
        "numpy>=1.24.3",
        "transformers>=4.35.2",
        "torch>=2.1.0",
        "scikit-learn>=1.3.2",
        "python-dateutil>=2.8.2",
    ],
    python_requires=">=3.8",
    author="VerdantAI",
    author_email="info@verdantai.com",
    url="https://github.com/VerdantAI-1234/ai-happy",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)