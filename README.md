# Bg Remover

![Language](https://img.shields.io/badge/Language-Python-3776AB?style=flat-square) ![Stars](https://img.shields.io/github/stars/Devanik21/BG-remover?style=flat-square&color=yellow) ![Forks](https://img.shields.io/github/forks/Devanik21/BG-remover?style=flat-square&color=blue) ![Author](https://img.shields.io/badge/Author-Devanik21-black?style=flat-square&logo=github) ![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

> Bg Remover — AI-powered image generation, transformation, and creative exploration.

---

**Topics:** `image-processing` · `background-removal` · `computer-vision` · `digital-image` · `dsp-techniques` · `image-denoising` · `image-segmentation` · `object-detection` · `yolo`

## Overview

Bg Remover is a generative image application that leverages diffusion models or GAN-based pipelines to create, transform, or stylise images from natural language prompts and visual inputs. It provides an interactive interface for experimenting with generative AI's visual capabilities.

The application supports text-to-image generation with configurable parameters (guidance scale, steps, seed, size), image-to-image transformation with adjustable strength, and a gallery for browsing and comparing generated outputs. All generation parameters are exposed in the UI for maximum experimental flexibility.

The backend can be configured to use cloud APIs (fal.ai, Replicate, Stability AI) for instant availability without local GPU, or local Diffusers pipelines for offline operation and maximum customisation.

---

## Motivation

Generative image models have fundamentally changed what's possible in visual creativity. This project was built to make these capabilities accessible and explorable without requiring deep ML expertise or expensive GPU infrastructure.

---

## Architecture

```
User Prompt + Parameters
        │
  Diffusion Pipeline (API or local)
        │
  Generated Image + Metadata
        │
  Gallery Display + Download
```

---

## Features

### Text-to-Image Generation
Generate high-quality images from natural language prompts with full parameter control over guidance, steps, seed, and dimensions.

### Negative Prompt Support
Specify elements to exclude from generated images for precise style and content control.

### Parameter Controls
Sliders for guidance scale (1.0–20.0), denoising steps (1–100), image dimensions, and seed for reproducibility.

### Generation History Gallery
All generated images are saved with their prompts and parameters in a scrollable gallery.

### Image Download
Download individual images or the full gallery as a ZIP file.

### Prompt Enhancement
Optional LLM-powered prompt expansion to convert terse inputs into detailed, style-rich generation prompts.

### Multiple Backend Support
Configure fal.ai, Replicate, Stability AI, or local Diffusers pipeline as the generation backend.

### Side-by-Side Comparison
Run the same prompt with different parameters and compare outputs in a split view.

---

## Tech Stack

| Library / Tool | Role | Why This Choice |
|---|---|---|
| **Diffusers / fal.ai SDK** | Generation backend | Diffusion model inference |
| **Streamlit / Gradio** | Web UI | Interactive parameter controls and gallery |
| **Pillow** | Image handling | Image saving, resizing, format conversion |
| **requests** | API communication | Cloud generation API calls |

> **Key packages detected in this repo:** `rembg` · `Pillow` · `streamlit`

---

## Getting Started

### Prerequisites

- Python 3.9+ (or Node.js 18+ for TypeScript/JS projects)
- `pip` or `npm` package manager
- Relevant API keys (see Configuration section)

### Installation

```bash
git clone https://github.com/Devanik21/BG-remover.git
cd BG-remover
pip install -r requirements.txt
python app.py
```

---

## Usage

```bash
python app.py

# Or with Streamlit
streamlit run app.py
```

---

## Configuration

| Variable | Default | Description |
|---|---|---|
| `API_KEY` | `(required)` | API key for the configured generation backend |
| `DEFAULT_MODEL` | `flux-schnell` | Default generation model |
| `DEFAULT_STEPS` | `20` | Default inference steps |

> Copy `.env.example` to `.env` and populate all required values before running.

---

## Project Structure

```
BG-remover/
├── README.md
├── requirements.txt
├── __init__.py
├── app.py
└── ...
```

---

## Roadmap

- [ ] ControlNet support for structure-guided generation
- [ ] Style transfer and image-to-image mode
- [ ] Batch generation from CSV prompts
- [ ] Video generation integration
- [ ] User accounts with cloud gallery persistence

---

## Contributing

Contributions, issues, and feature requests are welcome. Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'feat: add your feature'`)
4. Push to your branch (`git push origin feature/your-feature`)
5. Open a Pull Request

Please follow conventional commit messages and ensure any new code is documented.

---

## Notes

API keys for the configured generation backend are required for cloud inference. Local inference requires a CUDA-capable GPU.

---

## Author

**Devanik Debnath**  
B.Tech, Electronics & Communication Engineering  
National Institute of Technology Agartala

[![GitHub](https://img.shields.io/badge/GitHub-Devanik21-black?style=flat-square&logo=github)](https://github.com/Devanik21)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-devanik-blue?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/devanik/)

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

*Crafted with curiosity, precision, and a belief that good software is worth building well.*
