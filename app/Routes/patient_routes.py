from flask import Blueprint, request, jsonify
from app.schemas import patient_schema, patients_schema
from models import Patient, db


patient_bp = Blueprint('patient', __name__)

#list all patients
@patient_bp.route('/patient', methods=['GET'])
def get_patients():
    patients = Patient.query.all()
    #jsonify and serialise the data using the patient schema 
    return jsonify(patients_schema.dump(patients))

#register a patient
@patient_bp.route('/patient/add',methods = ['POST'])
def register_patient():
    data = request.get_json()

    #validate if all the required data is in the request
    required_fields = [
        'first_name', 'last_name', 'id_number', 'date_of_birth',
        'gender', 'phone_number', 'insurance_provider', 'policy_number'
    ]
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    #check if patient already exists
    if Patient.query.filter_by(id_number=data['id_number']).first():
        return jsonify({'error': 'Patient with that ID already exists'}), 400
    
    #Validate the data using the patient schema
    errors = patient_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    #add the new patient to the db
    try:
        new_patient = Patient(**data)
        db.session.add(new_patient)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 # Return any database error
    
    return jsonify({
        'message': 'Patient added successfully',
        'patient': patient_schema.dump(new_patient)
    }), 201


#get particular patient details
@patient_bp.route('/patient/<int:id>', methods=['GET'])
def get_patient_datails(id):
    patient = Patient.query.get_or_404(id)
    return jsonify(patient_schema.dump(patient))

#update the patient info
@patient_bp.route('/patient/<int:id>' methods=['PUT'])
def update_patient_details(id):
    patient = Patient.query.get_or_404(id)
    data = request.get_json()
    #if no data is provided return an error
    if not data:
        return jsonify({'message':'No data provided'}),400
    #validate the data using the patient schema
    errors = patient_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    #update the fields if they exist
    if 'first_name' in data:
        patient.first_name = data['first_name']
    if 'last_name' in data:
        patient.last_name = data['last_name']
    if 'date_of_birth' in data:
        patient.date_of_birth = data['date_of_birth']
    if 'id_number' in data:
        patient.id_number = data['id_number']
    if 'gender' in data:
        patient.gender = data['gender']
    if 'email' in data:
        patient.email = data['email']
    if 'insurance_provider' in data:
        patient.insurance_provider = data['insurance_provider']
    if 'policy_number' in data:
        patient.policy_number = data['policy_number']
    
    db.session.commit()

    return jsonify({
        'messsage': 'Patient details updated successfully',
        'patient': patient_schema.dump(patient)
    }), 200

#delete a patient
@patient_bp.route('/patient/<int:id>', methods=['DELETE'])
def delete_patient(id):
    patient = Patient.query.get_or_404(id)

    db.session.delete(patient)
    db.session.commit()
    return jsonify({'messahe': "Patient deleted successfully"}), 200

