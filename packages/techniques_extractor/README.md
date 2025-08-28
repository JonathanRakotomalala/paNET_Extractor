# techniques-extractor
<p align="center">
 <a href="https://www.python.org">
<img src="https://img.shields.io/badge/python->=3.10-blue"> 
</a>
</p>
The techniques_extractor makes inference to Llm to extract techniques as it is written from raw text. <br>
It uses <a href="https://huggingface.co/docs/transformers/index">transformers</a> from huggingface to load llm models into the cache (model Llama 3.2-3B-Instruct size is 5.99GB). 
An alternative is <a href="https://docs.vllm.ai/en/latest/index.html">vLLM</a>,
With vLlm the Llm inference can be handled separately from the project. <br>
The vLLM process can run inside a container (e.g., Docker) or a VM to ensure it has all the necessary resources and isolation from the main application.
It can be deployed on dedicated hardware (e.g., GPUs or TPUs) for optimal performance, without sharing resources with the main application.
here are some usefull links: 

1. installation : https://docs.vllm.ai/en/stable/getting_started/installation/index.html 
2. inference : https://docs.vllm.ai/en/stable/examples/index.html
3. deployment : https://docs.vllm.ai/en/latest/deployment/docker.html

### Usage

> Requires a huggingface token access for the llm model (here it's the Llama-3.2-3B-Instruct from huggingface) to be passed in environment variable named HUGGING_FACE_ACCESS_TOKEN

```console 
> from techniques_extractor import Llm
#Initialize the model
> Llm()
```

#### load
Loads a model of Llm 
```console
>Llm.load()
```
#### llm_run
Generate an answer
```console
> response = Llm.lllm_run("NiFe-layered double hydroxides (LDHs) are promising electrocatalysts for the oxygen evolution reaction (OER) in alkaline media. Here, operando X-ray diffraction (XRD) and X-ray total scattering are used with Pair Distribution Function (PDF) analysis to investigate the atomic structure of the catalytically active material and follow structural changes under operating conditions. XRD shows an interlayer contraction under applied oxidative potential, which relates to a transition from the α-LDH to the γ-LDH phase. The phase transition is reversible, and the α-LDH structure is recovered at 1.3 VRHE. However, PDF analysis shows an irreversible increase in the stacking disorder under operating conditions, along with a decrease in the LDH sheet size. The analysis thus shows that the operating conditions induce a breakdown of the particles leading to a decrease in crystallite size.")
>print(response)
'{\n  "techniques": [\n    "operando X-ray diffraction",\n    "X-ray total scattering",\n    "Pair Distribution Function (PDF) analysis"\n  ]\n}'
```