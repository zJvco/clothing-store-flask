from setuptools import setup, find_packages

"""
Major - significa mudanças muito grades no nosso projeto
Minor - é a versão mais comum (do dia a dia). Exemplo: Colocar features novas, extenções novas, páginas novas.
Path - é quando é feita alguma correção na aplicação.
"""


def read_file(filename):
    return [req.strip() for req in open(filename).readlines()]

setup(
    name="Clothing Store",
    version="0.10.0", # Major, Minor, Path
    description="",
    author="Jvco",
    packages=find_packages(exclude="./venv"),
    include_package_data=True,
    install_requires=read_file("requirements.txt")
)