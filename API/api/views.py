import random
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import cv2
import uuid
import os
from django.core.files.storage import FileSystemStorage

import numpy as np
import dicom
import zipfile

# 3d utils function
from .plot_utils import get_pixels_hu, resample, plotly_3d, make_mesh


from .models.inception.model import get_model
PX_SIZE = 256
L = 1e-3

MODEL_NAME = 'tf-model-{}-{}.model'.format(L, '256X256-10000X4-IMAGES')
basedir = os.path.abspath(os.path.dirname(__file__))


class Upload(APIView):
    def __init__(self):
        self.model = get_model()
        if os.path.exists('./models/inception/{}.meta'.format(MODEL_NAME)):
            self.model.load(MODEL_NAME)
            print('model loaded!', MODEL_NAME)

    @staticmethod
    def load_scan(path):
        print("\nreading dicom files\n")

        slices = [dicom.read_file(path + '/' + s) for s in os.listdir(path)]
        slices.sort(key = lambda x: float(x.ImagePositionPatient[2]))

        try:
            slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
        except:
            slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)

        for s in slices:
            s.SliceThickness = slice_thickness

        return slices


    @staticmethod
    def predict(self, path):
        a = b = c = d = 0,
        image_data = []
        count = len(os.listdir(path))
        for s in os.listdir(path):

            slice = dicom.read_file(path + '/' + s)
            img = cv2.resize(np.array(slice.pixel_array),(PX_SIZE,PX_SIZE))

            image_id = str(uuid.uuid1()) + ".jpg"
            image_path = path + '/' + image_id
            cv2.imwrite(image_path, img)

            img_data = np.array(img)

            data = img_data.reshape(PX_SIZE,PX_SIZE,1)
            model_out = self.model.predict([data])[0]

            print(model_out)

            a += model_out[0]
            b += model_out[1]
            c += model_out[2]
            d += model_out[3]

            image_data_raw = {
                "image_id": image_id,
                "score": model_out
            }
            image_data.append(image_data_raw)

        return a/count, b/count, c/count, d/count, image_data

    def post(self, request, format=None):

        file = request.FILES['file']
        fs = FileSystemStorage()
        id = str(uuid.uuid1())

        target = os.path.join(basedir, 'static/' + id)

        filename = fs.save(target + '.zip', file)

        fantasy_zip = zipfile.ZipFile(filename)
        fantasy_zip.extractall(target)
        fantasy_zip.close()

        scan = os.listdir(target)

        final_path = target + '/' + scan[0] + '/'
        zip_id = scan[0]
        slices = self.load_scan(final_path)

        # Predict
        a,b,c,d,image_data = self.predict(self, final_path)
        a = float("{0:.2f}".format(a[0]))
        b = float("{0:.2f}".format(b[0]))
        c = float("{0:.2f}".format(c[0]))
        d = float("{0:.2f}".format(d[0]))

        Plot
        pixels_hu = get_pixels_hu(slices=slices)
        pix_resampled, spacing = resample(pixels_hu, slices, [1,1,1])
        v, f = make_mesh(pix_resampled, 350)
        plotly_3d(v, f)

        return Response({
            'data': {
                'predictions': {
                    'grade_1': a,
                    'grade_2': b,
                    'grade_3': c,
                    'grade_4': d,
                },
                "result_id": id,
                "zip_id": zip_id,
                "image_data": image_data
            },
            'status': 200,
        }, status=status.HTTP_200_OK)
