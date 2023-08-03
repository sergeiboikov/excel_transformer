from transformer.BaseTransformer import BaseTransformer


class DeleteDuplicatesTransformer(BaseTransformer):
    keys = []

    def validate_params(self, params):
        if 'keys' not in params:
            raise ValueError("Valid keys are not set")
        print(f"params.get('keep')={params.get('keep')}")
        if 'keep' not in params and params.get('keep') not in ['first', 'last', False]:
            raise ValueError("Valid keep are not set")

    def transform(self, df):
        new_df = df.drop_duplicates(subset = self.keys,
                                    keep = self.keep).reset_index(drop = True)
        print('Duplicates by keys were deleted.')
        return new_df

    def __init__(self, params):
        super(DeleteDuplicatesTransformer, self).__init__(params)
        self.validate_params(params)

        self.keys = params.get('keys')
        self.keep = params.get('keep')
