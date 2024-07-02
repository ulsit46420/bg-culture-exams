# Code for the Bulgarian Maturity Exams Dataset

This repository contains the code for the dataset with multiple-choice questions from Bulgarian high school maturity exams in three subjects: Bulgarian Language and Literature, History and Civilization, and Geography and Economics.

[Huggingface dataset link](https://huggingface.co/datasets/ulsit46420/bg-culture-exams)

## Dataset Summary

The dataset consists of 2,599 multiple-choice questions extracted from official Bulgarian maturity exams administered between 2007 and 2024. It is designed to evaluate the performance of large language models on tasks related to Bulgarian language, literature, history, geography, and economics.

- Total questions: 2,599
- Training set: 329 questions 
- Test set: 2,270 questions
- Question format: Multiple choice with 4 options
- Subjects covered: Bulgarian Language and Literature, History and Civilization, Geography and Economics
- Time period: 2007-2024

![image/png](https://cdn-uploads.huggingface.co/production/uploads/6683f3e06b4de82b9ef422e9/fgsR5HERN6S9vrY18tnTJ.png)

## Intended Uses & Limitations

This dataset is intended for:
- Evaluating the multilingual capabilities of large language models, particularly in Bulgarian
- Assessing models' knowledge of Bulgarian language, literature, history, geography, and economics
- Benchmarking language models' performance on Bulgarian educational content

Limitations:
- Questions are publicly available, which may lead to data leakage in pre-trained models
- The dataset reflects the Bulgarian educational system and may not generalize to other contexts
- Only multiple-choice questions are included, limiting the assessment of open-ended language generation

## Benchmark results

![image/png](https://cdn-uploads.huggingface.co/production/uploads/6683f3e06b4de82b9ef422e9/pF41WdFg6HiE-AfHlWuPf.png)

![image/png](https://cdn-uploads.huggingface.co/production/uploads/6683f3e06b4de82b9ef422e9/-GV22fPMprhDyCBy_LQ66.png)

![image/png](https://cdn-uploads.huggingface.co/production/uploads/6683f3e06b4de82b9ef422e9/plf5SCb6PvJN-UPAk6ZnV.png)

![image/png](https://cdn-uploads.huggingface.co/production/uploads/6683f3e06b4de82b9ef422e9/GBClgaAYso0PxE0Qfev3h.png)

![image/png](https://cdn-uploads.huggingface.co/production/uploads/6683f3e06b4de82b9ef422e9/Yclo_Xitr6p2YGaAyIjkN.png)

![image/png](https://cdn-uploads.huggingface.co/production/uploads/6683f3e06b4de82b9ef422e9/AC7Ii8-2kIVKEFniAnwM_.png)

![image/png](https://cdn-uploads.huggingface.co/production/uploads/6683f3e06b4de82b9ef422e9/fcbQYvpNlffb6yi3rhnI5.png)

![image/png](https://cdn-uploads.huggingface.co/production/uploads/6683f3e06b4de82b9ef422e9/o0BF_bomz2jk8gkfcHnyD.png)

![image/png](https://cdn-uploads.huggingface.co/production/uploads/6683f3e06b4de82b9ef422e9/utMRhQ8ApP0R8mgnoaj1E.png)

## Data Collection and Preprocessing

The questions were extracted from official PDF documents of Bulgarian maturity exams published by the Ministry of Education and Science. The extraction and structuring process involved:

![image/png](https://cdn-uploads.huggingface.co/production/uploads/6683f3e06b4de82b9ef422e9/IduCW2R_XBTk_qg7iCzmB.png)

1. Converting PDFs to DOCX format
2. Converting DOCX to Markdown format
3. Using a large language model (DeepSeek V2) to extract and structure the questions
4. Manual verification and quality control

## Considerations for Using the Data

- Privacy: The dataset contains only publicly available exam questions and does not include any personal information.
- Demographic Bias: The content reflects the Bulgarian educational curriculum and may contain cultural biases.
- Ethical Considerations: Users should be aware of potential biases in educational content and use the dataset responsibly.

## Additional Information

- Source: Bulgarian Ministry of Education and Science
