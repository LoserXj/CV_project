import os
import argparse

from PIL import Image
import numpy as np

import torch
from torchvision.transforms.functional import to_tensor, to_pil_image

from .model import Generator

import cv2
import torchvision.transforms as transforms
from flask import Flask, request, make_response, send_from_directory
import cv2
import os
from deepface import DeepFace
import numpy as np

torch.backends.cudnn.enabled = False
torch.backends.cudnn.benchmark = False
torch.backends.cudnn.deterministic = True


def to_32s(x):
    return 256 if x < 256 else x - x % 32


def load_image(image_path, x32=True):
    img = Image.open(image_path).convert("RGB")
    print(img.size)
    w, h = img.size
    while w > 1000:
        w = w * 3 // 4
        h = h * 3 // 4
    while h > 1000:
        w = w * 3 // 4
        h = h * 3 // 4
    w = to_32s(w)
    h = to_32s(h)
    img = img.resize((to_32s(w), to_32s(h)), Image.Resampling.LANCZOS)
    print(img.size)

    return img


def test(args):
    device = args.device

    net = Generator()
    net.load_state_dict(torch.load(args.checkpoint, map_location="cpu"))
    net.to(device).eval()
    # print(f"model loaded: {args.checkpoint}")

    os.makedirs(args.output_dir, exist_ok=True)

    for image_name in sorted(os.listdir(args.input_dir)):
        if os.path.splitext(image_name)[-1].lower() not in [
            ".jpg",
            ".png",
            ".bmp",
            ".tiff",
        ]:
            continue

        image = load_image(os.path.join(args.input_dir, image_name), args.x32)

        with torch.no_grad():
            image = to_tensor(image).unsqueeze(0) * 2 - 1
            print(image.shape)
            out = net(image.to(device), args.upsample_align).cpu()
            out = out.squeeze(0).clip(-1, 1) * 0.5 + 0.5
            out = to_pil_image(out)

        out.save(os.path.join(args.output_dir, image_name))
        print(f"image saved: {image_name}")


def animate():
    device = "cpu"
    net = Generator()
    net.load_state_dict(
        torch.load("animegan2/weights/face_paint_512_v2.pt", map_location="cpu")
    )
    net.to(device).eval()
    filename = request.files["image"].filename
    image = request.files["image"].read()
    image_array = np.asarray(bytearray(image), dtype=np.uint8())
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    h = image.shape[0]
    w = image.shape[1]
    # while w > 1000:
    #     w = w * 3 // 4
    #     h = h * 3 // 4
    # while h > 1000:
    #     w = w * 3 // 4
    #     h = h * 3 // 4
    # w = to_32s(w)
    # h = to_32s(h)
    if w > 1200 or h > 1200:
        image = cv2.resize(image, (w // 2, h // 2), cv2.INTER_AREA)
    # image = cv2.resize(image, (w, h))
    transf = transforms.ToTensor()
    img_tensor = transf(image)
    with torch.no_grad():
        image = img_tensor.unsqueeze(0) * 2 - 1
        out = net(image.to(device), False).cpu()
        out = out.squeeze(0).clip(-1, 1) * 0.5 + 0.5
        array1 = out.numpy()
        maxValue = array1.max()
        array1 = array1 * 255 / maxValue
        mat = np.uint8(array1)
        mat = mat.transpose(1, 2, 0)
        cv2.imwrite("./animation/" + filename, mat)
        _, buffer = cv2.imencode(".jpg", mat)
        # 使用make_response创建响应
        response = make_response(buffer.tobytes())
        # 设置MIME类型
        response.mimetype = "image/jpeg"
        response.headers.set(
            "Content-Disposition", "attachment", filename="image_animate.jpg"
        )
        return response


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--checkpoint",
        type=str,
        default="./weights/face_paint_512_v2.pt",
    )
    parser.add_argument(
        "--input_dir",
        type=str,
        default="./imgs",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="./results",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cpu",
    )
    parser.add_argument(
        "--upsample_align",
        type=bool,
        default=False,
        help="Align corners in decoder upsampling layers",
    )
    parser.add_argument(
        "--x32", action="store_true", help="Resize images to multiple of 32"
    )
    args = parser.parse_args()

    animate()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--checkpoint",
        type=str,
        default="./weights/face_paint_512_v2.pt",
    )
    parser.add_argument(
        "--input_dir",
        type=str,
        default="./imgs",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="./results",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cpu",
    )
    parser.add_argument(
        "--upsample_align",
        type=bool,
        default=False,
        help="Align corners in decoder upsampling layers",
    )
    parser.add_argument(
        "--x32", action="store_true", help="Resize images to multiple of 32"
    )
    args = parser.parse_args()

    # test(args)
    animate()
