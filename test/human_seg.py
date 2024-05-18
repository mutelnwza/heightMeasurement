import torch
import torchvision.transforms as T
from PIL import Image
import matplotlib.pyplot as plt

# Load pre-trained DeepLabV3 model
model = torch.hub.load('pytorch/vision:v0.13.0', 'deeplabv3_resnet50', weights='DeepLabV3_ResNet50_Weights.DEFAULT')
model.eval()

# Preprocess the image
def preprocess(image_path):
    input_image = Image.open(image_path)
    preprocess = T.Compose([
        T.Resize(256),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    input_tensor = preprocess(input_image)
    input_batch = input_tensor.unsqueeze(0)
    return input_batch

# Predict
image_path = 'test_img/half.jpg'
input_batch = preprocess(image_path)
with torch.no_grad():
    output = model(input_batch)['out'][0]
output_predictions = output.argmax(0)

# Find the highest position of height (y) in the segmentation
y, x = torch.where(output_predictions == output_predictions.max())
highest_y_position = y.max().item()
print(f"The highest position of y in the segmentation is: {highest_y_position}")

# Visualize the results
plt.imshow(output_predictions.cpu().numpy())
plt.show()
