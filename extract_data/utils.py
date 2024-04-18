import os
import extract_msg
import pandas as pd
from io import BytesIO
from PIL import Image
from google.oauth2 import service_account
from google.cloud import vision
import re
import io

def extract_pan_num(string):
    pan_number = ''
    pan_pattern = r'\b(?:[A-Z]{5}\d{4}[A-Z])|(?:[A-Z]{2}X{6}\d[A-Z])\b'
    pan_search = re.findall(pan_pattern, string)
    if pan_search:
        pan_number = pan_search[0]
    return pan_number

def extract_tan_num(string):
    tan_number = ''
    tan_pattern =  r'\b[A-Z]{4}\d{5}[A-Z]{1}\b'
    tan_search = re.findall(tan_pattern, string)
    if tan_search:
        tan_number = tan_search[0]
    return tan_number

def extract_cin_num(string):
    cin_number = ''
    cin_pattern_1 = r'\b[A-Z]{1}[0-9]{5}[A-Z]{2}[0-9]{4}[A-Z]{3}\b'
    # Pattern to match CIN format 2
    cin_pattern_2 = r'\b[U][\d]{5}[A-Z]{2}[\d]{4}[A-Z]{3}[\d]{6}\b'
    # Combine both patterns using the OR operator (|)
    combined_pattern = f'({cin_pattern_1})|({cin_pattern_2})'
    cin_search = re.findall(combined_pattern, string)
    if cin_search:
        cin_number= cin_search[0]
    return cin_number


def google_vision_key():
    data = {}
    data['type'] = "service_account"
    data['project_id'] = 'firsthv'
    data['private_key_id'] = '972cfd39328aa3e7f7cd570c11be9e874889d81a'
    data['private_key'] = '-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCk/owH1VvRNcCk\niD6BCACKts+7VxGEVVqzt6wsEPjuwFVCAzz28rf5Pc+Nz0oeGxcEEb5Xqor/indq\nJJ0UgiFMsZUjyCW8/EUoTXui+Cpf83gOh49Qm3h57gssgBopFZtCCXAcZl9uFqqL\nUWJPhBQZ3wuOSEOYsYSrcFv8VOV8JmSzUQmtWeNnRCwxDEhEJpUKfba/1onQQ2xp\nYXyVeDHD+mtyqYTfeihhmpU9vmx7FXfowbmfsjRhOvpOuzKnl0WY59Y3U2Wd11nf\ndT7EdfLeWiNzfIwvpQ5fSE1DDPECxBGEY2Mbj5r1NOVh0SsidyhOYAJHmj0sEycK\n00A1jFfFAgMBAAECggEAFyKgNPr8WG4OmKOIDCS4mrq+jxjK2oDzam7PRBCPLz8l\n1U9J7aCkHl1F7K8LyAPpascoJvfBbMqYKvh+VCFZFP1zmaRXclP3SIrw0q20l2a2\nx2bHuDhMoOA5jeBairc+YXicUUcji3a/LDDZtaeh/+ywHJ/SZqdBoJ5tL4kh8pHf\n7bKi1aApv89i8A2xafb++nO2o/6gPEXxaAUFh9YQkr2TF5xDJHhtVWNuLTxgARKN\nH+qL+kUCX5cJ+D4+86T7lnZmdNtc/XPuMLAkVfQB7r2q3moEwqBqA3E8JWQzUNMl\nhvYNeYnULNEvvFfAqOKqpacEt/cOZB+pHAYDjvb0sQKBgQDWcF6q6HFyDjVM/c+S\nfOebZR8rZ8CmvE3ndt1eAomXCRuTYyroe5kA7cLntnsuLgKzKMBf7o4nbDu1794B\nQ/uPHulNNlvvC1thB0Rb2tpYrtvN1ghI99kfzkJY4fkIyv7si37vK0oSA7LQYEtH\nqnGIDCKJRIfi2M0m1oIB+kDdzQKBgQDE+O0zn7tRBQHQRR5Gt+06UcpS6YKYkyrH\nUdyYO7hlP42vSQ2SDGPQIxpeKBlEzq45Vg6V97SIEnkkxZkPoN6bZnPKj2Uk16E2\nzBBDnlcWyXKBdgnToRESPhVbiI6A/WGK7dgye+MJlkcFmYekvjNo1y18Yh143c8q\noHVNhrSp2QKBgQCC7iNvOPOjjzdOJh6qM6d6gxiv+O5xH8J1VGc/Mk9uL7ptmHwn\nbOfz4DhEIHA/twog9/3V1SNowLYIlUe5ABhFv7r1UP57CzUlHjnH1+2/fixpFokC\nfIpO2DI8cOUMUF2sclPzljvomeeBQXpVbKVbSwV/SJ+ri3Jfh1Pj/zfB9QKBgAfk\neYyx/811R+dSfa4TvJuzn0nHNYZrjzFBZHdtHSxhaYn2gWayvGUgovPW43xQU8bU\nXe1AaalyJAyHJmTr6z+K0WTybfkV8s3BS32KIK83DzGEy0wBji+O8UgjpqIghQIO\nGbWcJTLDJMFir364aFLxHE95lvi62ow4tbqPhTmxAoGAXyZPMfzxVoXnvwM/QMEt\n4CwknPU/bJCWYtkkfcceePuHnyMz+WU1oPBcPYDAL7ZhUbUtJ59NJ2TyPbj1knTV\nN+zEK22gXfyEnLSjGRm0BZh7Q4skUHjOYhBHxlCMMHbTNJFuDIJDqR4T4MxttomO\nqlABK+rEelnVoVf4gdiVh5k=\n-----END PRIVATE KEY-----\n'
    data['client_email'] = 'eb-speechtotext@firsthv.iam.gserviceaccount.com'
    data['client_id'] = '116979972600003388557'
    data['auth_uri'] = "https://accounts.google.com/o/oauth2/auth"
    data['token_uri'] = "https://oauth2.googleapis.com/token"
    data['auth_provider_x509_cert_url'] = "https://www.googleapis.com/oauth2/v1/certs"
    data['client_x509_cert_url'] = "https://www.googleapis.com/robot/v1/metadata/x509/eb-speechtotext%40firsthv.iam.gserviceaccount.com"
    return data


def detect_text_from_google_vision(content):
    """Detects text in the file."""

    print("Enterend into textract")
    ocr_string = ''
    try:
        GOOGLE_VISION_KEY = google_vision_key()
        credentials = service_account.Credentials.from_service_account_info(info=GOOGLE_VISION_KEY)
        client = vision.ImageAnnotatorClient(credentials=credentials)
        image = vision.Image(content=content)
        response = client.text_detection(image=image)
        texts = response.text_annotations
        ocr_string = texts[0].description
        if response.error.message:
            print("ocr_string have some error {}".format(response.error.message))
    except Exception as ex:
        print(ex)
    return ocr_string


"""this function works like after found docx this will delete the msg file"""

# import os
# import extract_msg

# def extract_word_files_from_msg(input_folder, output_folder):
#     # Ensure output folder exists
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)

#     # Iterate through each .msg file in the input folder
#     for filename in os.listdir(input_folder):
#         if filename.endswith('.msg'):
#             msg_file_path = os.path.join(input_folder, filename)
#             try:
#                 msg = extract_msg.Message(msg_file_path)
#                 docx_found = False  # Flag to track if a .docx file is found
#                 # Iterate through attachments in the .msg file
#                 for attachment in msg.attachments:
#                     try:
#                         # Check if attachment is a Word file
#                         if attachment.name.lower().endswith('.docx'):
#                             docx_found = True
#                             # Save Word file to output folder
#                             output_file_path = os.path.join(output_folder, attachment.name)
#                             with open(output_file_path, 'wb') as f:
#                                 f.write(attachment.data)
#                             print(f"Successfully saved .docx file '{attachment.name}'")
#                             break  # Exit the loop after saving the .docx file
#                     except AttributeError:
#                         print(f"Issue with processing attachment in {msg_file_path}")

#                 # Close the Message object to release the file handle
#                 msg.close()

#                 # Remove the .msg file only if a .docx file was found
#                 if docx_found:
#                     os.remove(msg_file_path)
#                     print(f".msg file '{filename}' deleted after successfully saving the .docx file.")
#                 else:
#                     print(f"No .docx file found in '{filename}', .msg file will not be deleted.")

#             except Exception as e:
#                 print(f"Error processing {msg_file_path}: {e}")


import os
import extract_msg

def extract_word_files_from_msg(input_folder, output_folder):
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through each .msg file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.msg'):
            msg_file_path = os.path.join(input_folder, filename)
            msg_filename = os.path.splitext(filename)[0]  # Extract filename without extension
            try:
                msg = extract_msg.Message(msg_file_path)
                docx_found = False  # Flag to track if a .docx file is found
                # Iterate through attachments in the .msg file
                for attachment in msg.attachments:
                    try:
                        # Check if attachment is a Word file
                        if attachment.name.lower().endswith('.docx'):
                            docx_found = True
                            # Construct the output filename using both .docx and .msg filenames
                            output_filename = f"{os.path.splitext(attachment.name)[0]}_{msg_filename}.docx"  # Concatenate .docx and .msg filenames
                            output_file_path = os.path.join(output_folder, output_filename)
                            with open(output_file_path, 'wb') as f:
                                f.write(attachment.data)
                            print(f"Successfully saved .docx file '{output_filename}'")
                            print(f".msg file '{filename}' one docx file fetched operation seccessfully completed. ")
                            break  # Exit the loop after saving the .docx file
                    except AttributeError:
                        print(f"Issue with processing attachment in {msg_file_path}")

                # Close the Message object to release the file handle
                msg.close()

                # Remove the .msg file only if a .docx file was found
                if docx_found:
                    os.remove(msg_file_path)
                    print(f".msg file '{filename}' deleted after successfully saving the .docx file.")
                    
                else:
                    print(f"No .docx file found in '{filename}', .msg file will not be deleted.")

            except Exception as e:
                print(f"Error processing {msg_file_path}: {e}")





"""Final Code"""

def extract_data_from_img(directory, doc_file_path):
    excel_dir = 'D:/HCL/extrCost/extracted_data_excel/'
    excel_file_path = os.path.join(excel_dir, 'extracted_data_production.xlsx')

    if os.path.exists(excel_file_path):
        # Load existing Excel file
        df = pd.read_excel(excel_file_path)
    else:
        # Create a new DataFrame if Excel file doesn't exist
        df = pd.DataFrame(columns=["CIN", "PAN", "TAN", "Word_File_Name"])

    directory_files = os.listdir(directory)
    new_data = {"CIN": [], "PAN": [], "TAN": [], "Word_File_Name": []}

    for file in directory_files:
        image_path = os.path.join(directory, file)
        image = Image.open(image_path)
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='PNG')
        bytes_data = image_bytes.getvalue()
        extracted_text = detect_text_from_google_vision(bytes_data)
        pan = extract_pan_num(extracted_text)
        tan = extract_tan_num(extracted_text)
        cin = extract_cin_num(extracted_text)

        if pan is not None and pan:
            new_data["PAN"].append(pan)

        if tan is not None and tan:
            new_data["TAN"].append(tan)

        if cin is not None and cin:
            new_data["CIN"].append(cin)

    
    new_data["Word_File_Name"].append(doc_file_path)
    new_data["CIN"]=list(set(new_data["CIN"]))
    new_data["PAN"]=list(set(new_data["PAN"]))
    new_data["TAN"]=list(set(new_data["TAN"]))
    # Find the length of the longest list
    max_length = max(len(new_data["PAN"]), len(new_data["TAN"]), len(new_data["CIN"]), len(new_data["Word_File_Name"]))

    # Pad shorter lists with None to match the length of the longest list
    new_data["PAN"] += [None] * (max_length - len(new_data["PAN"]))
    new_data["TAN"] += [None] * (max_length - len(new_data["TAN"]))
    new_data["CIN"] += [None] * (max_length - len(new_data["CIN"]))
    new_data["Word_File_Name"] += [None] * (max_length - len(new_data["Word_File_Name"]))

    # Convert new_data to DataFrame
    new_df = pd.DataFrame(new_data)

    # Append new_df to df if df is not empty
    if not df.empty:
        df = pd.concat([df, new_df], ignore_index=True)
    else:
        df = new_df

    # Write the DataFrame to the Excel file
    df.to_excel(excel_file_path, index=False)
    return excel_file_path
