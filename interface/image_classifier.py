import torch
from torchvision.models import squeezenet1_1, SqueezeNet1_1_Weights
from torchvision.io import decode_image
import torchvision.transforms as transforms
import torch.nn as NN

APP_PATH = "interface\\"

def classify(image_path, model_path=None):
    MODEL_PATH = model_path or APP_PATH + "model.pth"
    
    process = transforms.Compose([
        transforms.ConvertImageDtype(torch.float32),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    ### Model Creation ###
    model = squeezenet1_1(weights=SqueezeNet1_1_Weights.DEFAULT)
    model.classifier[1] = NN.Conv2d(512, 2, kernel_size=(1, 1),
                                  stride=(1, 1))  # replace final layer with binary classifier

    ### Restore Trained Weights ###
    saved_state = torch.load(MODEL_PATH)
    model.load_state_dict(saved_state['model_state_dict'])

    ### Process Image ###
    image_t = decode_image(image_path)
    image_norm = process(image_t).unsqueeze(0)
    with torch.inference_mode():
        output = model(image_norm)
    probabilities = torch.softmax(output, dim=1)
    classifications = torch.argmax(probabilities, dim=1)
    outcome = classifications[0].item()
    return {0: "Undamaged", 1:"Damaged"}[outcome]

if __name__ == "__main__":
    image_path = "616747.500000_3469528.500000_617131.500000_3469144.500000.jpg"
    print("Classification:", classify(image_path))


