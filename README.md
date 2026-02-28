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


## Contribution Description

This fork offers the following contributions:
- [Repository Refresh](#repository-refresh) - updates the dependencies such that the code could be run on modern Python package ecosystem and fix several compatability issues.
- [Guaranteed K-anonymity](#guaranteed-k-anonymity) - adds a new parameter `guaranteed_k_anonymity` to the `GeneralizeToRepresentative` class that allows you to increase the minimum samples in the leaves of the starting decision tree, leading to higher generalization.

### Repository Refresh
> The project dependencies were updated to modern Python (3.11) package ecosystem versions and compatability issues fixed. Introduced proper dependency specification locks via [Poetry](https://python-poetry.org/) project manager. Code formatting tools added via pre-commit hooks.

#### Setup Instructions
You can instal necessary dependencies and pre-commit hooks via:
```bash
poetry intall
poetry run pre-commit install
```

After which, you can run a proper generalization example via [minimization_adult_new.ipynb](./notebooks/contribution/minimization_adult_new.ipynb) notebook.

#### Contribution glossary
1. Introduced proper dependency locking via [Poetry](https://python-poetry.org/) and updated dependencies (here)
2. Added code automated code formatting ([here](./pyproject.toml))
3. Made new package compatability changes (mainly for newer numpy versions) (here)
4. Resolved the `UserWarnings` that were caused by fitting the minimizer with named features while running inference on raw numpy arrays (here)
5. Added `calculate_disclosure_risk` function to calculate the "Disclosure Risk" metric as introduced in the original paper ([here](./apt/utils/metrics/metrics.py)).
6. Added an updated [minimization_adult_new.ipynb](./notebooks/contribution/minimization_adult_new.ipynb) notebook to demonstrate working base functionality after above changes ([here](./notebooks/contribution/minimization_adult_new.ipynb))

### Guaranteed k-anonymity
>The original codebase hardcodes the surrogate decision tree to split until it reaches perfectly homogeneous leaves, which often results in hyper-specific clusters containing only a single or a few data points. Then, it relies on the uprooting algorithm to retroactively increase generalizations by pruning these highly specific branches. However, if the accuracy drops below the threshold too quickly, this pruning is halted, leaving those micro-clusters exposed and highly vulnerable to **identity disclosure attacks**.

We introduce the `guaranteed_k_anonymity` parameter to allow the surrogate Decision Tree to train branches with a specific number of minimum datapoints (as opposed to minimum of 1 by default). This directly addresses the authors' own suggestion to explore "the number of samples in each leaf" to optimize generalizations and reduce unhealthy overfitting of the surrogate model.

```python
minimizer = default_minimizer = GeneralizeToRepresentative(
    model,
    guaranteed_k_anonymity = 5 # controls the min leaves in the decision tree

)
```

Please see a working example in the [guaranteed_k_anonymity.ipynb](./notebooks/contribution/guaranteed_k_anonymity.ipynb) notebook for more details It shows you how increasing this paramter can lead to better generalization (i.e. reduced disclosure risk) and lower loss of accuracy.

#### Contribution glossary
1. Added the `guaranteed_k_anonymity` parameter to the original `GeneralizeToRepresentative` transformer (here)
2. Added the [guaranteed_k_anonymity.ipynb](./notebooks/contribution/guaranteed_k_anonymity.ipynb) notebook to demonstrate the benefit of this contribution.

Citation
--------
Abigail Goldsteen, Ola Saadi, Ron Shmelkin, Shlomit Shachor, Natalia Razinkov,
"AI privacy toolkit", SoftwareX, Volume 22, 2023, 101352, ISSN 2352-7110, https://doi.org/10.1016/j.softx.2023.101352.
