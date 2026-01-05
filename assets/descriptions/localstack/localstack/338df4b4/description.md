# Title
Move Lambda v1 provider to legacy package

# Summary
Refactor Lambda v1 (old provider) code into dedicated `legacy` package to prepare for removal in 3.0 and minimize breaking changes.

# Why
- Prepare for deprecation/removal of old Lambda provider
- Minimize major changes upon 3.0 release
- Mirror structure already used in localstack-ext
- Clearly separate legacy provider from new provider

# Changes

**Move Lambda V1 implementation to `legacy` package:**
- `lambda_api.py` → `legacy/lambda_api.py`
- `lambda_executors.py` → `legacy/lambda_executors.py`  
- `lambda_models.py` → `legacy/lambda_models.py`
- `lambda_starter.py` → `legacy/lambda_starter.py`
- Extract legacy-specific utils → `legacy/lambda_utils.py`
- Extract legacy AWS models → `legacy/aws_models.py` (from `utils/aws/aws_models.py`)
- Extract legacy DLQ utils → `legacy/dead_letter_queue.py`

**Split up `lambda_utils.py`:**
- Move old provider code → `legacy/lambda_utils.py`
- Move event source listener helpers → `event_source_listeners/utils.py`  
- Move Docker/container networking helpers → `networking.py`
- Keep minimal shared helpers in main `lambda_utils.py`

**Update imports:**
- Event source listener adapters
- Lambda tests (`test_lambda_*.py`)
- CloudFormation IAM models
- Service providers
- API Gateway tests

**Cleanup:**
- Add/update documentation strings
- Add `TODO[LambdaV1]` markers for future cleanup
- Deprecate old runtime constants
- Refactor deprecated usages of runtime variables

# Notes
- Pure refactoring, no behavior changes
- Legacy provider remains functional
- Tests updated to new import paths