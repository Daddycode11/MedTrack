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

#### Consultations

The following unit tests are implemented in the `consultations` application, found under `consultations/tests.py`:

1. **MedicalSpecialty**:
   - `test_creation`: Verifies that a `MedicalSpecialty` instance is created with the correct attributes.
   - `test_str_representation`: Ensures the `__str__` method returns the correct string representation.

2. **Physician**:
   - `test_creation`: Verifies that a `Physician` instance is created with the correct attributes, including the relationship to a `MedicalSpecialty`.
   - `test_str_representation`: Ensures the `__str__` method returns the correct string representation.

3. **ConsultationLocation**:
   - `test_creation`: Verifies that a `ConsultationLocation` instance is created with the correct attributes.
   - `test_str_representation`: Ensures the `__str__` method returns the correct string representation.

4. **ConsultationReason**:
   - `test_creation`: Verifies that a `ConsultationReason` instance is created with the correct attributes.
   - `test_str_representation`: Ensures the `__str__` method returns the correct string representation.

5. **Consultation**:
   - `test_creation`: Verifies that a `Consultation` instance is created with the correct attributes, including relationships to `PDLProfile`, `Physician`, `ConsultationLocation`, and `ConsultationReason`.
   - `test_str_representation`: Ensures the `__str__` method returns the correct string representation.
   - `test_unique_constraints`: Tests the unique constraints defined in the `Consultation` model to ensure no duplicate consultations are created for the same `PDLProfile`, `Physician`, or `Location` in the same time block.

To run the unit tests for the `consultations` app, use the following command:

```bash
python manage.py test consultations
```

The result should look like this:

```bash
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
............
----------------------------------------------------------------------
Ran 13 tests in 0.006s

OK
Destroying test database for alias 'default'...
```
