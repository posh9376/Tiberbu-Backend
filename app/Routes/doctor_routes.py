from flask import Blueprint, request, jsonify
from app.schemas import doctor_schema, doctors_schema
from models import Doctor, db


doctor_bp = Blueprint('doctor', __name__)

#list all doctors
@doctor_bp.route('/doctor', methods=['GET'])
def get_doctors():
    doctors = Doctor.query.all()
    #jsonify and serialize the data using the doctor schema 
    return jsonify(doctors_schema.dump(doctors))

#register a doctor
@doctor_bp.route('/doctor/add', methods=['POST'])
def register_doctor():
    data = request.get_json()
    #validate if all the required data is in the request
    required_fields = [
        'name', 'specialisation_id', 'phone', 'email',
        'bio', 'kmpdc_number'
    ]
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    #check if Doctor already exists
    if Doctor.query.filter_by(kmpdc_number=data['kmpdc_number']).first():
        return jsonify({'error': 'Doctor with that kmpdc number already exists'}), 400
    
    #Validate the data using the doctor schema
    errors = doctor_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    #add the new doctor to the db
    try:
        new_doctor = Doctor(**data)
        db.session.add(new_doctor)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 # Return any database error
    
    return jsonify({
        'message': 'Doctor added successfully',
        'doctor': doctor_schema.dump(new_doctor)
    }), 201


#get particular doctor details
@doctor_bp.route('/doctor/<int:id>', methods=['GET'])
def get_doctor_datails(id):
    doctor = Doctor.query.get_or_404(id)
    return jsonify(doctor_schema.dump(doctor))

#update the doctor info
@doctor_bp.route('/doctor', methods=['GET'])
def update_doctor_details(id):
    doctor = Doctor.query.get_or_404(id)
    data = request.get_json()
    #if no data is provided return an error
    if not data:
        return jsonify({'message':'No data provided'}),400
    #validate the data using the doctor schema
    errors = doctor_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    #update the fields if they exist
    if 'name' in data:
        doctor.name = data['name']
    if 'specialisation_id' in data:
        doctor.specialisation_id = data['specialisation_id']
    if 'phone' in data:
        doctor.phone = data['phone']
    if 'bio' in data:
        doctor.bio = data['bio']
    if 'kmpdc_number' in data:
        doctor.kmpdc_number = data['kmpdc_number']
    if 'email' in data:
        doctor.email = data['email']
    
    db.session.commit()

    return jsonify({
        'messsage': 'Doctor details updated successfully',
        'doctor': doctor_schema.dump(doctor)
    }), 200

#delete a doctor
@doctor_bp.route('/doctor/<int:id>', methods=['DELETE'])
def delete_doctor(id):
    doctor= Doctor.query.get_or_404(id)

    db.session.delete(doctor)
    db.session.commit()
    return jsonify({'message': "Doctor deleted successfully"}), 200

