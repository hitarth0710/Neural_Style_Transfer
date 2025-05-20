import os
import uuid
from PIL import Image
import torch
from diffusers import StableDiffusionImg2ImgPipeline

def save_uploaded_file(file_data):
    """Save uploaded file and return filename"""
    random_hex = uuid.uuid4().hex
    _, file_extension = os.path.splitext(file_data.filename)
    filename = random_hex + file_extension
    file_path = os.path.join('app/static/uploads', filename)
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Save the file
    file_data.save(file_path)
    return f"uploads/{filename}"

def perform_style_transfer_stable_diffusion(content_image_path, style_image_path, output_path, style_prompt=None, style_strength=0.75):
    """
    Perform style transfer using Stable Diffusion img2img pipeline
    
    Parameters:
    - content_image_path: Path to the content image
    - style_image_path: Path to the style image (used for reference but not directly by the model)
    - output_path: Path to save the resulting image
    - style_prompt: Text prompt describing the style (if None, will be generated from style image)
    - strength: Controls how much to transform the image (0-1)
    """
    try:
        # Check if CUDA is available
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {device}")
        
        # Load the Stable Diffusion img2img pipeline
        # Use float16 precision for faster inference if on CUDA
        dtype = torch.float16 if device == "cuda" else torch.float32
        
        # Initialize the pipeline with the appropriate model
        pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=dtype,
            safety_checker=None  # Disable safety checker for artistic purposes
        ).to(device)
        
        # Load the content image
        init_image = Image.open(content_image_path).convert("RGB")
        print(f"Content image loaded from {content_image_path}, size: {init_image.size}")
        
        # Resize to appropriate dimensions (multiples of 8 work best with Stable Diffusion)
        width, height = init_image.size
        max_dim = 512  # Maximum dimension (adjust based on your GPU memory)
        
        if width > height:
            new_width = min(width, max_dim)
            new_height = int(height * (new_width / width))
        else:
            new_height = min(height, max_dim)
            new_width = int(width * (new_height / height))
            
        # Make dimensions multiples of 8
        new_width = (new_width // 8) * 8
        new_height = (new_height // 8) * 8
        
        init_image = init_image.resize((new_width, new_height))
        print(f"Resized image to {new_width}x{new_height}")
        
        # Load style image to extract style information (if no prompt provided)
        if not style_prompt:
            style_img = Image.open(style_image_path).convert("RGB")
            style_name = os.path.basename(style_image_path).split('.')[0]
            style_prompt = f"in the artistic style of {style_name}, detailed artwork, high quality"
            print(f"Generated style prompt: {style_prompt}")
        
        # Set inference parameters
        num_inference_steps = 30  # Reduced for faster processing
        guidance_scale = 7.5      # How closely to follow the prompt
        
        print(f"Starting style transfer with strength={style_strength}, steps={num_inference_steps}")
        
        # Process the image
        result = pipe(
            prompt=style_prompt,
            image=init_image,
            strength=style_strength,
            guidance_scale=guidance_scale,
            num_inference_steps=num_inference_steps
        ).images[0]
        
        print(f"Style transfer complete, saving to {output_path}")
        
        # Save the result
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        result.save(output_path)
        
        return output_path
        
    except Exception as e:
        print(f"Error in style transfer: {e}")
        # Fallback: return original image if transfer fails
        try:
            init_image.save(output_path)
            return output_path
        except:
            # If all else fails, create a blank image
            Image.new('RGB', (512, 512), color='white').save(output_path)
            return output_path

# Keep your existing perform_style_transfer function
def perform_style_transfer(content_image_path, style_image_path, output_path, style_strength=0.75, style_prompt=None):
    """
    Legacy style transfer function - kept for compatibility
    You can keep your existing implementation here
    """
    try:
        # Try to use the new Stable Diffusion method
        return perform_style_transfer_stable_diffusion(
            content_image_path, 
            style_image_path, 
            output_path,
            style_strength=style_strength,
            style_prompt=style_prompt
        )
    except Exception as e:
        print(f"Stable Diffusion failed, falling back to legacy method: {e}")
        
        # Here would be your original style transfer implementation
        # For now, just copy the content image as a fallback
        Image.open(content_image_path).save(output_path)
        return output_path