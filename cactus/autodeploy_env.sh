# Env vars to determine what steps to run in autodeploy yeh

# Build an image with the new django only, not the python packages
export IMAGE_DJANGO=true

# Also build the python packages
export IMAGE_PIP=true

# Run the migrate command.
export MIGRATIONS=true

# Load the script in cactus/autodeploy_custom.sh
export CUSTOM_SHELL=false

# Load the fixtures
export LOADDATA=false

# Upload the static files to a bucket
export STATIC=false

# For when new settings in the deployment of kubernetes are added
export NEW_RELEASE=false

# Add a new cronjob
export CRONJOB=true
