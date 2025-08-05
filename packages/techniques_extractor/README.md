# techniques-extractor
This package use an LLM to extract techniques from raw text


### Usage

> Requires a token access for the llm model (here it's the Llama-3.2-3B-Instruct) :  ACCESS_TOKEN

```console 
   from techniques_extractor import Llm
   #Initialize the model
   Llm()
```



#### llm_run
```console
   > print(Llm.lllm_run("NiFe-layered double hydroxides (LDHs) are promising electrocatalysts for the oxygen evolution reaction (OER) in alkaline media. Here, operando X-ray diffraction (XRD) and X-ray total scattering are used with Pair Distribution Function (PDF) analysis to investigate the atomic structure of the catalytically active material and follow structural changes under operating conditions. XRD shows an interlayer contraction under applied oxidative potential, which relates to a transition from the α-LDH to the γ-LDH phase. The phase transition is reversible, and the α-LDH structure is recovered at 1.3 VRHE. However, PDF analysis shows an irreversible increase in the stacking disorder under operating conditions, along with a decrease in the LDH sheet size. The analysis thus shows that the operating conditions induce a breakdown of the particles leading to a decrease in crystallite size."))
   '{\n  "techniques": [\n    "operando X-ray diffraction",\n    "X-ray total scattering",\n    "Pair Distribution Function (PDF) analysis"\n  ]\n}'
```