from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import fields, validate
from .models import Patient, Doctor, Specialisation, Appointment, Availability, MedicalRecord, MedicalRecordAccess
from .extensions import db

class PatientSchema(SQLAlchemyAutoSchema):
    '''This is a schema using sqlalchemy auto schema to create a schema for patients'''
    class Meta:
        model = Patient
        load_instance = True
        sqla_session = db.session
        include_relationships = True

    id = auto_field(dump_only=True)
    first_name = auto_field(required=True, validate=validate.Length(min=1, max=50))
    last_name = auto_field(required=True, validate=validate.Length(min=1, max=50))
    id_number = auto_field(required=True, validate=validate.Length(min=5, max=50))
    date_of_birth = auto_field(required=True)
    gender = auto_field(required=True, validate=validate.OneOf(['Male', 'Female', 'Other']))
    phone_number = auto_field(required=True, validate=validate.Length(min=10, max=15))
    email = auto_field(validate=validate.Email())
    insurance_provider = auto_field(required=True, validate=validate.Length(min=2, max=100))
    policy_number = auto_field(required=True, validate=validate.Length(min=5, max=50))
    created_at = auto_field(dump_only=True)

    appointments = fields.Nested('AppointmentSchema', many=True, exclude=('patient',), dump_only=True)
    medical_records = fields.Nested('MedicalRecordSchema', many=True, exclude=('patient',), dump_only=True)

class DoctorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Doctor
        load_instance = True
        sqla_session = db.session
        include_relationships = True

    id = auto_field(dump_only=True)
    name = auto_field(required=True, validate=validate.Length(min=1, max=100))
    kmpdc_number = auto_field(required=True, validate=validate.Length(min=5, max=50))
    specialisation_id = auto_field(required=True)
    phone = auto_field(required=True, validate=validate.Length(min=10, max=20))
    email = auto_field(validate=validate.Email())
    bio = auto_field(required=True)
    created_at = auto_field(dump_only=True)

    appointments = fields.Nested('AppointmentSchema', many=True, exclude=('doctor',), dump_only=True)
    availabilities = fields.Nested('AvailabilitySchema', many=True, exclude=('doctor',), dump_only=True)
    medical_record_access = fields.Nested('MedicalRecordAccessSchema', many=True, exclude=('doctor',), dump_only=True)

class SpecialisationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Specialisation
        load_instance = True
        sqla_session = db.session

    id = auto_field(dump_only=True)
    name = auto_field(required=True, validate=validate.Length(min=1, max=50))
    description = auto_field()

class AppointmentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Appointment
        load_instance = True
        sqla_session = db.session
        include_relationships = True

    id = auto_field(dump_only=True)
    patient_id = auto_field(required=True)
    doctor_id = auto_field(required=True)
    scheduled_time = auto_field(required=True)
    duration = auto_field(required=True)
    status = auto_field(required=True, validate=validate.OneOf(['Scheduled', 'Completed', 'Cancelled']))
    reason = auto_field(required=True)
    notes = auto_field()
    created_at = auto_field(dump_only=True)

class AvailabilitySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Availability
        load_instance = True
        sqla_session = db.session

    id = auto_field(dump_only=True)
    doctor_id = auto_field(required=True)
    day_of_week = auto_field(required=True, validate=validate.Range(min=0, max=6))
    start_time = auto_field(required=True)
    end_time = auto_field(required=True)
    recurring = auto_field()
    valid_from = auto_field()
    valid_to = auto_field()

class MedicalRecordSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MedicalRecord
        load_instance = True
        sqla_session = db.session
        include_relationships = True

    id = auto_field(dump_only=True)
    patient_id = auto_field(required=True)
    appointment_id = auto_field()
    record_type = auto_field(required=True)
    title = auto_field(required=True)
    description = auto_field(required=True)
    date_recorded = auto_field(required=True)
    created_at = auto_field(dump_only=True)

    access_grants = fields.Nested('MedicalRecordAccessSchema', many=True, exclude=('medical_record',), dump_only=True)

class MedicalRecordAccessSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MedicalRecordAccess
        load_instance = True
        sqla_session = db.session

    id = auto_field(dump_only=True)
    record_id = auto_field(required=True)
    doctor_id = auto_field(required=True)
    access_granted_at = auto_field(dump_only=True)
    access_revoked_at = auto_field()


#schema instances
patient_schema = PatientSchema()
patients_schema = PatientSchema(many=True)

doctor_schema = DoctorSchema()
doctors_schema = DoctorSchema(many=True)

appointment_schema = AppointmentSchema()
appointments_schema = AppointmentSchema(many=True)

medical_record_schema = MedicalRecordSchema()
medical_records_schema = MedicalRecordSchema(many=True)


