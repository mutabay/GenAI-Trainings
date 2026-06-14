# LLMOps Notes

LLMOps is used to manage the lifecycle of large language models. Data preparation, model tuning, automation, deployment, monitoring, and safety are included.

## Data Preparation

Good training data is required for effective model tuning.

- Relevant data is selected from BigQuery.
- Questions and accepted answers are joined.
- Instructions are added to describe the expected task.
- Data is divided into training and evaluation sets.
- Data is stored in JSONL format.
- Dataset versions are kept for reproducibility.

Large datasets should be filtered in the SQL query instead of being loaded fully into memory.

## Kubeflow Pipelines

Kubeflow Pipelines is used to automate machine learning workflows.

- **Component:** A single, reusable workflow step.
- **Pipeline:** A group of connected components.
- **PipelineTask:** An object created when a component is called.
- **Output:** A value passed from one component to another.

Components are created with `@dsl.component`:

```python
@dsl.component
def prepare_data(path: str) -> str:
    return path
```

Pipelines are created with `@dsl.pipeline`:

```python
@dsl.pipeline
def training_pipeline(path: str):
    prepare_data(path=path)
```

Named arguments must be used when components are called. Outputs must be passed with `.output`.

Pipelines are compiled into YAML:

```python
compiler.Compiler().compile(training_pipeline, "pipeline.yaml")
```

The YAML file can be executed with Vertex AI Pipelines.

## Model Tuning

Training and evaluation datasets are supplied to a tuning pipeline.

Important settings include:

- Number of training steps
- Evaluation interval
- Base model
- Model name and version
- Pipeline caching

Model versioning supports reproducibility, auditing, and rollback.

## Predictions and Prompts

A tuned model is accessed through a deployed endpoint.

Production prompts should follow the same structure as the prompts used during training. Different prompt formats may reduce model performance.

A prompt can contain:

```text
Instruction + User question
```

## Safety and Citations

Model responses may include:

- A blocked status
- Safety categories and probability scores
- Citation metadata

Additional safety thresholds can be applied after a response is received.

## Main Lessons

- Data quality affects model quality.
- Pipelines make workflows repeatable and automated.
- Small, reusable components make failures easier to manage.
- Versioning should be applied to data, models, and pipelines.
- Training and production prompts should remain consistent.
- Safety checks should be included in production workflows.
