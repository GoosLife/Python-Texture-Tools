from PIL import Image
import os

def find_texture_maps(folder_path):
    # Dictionary to hold the mapping of prefixes to their corresponding file paths
    texture_files = {}

    # Loop through all files in the given folder
    for file in os.listdir(folder_path):
        # Check if the file matches the expected pattern
        for suffix in ['metallic', 'AO', 'GLOSS']:
            if file.lower().endswith(suffix.lower() + '.jpeg') or file.lower().endswith(suffix.lower() + '.png'):
                prefix = file.rsplit('_', 1)[0]
                texture_type = suffix.upper()
                if prefix not in texture_files:
                    texture_files[prefix] = {}
                texture_files[prefix][texture_type] = os.path.join(folder_path, file)
                break

    return texture_files

def combine_maps(prefix, texture_map_paths, output_folder):
    # Initialize a dictionary to hold the images
    images = {}
    # Check if there are at least two texture maps to combine
    if len(texture_map_paths) < 2:
        return
    for map_type, path in texture_map_paths.items():
        # Load and convert the image to grayscale
        images[map_type] = Image.open(path).convert('L')
    
    # Assume all images are the same size as the first
    width, height = next(iter(images.values())).size

    # Create a new image with RGBA mode
    combined_img = Image.new("RGBA", (width, height))
    
    # Load pixels
    for x in range(width):
        for y in range(height):
            pixels = {
                'METALLIC': images['METALLIC'].getpixel((x, y)) if 'METALLIC' in images else 0,
                'AO': images['AO'].getpixel((x, y)) if 'AO' in images else 0,
                'GLOSS': images['GLOSS'].getpixel((x, y)) if 'GLOSS' in images else 255, # Default alpha to 255
            }
            # Set the pixels accordingly
            combined_img.putpixel((x, y), (pixels['METALLIC'], pixels['AO'], 0, pixels['GLOSS']))
    
    # Define the output file name based on available maps
    output_file_name = f"{prefix}_{'_'.join(texture_map_paths.keys())}.png"
    output_path = os.path.join(output_folder, output_file_name)
    
    # Save the combined image
    combined_img.save(output_path)
    print(f"Saved combined texture to {output_path}")

def process_folder(folder_path, output_folder):
    texture_map_groups = find_texture_maps(folder_path)
    
    for prefix, paths in texture_map_groups.items():
        if ('METALLIC') in  paths:
            combine_maps(prefix, paths, output_folder)

# Example usage
source_folder = os.getcwd()
output_folder = os.getcwd()
process_folder(source_folder, output_folder)