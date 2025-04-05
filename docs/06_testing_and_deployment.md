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

### Using the Github Actions CI/CD Pipeline

The project uses a CI/CD pipeline powered by GitHub Actions to automate testing and ensure code quality. The pipeline is defined in the `.github/workflows/django.yml` file and is triggered whenever a commit is pushed to the `main` branch or a pull request is created. It tests the code against Python versions 3.11 and 3.12 to ensure compatibility.

### Key Steps in the Workflow

1. **Triggering the Workflow**: The pipeline runs automatically on `push` and `pull_request` events targeting the `main` branch.

2. **Setting Up the Environment**:
   - The workflow uses the latest Ubuntu environment (`ubuntu-latest`) to run the tests. Since Django is a Python web framework, the choice of Ubuntu should not affect the tests as it should run on any operating system.
   - It sets up Python versions 3.11 and 3.12 to test compatibility across multiple versions.

3. **Installing Dependencies**:
   - The pipeline installs all required dependencies listed in the `requirements.txt` file to ensure the environment is ready for testing.

4. **Running Unit Tests**:
   - The workflow executes the Django unit tests using the `python manage.py test` command to validate the code.

5. **Reporting Results**:
   - The results of the tests are reported back to the GitHub Actions interface, providing immediate feedback on the status of the code. If all tests pass, the commit is considered successful and there will be a green checkmark next to the commit in the project page. If any test fails, the commit will show a red x icon, indicating that there are issues that need to be addressed.



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
#### Medications

The following unit tests are implemented in the `medications` application, found under `medications/tests.py`:

1. **Pharmacist**:
   - `test_pharmacist_creation`: Verifies that a `Pharmacist` instance is created with the correct attributes, including `username`, `phone_number`, and `address`.
   - `test_pharmacist_str`: Ensures the `__str__` method returns the correct string representation of the pharmacist.

2. **MedicationType**:
   - `test_medication_type_creation`: Verifies that a `MedicationType` instance is created with the correct name.
   - `test_medication_type_str`: Ensures the `__str__` method returns the correct string representation of the medication type.

3. **MedicationGenericName**:
   - `test_generic_name_creation`: Verifies that a `MedicationGenericName` instance is created with the correct attributes, including the relationship to a `MedicationType`.
   - `test_generic_name_str`: Ensures the `__str__` method returns the correct string representation of the generic name.

4. **Medication**:
   - `test_medication_creation`: Verifies that a `Medication` instance is created with the correct attributes, including relationships to `MedicationGenericName` and other fields like `dosage_form`, `strength`, and `manufacturer`.
   - `test_medication_str`: Ensures the `__str__` method returns the correct string representation of the medication.

5. **MedicationInventory**:
   - `test_inventory_creation`: Verifies that a `MedicationInventory` instance is created with the correct attributes, including the relationship to a `Medication`, `quantity`, `expiration_date`, and `location`.
   - `test_inventory_str`: Ensures the `__str__` method returns the correct string representation of the inventory.

6. **MedicationPrescription**:
   - `test_prescription_creation`: Verifies that a `MedicationPrescription` instance is created with the correct attributes, including relationships to `PDLProfile`, `Medication`, and `Physician`, as well as fields like `dosage`, `frequency`, and `duration`.
   - `test_prescription_str`: Ensures the `__str__` method returns the correct string representation of the prescription.

To run the unit tests for the `medications` app, use the following command:

```bash
python manage.py test medications
```

The result should look like this:

```bash
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..................
----------------------------------------------------------------------
Ran 18 tests in 0.012s

OK
Destroying test database for alias 'default'...
```


