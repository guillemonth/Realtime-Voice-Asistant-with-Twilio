# Setup steps
1. First clone the repository
    ```bash
    git clone https://github.com/guillemonth/Realtime-Voice-Asistant-with-Twilio.git
   ```

2. Create the virtual environment, in this case, i've chose to use [`uv`](https://docs.astral.sh/uv/guides/install-python/)
    ```bash
    #install uv
    pip instal uv

    #creation of the virtual environment
    uv venv
    ```

3. Initiate the environment
    ```bash
    #the location of the script might change depending on previous steps 
    <venv folder name>/Scripts/activate.bat #windows
    source .venv/bin/activate #linux
    ```

4. Once we have the env created, we hace to install the required packages. 
    ```bash
    uv sync
    ```
In case you opt to not to use a env manager, you can also setup the environment with the following commands:
```bash
#creation of the virtual environment
python -m venv [env name]

#instalation of the required packages
pip install -r requirements.txt
```
