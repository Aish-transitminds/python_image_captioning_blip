from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import gradio as gr
import os

# Load model and processor
def load_model():
    try:
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        return processor, model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None, None

# Define the caption generation function
def generate_caption(img, processor, model):
    try:
        if not isinstance(img, Image.Image):
            img = Image.fromarray(img)  # Ensure the input is a PIL Image
        
        # Preprocess the image
        inputs = processor(images=img, return_tensors="pt")

        # Generate the caption
        output_ids = model.generate(**inputs)
        
        # Decode the output
        caption = processor.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return caption
    except Exception as e:
        return f"Error generating caption: {e}"

# Main block to ensure multiprocessing works correctly
if __name__ == "__main__":
    # Load model and processor
    processor, model = load_model()
    if processor is None or model is None:
        print("Failed to load the model. Exiting.")
    else:
        # Design the Gradio interface
        with gr.Blocks() as demo:

            # Add a background image using CSS
            demo.add(gr.HTML(
                """
                <style>
                    body {
                        margin: 0;
                        padding: 0;
                        background-image: url('file:///C:/Users/Aish/OneDrive/Desktop/python_image_captioning_blip/background.jpg');
                        background-size: cover;
                        background-position: center;
                        height: 100vh;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                    }

                    #root {
                        position: relative;
                        width: 100%;
                        height: 100%;
                    }

                    .gr-button {
                        font-size: 18px;
                        padding: 12px 24px;
                        border-radius: 12px;
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        cursor: pointer;
                        font-weight: bold;
                        text-transform: uppercase;
                        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
                        transition: all 0.3s ease;
                    }

                    .gr-button:hover {
                        transform: scale(1.1);
                        background-color: #45a049;
                        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.4);
                    }

                    .gr-button:active {
                        background-color: #388e3c;
                        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
                    }

                    .gr-image {
                        transition: transform 0.3s ease, box-shadow 0.3s ease;
                    }
                    .gr-image:hover {
                        transform: scale(1.05);
                        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
                    }

                    .gr-textbox {
                        font-family: 'Arial', sans-serif;
                        font-size: 16px;
                        transition: border-color 0.3s ease, box-shadow 0.3s ease;
                    }
                    .gr-textbox:focus {
                        border-color: #4CAF50;
                        box-shadow: 0 0 10px rgba(76, 175, 80, 0.5);
                    }

                    .gr-markdown {
                        font-size: 24px;
                        font-weight: bold;
                        text-align: center;
                        color: white;
                    }
                </style>
                """
            ))

            # Header and Upload section
            with gr.Row():
                with gr.Column():
                    image_input = gr.Image(label="Upload Your Image", type="numpy", elem_classes="gr-image")
                with gr.Column():
                    gr.Markdown(
                        """
                        # 📸 AI Image Captioning
                        Upload an image, and the AI will generate a descriptive caption for it!
                        """
                    )
                    caption_output = gr.Textbox(label="Generated Caption", lines=3, interactive=False, elem_classes="gr-textbox")

            # Button for caption generation
            generate_button = gr.Button("Generate Caption", elem_classes="gr-button")

            # Connect the function
            generate_button.click(
                fn=lambda img: generate_caption(img, processor, model),
                inputs=[image_input],
                outputs=[caption_output]
            )

            # Footer
            gr.Markdown(
                """
                Created by [AISH](#). Powered by the BLIP Model.
                """
            )

        # Launch the application
        demo.launch()
