# Script para estudar

> **Curso de Python completo:** veja a pasta [`curso-python/`](curso-python/README.md)
> (aulas, exercícios com correção automática, projeto final, guia de carreira e apostila
> em PDF).

- Ambiente virtual isolado
- Linters e formatadores automáticos


## 🧪 Rodando Testes

O projeto usa [pytest](https://docs.pytest.org/) para testes automatizados:

```bash
pytest
```

---

## 🎨 Formatando o código

Estou usando `black` para formatação automática e `isort` para organização dos imports.

```bash
black .
isort .
```

Essas ferramentas seguem as regras definidas em `pyproject.toml`.

---

## 🧪 Linting

Os linters ajudam a manter o código limpo:

- `pylint`
- `flake8`

Exemplo de uso:

```bash
pylint src/
flake8 src/
```
