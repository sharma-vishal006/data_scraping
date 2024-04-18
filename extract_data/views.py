from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from io import BytesIO
import requests, os, re, io
from PIL import Image
from google.oauth2 import service_account
from google.cloud import vision
from docx import Document
import pandas as pd
from django.http import JsonResponse
from rest_framework.decorators import action
from .utils import extract_data_from_img


def extract_images_from_docx(docx):
    try:
        images = []
        for rel in docx.part.rels.values():
            if "image" in rel.target_ref:
                image_data = rel.target_part.blob
                images.append(image_data)        
    except Exception as ex:
        print(f"Error extracting images from DOCX: {ex}")
    return images    


 
 
 
def delete_images(directory_path):
    files = os.listdir(directory_path)
    for file in files:
        file_path = os.path.join(directory_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
        else:    
            pass
    return True




class ExtractImageFromDoc(APIView):

    def get(self, request):
        directory = "Directory where you want to store docx file"
        directory_files = os.listdir(directory)
        all_files_processed = False  # Flag to track if all files have been processed
        
        while not all_files_processed:
            all_files_processed = True  # Assume all files have been processed until proven otherwise
            
            for doc_files in directory_files:
                doc_file_name = doc_files
                file_path = os.path.join(directory, doc_files)
                
                if not os.path.exists(file_path):
                    # Skip if the file no longer exists
                    continue
                
                try:
                    with open(file_path, "rb") as file:
                        content = file.read()
                    bytesio_obj = BytesIO(content)
                    
                    bytesio_obj.seek(0)
                    docx_content = BytesIO(bytesio_obj.getvalue())
                    docx = Document(docx_content)
                    images = extract_images_from_docx(docx=docx)
                    
                    if images:
                        os.remove(file_path)
                        directory_path = "folder path where you want to store fetched images from docx file"
                        
                        for i, image in enumerate(images):
                            filename = "img_"+str(i)+'.png'
                            os.makedirs(directory_path, exist_ok=True)
                            image_file_path = os.path.join(directory_path, filename)
                            
                            with open(image_file_path, "wb") as img_file:
                                img_file.write(image)
                        
                        # Extract and process data from images
                        data = extract_data_from_img(directory_path, doc_file_name)  
                        
                        # Iterate over each file in the directory and delete them
                        for img_file_name in os.listdir(directory_path):
                            img_file_path = os.path.join(directory_path, img_file_name)
                            try:
                                if os.path.isfile(img_file_path):
                                    os.remove(img_file_path)
                            except Exception as e:
                                print(f"Error deleting file {img_file_path}: {e}")

                        # Set the flag to False if there are still files remaining
                        all_files_processed = False
                        
                except Exception as ex:
                    print(f"Error processing {file}: {ex}")
        
        return Response({"message": "All docx files processed and data saved successfully into Excel file."}, status=status.HTTP_200_OK)
    


class Msgtoword(APIView):
    # @action(detail=False, methods=["post"])
    def post(self, request):
        input_path = 'Directory input path from where you will pick msg files'
        output_path = 'Directory output path where you want to save docx files'
        from .utils import extract_word_files_from_msg
        # Call the trim_video function
        try:
            print("Exctracting data started.......")
            try:
                extract_word_files_from_msg(input_path, output_path)
            except Exception as e:
                print("Exception has been occured:",e)
            response_data = {"message": "Fetching data from the msg file success."}
            return JsonResponse(response_data, status=200)
        except Exception as e:
            response_data = {"error": str(e)}
            return JsonResponse(response_data, status=500)

