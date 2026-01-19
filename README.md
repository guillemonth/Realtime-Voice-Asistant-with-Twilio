This is a small project to test the capabilities of the live API from google.
In this ocasion I've created a small virtual assistant to handle phone calls.
To do so, It uses the following tools:
- **Twilio**: Handles the phone calls.
- **Google Cloud Platform**: Hosts the llm model.
- **Python/FastAPI**: Backend server to handle the logic.
![base design](./img/base_design.png)


In order to setup the system, you need to complete the following steps:
# 1. Install the code
## 1. Prepare the environment
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
    source <venv folder name>/bin/activate #linux
    ```

4. Once we have the env created, we hace to install the required packages. 
    ```bash
    uv sync
    ```
In case you opt to not to use a env manager, you can also setup the environment with the following commands:
```bash
#creation of the virtual environment
python -m venv [env name]

#activating the virtial environment
<venv folder name>/Scripts/activate.bat #windows
source <venv folder name>/bin/activate #linux

#instalation of the required packages
pip install -r requirements.txt
```

To create the `.env` file, copy the file named `template.env` 
## 2. Running the server
In order to run the server, we first need to open a terminal window where the environment is running. Once that's checked, run the following command:
```bash
uvicorn main:app --port=8000
#This will start the FastApi server
```

Additionally, we need to expose the port to the Internet so Twilio can connect with the server. Some of the ways to do so are:
1. [Ngrok](https://ngrok.com/): creates a tunnel between your local port and the Internet and allows you create public services. Also allows you to reserve a static url to access.
2. [Visual Studio Ports](https://code.visualstudio.com/docs/debugtest/port-forwarding): Feature from Visual Studio that allows you to create a public endpoint redirecting a local server (make sure to choose the same port as used in the previous command). You may also need to make the port Public. By default is private and it won't work

Once we have our server exposed, store the url generated to later use it in the twilio config.
# 2. Setup Twilio
Twilio is a cloud software used to manage connections with clients via messages, emails or phone calls. In its free tier, gives 15€ of free credit wich is more than enough for this case.

## 1. First create an account : [link]([htttps://aaaa](https://login.twilio.com/u/signup?state=hKFo2SAyR0J1djBvN0JsNko4bjM2Y3RIendzLVBDZEtZS3BiZ6Fur3VuaXZlcnNhbC1sb2dpbqN0aWTZIEJQNnVWR3NGZURXai0xSDdLNHpBT3l0aHBVdWNyekJlo2NpZNkgTW05M1lTTDVSclpmNzdobUlKZFI3QktZYjZPOXV1cks))
You'll need and email account, and a phone number.
## 2. Buy a Phone Number: [link](https://console.twilio.com/us1/develop/phone-numbers/manage/search?isoCountry=US&types[]=Local&types[]=Mobile&types[]=Tollfree&capabilities[]=Fax&capabilities[]=Mms&capabilities[]=Sms&capabilities[]=Voice&searchTerm=&searchFilter=left&searchType=number)
   ![buy a phone](./img/buy_phone.png)
In case of buying a phone outside your current country, make sure that your phone company allows international calls.
## 3. Configue the phone number
Once the phone is bought, enter on its configuration and paste the url from **Step 2** and click the `Save Configuration` button at the bottom of the page.
![configure a phone](./img/configure_phone.png)
# 3. Configure Google Vertex AI 
## 1. Select project in Google Cloud
If you don't have a Google Cloud Account already, first [create one](https://cloud.google.com/products/storage?). Google gives you 200$ of free credit and 2 months to use it. If you do have one, select the project you want to use in this case.

## 2. Enable Vertex AI API
1. Once the desired project is selected, go to the [Vertex AI page](https://console.cloud.google.com/marketplace/product/google/aiplatform.googleapis.com) and enable the API
 
## 3. Enable Generative Language API
1. Go to the [Generative Language page](https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/credentials) and enable the API

## 4. Generate Service Account JSON
To authenticate in the API, we are going to use a service account credentials. If you already have the service account json, you can skip this step.

To create a service account, follow this steps:
1. Go to the [service account creation page](https://console.cloud.google.com/projectselector2/iam-admin/serviceaccounts/create) and follow the steps 
2. Once created, look for the service account that was just created, and click on the three dots on the right and `click manage keys`
![manage keys](./img/manage_keys.png)
1. Now create a new key and select `JSON`
![create new key](./img/create_new_key.png)

this will create a json file that, will look like this, but with your private keys:
```JSON
{
"type": "service_account",
"project_id": "",
"private_key_id": "",
"private_key": "-----BEGIN PRIVATE KEY----------END PRIVATE KEY-----",
"client_email": "",
"client_id": "",
"auth_uri": "https://accounts.google.com/o/oauth2/auth",
"token_uri": "https://oauth2.googleapis.com/token",
"auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
"client_x509_cert_url": "",
"universe_domain": "googleapis.com"
}
```

With this info, complete the `.env file` filling each variable with its equivalent node of the json file.