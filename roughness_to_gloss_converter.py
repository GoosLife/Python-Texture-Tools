from PIL import Image
import os

def convert_roughness_to_gloss(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for filename in os.listdir(input_dir):
        if 'roughness' in filename.lower() and filename.lower().endswith(('png', 'jpg', 'jpeg', 'tiff', 'bmp')):
            gloss_filename = filename.replace('roughness', 'GLOSS')
            roughness_path = os.path.join(input_dir, filename)
            gloss_path = os.path.join(output_dir, gloss_filename)
            
            with Image.open(roughness_path) as img:
                # Convert to grayscale in case it's not
                img = img.convert('L')
                # Invert image
                img = Image.eval(img, lambda x: 255 - x)
                img.save(gloss_path)

# Example usage
input_directory = os.getcwd()
output_directory =  os.getcwd()
convert_roughness_to_gloss(input_directory, output_directory)
