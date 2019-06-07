import copy


class ReadonlyModelFormMixin(object):
    """
    make model form readonly. define a modelform first then extend a sub one and also inherit this
    """
    readonly_exclude = ()

    def get_update_fields(self):
        # exclude field not belong this model from
        update_fields = copy.deepcopy(self.readonly_exclude)
        fields_name = [field.name for field in self.instance._meta.get_fields()]
        for field in self.readonly_exclude:
            if field not in fields_name:
                update_fields.remove(field)

        return update_fields

    def __init__(self, *args, **kwargs):
        super(ReadonlyModelFormMixin, self).__init__(*args, **kwargs)
        for key, field in self.fields.items():
            if key in self.readonly_exclude:
                continue

            # .disabled is new attr in Django 1.9, will ignore this field when submit, so no worry about html tamper
            field.disabled = True
            field.widget.attrs['readonly'] = True
            field.required = False

    def save(self, commit=True):
        if self.readonly_exclude:
            if self.errors:
                raise ValueError(
                    "The %s could not be %s because the data didn't validate." % (
                        self.instance._meta.object_name,
                        'created' if self.instance._state.adding else 'changed',
                    )
                )
            if commit:
                self.instance.save(update_fields=self.get_update_fields())
                self._save_m2m()
            else:
                self.save_m2m = self._save_m2m
            return self.instance
        else:
            # without saving
            return self.instance
