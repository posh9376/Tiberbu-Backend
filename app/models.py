from .extensions import db
from datetime import datetime

class Patient(db.Model):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    id_number = db.Column(db.String(50), nullable=False, unique=True)
    date_of_birth = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(50), nullable=False)  # Fixed capitalization to lowercase
    phone_number = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=True)
    insurance_provider = db.Column(db.String(100), nullable=False)
    policy_number = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    appointments = db.relationship('Appointment', back_populates='patient', cascade='all, delete-orphan')
    medical_records = db.relationship('MedicalRecord', back_populates='patient', cascade='all, delete-orphan')


class Doctor(db.Model):
    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    kmpdc_number = db.Column(db.String(20), nullable=False, unique=True)
    specialisation_id = db.Column(db.Integer, db.ForeignKey('specialisations.id'), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    specialisation = db.relationship('Specialisation', back_populates='doctors')
    appointments = db.relationship('Appointment', back_populates='doctor', cascade='all, delete-orphan')
    availabilities = db.relationship('Availability', back_populates='doctor', cascade='all, delete-orphan')
    medical_record_access = db.relationship('MedicalRecordAccess', back_populates='doctor', cascade='all, delete-orphan')


class Specialisation(db.Model):
    __tablename__ = 'specialisations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)  # Fixed typo from 'db.Columnn'
    description = db.Column(db.Text)  # Fixed typo from 'descripton'

    # Relationships
    doctors = db.relationship('Doctor', back_populates='specialisation')  # Pluralized for one-to-many


class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)  # Fixed typo from 'db.FoeignKey'
    scheduled_time = db.Column(db.DateTime, nullable=False)  # Changed from String to DateTime
    duration = db.Column(db.Integer, nullable=False)  # in minutes
    status = db.Column(db.String(50), nullable=False, default='Scheduled')  # Added default
    reason = db.Column(db.Text, nullable=False)  # Fixed capitalization to lowercase
    notes = db.Column(db.Text, nullable=True)  # Added notes field
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    patient = db.relationship('Patient', back_populates='appointments')
    doctor = db.relationship('Doctor', back_populates='appointments')
    medical_records = db.relationship('MedicalRecord', back_populates='appointment', cascade='all, delete-orphan')


class Availability(db.Model):
    __tablename__ = 'availabilities'

    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'),nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)  # 0-6 (Monday-Sunday)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    recurring = db.Column(db.Boolean, default=True)
    valid_from = db.Column(db.Date)
    valid_to = db.Column(db.Date)

    # Relationship
    doctor = db.relationship('Doctor', back_populates='availabilities')


# Medical Records Models (Bonus)
class MedicalRecord(db.Model):
    __tablename__ = 'medical_records'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=True)
    record_type = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_recorded = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    patient = db.relationship('Patient', back_populates='medical_records')
    appointment = db.relationship('Appointment', back_populates='medical_records')
    access_grants = db.relationship('MedicalRecordAccess', back_populates='medical_record', cascade='all, delete-orphan')


class MedicalRecordAccess(db.Model):
    __tablename__ = 'medical_record_access'

    id = db.Column(db.Integer, primary_key=True)
    record_id = db.Column(db.Integer, db.ForeignKey('medical_records.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    access_granted_at = db.Column(db.DateTime, default=datetime.utcnow)
    access_revoked_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    medical_record = db.relationship('MedicalRecord', back_populates='access_grants')
    doctor = db.relationship('Doctor', back_populates='medical_record_access')