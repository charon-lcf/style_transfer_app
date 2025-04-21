import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import torch
from torchvision import transforms
import re

from transformer_net import TransformerNet

# ========== 模型配置 ==========
MODEL_DIR = "models"
STYLE_MODELS = {
    "Mosaic (梵高)": "mosaic.pth",
    "Udnie (现代风格)": "udnie.pth",
    "Rain Princess (雨中巴黎)": "rain_princess.pth",
    "Candy (糖果风格)": "candy.pth",
}

# ========== 风格迁移函数 ==========
def stylize_image(content_image_path, model_path, output_path):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    content_image = Image.open(content_image_path).convert("RGB")
    transform = transforms.Compose([
        transforms.Resize(512),
        transforms.ToTensor(),
        transforms.Lambda(lambda x: x.mul(255))
    ])
    content_tensor = transform(content_image).unsqueeze(0).to(device)

    style_model = TransformerNet()
    state_dict = torch.load(model_path)
    for k in list(state_dict.keys()):
        if re.search(r'in\d+\.running_(mean|var)$', k):
            del state_dict[k]
    style_model.load_state_dict(state_dict)
    style_model.to(device).eval()

    with torch.no_grad():
        output_tensor = style_model(content_tensor).cpu()[0]
    output_image = output_tensor.clone().clamp(0, 255).numpy()
    output_image = output_image.transpose(1, 2, 0).astype("uint8")
    output_pil = Image.fromarray(output_image)
    output_pil.save(output_path)
    return output_path

# ========== 主界面类 ==========
class StyleTransferApp:
    def __init__(self, root):
        self.root = root
        self.root.title("风格转换小工具")
        self.root.geometry("800x500")

        self.image_path = None
        self.output_image_path = None
        self.style_var = tk.StringVar(value="Mosaic")  # 默认值设置为“mosaic”

        # 顶部风格选择菜单
        control_frame = tk.Frame(root)
        control_frame.pack(side=tk.TOP, pady=10)
        tk.Label(control_frame, text="选择风格: ").pack(side=tk.LEFT)
        tk.OptionMenu(control_frame, self.style_var, *STYLE_MODELS.keys()).pack(side=tk.LEFT)

        # 图像区域（左右）
        image_frame = tk.Frame(root)
        image_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.input_canvas = tk.Label(image_frame, text="点击选择图片", width=50, height=30, bg="#dddddd", font=("Arial", 12))
        self.input_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        self.input_canvas.bind("<Button-1>", self.on_image_click)

        self.output_canvas = tk.Label(image_frame, text="风格图", width=50, height=30, bg="#eeeeee", font=("Arial", 12))
        self.output_canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

    def on_image_click(self, event):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
        if not path:
            return
        self.image_path = path
        self.display_image(path, self.input_canvas)

        # 获取当前选择的风格
        style = self.style_var.get()
        if not style or style not in STYLE_MODELS:
            messagebox.showerror("错误", "请选择一个有效的风格")
            return

        model_filename = STYLE_MODELS.get(style)
        model_path = os.path.join(MODEL_DIR, model_filename)

        if not os.path.exists(model_path):
            messagebox.showerror("模型缺失", f"模型文件不存在: {model_path}")
            return

        base_name = os.path.splitext(os.path.basename(self.image_path))[0]
        output_path = os.path.join(os.getcwd(), f"{base_name}_{style}.jpg")

        try:
            stylize_image(self.image_path, model_path, output_path)
            self.output_image_path = output_path
            self.display_image(output_path, self.output_canvas)
            messagebox.showinfo("完成", f"风格图片已保存到:\n{output_path}")
        except Exception as e:
            messagebox.showerror("出错啦", str(e))

    def display_image(self, image_path, widget_label):
        img = Image.open(image_path)
        img.thumbnail((350, 350))
        img_tk = ImageTk.PhotoImage(img)
        widget_label.configure(image=img_tk)
        widget_label.image = img_tk
        widget_label.configure(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = StyleTransferApp(root)
    root.mainloop()
