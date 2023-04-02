#!/bin/bash

# Check number of arguments
if [ $# -ne 1 ];then
    echo "Usage: $0 sdf_dir"
    exit 1
fi

# Check the argument is a directory
if [ ! -d "$1" ]; then
  echo "El directorio $1 no existe"
  exit 1
fi

# Convert to urdf all sdf files
for file in "$1"/*.sdf; do
  if [ -f "$file" ]; then
    file_name=$(echo "$file" | sed 's/.*\///;s/\..*$//')
    rosrun pysdf sdf2urdf.py "$file" "$1/urdf/$file_name.urdf" > /dev/null
  fi
done
