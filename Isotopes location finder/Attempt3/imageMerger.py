from PIL import Image

def merge_with_black_replacement(image_paths, output_path):
    # Open the first image and convert to RGBA
    base_image = Image.open(image_paths[0]).convert("RGBA")
    
    # Create the final image initialized with the first image
    merged_image = Image.new("RGBA", base_image.size)
    merged_image.paste(base_image)

    for image_path in image_paths[1:]:
        overlay_image = Image.open(image_path).convert("RGBA")

        # Ensure the overlay size matches the base image, resize if necessary
        if overlay_image.size != base_image.size:
            overlay_image = overlay_image.resize(base_image.size)

        # Go through each pixel and replace black pixels with non-black pixels from the overlay
        base_pixels = merged_image.load()
        overlay_pixels = overlay_image.load()
        
        for y in range(merged_image.height):
            for x in range(merged_image.width):
                base_pixel = base_pixels[x, y]
                overlay_pixel = overlay_pixels[x, y]

                # Replace black pixel in base image with non-black pixel in overlay if needed
                if base_pixel[:3] == (0, 0, 0) and overlay_pixel[:3] != (0, 0, 0):
                    base_pixels[x, y] = overlay_pixel

    # Convert final merged image to RGB before saving as JPEG
    final_image = merged_image.convert("RGB")
    final_image.save(output_path)

# Example usage:
image_paths = ['/Users/kaixinxue/Desktop/M400/GammaRobotFinalTest/20250321-193251_GammaRobot_Final_Test_multi_05/20250321-193626_SS/highResolutionCo60.jpg','/Users/kaixinxue/Desktop/M400/GammaRobotFinalTest/20250321-193251_GammaRobot_Final_Test_multi_05/20250321-193626_SS/highResolutionCs137.jpg']  # List of your images' paths
output_path = '/Users/kaixinxue/Desktop/M400/GammaRobotFinalTest/20250321-193251_GammaRobot_Final_Test_multi_05/20250321-193626_SS/imageMerged.jpg'
merge_with_black_replacement(image_paths, output_path)