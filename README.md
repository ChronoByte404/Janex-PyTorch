# Janex
A free open-source framework which can be used to build Machine Learning tools, LLMs, and Natural Language Processing scripts with full simplicity.

<h2> What is the purpose of Janex? </h2>

Monopolistic companies are confining their Artificial Intelligence research to themselves, and capitalising on it. Even companies that swore to open source their software (OpenAI) went back on their morals, with the releases of GPT-3+, as did other powerful businesses.

These businesses go on to share their privatised research with governments, but rarely with the public. As such, my aim is to create a framework that you can use to easily construct your own language models, and other machine learning algorithms, as I believe this power should not be held firmly in the hands of corrupt rich politicians and advantaged capitalists.

Released under the GNU General License Version 3.0, Janex will improve and become a useful tool for users to conduct their own research in the potential of Artifical Intelligence.

<h3> How to use </h3>

<h4> Adding to your project </h4>

Firstly, clone the git repository to the local directory of your project.

```
gh repo clone Cipher58/Janex
```

Secondly, import the Janex toolkit into your code by adding this line

```
from Janex import Janex
```

<h4>Using Janex in your code</h4>

**Tokenizing:**

To utilise the tokenizer feature, here is an example of how it can be used.

```
input_string = "Hello! What is your name?"

words = Tokenize(input_string)

print(words)
```
**Intent classifying:**

To compare the input with the patterns from your intents.json storage file, you have to declare the intents file path.

```
intents_file_path = "intents.json"

Class = patterncompare(input_string, intents_file_path)

print(Class)
```
<h3> Functionality </h3>

<h4>Version 0.0.1</h4>

- Word tokenizer ✓
- Intent classifier ✓
- Language Model Builder (TBD)
- Support for Darwin, Unix-like and Windows ✓
