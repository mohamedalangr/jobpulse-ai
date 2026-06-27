def override_search_use_case():
    class MockSearchUseCase:
        def execute(self, query, context):
            return []
    return MockSearchUseCase()
