__version__ = "2.11.0"


from .data import (
    DataProcessor,
    InputExample,
    InputFeatures,
    SingleSentenceClassificationProcessor,
    glue_convert_examples_to_features,
    glue_output_modes,
    glue_processors,
    glue_tasks_num_labels,
    is_sklearn_available,
)

if is_sklearn_available():
    from .data import glue_compute_metrics

from .data.datasets import GlueDataset, GlueDataTrainingArguments