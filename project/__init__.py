import torch
import torchvision.transforms as transforms
import numpy as np
from torchvision.transforms import Resize, ToTensor, ToPILImage
from PIL import Image


def encode(img, bottleneck):
    """
    Your code here
    img: a 256x256 PIL Image
    bottleneck: an integer from {4096,16384,65536}
    return: a numpy array less <= bottleneck bytes
    """
    input_transform = transforms.Compose([Resize((256, 256)), ToTensor()])
    x = input_transform(img).unsqueeze(0)

    h1 = (
        torch.zeros(1, 256, 64, 64),
        torch.zeros(1, 256, 64, 64)
    )
    h2 = (
        torch.zeros(1, 512, 32, 32),
        torch.zeros(1, 512, 32, 32))
    h3 = (
        torch.zeros(1, 512, 16, 16),
        torch.zeros(1, 512, 16, 16)
    )

    codes = binarizer.forward(encoder(x, h1, h2, h3)[0]).detach().numpy().astype(np.int8)
    codes = np.packbits(codes, axis=1)
    print(f"nbytes: {codes.nbytes}")
    return codes
    
def decode(x, bottleneck):
    """
    Your code here
    x: a numpy array
    bottleneck: an integer from {4096,16384,65536}
    return a 256x256 PIL Image
    """
    x = np.unpackbits(x, axis=1)
    h1 = (
        torch.zeros(1, 512, 16, 16),
        torch.zeros(1, 512, 16, 16)
    )
    h2 = (
        torch.zeros(1, 512, 32, 32),
        torch.zeros(1, 512, 32, 32)
    )
    h3 = (
        torch.zeros(1, 256, 64, 64),
        torch.zeros(1, 256, 64, 64)
    )
    h4 = (
        torch.zeros(1, 128, 128, 128),
        torch.zeros(1, 128, 128, 128)
    )

    output = decoder.forward(torch.Tensor(x), h1, h2, h3, h4)[0]
    output = output.squeeze(0)
    tensor_to_image = transforms.ToPILImage()
    image = tensor_to_image(output)
    return image


"""
Loading in Model
"""
from .models import Encoder, Binarizer, Decoder

encoder = Encoder()
binarizer = Binarizer()
decoder = Decoder()

encoder.eval()
binarizer.eval()
decoder.eval()

# Load model weights here
model_name = 'clstm_sigmoid_stochastic_scheduler'
encoder.load_state_dict(torch.load('project/save/{model_name}_e.pth'.format(model_name=model_name), map_location='cpu')['model_state_dict'])
binarizer.load_state_dict(torch.load('project/save/{model_name}_b.pth'.format(model_name=model_name), map_location='cpu')['model_state_dict'])
decoder.load_state_dict(torch.load('project/save/{model_name}_d.pth'.format(model_name=model_name), map_location='cpu')['model_state_dict'])
