# techniques-extractor
<p align="center">
 <a href="https://www.python.org">
<img src="https://img.shields.io/badge/python->=3.10-blue"> 
</a>
</p>
The techniques_extractor makes inference to Llm to extract techniques as it is written from raw text

### Usage

> Requires a hugging_face token access for the llm model (here it's the Llama-3.2-3B-Instruct from huggingface) :  HUGGING_FACE_ACCESS_TOKEN

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