import toml

def generate_conda_yaml(toml_file, yaml_file):
    # Load pyproject.toml
    with open(toml_file, 'r') as f:
        toml_data = toml.load(f)

    # Extract dependencies
    dependencies = toml_data['tool']['poetry']['dependencies']

    # Generate YAML content
    yaml_content = f"name: {toml_data['tool']['poetry']['name']}\n"
    yaml_content += "channels:\n"
    yaml_content += "  - defaults\n"
    yaml_content += "dependencies:\n"
    for package, version in dependencies.items():
        if version.startswith('^'):
            version = version[1:]
        yaml_content += f"  - {package}={version}\n"

    # Write YAML content to file
    with open(yaml_file, 'w') as f:
        f.write(yaml_content)

# Specify the paths to your pyproject.toml and desired output YAML file
pyproject_toml = 'pyproject.toml'
conda_yaml = 'requirements.yml'

# Generate the Conda YAML file
generate_conda_yaml(pyproject_toml, conda_yaml)
