from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import cv2
import os
import numpy as np
import brightest_patch
from fastapi.staticfiles import StaticFiles
import time

app = FastAPI()



origins = [
    '*',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the path to the "static" folder where you want to save the images
static_folder = os.path.join(os.path.dirname(__file__), "static")

# Ensure the "static" folder exists, create it if necessary
os.makedirs(static_folder, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_folder), name="static")

# @app.get("/")
# async def main():
#     return {"message": "Hello World"}


@app.post("/process-image")
async def upload_image(file: UploadFile):
    # Process the uploaded image (replace with your processing logic)
    # timestr = time.strftime("%Y%m%d-%H%M%S")
    if not file:
        raise HTTPException(status_code=400, detail="No image provided")

    # Save the uploaded image to the "static" folder
    image_path = os.path.join(static_folder, file.filename)
    with open(image_path, "wb") as image_file:
        image_file.write(file.file.read())


    patches = []
    patch_coordinates = [] 
    patch_mean_intensities = []

    brightest_patch.extract_patches(image_path, patches, patch_coordinates, patch_mean_intensities)

    # Return the computed results as JSON response
    
    brightest_four, brightest_patches_coordinates, mean_brightness = brightest_patch.four_brightest_patches(patches, patch_coordinates, patch_mean_intensities)

    corners = brightest_patch.patch_centers(brightest_patches_coordinates)

    area = brightest_patch.compute_area(corners)
    timestr = time.strftime("%Y%m%d-%H%M%S")
    
    output_basename = os.path.splitext(os.path.basename(image_path))[0]
    output_path = os.path.join(static_folder, output_basename+timestr+".png")
    brightest_patch.draw_area(image_path, corners, output_path)

    print(f'the area of the quadrilateral which the corners are the centers of the brightest patches of the image is: {area} pixels')

    return {"output_path": output_path, "message": f'the area of the quadrilateral which the corners are the centers of the brightest patches of the image is: {area} pixels'}

# favicon.ico
# timestamp for the input too? (yes to solve problems with input with the same name)

# Serve the HTML file
@app.get("/")
async def get_upload_page():
    html = await open("frontend/brightest_patches.html", "rb").read().decode("utf-8")
    return html