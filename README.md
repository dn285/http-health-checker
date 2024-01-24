# http-health-checker

Program that checks the health of a set of HTTP endpoints. 

## Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

## Installation

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/dn285/http-health-checker.git
    cd health-check-application
    ```

2. **Set Up a Virtual Environment (Optional):**

    - Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

    - MacOS/Linus:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the application with the following command:

```bash
python src/health_checker.py [path_to_yaml_file]
```
- `path_to_yaml_file` is the path to the YAML file containing the endpoints. If not specified, the application will use the default file `endpoints.yml` found in `src`, which contains a sample YAML.

Alternatively, the user may replace the contents of `endpoints.yml` with the desired YAML.

## Testing

To run the automated unit tests for this system, execute:
```bash
pytest
```

## Acknowledgements

This project was created for the [Fetch](https://fetch.com/) Site Reliability Engineer take-home exercise.