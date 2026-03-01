[![OpenSSF Best Practices](https://bestpractices.coreinfrastructure.org/projects/5836/badge)](https://bestpractices.coreinfrastructure.org/projects/5836)

# ai-privacy-toolkit

- [Original Description](#original-description) - the README of the original code by the authors
- [Contribution Description](#contribution-description) - description of the changes in this contribution fork.

## Original Description
<p align="center">
  <img src="docs/images/logo with text.jpg?raw=true" width="467" title="ai-privacy-toolkit logo">
</p>
<br />

A toolkit for tools and techniques related to the privacy and compliance of AI models.

The [**anonymization**](apt/anonymization/README.md) module contains methods for anonymizing ML model
training data, so that when a model is retrained on the anonymized data, the model itself will also be
considered anonymous. This may help exempt the model from different obligations and restrictions
set out in data protection regulations such as GDPR, CCPA, etc.

The [**minimization**](apt/minimization/README.md) module contains methods to help adhere to the data
minimization principle in GDPR for ML models. It enables to reduce the amount of
personal data needed to perform predictions with a machine learning model, while still enabling the model
to make accurate predictions. This is done by by removing or generalizing some of the input features.

The [**dataset assessment**](apt/risk/data_assessment/README.md) module implements a tool for privacy assessment of
synthetic datasets that are to be used in AI model training.

Official ai-privacy-toolkit documentation: https://ai-privacy-toolkit.readthedocs.io/en/latest/

Installation: pip install ai-privacy-toolkit

For more information or help using or improving the toolkit, please contact Abigail Goldsteen at abigailt@il.ibm.com,
or join our Slack channel: https://aip360.mybluemix.net/community.

We welcome new contributors! If you're interested, take a look at our [**contribution guidelines**](https://github.com/IBM/ai-privacy-toolkit/wiki/Contributing).

**Related toolkits:**

ai-minimization-toolkit - has been migrated into this toolkit.

[differential-privacy-library](https://github.com/IBM/differential-privacy-library): A
general-purpose library for experimenting with, investigating and developing applications in,
differential privacy.

[adversarial-robustness-toolbox](https://github.com/Trusted-AI/adversarial-robustness-toolbox):
A Python library for Machine Learning Security. Includes an attack module called *inference* that contains privacy attacks on ML models
(membership inference, attribute inference, model inversion and database reconstruction) as well as a *privacy* metrics module that contains
membership leakage metrics for ML models.

[adversarial-robustness-toolbox](https://github.com/Trusted-AI/adversarial-robustness-toolbox):
A Python library for Machine Learning Security. Includes an attack module called *inference* that contains privacy attacks on ML models
(membership inference, attribute inference, model inversion and database reconstruction) as well as a *privacy* metrics module that contains
membership leakage metrics for ML models.




## Contribution Description

This fork offers the following contributions:
- [Repository Refresh & Performance Improvements](#repository-refresh--performance-improvements) - updates project to modern Python package ecosystem. Adds automated code-formatting. Speeds up `GeneralizeToRepresentative` with vectorized math optimizations.

- [Guaranteed K-anonymity](#guaranteed-k-anonymity) - adds a new parameter `guaranteed_k_anonymity` to the `GeneralizeToRepresentative` class that allows you to increase the minimum samples in the leaves of the starting decision tree, leading to higher generalization.

- [Sensitvity Weights](#guaranteed-k-anonymity) - adds a new parameter `sensitivity_weights` to the `GeneralizeToRepresentative` class that allows discouraging the accuracy improvement algorithm from degeneralizing contextually sensitive features.

- [Dynamic Generalization](#dynamic-generalization) - adds a `get_dynamic_generalizations` function that dynamically calculates & updates generalizations based on provided partial feature values.

> **NOTE**: Most of the contributions are linked to the code changes in the **glossary** sections. However, you can find all the changes by viewing the main [minimizer.py](./apt/minimization/minimizer.py) script and searching for "CONTRIBUTION" tags


### Repository Refresh & Performance Improvements
> Original repository is dated. We updated it to modern Python (3.11) package ecosystem versions and fixed compatability issues. Introduced proper dependency specification locks via [Poetry](https://python-poetry.org/) project manager. Code formatting tools added via pre-commit hooks. Optimized `GeneralizeToRepresentative` with vectorized math optimizations.

#### Setup Instructions
You can instal necessary dependencies and pre-commit hooks via:
```bash
poetry intall
poetry run pre-commit install
```

After which, you can run a proper generalization example via [minimization_adult_new.ipynb](./notebooks/contribution/minimization_adult_new.ipynb) notebook.

#### Contribution glossary
1. Introduced proper dependency locking via [Poetry](https://python-poetry.org/) and updated dependencies ([here](https://github.com/Miautawn/ai-privacy-toolkit/blob/main/pyproject.toml))
2. Added code automated code formatting ([here](https://github.com/Miautawn/ai-privacy-toolkit/blob/main/.pre-commit-config.yaml))
3. Made new package compatability changes (mainly for newer numpy versions) ([here](https://github.com/Miautawn/ai-privacy-toolkit/blob/29032e677eeef50bd8d0adf5a155aac99175a699/apt/minimization/minimizer.py#L784))
4. Resolved the `UserWarnings` that were caused by fitting the minimizer with named features while running inference on raw numpy arrays ([here](https://github.com/Miautawn/ai-privacy-toolkit/blob/29032e677eeef50bd8d0adf5a155aac99175a699/apt/minimization/minimizer.py#L401))
5. **Optimized key calculations to use vectorized math operations inside the "accuracy improvement" loop of `GeneralizeToRepresentative`.** This allows the minimization algorithm to run on normal-sized datasets (previously even 1k of data points would take minutes) ([here](https://github.com/Miautawn/ai-privacy-toolkit/blob/29032e677eeef50bd8d0adf5a155aac99175a699/apt/minimization/minimizer.py#L1328))
6. Added `calculate_disclosure_risk` function to calculate the "Disclosure Risk" metric as introduced in the original paper ([here](./apt/utils/metrics/metrics.py)).
7. Added an updated [minimization_adult_new.ipynb](./notebooks/contribution/minimization_adult_new.ipynb) notebook to demonstrate working base functionality after above changes ([here](./notebooks/contribution/minimization_adult_new.ipynb))

### Guaranteed k-anonymity
>The original codebase hardcodes the surrogate decision tree to split until it reaches perfectly homogeneous leaves, which often results in hyper-specific clusters containing only a single or a few data points. Then, it relies on the uprooting algorithm to retroactively increase generalizations by pruning these highly specific branches. However, if the accuracy drops below the threshold too quickly, this pruning is halted, leaving those micro-clusters exposed and highly vulnerable to **identity disclosure attacks**.

We introduce the `guaranteed_k_anonymity` parameter to allow the surrogate Decision Tree to train branches with a specific number of minimum datapoints (as opposed to minimum of 1 by default). This directly addresses the authors' own suggestion to explore "the number of samples in each leaf" to optimize generalizations and reduce unhealthy overfitting of the surrogate model.

```python
minimizer = default_minimizer = GeneralizeToRepresentative(
    model,
    guaranteed_k_anonymity = 5 # controls the min leaves in the decision tree

)
```

Under the hood, it directly sets the `min_samples_leaves` parameter for scikit-learn DecisionTree models:
```python
def fit():
  ...
  self._dt = DecisionTreeClassifier(
      min_samples_leaf=self.guaranteed_k_anonymity, # <- we control this
  )
  ...
```

Please see a working example in the [guaranteed_k_anonymity.ipynb](./notebooks/contribution/guaranteed_k_anonymity.ipynb) notebook for more details It shows you how increasing this paramter can lead to better generalization (i.e. reduced disclosure risk) and lower loss of accuracy.

#### Contribution glossary
1. Added the `guaranteed_k_anonymity` parameter to the original `GeneralizeToRepresentative` transformer ([here](https://github.com/Miautawn/ai-privacy-toolkit/blob/29032e677eeef50bd8d0adf5a155aac99175a699/apt/minimization/minimizer.py#L381))
2. Added the [guaranteed_k_anonymity.ipynb](./notebooks/contribution/guaranteed_k_anonymity.ipynb) notebook to demonstrate the benefit of this contribution.

### Sensitvity Weights
> Currently, if the initially trained surrogate is weaker than the desired accuracy threshold, the algorithm selectively degeneralizes features completely. It does so by weighting the reveal of information by the accuracy gained, **however it doesn't take into account the real-world contextual sensitivity of features.**

We introduce `sensitivity_weights` parameter which allows the us to insert domain knowledge into the degeneralization logic. For example, if we know that `age` is an incredibly sensitive feature, we can prevent the algorithm from degeneralizing it by setting an explicitly higher weight for it:
```python
minimizer = default_minimizer = GeneralizeToRepresentative(
    model,
    sensitivity_weights = {'age': 10} # default weight is 1

)
```

During the "accuracy improvement" stage, we multiply the feature's NCP score with their weights, thus ranking them lower in the feature candidate list:
```python
def _get_feature_to_remove():
  ...
  for feature in self.features:
    feature_ncp = self._calculate_ncp_for_feature_from_cells()

    weight = self.sensitivity_weights.get(feature, 1.0)
    feature_ncp = feature_ncp * weight
  ...
```

Additionally, we use the weighted average for the final dataset NCP calculation after training (see the `_calc_ncp_for_generalization()` function):
```python
def _calc_ncp_for_generalization():
  total_ncp = 0
  total_weight = 0
  ...

  for feature in self.features:
    total_ncp += self._calc_ncp(feature)
    total_weight += self.sensitivity_weights.get(feature, 1.0)

  ...
  return total_ncp / total_weight
```

Please see a working example in [sensitivity_weights.ipynb](./notebooks/contribution/sensitivity_weights.ipynb) notebook.

#### Contribution glossary
1. Added the `sensitivity_weights` parameter to the original `GeneralizeToRepresentative` transformer ([here](https://github.com/Miautawn/ai-privacy-toolkit/blob/29032e677eeef50bd8d0adf5a155aac99175a699/apt/minimization/minimizer.py#L1353))
2. Added the [sensitivity_weights.ipynb](./notebooks/contribution/sensitivity_weights.ipynb) notebook to demonstrate the benefit of this contribution.


### Dynamic Generalization
> Currently, even with proper generalizations, the potential user still has to send ALL of their information for it to be abstracted away using the surrogate model. Instead, we use the fitted surrogate model to dynamically update generalizations and the need for additional information based on partial user inputs.
>
> **This approach allows us to make "dynamic forms" that ask for only the information that is trully needed, thus minimizing the data collection in the truest form! **

We add the `get_dynamic_generalizations(known_features: dict)` function which dynamically calculates the best generalizations for the remaining features based on the provided partial feature values.

Under the hood, it takes the current leves (i.e. cells) of the surrogate model and eliminates those for which the `known_features` are outside their ranges. Then we recalculate the generalizations for the surviving leaves. It may be that all of surviving leaves point to the same label, meaning that we can use the currently known features to get the final prediction - eliminating the need for asking for all of the information!

```python
minimizer = GeneralizeToRepresentative(
    model,
    guaranteed_k_anonymity=1,  # must set it to form homogenous leaves
)

current_form = minimizer.get_dynamic_generalizations({"age": 32})

# print(current_form["ranges"]) will print consolidated generalizations
# that will be more general!

if current_form.get("status") == "Complete":
  print("No more info needed!")
else:
  print("Need additional known features")
```

Please look at the [dynamic_forms.ipynb](./notebooks/contribution/dynamic_forms.ipynb) for a working example of dynamic forms!


#### Contribution glossary
1. Added the `get_dynamic_generalizations` function to calculate generalizations based on partial inputs ([here](https://github.com/Miautawn/ai-privacy-toolkit/blob/29032e677eeef50bd8d0adf5a155aac99175a699/apt/minimization/minimizer.py#L1696))
2. Added the [dynamic_forms.ipymb](./notebooks/contribution/dynamic_forms.ipynb) to  demonstrate the benefit of this contribution.



Citation
--------
Abigail Goldsteen, Ola Saadi, Ron Shmelkin, Shlomit Shachor, Natalia Razinkov,
"AI privacy toolkit", SoftwareX, Volume 22, 2023, 101352, ISSN 2352-7110, https://doi.org/10.1016/j.softx.2023.101352.
