# 06. Testing and Deployment

## Testing

### Running Unit Tests

Individual unit tests are written for each application in this project. These tests are located in the `tests` directory of each application. To run the unit tests, use the following command:

```bash
python manage.py test
```

To run a specific test case or test suite, use the following command:

```bash
python manage.py test <app_name>.tests.<TestCaseName>
```
For example, to run the tests in the `pdl` application, use:

```bash
python manage.py test pdl.tests
```

The result should look like this:

```bash
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.
----------------------------------------------------------------------
Ran 8 tests in 0.123s
OK
Destroying test database for alias 'default'...
```

### Documentation of Unit Tests

#### PDL

The following unit tests are implemented in the `pdl` application, found under `pdl/tests.py`:

1. **DetentionStatus**:
   - Tests the string representation of the model.
   - Verifies the verbose name and plural verbose name.

2. **PDLProfile**:
   - Tests the string representation of the model.
   - Ensures that the `email` field is unique.

3. **DetentionReason**:
   - Tests the string representation of the model.

4. **DetentionInstance**:
   - Tests the string representation of the model.
   - Verifies the ordering of detention instances.

To run the unit tests for the `pdl` app, use the following command:

```bash
python manage.py test pdl
```

The result should look like this:

```bash
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
......
----------------------------------------------------------------------
Ran 8 tests in 0.003s
OK
Destroying test database for alias 'default'...
```
