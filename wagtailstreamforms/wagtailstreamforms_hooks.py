import json
from copy import deepcopy

from django.core.serializers.json import DjangoJSONEncoder
from django.template.defaultfilters import pluralize

from wagtailstreamforms.hooks import register
from wagtailstreamforms.models import FormSubmissionFile


@register('process_form_submission')
def save_form_submission_data(instance, form):
    """ saves the form submission data """

    # copy the cleaned_data so we dont mess with the original
    submission_data = deepcopy(form.cleaned_data)

    # change the submission data to a count of the files
    for field in form.files.keys():
        count = len(form.files.getlist(field))
        submission_data[field] = '{} file{}'.format(count, pluralize(count))

    # save the submission data
    submission = instance.get_submission_class().objects.create(
        form_data=json.dumps(submission_data, cls=DjangoJSONEncoder),
        form=instance
    )

    # save the form files
    for field in form.files:
        for file in form.files.getlist(field):
            FormSubmissionFile.objects.create(
                submission=submission,
                field=field,
                file=file
            )
