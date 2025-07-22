import textwrap
import torch
# from src.main import my_llm
from transformers import pipeline,AutoModelForCausalLM,AutoTokenizer
import os
from huggingface_hub import login
from accelerate import Accelerator

DOCUMENT_SUMMARY = textwrap.dedent("""
   Given a synchrotron-based scientific document, create a very concise yet comprehensive summary in proper scientific prose. Your summary should follow this structure:
    
   Begin with a sentence describing the primary scientific domains and topics covered in the document.
   Follow with a clear sentence explaining the research objectives, hypotheses being tested, and the significance of the work.
   Next, provide a brief cohesive paragraph describing the primary experimental techniques employed, explaining their purpose and how they complement each other in addressing the research questions (provide both technique name and acronym).
   Then continue with a concise paragraph describing the materials (or samples) studied.
   Conclude, with the main findings and results.
   Don't include any reference. Don't include any information related to grant and funding. Only summarize the content of the document.
   Throughout the summary, maintain formal scientific style with proper sentence structure, appropriate transitions between ideas, and precise terminology. Each section should flow naturally into the next, creating a unified and informative overview of the research without using section headers or numbered lists.
    
   Document to analyze:
   """)

DOCUMENT_METADATA_EXTRACTION = textwrap.dedent("""
    
Given a scientific text and your knowledge of synchrotron experimental techniques, analyze the text and return a JSON object with the following structure:

    {{
      "techniques": [list of technique acronyms and/or full technique names, or an empty list if no techniques are explicitly mentioned]
    }}

    Requirements:

        Techniques:

            ONLY include techniques explicitly mentioned in the text.

            Use the exact name and casing (capitalization) as it appears(written) in the text (e.g., SAXS, XANES).

            If no techniques are mentioned, return an empty list [].

            Do not infer techniques from experimental results or sample characterization mentions.

            Do not combine multiple techniques (e.g., "operando absorption and X-ray diffraction tomography" → ["operando absorption", "X-ray diffraction tomography"]).

            Do not include techniques that might be commonly used in the field but are not explicitly stated in the text.
            
            Do not include techniques such as SAXS, XANES, operando absorption and X-ray diffraction tomography or any other that is **not** mentioned in the provided text. Only include those that appear in the text verbatim.

        Output content:

            Only include explicitly stated techniques.

            Each technique should be listed once (no duplicates).

            Only provide the RAW JSON object (no extra text).

            Each technique must be directly quotable from the provided source text.

    Note: If no techniques are explicitly mentioned in the text, return an empty list [].
    
   Text to analyze:
   """)

QUERY_1 = "In this contribution small-angle scattering from layered systems is  considered. When a colloidal dispersion is stirred it usually decomposes  into layers. There are two important questions concerning these layers:  What is the structure in a layer? What is the stacking structure  between such layers? For concentrated colloidal dispersions both these  questions can be investigated by small-angle scattering experiments. It  will become apparent that the answer is also important for technical  applications. Both a theoretical description as well as an experimental  verification are given in the paper"
QUERY_2 = "NiFe-layered double hydroxides (LDHs) are promising electrocatalysts for the oxygen evolution reaction (OER) in alkaline media. Here, operando X-ray diffraction (XRD) and X-ray total scattering are used with Pair Distribution Function (PDF) analysis to investigate the atomic structure of the catalytically active material and follow structural changes under operating conditions. XRD shows an interlayer contraction under applied oxidative potential, which relates to a transition from the α-LDH to the γ-LDH phase. The phase transition is reversible, and the α-LDH structure is recovered at 1.3 VRHE. However, PDF analysis shows an irreversible increase in the stacking disorder under operating conditions, along with a decrease in the LDH sheet size. The analysis thus shows that the operating conditions induce a breakdown of the particles leading to a decrease in crystallite size."
QUERY_3 = "Un outillage lithique acheuléen, une riche faune du Pléistocène moyen et quatre dents d'hominidés ont été extraites du remplissage de la cavité de la carrière Thomas I, célèbre depuis la découverte en 1969 d'une hémi-mandibule humaine. Depuis 1988, des fouilles sont conduites dans ce site dans le cadre du programme franco-marocain \" Casablanca \". Une riche faune mammalienne et quelques restes de reptiles et d'oiseaux sont associés à l'industrie lithique dans l'unité stratigraphique 4. La faune, introduite par les carnivores, indique un paysage peu boisé et le stade évolutif des divers taxons suggère un âge plus récent que celui de Tighenif (Algérie). Les marques de découpe sont absentes, ce qui pose la question du rôle des hominidés dans l'accumulation des restes fauniques. Le travail de la pierre était orienté vers la production d'éclats et de rares bifaces ont été introduits dans cette partie du site. Quatre dents humaines ont été exhumées entre 1994 et 2005. La datation ICP-MS par ablation laser combinant l'ESR et les séries de l'Uranium pour modéliser l'enrichissement en Uranium a été appliquée à une prémolaire humaine : elle a fourni un âge de 501+94-76 ka. De nouvelles mesures d'âge par OSL sur les sédiments encadrant la dent datée ont respectivement donné 420 ± 34 ka au dessus et 391 ± 32 ka en dessous confirmant un âge minimum centré sur une période relativement ancienne du Pléistocène moyen."


class Llm:
    # accelerator a huggingface library to optimize the model's execution

    ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
    # login to huggingface 
    login(token=ACCESS_TOKEN)
    pipe=None
    def __init__(self):
        accelerator = Accelerator()
    # https://huggingface.co/docs/transformers.js/api/pipelines#pipelinestextgenerationpipeline
        # temperature : a paramater of the generation, but it can be used in pipeline if the llm model support auto-regressive generation : https://huggingface.co/docs/transformers.js/en/pipelines#natural-language-processing https://huggingface.co/docs/transformers.js/main/en/api/utils/generation#utilsgenerationgenerationconfigtype--code-object-code
        #top_k : The number of highest probability vocabulary tokens to keep for top-k-filtering
        #top_p :  Default value i s 1. If set to float < 1, only the smallest set of most probable tokens with probabilities that add up to top_p or higher are kept for generation.
        #prompt_lookup_num_tokens : The number of tokens to be output as candidate tokens. https://huggingface.co/docs/transformers/main/en/main_classes/text_generation#transformers.GenerationConfig.prompt_lookup_num_tokens
        # for more information about text generation and the parameters : https://huggingface.co/docs/transformers/main_classes/text_generation
        self.model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-3B-Instruct",torch_dtype=torch.bfloat16, pad_token_id=0)
        self.tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-3B-Instruct")
        self.model, self.tokenizer = accelerator.prepare(self.model, self.tokenizer)
        # Initialize the text generation pipeline
        self.pipe = pipeline(
            "text-generation", model=self.model, tokenizer=self.tokenizer, temperature=0.35, top_p=0.98, top_k=11
        )


    def llm_run(self,input: str):
        """Download or Load the model locally then make an infering

        Args:
           input a string, the user's text
        Returns:
           String of a json containing the techniques
        """
        messages = [
            {"role": "user", "content": DOCUMENT_METADATA_EXTRACTION + input},
        ]
        # make the model generate an answer
        answer = self.pipe(messages)

        print(answer)

        # get the answer generated 
        response = answer[0]["generated_text"][1]["content"]

        return response
