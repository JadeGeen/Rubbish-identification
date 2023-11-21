import torch

from ram.models import ram
from ram import inference_ram as inference
from ram import get_transform


def api(img: torch.Tensor, ) -> str:
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    transform = get_transform(image_size = img.size)
    model = ram(pretrained = 'ram_swin_large_14m.pth', image_size = img.size, vit = 'swin_1')
    model.eval()
    model = model.to(device)
    image = transform(img).unsqueeze(0).to(device)
    res = inference(image, model)
    return res[1]