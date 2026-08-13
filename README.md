<!-- Banner: auto dark/light -->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
  <img alt="Viet Anh Vu — AI Engineer" src="assets/banner-light.svg">
</picture>

<!-- Typing animation -->
<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&duration=3000&pause=1000&color=A855F7&center=true&vCenter=true&random=false&width=680&lines=Automated+Essay+Scoring+%40+Prep+Education;LLM+Serving%3A+vLLM+%2B+PagedAttention;Healthcare+AI+%7C+EdTech+AI+%7C+Computer+Vision;IEEE+CEC+2024+%26+Springer+JAIHC+2026" alt="Typing SVG"/>
</p>

<!-- Badges -->
<p align="center">
  <a href="mailto:vietanhresearcher@gmail.com">
    <img src="https://img.shields.io/badge/Email-vietanhresearcher%40gmail.com-informational?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"/>
  </a>
  <a href="https://www.linkedin.com/in/anh-vu-researcher">
    <img src="https://img.shields.io/badge/LinkedIn-Anh%20Vu-blue?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/>
  </a>
  <a href="https://orcid.org/0009-0006-6977-5922">
    <img src="https://img.shields.io/badge/ORCID-0009--0006--6977--5922-A6CE39?style=for-the-badge&logo=orcid&logoColor=white" alt="ORCID"/>
  </a>
  <a href="data/resume.pdf">
    <img src="https://img.shields.io/badge/CV-resume.pdf-critical?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" alt="CV"/>
  </a>
</p>
<p align="center">
  <img src="https://img.shields.io/badge/Hanoi-Viet%20Nam-orange?style=flat-square&logo=google-maps&logoColor=white" alt="Location"/>
  <img src="https://komarev.com/ghpvc/?username=VuVietAnh2309&label=Profile%20views&style=flat-square" alt="Visitors"/>
</p>

---

## 🧑‍💻 About me

> AI Engineer & MSc student — I build and **ship** ML/LLM systems to production, mostly in Education and Healthcare.

- 🏢 **AI Engineer @ Prep Education** — Automated Essay Scoring, grammar correction & LLM serving for IELTS learners
- 🎓 **MSc, Computer Science** @ HUST (Jun 2025 – Present) · BSc (Honours), CPA 3.48/4.0
- 📄 **2 published papers** — [IEEE CEC 2024](https://doi.org/10.1109/CEC60901.2024.10612029) · [Springer JAIHC 2026](https://doi.org/10.1007/s12652-026-05116-0)
- ⚡ Day-to-day: **vLLM** (continuous batching, PagedAttention), async GPU batching, Docker → GitLab CI/CD → ArgoCD → K8s
- 🏆 **2nd Prize — WiDS Datathon 2023** (Kaggle)
- 📎 CV: [`resume.pdf`](data/resume.pdf)

---

## 💼 Experience

### <img src="https://img.shields.io/badge/Current-00c853?style=flat-square" alt="Current"/> Prep Education — AI Engineer · Oct 2025 – Present

<details>
<summary>🎯 <b>Automated Essay Scoring (AES)</b> — IELTS Writing & Speaking</summary>
<br/>

| Component | Details |
|-----------|---------|
| **Speaking** | ML models + APA (pronunciation) + GEC (grammar) + Dify (vocabulary & lexical diversity) |
| **Writing** | **PANN** — cross-prompt DeBERTa-V3, 189M params · quantized **T5** → 120M params |
| **Metrics** | Speaking: Acc ±0.5 ~82%, QWK & PCC ~90% · Writing: Acc ±0.5 ~85% (Task 1) / ~87% (Task 2), ±1 ~98% |
| **MLOps** | Docker → GitLab CI/CD → ArgoCD → production Kubernetes |
| **Scale** | Dynamic batching + request queuing for thousands of concurrent assessments |
</details>

<details>
<summary>✏️ <b>English Lexical Grammar (ELG) Correction</b> — hybrid rules + LLM, served on vLLM</summary>
<br/>

- Hybrid correction: **deterministic rule-based pattern matching** + LLM inference for complex constructs
- Covers grammar, vocabulary misuse, spelling, collocations, idiomatic expressions, linking devices, phrase usage
- **F0.5 ~60%** on private test sets — tuned toward precision to minimise false corrections
- 🔍 **LLM-as-judge evaluation framework** — an evaluator LLM scores each sample against an explicit rubric
  (grammatical correctness, meaning preservation, minimal-edit fidelity, error-type accuracy, naturalness),
  surfacing failure modes that F0.5/BLEU cannot capture: over-correction, paraphrasing drift, false positives
- 🚀 Serving: **vLLM** backend (continuous batching, PagedAttention) for high-throughput, low-latency inference
- Application-level request batching & caching layered on top of vLLM to cut tail latency under bursty traffic
- Deployed to **thousands of students daily**
</details>

<details>
<summary>🀄 <b>Chinese Vocabulary Extraction Pipeline</b> — image → structured vocabulary data</summary>
<br/>

Turns images of Chinese text into structured vocabulary (simplified/traditional, pinyin, POS, bilingual definitions)
for flashcards and learning content.

**5-stage pipeline**

```
PP-OCRv5 (detect + recognise)
   → custom cleaner (reading order, line merging, confidence filtering)
   → linguistic analysis (jieba segmentation · pypinyin · OpenCC simplified⇄traditional · POS tagging)
   → self-hosted Qwen3.5-4B-Instruct-2507 enrichment (vLLM: continuous batching + PagedAttention)
   → schema validator
```

- 📊 **Benchmarked two-stage vs single-stage**: a VLM baseline (Qwen3.6-35B-A3B on the raw image) lost to the
  two-stage OCR → LLM pipeline on dense Chinese text — higher accuracy, lower end-to-end latency,
  substantially lower inference cost, and each stage independently testable
- 🧩 **Hybrid LLM strategy** — libraries handle deterministic work (segmentation, pinyin, traditional conversion);
  the LLM only resolves what libraries cannot do without context (polyphonic pinyin, ambiguous 1-to-many
  traditional mappings, bilingual definitions), cutting token usage significantly
- 🎛️ Chinese linguistic rules encoded in the prompt: numeral-and-measure splits, particle separation,
  erhua handling, fixed-phrase preservation, place-name conventions
- 💾 **GPU memory tuning** on PaddlePaddle — capped VRAM allocation fraction + resized inputs to max 1920px:
  idle VRAM **8.7 GB → ~600 MB**, peak **~2.4 GB** on a 24 GB card
- ⚙️ **Async OCR batcher** over an `asyncio` queue — collects concurrent requests into GPU batches
  (up to 8 images/forward pass, 50 ms collection window) without blocking the event loop
- 🌐 **FastAPI** service (`predict`, `pipeline`, `health` + Swagger UI), definitions in **vi / en / zh / ja / ko**,
  **Streamlit** dev UI, packaged with Docker + NVIDIA Container Toolkit
</details>

### <img src="https://img.shields.io/badge/2024--2025-1e88e5?style=flat-square" alt="2024-2025"/> Vietsens Technology Group — AI Engineer · Sep 2024 – Sep 2025

<details>
<summary>🏥 <b>AI Healthcare Assistant</b> — LLMs, NLP, HIS integration</summary>
<br/>

- AI agents assisting doctors with medical history inquiry, prescription and diagnostics
- Deployed inside the **National Hospital Management Software**, adopted by **Bach Mai Hospital**
- Modules for patient data analysis, case management assistance and initial diagnosis support
- Integrated with existing hospital information systems (HIS)
</details>

<details>
<summary>💊 <b>Prescription Recommendation & Conflict Detection</b></summary>
<br/>

- Predictive system supporting medication prescribing from electronic health records
- Classical classifiers (Decision Trees, Random Forests, SVM) + advanced classifiers for accuracy
- **LLMs** to evaluate prescriptions, detect duplicate active ingredients and flag drug–drug interactions
- Decision-support tool aimed at reducing prescription errors
</details>

### <img src="https://img.shields.io/badge/Intern-ff9800?style=flat-square" alt="Intern"/> FPT Information System — AI Engineer Intern · Aug 2023 – May 2024

<details>
<summary>📄 <b>OCR for Financial Reports</b> — PaddleOCR, TrOCR, LayoutLMv3</summary>
<br/>

- End-to-end pipeline: pre-processing (deskew, binarise, denoise) → detection → layout understanding → NER + regex normalisation
- **LayoutLM / LayoutLMv3** for document layout: tables, figures, key-value pairs from bank financial reports
- Deployed as part of an AI pipeline assisting financial data analysts
</details>

<details>
<summary>🖼️ <b>Image Captioning</b></summary>
<br/>

- Caption generation with Transformers + CNNs and attention mechanisms
</details>

---

## 📚 Publications

<table>
  <tr>
    <td>📖</td>
    <td>
      <b>Enhancing facial expression recognition with lightweight attention-based CNN</b><br/>
      <sub><b>Viet Anh Vu</b>, Gia Khanh Pham, Quy Nam Tran, Son Tung Do,
      <a href="https://scholar.google.com/citations?hl=en&user=z0ThpI3yfS8C">Danh Tuyen Pham</a> &
      <a href="https://scholar.google.com/citations?hl=en&user=C0XxcJcAAAAJ">Van Hai Pham</a></sub><br/>
      <sub><i>Journal of Ambient Intelligence and Humanized Computing</i> (Springer), 10 Aug 2026</sub><br/>
      <a href="https://doi.org/10.1007/s12652-026-05116-0">
        <img src="https://img.shields.io/badge/Springer_JAIHC_2026-Published-success?style=flat-square" alt="Published"/>
      </a>
      <img src="https://img.shields.io/badge/DOI-10.1007%2Fs12652--026--05116--0-blue?style=flat-square" alt="DOI"/>
    </td>
  </tr>
  <tr>
    <td>📖</td>
    <td>
      <b>VISTA</b> — A Variable Length Genetic Algorithm and LSTM-Based Surrogate Assisted Ensemble Selection algorithm in Multiple Layers Ensemble System<br/>
      <sub>Kate Han, Truong Thanh Nguyen, <b>Viet Anh Vu</b>, Alan Wee-Chung Liew, Truong Dang &
      <a href="https://scholar.google.com/citations?hl=en&user=Pjxn9IUAAAAJ">Tien Thanh Nguyen</a></sub><br/>
      <sub><i>2024 IEEE Congress on Evolutionary Computation (CEC)</i>, Yokohama, Japan, 30 Jun – 5 Jul 2024, pp. 1–9</sub><br/>
      <a href="https://doi.org/10.1109/CEC60901.2024.10612029">
        <img src="https://img.shields.io/badge/IEEE_CEC_2024-Published-success?style=flat-square" alt="Published"/>
      </a>
      <img src="https://img.shields.io/badge/DOI-10.1109%2FCEC60901.2024.10612029-blue?style=flat-square" alt="DOI"/>
    </td>
  </tr>
</table>

**Research supervision**

| Supervisor | Affiliation | Since | Area |
|-----------|------------|-------|------|
| Dr. Kate Han & [Dr. Tien Thanh Nguyen](https://scholar.google.com/citations?hl=en&user=Pjxn9IUAAAAJ) <sub>🎓</sub> | Robert Gordon University <sub>(T.T. Nguyen)</sub> | Mar 2023 | Machine Learning & Ensemble Learning · Genetic Algorithms · statistical testing |
| [Assoc. Prof. Pham Van Hai](https://scholar.google.com/citations?hl=en&user=C0XxcJcAAAAJ) <sub>🎓</sub> | HUST — SoICT | Sep 2023 | Computer Vision & Deep Learning |
| [Dr. Pham Danh Tuyen](https://scholar.google.com/citations?hl=en&user=z0ThpI3yfS8C) <sub>🎓</sub> | [PTIT](https://sea.ptit.edu.vn/ts-pham-danh-tuyen/) — School of Electronics Engineering 1 | Dec 2024 | Computer Vision · image processing · machine learning on edge devices |

<sub>🎓 = Google Scholar</sub>

---

## 🛠️ Skills & Tools

<table>
  <tr>
    <td><b>Languages</b></td>
    <td>
      <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white"/>
      <img src="https://img.shields.io/badge/C++-00599C?style=flat-square&logo=cplusplus&logoColor=white"/>
      <img src="https://img.shields.io/badge/Bash-4EAA25?style=flat-square&logo=gnubash&logoColor=white"/>
    </td>
  </tr>
  <tr>
    <td><b>ML / DL</b></td>
    <td>
      <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white"/>
      <img src="https://img.shields.io/badge/Keras-D00000?style=flat-square&logo=keras&logoColor=white"/>
      <img src="https://img.shields.io/badge/HuggingFace-FFD21E?style=flat-square&logo=huggingface&logoColor=black"/>
      <img src="https://img.shields.io/badge/PaddlePaddle-0062B0?style=flat-square&logo=paddlepaddle&logoColor=white"/>
    </td>
  </tr>
  <tr>
    <td><b>LLM serving</b></td>
    <td>
      <img src="https://img.shields.io/badge/vLLM-30A2FF?style=flat-square"/>
      <img src="https://img.shields.io/badge/PagedAttention-6E56CF?style=flat-square"/>
      <img src="https://img.shields.io/badge/Continuous_batching-6E56CF?style=flat-square"/>
      <img src="https://img.shields.io/badge/Quantization-6E56CF?style=flat-square"/>
      <br/>
      <sub>Qwen3.5 · DeBERTa-V3 · T5 · Dify · LLM-as-judge evaluation · prompt engineering</sub>
    </td>
  </tr>
  <tr>
    <td><b>Serving & APIs</b></td>
    <td>
      <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white"/>
      <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white"/>
      <img src="https://img.shields.io/badge/asyncio-3776AB?style=flat-square&logo=python&logoColor=white"/>
      <br/>
      <sub>async GPU batching · dynamic batching · request queuing · caching strategies · GPU/VRAM tuning</sub>
    </td>
  </tr>
  <tr>
    <td><b>MLOps</b></td>
    <td>
      <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white"/>
      <img src="https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white"/>
      <img src="https://img.shields.io/badge/GitLab_CI/CD-FC6D26?style=flat-square&logo=gitlab&logoColor=white"/>
      <img src="https://img.shields.io/badge/ArgoCD-EF7B4D?style=flat-square&logo=argo&logoColor=white"/>
      <img src="https://img.shields.io/badge/NVIDIA_Container_Toolkit-76B900?style=flat-square&logo=nvidia&logoColor=white"/>
      <br/>
      <sub>model serving optimization · production monitoring</sub>
    </td>
  </tr>
  <tr>
    <td><b>OCR & Documents</b></td>
    <td>PP-OCRv5 · PaddleOCR · Tesseract · TrOCR · LayoutLM / LayoutLMv3 · NER + regex normalisation</td>
  </tr>
  <tr>
    <td><b>Computer Vision</b></td>
    <td>Object detection · Segmentation (UNet, UNet_v2) · image processing · MobileNetV2 · attention classifiers</td>
  </tr>
  <tr>
    <td><b>NLP</b></td>
    <td>LLMs · Question Answering · grammatical error correction · ABSA · speaker verification · jieba / pypinyin / OpenCC</td>
  </tr>
  <tr>
    <td><b>Focus areas</b></td>
    <td>Deep Learning · Computer Vision · LLMs · Healthcare AI · Education AI · Ensemble Learning · Genetic Algorithms</td>
  </tr>
</table>

---

## 📂 Selected repositories

| Repo | What it is |
|------|-----------|
| [FER_Lightweight_CNN_based_model](https://github.com/VuVietAnh2309/FER_Lightweight_CNN_based_model) ⭐4 | Code for the **published JAIHC 2026 paper** — attention-based MobileNetV2 for facial expression recognition on edge devices |
| [Fundamental_RAG](https://github.com/VuVietAnh2309/Fundamental_RAG) ⭐1 | Retrieval-Augmented Generation fundamentals |
| [adaptive_information_retrival](https://github.com/VuVietAnh2309/adaptive_information_retrival) | Adaptive information retrieval experiments |
| [medical_fusion_image](https://github.com/VuVietAnh2309/medical_fusion_image) · [Image_fusion_datasets](https://github.com/VuVietAnh2309/Image_fusion_datasets) | Medical image fusion — models and datasets |
| [Image_generation](https://github.com/VuVietAnh2309/Image_generation) ⭐2 | Generative image modelling notebooks |
| [HPC---Laplace](https://github.com/VuVietAnh2309/HPC---Laplace) | High-performance computing — Laplace solver in C |

---

## 🎓 Education & Certifications

| | Degree / Certification | Institution | Period |
|---|--------|------------|--------|
| 🎓 | **MSc, Computer Science** | HUST | Jun 2025 – Present |
| 🎓 | **BSc (Honours), Computer Science** | HUST — CPA 3.48/4.0 | Oct 2020 – Jul 2024 |
| 📜 | IBM Python for Data Science | IBM | Completed |
| 📜 | Intro to Machine Learning | Kaggle | Completed |
| 📜 | Computer Vision | Kaggle | Completed |
| 🗣️ | English — **VSTEP B2** | — | Mar 2025 |

---

## 📈 GitHub at a glance

<sub>All cards below are generated inside this repo by GitHub Actions and committed as static SVGs — no external service to go down.</sub>

<p align="center">
  <img src="assets/metrics.svg" alt="GitHub metrics" width="80%"/>
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/snake-dark.svg">
    <img alt="Contribution snake" src="assets/snake.svg" width="90%">
  </picture>
</p>

---

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:00d2ff,50:a855f7,100:00f5a0&height=80&section=footer"/>
</p>
