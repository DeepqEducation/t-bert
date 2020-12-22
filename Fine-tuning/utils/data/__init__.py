from .metrics import is_sklearn_available

from .processors import (
    DataProcessor,
    InputExample,
    InputFeatures,
    SingleSentenceClassificationProcessor,
    glue_convert_examples_to_features,
    glue_output_modes,
    glue_processors,
    glue_tasks_num_labels,

)


if is_sklearn_available():
    from .metrics import glue_compute_metrics
