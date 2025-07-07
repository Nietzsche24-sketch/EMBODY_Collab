ToonShade is a local AI-powered cartoonifier that processes real human faces and outputs high-resolution cartoon-stylized versions — while preserving facial identity and likeness.

## 📁 Submodules

- `whitebox_cartoonization/`: Core inference model (based on White-box Cartoonization)
- `example_output/`: Output previews from inference
- `true_cartoonify.sh`: Script for batch conversion of input photos

## 🛠️ Tech Stack

- Python 3.10
- TensorFlow (<=2.12 preferred)
- OpenCV
- Pretrained weights (used from white-box-cartoonization repo)

## 🚧 Known Issues

- TensorFlow 2.13+ causes `TF_bfloat16_type()` errors. Downgrade to 2.12 to avoid.
- Ensure no nested Git repos (`.git/`) are embedded in `whitebox_cartoonization/`.

## 🧠 Roadmap Ideas

- [ ] Add CLI for bulk face cartoonifying
- [ ] Face detection + cropping
- [ ] iOS shortcut / drag-and-drop GUI
- [ ] Integration with EMBODY avatar system

---

© 2025 Nietzsche24-sketch
