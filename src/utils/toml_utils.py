from toml import load

def get_authors():
    """
    Get the list of authors from the pyproject.toml file.
    """
    import os
    
    # Path to your pyproject.toml file
    pyproject_toml_path = "pyproject.toml"

    # Load the pyproject.toml file
    with open(pyproject_toml_path, "r") as file:
        pyproject_toml = load(file)

    # Get the author information
    return pyproject_toml.get("tool", {}) \
                        .get("poetry", {}) \
                        .get("authors", [])
