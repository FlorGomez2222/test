import streamlit as st
import os
import json
from time import perf_counter
import ifcjson

# Título de la app
st.title("IFC to JSON Converter")

# Cargar archivo IFC
uploaded_file = st.file_uploader("Subir archivo IFC", type=["ifc"])

# Opciones de configuración
version = st.selectbox("Seleccionar versión de IFCJSON", ["4", "5a"])
compact = st.checkbox("Modo Compacto")
no_inverse = st.checkbox("No Inverse Relationships")
empty_properties = st.checkbox("Incluir Propiedades Vacías")
no_ownerhistory = st.checkbox("Eliminar IfcOwnerHistory")
geometry = st.selectbox("Tipo de Salida de Geometría", ["unchanged", "none", "tessellate"])

# Botón de conversión
if uploaded_file and st.button("Convertir a JSON"):
    t1_start = perf_counter()

    try:
        # Guardar el archivo IFC temporalmente
        ifc_path = "temp.ifc"
        with open(ifc_path, "wb") as f:
            f.write(uploaded_file.read())

        # Procesar conversión IFC a JSON
        if version == "4":
            json_data = ifcjson.IFC2JSON4(
                ifc_path,
                compact,
                NO_INVERSE=no_inverse,
                EMPTY_PROPERTIES=empty_properties,
                NO_OWNERHISTORY=no_ownerhistory,
                GEOMETRY=geometry
            ).spf2Json()
        elif version == "5a":
            json_data = ifcjson.IFC2JSON5a(
                ifc_path,
                compact,
                EMPTY_PROPERTIES=empty_properties
            ).spf2Json()
        else:
            st.error(f"Versión {version} no soportada.")
            st.stop()

        # Guardar JSON como archivo temporal
        json_path = "output.json"
        with open(json_path, 'w') as outfile:
            json.dump(json_data, outfile, indent=None if compact else 2)

        t1_stop = perf_counter()
        st.success(f"Conversión completada en {t1_stop - t1_start:.2f} segundos.")

        # Agregar botón de descarga
        with open(json_path, "rb") as f:
            st.download_button(
                label="Descargar JSON",
                data=f,
                file_name="converted.json",
                mime="application/json"
            )

    except Exception as e:
        st.error(f"Ocurrió un error: {str(e)}")
