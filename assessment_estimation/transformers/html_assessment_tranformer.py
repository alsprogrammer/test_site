from assessment_estimation.subjects import Assessment
from assessment_estimation.transformers.assessment_transformer_abs import AssessmentTransformer
from flask import render_template


class HTMLAssessmentTransformer(AssessmentTransformer):
    def __init__(self):
        self.template_name = "test_site.html"

    def transform(self, assessment_to_transform: Assessment):
        return render_template(self.template_name, title="Добро пожаловать!",
                               assessment_uid=assessment_to_transform.uuid, assessment=assessment_to_transform)