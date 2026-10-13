> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Optimize prompts for more stable outputs

Prompt engineering bridges users and models. Good prompts are critical for reliable reasoning and generation. The examples below move from simple to complex and show how to tune prompts for summarization, reasoning, and transformation tasks.

## Prompt design principles

### Principle 1: Write clear, specific instructions

#### 1. Be explicit

* **Vague instruction**: ❌
  ```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
  Talk about art.
  ```
  Too broad; the model may produce an unfocused overview.
* **Specific instruction**: ✅
  ```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
  Explain the characteristics of Impressionist painting and list three famous Impressionist painters.
  ```
  Calls out the art movement and the expected outputs.

#### 2. Add necessary detail

* **Sparse instruction**: ❌
  ```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
  Explain economics.
  ```
  Overly broad.
* **Detailed instruction**: ✅
  ```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
  Explain the theory of supply and demand, especially how equilibrium affects prices. Give examples of price changes when supply exceeds demand and when demand exceeds supply.
  ```
  Defines the concept and the required examples.

#### 3. Use delimiters

* **No delimiter**: ❌
  ```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
  Analyze this text and summarize the main points
  ```
  Unclear which part is content vs. instruction.
* **With delimiters**: ✅
  ```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
  Analyze the text enclosed in <TEXT></TEXT> and summarize the main points.
  <TEXT>...content to analyze...</TEXT>
  ```
  Separates the content from the instruction.

#### 4. Account for edge cases

* **No conditions**: ❌
  ```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
  List the errors in the text.
  ```
  Error type is unspecified.
* **With conditions**: ✅
  ```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
  Check the text for grammar errors. If there are errors, point them out and correct them; if not, say there are none.
  ```
  Guides the model through the check-and-report flow.

#### 5. Use few-shot examples

* **No example**: ❌
  ```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
  Explain how metaphors work.
  ```
  Tone and style are unspecified.
* **Provide an example**: ✅
  ```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
  Here is a sample dialogue. Explain how the metaphor is used.
  Person A: How can someone become a great leader?
  Person B: Like a ship’s captain steering through a storm—stay on course and guide the crew forward.
  ```
  Sets expectations for tone, style, and output.

### Principle 2: Give the model time to think

LLMs need space to reason. If you rush them, answers may be shallow or wrong. Encourage step-by-step thinking—e.g., list different perspectives before concluding. This improves logical reasoning and accuracy.

#### 1. Specify task steps

Below is a prompt that guides the model through a story analysis:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
Follow these steps to analyze the text and produce the final result.
1. Summarize the text in one sentence.
2. Translate the summary into English.
3. List the character names.
4. Output a JSON object containing the summary and the number of names.
Text:
Sun Wukong and Zhu Bajie went to Huaguo Mountain to pick peaches. Sun Wukong jumped ahead playfully while Zhu Bajie strolled behind. When they arrived, Sun Wukong climbed trees to pick peaches. Zhu Bajie got impatient, searched for peaches himself, and slipped into a puddle, getting covered in mud. Sun Wukong laughed at him. They brought the peaches back to Tang Seng.
```

Model output:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
1. Summary: Sun Wukong and Zhu Bajie picked peaches at Huaguo Mountain; Zhu Bajie fell into a puddle; they returned to Tang Seng with the peaches.
2. Translation: Sun Wukong and Zhu Bajie went to Huaguo Mountain to pick peaches. Zhu Bajie accidentally fell into a puddle. Finally, they returned to Tang Seng with the peaches.
3. Names: Sun Wukong, Zhu Bajie
4. Output: {"summary": "Sun Wukong and Zhu Bajie picked peaches at Huaguo Mountain; Zhu Bajie fell into a puddle; they returned to Tang Seng with the peaches.", "num_names": 2}
```

#### 2. Encourage self-reflection (Andrew Ng’s reflective workflow)

Invite the model to reason before judging. For example, when checking whether a math answer is correct, ask the model to solve the problem itself, then compare. Here is a three-step reflective prompt:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
Follow these steps and provide the final result.
Step 1: Solve the problem yourself.
Step 2: Verify your answer. If correct, return it directly; if incorrect, suggest how to fix it.
Step 3: Solve the problem using your suggestion. Verify again as in step 2.
Problem:
There are chickens and rabbits in a cage with 35 heads and 94 legs in total. How many chickens and rabbits are there?
```

Model reasoning

First pass (incorrect on purpose):

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
Chickens: 21, Rabbits: 14.
```

Second pass verification:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
Chickens 21 * 2 = 42 legs
Rabbits 14 * 4 = 56 legs
Total = 98 legs
The problem states 94 legs, so this is wrong. Use algebra and reason step by step.
```

Third pass step-by-step solution:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
Let chickens = x and rabbits = y.
1. From the heads: x + y = 35 → y = 35 - x.
2. From the legs: 2x + 4y = 94.
   Substitute y: 2x + 4(35 - x) = 94.
   Expand: 2x + 140 - 4x = 94.
   Rearrange: -2x = -46.
   Solve: x = 23.
   Substitute back: 23 + y = 35 → y = 12.
   Checked: answer is chickens 23, rabbits 12.
```

## Common prompt references

### Text analysis

#### 1. Sentiment analysis

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
## Role
- You are a sentiment analyst.

## Goal
- Analyze the given text and classify its sentiment as positive, negative, or neutral for market analysis, customer feedback, or public opinion monitoring. Positive sentiment includes words expressing liking, satisfaction, or praise; negative sentiment includes dissatisfaction, complaints, or criticism; neutral sentiment is objective description without obvious emotion.

## Constraints
- Output only the sentiment category: positive, negative, or neutral.

## Output
- Output format: sentiment category

## Workflow
1. Read the text enclosed in <TEXT></TEXT>: <TEXT>...text to analyze...</TEXT>.
2. Determine its sentiment.
3. Output the sentiment (positive, negative, or neutral).
```

#### 2. Document analysis

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
## Role
- You are a document analyst.

## Goal
- Efficiently analyze documents, extract the core content, produce a clear summary, and pull key information.

## Constraints
- Output only the summary and key information—no extra content.

## Output
- Output format: document summary and key information

## Workflow
1. Read the text enclosed in <TEXT></TEXT>: <TEXT>...text to analyze...</TEXT>.
2. Write a concise summary highlighting the main points.
3. Extract key information such as facts, data, or conclusions.
4. Output the summary and key information in the specified format.
```

#### 3. Translation

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
## Role
- You are a translation expert.

## Goal
- Accurately translate text from one language to another with natural fluency.

## Constraints
- Output must follow the target language’s grammar and cultural context without deviating from the original meaning.

## Output
- Output format: final translation

## Workflow
1. Read the text enclosed in <TEXT></TEXT>: <TEXT>...text to translate...</TEXT>.
2. Produce an initial translation that preserves meaning.
3. Compare the translation to the source and suggest improvements for accuracy, fluency, and cultural fit.
4. Apply the improvements and produce the final translation.
5. Output the final translation.
```

## Notes

LLMs can hallucinate—generate plausible but false information. Reduce this risk with better prompt design (e.g., cite sources, use reflective workflows) and with Tool Calls to fetch or compute authoritative data.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.