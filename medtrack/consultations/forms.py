from django import forms
from .models import Consultation
from pdl.models import PDLProfile
from consultations.models import Physician, ConsultationLocation, ConsultationReason

class ScheduleConsultationForm(forms.ModelForm):
    """
    Form for scheduling or rescheduling a consultation, including
    Past Medical History, Physical Exam on Arrival, TB screening, and Final Remarks.
    """

    class Meta:
        model = Consultation
        fields = [
            # --- Consultation Details ---
            'pdl_profile',                 # NOTE: your template had pdlr_profile; use pdl_profile
            'physician',
            'location',
            'reason',
            'consultation_date_date_only',
            'consultation_time_block',
            'is_an_emergency',
            'notes',

            # --- Past Medical History (pmh_) ---
            'pmh_pediatric_history',
            'pmh_major_adult_illnesses',
            'pmh_major_surgeries',
            'pmh_serious_injuries',
            'pmh_limitations',
            'pmh_medication_history',
            'pmh_transfusions_reactions',
            'pmh_mental_emotional',
            'pmh_blood_type',
            'pmh_allergies',
            'pmh_family_history',          # single-choice per your request
            'pmh_psychiatric_history',
            'pmh_psychiatric_when',
            'pmh_psychiatric_facility',
            'pmh_arv_treatment',
            'pmh_arv_details',
            'pmh_vaccines',
            'pmh_alcohol_drinker',
            'pmh_smoking',
            'pmh_illicit_drugs',
            'pmh_poly_drug_use',

            # --- Physical Exam on Arrival (pea_) ---
            'pea_temperature',
            'pea_blood_pressure',
            'pea_heart_rate',
            'pea_rr',
            'pea_height',
            'pea_weight',
            'pea_bmi',
            'pea_general_appearance',
            'pea_head_eyes_ears_nose_throat',
            'pea_neck',
            'pea_chest_lungs',
            'pea_heart',
            'pea_abdomen',
            'pea_genito_urinary',
            'pea_musculoskeletal',
            'pea_extremities',
            'pea_other_findings',

            # --- TB Entry Screening (tb_) ---
            'tb_unexplained_cough',
            'tb_bmi_less_18_5',
            'tb_blood_streaked_sputum',
            'tb_cxr_suggestive',
            'tb_previous_treatment',
            'tb_exposure',
            'tb_remarks',

            # --- Final Remarks (fr_) ---
            'fr_conclusion',
            'fr_other_impressions',
            'fr_recommendation',
        ]

        widgets = {
            # --- Consultation Details ---
            'pdl_profile': forms.Select(attrs={'class': 'form-select'}),
            'physician': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.Select(attrs={'class': 'form-select'}),
            'reason': forms.Select(attrs={'class': 'form-select'}),
            'consultation_date_date_only': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'consultation_time_block': forms.Select(attrs={'class': 'form-select'}),
            'is_an_emergency': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),

            # --- PMH text fields ---
            'pmh_pediatric_history': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'pmh_major_adult_illnesses': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'pmh_major_surgeries': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'pmh_serious_injuries': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'pmh_limitations': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'pmh_medication_history': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'pmh_transfusions_reactions': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'pmh_mental_emotional': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'pmh_blood_type': forms.Select(attrs={'class': 'form-select'}),
            'pmh_allergies': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'pmh_family_history': forms.Select(attrs={'class': 'form-select'}),  # single-select
            'pmh_psychiatric_history': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pmh_psychiatric_when': forms.TextInput(attrs={'class': 'form-control'}),
            'pmh_psychiatric_facility': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pmh_arv_treatment': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pmh_arv_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'pmh_vaccines': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'pmh_alcohol_drinker': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pmh_smoking': forms.Select(attrs={'class': 'form-select'}),
            'pmh_illicit_drugs': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pmh_poly_drug_use': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

            # --- PEA vitals ---
            'pea_temperature': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'pea_blood_pressure': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 120/80'}),
            'pea_heart_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0'}),
            'pea_rr': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0'}),
            'pea_height': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0'}),
            'pea_weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0'}),
            'pea_bmi': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0'}),

            # --- PEA complaint booleans ---
            'pea_general_appearance': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pea_head_eyes_ears_nose_throat': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pea_neck': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pea_chest_lungs': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pea_heart': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pea_abdomen': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pea_genito_urinary': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pea_musculoskeletal': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pea_extremities': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pea_other_findings': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),

            # --- TB Screening ---
            'tb_unexplained_cough': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tb_bmi_less_18_5': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tb_blood_streaked_sputum': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tb_cxr_suggestive': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tb_previous_treatment': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tb_exposure': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tb_remarks': forms.Select(attrs={'class': 'form-select'}),

            # --- Final Remarks ---
            'fr_conclusion': forms.Select(attrs={'class': 'form-select'}),
            'fr_other_impressions': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'fr_recommendation': forms.Select(attrs={'class': 'form-select'}),
        }

    # Optional: ensure a logical render order if needed by Django
    field_order = [
        'pdl_profile', 'physician', 'location', 'reason',
        'consultation_date_date_only', 'consultation_time_block', 'is_an_emergency', 'notes',
        'pmh_pediatric_history', 'pmh_major_adult_illnesses', 'pmh_major_surgeries',
        'pmh_serious_injuries', 'pmh_limitations', 'pmh_medication_history',
        'pmh_transfusions_reactions', 'pmh_mental_emotional', 'pmh_blood_type', 'pmh_allergies',
        'pmh_family_history', 'pmh_psychiatric_history', 'pmh_psychiatric_when',
        'pmh_psychiatric_facility', 'pmh_arv_treatment', 'pmh_arv_details',
        'pmh_vaccines', 'pmh_alcohol_drinker', 'pmh_smoking', 'pmh_illicit_drugs', 'pmh_poly_drug_use',
        'pea_temperature', 'pea_blood_pressure', 'pea_heart_rate', 'pea_rr',
        'pea_height', 'pea_weight', 'pea_bmi',
        'pea_general_appearance', 'pea_head_eyes_ears_nose_throat', 'pea_neck', 'pea_chest_lungs',
        'pea_heart', 'pea_abdomen', 'pea_genito_urinary', 'pea_musculoskeletal', 'pea_extremities',
        'pea_other_findings',
        'tb_unexplained_cough', 'tb_bmi_less_18_5', 'tb_blood_streaked_sputum',
        'tb_cxr_suggestive', 'tb_previous_treatment', 'tb_exposure', 'tb_remarks',
        'fr_conclusion', 'fr_other_impressions', 'fr_recommendation',
    ]
