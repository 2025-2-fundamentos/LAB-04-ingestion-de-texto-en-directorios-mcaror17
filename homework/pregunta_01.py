# pylint: disable=import-outside-toplevel
# pylint: disable=line-too-long
# flake8: noqa
"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""
import os
import zipfile
import pandas as pd

def pregunta_01():
    """
    La información requerida para este laboratio esta almacenada en el
    archivo "files/input.zip" ubicado en la carpeta raíz.
    Descomprima este archivo.

    Como resultado se creara la carpeta "input" en la raiz del
    repositorio, la cual contiene la siguiente estructura de archivos:


    ```
    train/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    test/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    ```

    A partir de esta informacion escriba el código que permita generar
    dos archivos llamados "train_dataset.csv" y "test_dataset.csv". Estos
    archivos deben estar ubicados en la carpeta "output" ubicada en la raiz
    del repositorio.

    Estos archivos deben tener la siguiente estructura:

    * phrase: Texto de la frase. hay una frase por cada archivo de texto.
    * sentiment: Sentimiento de la frase. Puede ser "positive", "negative"
      o "neutral". Este corresponde al nombre del directorio donde se
      encuentra ubicado el archivo.

    Cada archivo tendria una estructura similar a la siguiente:

    ```
    |    | phrase                                                                                                                                                                 | target   |
    |---:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|
    |  0 | Cardona slowed her vehicle , turned around and returned to the intersection , where she called 911                                                                     | neutral  |
    |  1 | Market data and analytics are derived from primary and secondary research                                                                                              | neutral  |
    |  2 | Exel is headquartered in Mantyharju in Finland                                                                                                                         | neutral  |
    |  3 | Both operating profit and net sales for the three-month period increased , respectively from EUR16 .0 m and EUR139m , as compared to the corresponding quarter in 2006 | positive |
    |  4 | Tampere Science Parks is a Finnish company that owns , leases and builds office properties and it specialises in facilities for technology-oriented businesses         | neutral  |
    ```


    """
    zip_path = "files/input.zip"
    extract_path = "files/input"  # carpeta donde se descomprime
    output_path = "files/output"

    os.makedirs(output_path, exist_ok=True)

    # Descomprimir el ZIP (si no existe la carpeta descomprimida)
    if not os.path.exists(extract_path):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall("files")  # extraemos directamente en files/

    # La carpeta raíz dentro del ZIP es 'input'
    data_root = os.path.join("files", "input")

    def build_dataset(folder_path):
        data = []
        for sentiment in ["negative", "neutral", "positive"]:
            sentiment_path = os.path.join(folder_path, sentiment)
            if not os.path.exists(sentiment_path):
                continue
            for filename in sorted(os.listdir(sentiment_path)):
                file_path = os.path.join(sentiment_path, filename)
                if os.path.isfile(file_path) and filename.endswith(".txt"):
                    with open(file_path, "r", encoding="utf-8") as f:
                        phrase = f.read().strip()
                        if phrase:
                            data.append({"phrase": phrase, "target": sentiment})
        return pd.DataFrame(data)

    # Crear datasets
    train_df = build_dataset(os.path.join(data_root, "train"))
    test_df = build_dataset(os.path.join(data_root, "test"))

    if train_df.empty or test_df.empty:
        raise ValueError("El dataset está vacío. Verifica la ruta de extracción.")

    # Guardar CSVs
    train_df.to_csv(os.path.join(output_path, "train_dataset.csv"), index=False)
    test_df.to_csv(os.path.join(output_path, "test_dataset.csv"), index=False)
