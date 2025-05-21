from flask import Blueprint, request, jsonify
from app.schemas import appointment_schema, appointments_schema
from models import Appointment

appointmnent_bp = Blueprint('appointments', __name__, url_prefix=('/appointments'))

#get all appointments
@appointmnent_bp.route('/', methods=['GET'])
def get_all_appointments():
    appointments = Appointment.query.all()
    return jsonify(appointments_schema.dump(appointments))

#get a specific patient appointments
@appointmnent_bp.route('/<int:patient_id>', methods=['GET'])
def get_patient_appointments(patient_id):
    appointments = Appointment.query.filter_by(patient_id=patient_id).all()
    return jsonify(appointments_schema.dump(appointments))

#get a specific doctors appointments
appointmnent_bp.route('/<doctor_id>', methods=['GET'])
def get_all_doctors_appointments(doctor_id):
    appointments = Appointment.query.filter_by(doctor_id=doctor_id).all()
    return jsonify(appointments_schema.dump(appointments))

#get appointments by status
appointmnent_bp.route('/<status>', methods=['GET'])
def get_appointments_by_status(status):
    appointments = Appointment.query.filter_by(status=status).all()
    return jsonify(appointments_schema.dump(appointments))

#create an appointment
@appointmnent_bp.route('/add', methods=['POST'])
def create_appointment():
    #get data from the request
    data = request.get_json()

    #validate that all the required fields are there
    required_fields = [
        'patient_id', 'doctor_id', 'scheduled_time', 'duration',
        'status', 'reason', 'notes'
    ]
    #verify if all the requiered fields are there
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    
