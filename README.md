# Wiki Infographics

Wiki Infographics is a platform to leverage structured information within Wikimedia projects to create informative and visually engaging infographics in both fixed and dynamic formats, under an open license. It is available at https://infographics.toolforge.org.

The frontend codebase is available in this repository [wiki_infographics
](https://github.com/WikiMovimentoBrasil/wiki_infographics)

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Contributing](#contributing)
- [License](#license)

## Getting started:

### Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3
- Flask 3.0.3

### Installation

1. Clone the repository

   ```bash
   git clone https://github.com/WikiMovimentoBrasil/wiki_infographics-backend.git

   ```

2. Navigate to the project directory:

   ```bash
   cd wiki_infographics-backend

   ```

3. Create virtual environment

   ```bash
   python -m venv venv

   ```

4. Activate the virtual environment

   ```bash
   .\venv\Scripts\activate

   ```

5. Install project dependencies:

   ```bash
   pip install -r requirements.txt

   ```

6. create a `config.yaml` file in your directory by copying `config-example.yaml` and filling the fields with the proper values.

7. Start the development server:
   ```bash
    python app.py
   ```

You should now be able to access the project at http://localhost:8000 in your web browser

To connect frontend with this backend go to this repository [wiki_infographics
](https://github.com/WikiMovimentoBrasil/wiki_infographics)

## Running in toolforge
### Rebuild the image (after a code change)
```
> ssh login.toolforge.org
> toolforge~# become <yourtool>
> yourtool@toolforge~# toolforge build start --image-name backend <url_for_this_repo>

## If already exists, restart it
> yourtool@toolforge~# toolforge job restart backend

## If starting up for the first time
> yourtool@toolforge~# toolforge job run \
    --command "backend" \
    --image tools-harbor.wmcloud.org/tool-<your_tool>/backend:latest \
    --port 8000 \
    --continuous \
    --mount=all \
    backend
```

More info on buildservice (debugging, etc.) [here](https://wikitech.wikimedia.org/wiki/Help:Toolforge/Build_Service)


## Contributing

Contributions are welcome! To contribute to Wiki Infographics, follow these steps:

1. Fork the repository
2. Create a new branch: git checkout -b feature/your-feature
3. Make your changes and commit them: git commit -m 'Add some feature'
4. Push to the branch: git push origin feature/your-feature
5. Create a pull request on GitHub

## Todos

- [ ] Save users successful SPARQL queries

## License

This project is licensed under the [MIT License](https://opensource.org/license/mit) - see the LICENSE file for details.
