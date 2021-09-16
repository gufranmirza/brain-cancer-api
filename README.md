### Brain Cancer API
This repository contains the API server that serves the trained model for deltecting the brain cancer from given `DICOM` images
API accepts the zipped file of `DICOM` images and run throught it trained model and predicts possible stage of cancer a from that images.
Its has four output classes 
- Stage I
- Stage II
- Stage III
- Stage IV

---

### Project Structure
Below is the details about the structure of the project
#### `/api`
- It contains the API server written in Python, It eexposes the Restful API for consumers
- `/upload` route accepts the zip file containing the `DICOM` images of a Brain
- It returns following response after runnig images through the Modle
```
{
    'predictions': {
        'grade_1': string,
        'grade_2': string,
        'grade_3': string,
        'grade_4': string,
    },
    "result_id": string
    "zip_id": string
}
```
Where each grade represents the possibility in percentage of having a Branin cancer of that stage

#### `/prepare_data`
This folder contains the Jupyter notebooks to pre-process the data for trainin. You can modify the size of data and image size in pixels from variables defined into the Juoyter notebooks. Processed data is stored as numpy array.

Training data for each stage of Brain Cancer can be found here https://wiki.cancerimagingarchive.net/display/Public/Brain-Tumor-Progression

#### `/train_models`
This folder contains the different Jupyter Notebooks for training the model. You can choose any of the model from the given models
- alexnet
- googlenet
- inception

Once model is trained, it can be served via server.

---

### Runnnig Server
There already trained models present at the `/api/api/models/inception`, in order to use it, we need to run API server run the follwoing
```
cd api

pip3 install -r requirements.txt

python3 manage.py runserver
```

---

### Frontend
You can use this frontend repository to upload image and interactive vizualization
- https://github.com/gufranmirza/brain-cancer-ui

----

![newplot (1)](https://user-images.githubusercontent.com/17959487/133690282-7664761b-c0e1-479a-b487-66b1c812dfe1.png)
![Screenshot from 2021-09-17 03-37-34](https://user-images.githubusercontent.com/17959487/133692129-00e3f7c7-77e9-4851-b695-c63c6ef30e64.png)

