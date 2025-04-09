# Medtrack User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Features](#features)
   - [PDL Management](#pdl-management)
   - [Consultation Management](#consultation-management)
   - [Medication Management](#medication-management)
4. [How to Use](#how-to-use)
   - [Logging In](#logging-in)
   - [Navigating the Dashboard](#navigating-the-dashboard)
   - [Using Filters](#using-filters)
   - [Switching Themes](#switching-themes)
5. [IT Admin (Django Administrator) Features](#it-admin-django-administrator-features)
   - [Accessing the Django Admin Panel](#accessing-the-django-admin-panel)
   - [Available Admin Models](#available-admin-models)
   - [Adding or Modifying Records](#adding-or-modifying-records)
   - [User Management](#user-management)
   - [Group and Role Management](#group-and-role-management)
   - [Custom Filters and Search](#custom-filters-and-search)
   - [Bulk Actions](#bulk-actions)
   - [Logging and History](#logging-and-history)
   - [Theme or Global Settings](#theme-or-global-settings)
   - [Security Notes](#security-notes)
6. [Contact Support](#contact-support)
7. [Testing and Development](#testing-and-development)
   - [Running Tests](#running-tests)

---

## Introduction
Medtrack is a comprehensive platform designed to streamline the management of medical records, consultations, and medications. It is tailored for healthcare professionals and administrators to ensure seamless healthcare management.

---

## Getting Started
1. **Access the App**: Open the app in your browser at the provided URL.
2. **Login Credentials**: Use your assigned username and password to log in.
3. **Navigation**: Use the navigation bar at the top to access different sections of the app.

---

## Features

### PDL Management

1. **Viewing PDL Profiles**:
    - Navigate to the **PDL List** section from the navigation bar.
    - Browse the list of PDL profiles displayed.
    - Use the search bar to find a specific PDL by name or ID.

2. **Adding a New PDL Profile**:
    - Click the **Add New PDL** button in the **PDL List** section.
    - Fill in the required fields, such as:
      - Full Name
      - Date of Birth
      - Identification Number
      - Detention Details
    - Click **Save** to create the new profile.

3. **Updating an Existing PDL Profile**:
    - Locate the PDL profile you want to update in the **PDL List**.
    - Click the **Edit** button next to the profile.
    - Modify the necessary fields, such as:
      - Status (e.g., Active, Released)
      - Detention Details
      - Medical History
    - Click **Update** to save the changes.

4. **Managing Detention Instances**:
    - Open the PDL profile you want to manage.
    - Navigate to the **Detention Instances** tab.
    - Add a new detention instance by clicking **Add Instance** and filling in:
      - Detention Start Date
      - Detention End Date (if applicable)
      - Facility Name
    - Edit or delete existing detention instances as needed.

5. **Tracking PDL Statuses**:
    - Use the **Status Overview** feature in the **PDL List** section.
    - Filter PDLs by their current status (e.g., Active, Released, Transferred).
    - Generate reports for specific statuses if required.


### Consultation Management

1. **Scheduling a Consultation**:
    - Navigate to the **Consultation Calendar** section from the navigation bar.
    - Click the **Schedule Consultation** button.
    - Fill in the required details, such as:
      - Physician Name
      - PDL Name
      - Date and Time
      - Consultation Type (e.g., Initial, Follow-up)
    - Click **Save** to schedule the consultation.

2. **Viewing Scheduled Consultations**:
    - Open the **Consultation Calendar** section.
    - Browse the calendar to view scheduled consultations.
    - Use the filters to search for consultations by:
      - Physician
      - PDL
      - Date Range
    - Click on a consultation entry to view its details.

3. **Managing Consultations**:
    - Locate the consultation you want to manage in the **Consultation Calendar**.
    - Click the **Edit** button to modify consultation details, such as:
      - Rescheduling the date and time
      - Changing the assigned physician or PDL
    - Click **Update** to save the changes.
    - To cancel a consultation, click the **Cancel** button and confirm the action.

4. **Accessing Consultation History**:
    - Navigate to a specific PDL profile from the **PDL List** section.
    - Open the **Consultation History** tab within the profile.
    - Review past consultations, including:
      - Dates and times
      - Physicians involved
      - Notes or outcomes recorded during the consultations.

5. **Generating Consultation Reports**:
    - Use the **Reports** feature in the **Consultation Calendar** section.
    - Select the desired filters, such as:
      - Date Range
      - Physician
      - Consultation Type
    - Generate and export reports in formats like PDF or Excel for record-keeping or analysis.

### Medication Management

1. **Viewing Medication Inventories**:
    - Navigate to the **Medications** section from the navigation bar.
    - Browse the list of available medications displayed.
    - Use the search bar to find a specific medication by name, generic name, or route of administration.

2. **Adding a New Medication**:
    - Click the **Add New Medication** button in the **Medications** section.
    - Fill in the required fields, such as:
      - Medication Name
      - Generic Name
      - Dosage Form (e.g., Tablet, Syrup)
      - Route of Administration (e.g., Oral, Intravenous)
      - Stock Quantity
    - Click **Save** to add the medication to the inventory.

3. **Updating Medication Details**:
    - Locate the medication you want to update in the **Medications** section.
    - Click the **Edit** button next to the medication entry.
    - Modify the necessary fields, such as:
      - Stock Quantity
      - Expiration Date
      - Dosage Instructions
    - Click **Update** to save the changes.

4. **Prescribing Medications to PDLs**:
    - Open the PDL profile to whom you want to prescribe medication.
    - Navigate to the **Prescriptions** tab within the profile.
    - Click the **Add Prescription** button and fill in:
      - Medication Name
      - Dosage Instructions
      - Duration (e.g., 7 days, 2 weeks)
      - Notes or special instructions (if any)
    - Click **Save** to issue the prescription.

5. **Filtering Medications**:
    - Use the filter options in the **Medications** section to search for medications by:
      - Name
      - Generic Name
      - Route of Administration
    - Click **Apply Filters** to view the filtered results.

6. **Managing Medication Stock** (IT ADMIN ONLY):
    - Navigate to the **Stock Management** tab in the **Medications** section.
    - Add new stock by clicking the **Add Stock** button and entering:
      - Medication Name
      - Quantity
      - Batch Number
      - Expiration Date
    - Update or remove stock entries as needed to maintain accurate inventory records.

7. **Generating Medication Reports**:
    - Use the **Reports** feature in the **Medications** section.
    - Select the desired filters, such as:
      - Date Range
      - Medication Name
      - Stock Levels
    - Generate and export reports in formats like PDF or Excel for inventory tracking or analysis.

---

## IT Admin (Django Administrator) Features

The Django Admin Panel provides IT administrators with powerful tools to manage backend data and configurations. This section outlines how to access and use the Django Admin interface in Medtrack.

### Accessing the Django Admin Panel
1. Navigate to the admin login page, usually at `/admin`.
2. Enter your admin username and password.
3. Click **Login** to access the admin dashboard.

### Available Admin Models
Once logged in, you’ll see a list of registered models. These typically include:
- **Users**: Manage system users and their permissions.
- **Groups**: Create and manage permission groups.
- **PDLs**: View and edit PDL profiles.
- **Detention Instances**: Manage detention details separately from the PDL profile page.
- **Consultations**: Access all scheduled consultations.
- **Medications**: Manage global medication records.
- **Prescriptions**: View and modify issued prescriptions.
- **Audit Logs**: *(If enabled)* Track changes made within the system.
- **Themes/Settings**: *(If implemented)* Control global UI or system settings.

### Adding or Modifying Records
1. Click on a model (e.g., **Medications**) to view a list of entries.
2. Use the **Add** button (top-right) to create a new entry.
3. To edit an existing record, click its name or the **Edit** button next to it.
4. Modify fields as necessary, then click **Save**.

### User Management
- Go to the **Users** model.
- Add or remove users, reset passwords, and assign them to groups.
- Use the **Permissions** section within the user form to grant specific access levels (e.g., view only, add, change, delete).
- Optionally assign **staff status** or **superuser status** for higher access privileges.

### Group and Role Management
1. Navigate to the **Groups** section.
2. Add a new group and assign permissions granularly (per model and action).
3. Assign users to these groups from the **Users** model for consistent access control.

### Custom Filters and Search
- Use the search bar and filters on the changelist view (list of entries) to find data quickly.
- These filters may include dates, names, IDs, or statuses depending on the model’s configuration.

### Bulk Actions
1. Use the checkboxes beside entries to select multiple records.
2. Select an action from the **Action** dropdown, such as **Delete selected**, and confirm.

### Logging and History
- Most model entries support a **History** view.
- Click into a record and use the **History** button to see past changes (user, timestamp, change details).

### Theme or Global Settings *(Optional)*
If your Medtrack instance includes admin-level UI or global settings:
1. Navigate to the **Settings** or **Themes** model.
2. Change system-wide preferences such as default view mode, color scheme, or time zones.
3. Click **Save** to apply changes instantly across users *(if configured)*.

### Security Notes
- Always use strong passwords for admin accounts.
- Enable 2FA if supported.
- Limit superuser access to essential personnel only.
- Regularly audit user permissions and system logs.

## How to Use

### Logging In
1. Navigate to the login page.
2. Enter your username and password.
3. Click the **Login** button.

### Navigating the Dashboard
- Use the navigation bar to access:
  - **Home**: Overview of the app.
  - **Consultation Calendar**: View scheduled consultations.
  - **PDL List**: Manage PDL profiles.
  - **Medications**: Manage medication inventories and prescriptions.

### Using Filters
- Navigate to the **Medications** section.
- Use the filter options to search for medications by:
  - Name
  - Generic Name
  - Route of Administration
- Click **Apply Filters** to view the filtered results.

### Switching Themes
- Use the **Switch to Light/Dark Mode** button in the top-right corner to toggle between light and dark themes.

---

## Testing and Development
### Running Tests
To run the test suite, use the following command:
```bash
python manage.py test