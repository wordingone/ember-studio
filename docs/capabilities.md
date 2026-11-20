# The five capabilities

Ember Studio is organised around five things a research environment must let you do. This page says, for each, what the program does today and what it does not. It describes the build the documentation was checked against ([release note](releases/0.5.0-de6494fe.md)); no release has been published yet. The longer list of what does not work is in [known limits](known-limits.md); where this page and that one differ, that one is the stricter.

| Capability | What you can do today | What you cannot do yet |
| --- | --- | --- |
| Construct | See the models on disk, grouped by role ([models](tabs/models.md)). The Research tab has project-file buttons (NEW, OPEN, SAVE, ADD EXPERIMENT, ADD HYPOTHESIS, ADD MODEL) that this guide did not exercise ([research](tabs/research.md)) | Draw or edit an architecture, compose datasets into a mixture, edit a training pipeline |
| Experiment | Start, watch and stop a governed training hour through the lab ([Hour view](tabs/hour-view.md), [train](tabs/train.md)); read finished and running jobs ([console](tabs/console.md), [timeline](tabs/timeline.md)) | A saved experiment form with typed hyperparameters, a queue, a compare view of two runs' hyperparameters |
| Inspect | A two-model compare frame on Models ([models](tabs/models.md#compare)); the transplant edits of each arm and a tower of the live model's layers with their tensors ([weights](tabs/weights.md)); donor and recipient networks drawn in 3D with their layers ([research](tabs/research.md)) | Activations, attention maps and gradients on a prompt |
| Investigate capability | Read transplant pairs scored against a 3 SE bar, with donor and recipient scores ([evals](tabs/evals.md)) | Start an evaluation from Studio, write a hypothesis against a weakness and link the test |
| Automate research | Chat with a model (the lab's resident model, or any model you name in a provider config file) that reads and edits files in a working folder you choose, under approvals ([agent](tabs/agent.md)) | A proposal inbox where an agent files an experiment for you to approve |

## Reading this table

- **Today** means built and, where [known limits](known-limits.md) does not say otherwise, operated.
- **Cannot yet** means not built. Nothing in that column is described as a feature anywhere else in these docs.
- Several controls are built but were not exercised for the documentation; [known limits](known-limits.md) lists them.
- The roadmap in [ROADMAP.md](../ROADMAP.md) is plans, not features.
