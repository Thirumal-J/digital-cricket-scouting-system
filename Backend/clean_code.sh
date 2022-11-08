autoflake --in-place --remove-unused-variables --remove-all-unused-imports .\\app.py
autoflake --in-place --remove-unused-variables --remove-all-unused-imports .\\config.py

autopep8 --in-place .\\app.py