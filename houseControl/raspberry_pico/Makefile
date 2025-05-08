# Makefile
# Configura el puerto de conexión
PORT=/dev/ttyACM0

# Encuentra todos los archivos .py en el directorio actual
PY_FILES=$(wildcard *.py)

# Regla principal
all: upload

# Regla para copiar cada archivo .py al dispositivo
upload:
	@for file in $(PY_FILES); do \
		echo "Copiando $$file..."; \
		mpremote connect $(PORT) rm $$file ; \
		mpremote connect $(PORT) cp $$file :; \
	done
	mpremote connect $(PORT) run main.py
