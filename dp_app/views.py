from django.shortcuts import render, redirect
from .models import History
import pandas as pd
import os
import joblib
from .models import PredictionHistory  # <- Import your model

path = os.path.dirname(__file__)
model = joblib.load(open(os.path.join(path, 'best_model.pkl'), 'rb'))
label_encoder = joblib.load(open(os.path.join(path, 'label_encode.pkl'), 'rb'))


def index(req):
    return render(req, 'index.html')


def prediction(req):
    if req.method == 'POST':
        fever = req.POST['fever']
        headache = req.POST['headache']
        nausea = req.POST['nausea']
        vomiting = req.POST['vomiting']
        fatigue = req.POST['fatigue']
        joint_pain = req.POST['joint_pain']
        skin_rash = req.POST['skin_rash']
        cough = req.POST['cough']
        weight_loss = req.POST['weight_loss']
        yellow_eyes = req.POST['yellow_eyes']

        symptoms = ['fever', 'headache', 'nausea', 'vomiting', 'fatigue',
                    'joint_pain', 'skin_rash', 'cough', 'weight_loss', 'yellow_eyes']
        user_input = [fever, headache, nausea, vomiting, fatigue,
                      joint_pain, skin_rash, cough, weight_loss, yellow_eyes]

        # ✅ Check if all are 0 (i.e., "No" selected for every symptom)
        if all(val == '0' for val in user_input):
            return render(req, 'prediction.html', {
                'res': 'Please select at least one symptom to get a valid prediction.'
            })

        # Proceed with prediction
        input_df = pd.DataFrame([user_input], columns=symptoms)
        prediction_result = model.predict(input_df)[0]
        predicted_value = label_encoder.inverse_transform([prediction_result])[0]

        # Save to history
        PredictionHistory.objects.create(
            symptoms=", ".join([s for s, v in zip(symptoms, user_input) if v == '1']),
            result=predicted_value
        )

        return render(req, 'prediction.html', {'res': predicted_value})

    return render(req, 'prediction.html')



def history(req):
    records = PredictionHistory.objects.all().order_by('-timestamp')
    return render(req, 'history.html', {'records': records})


def upload_report(request):
    if request.method == 'POST':
        try:
            file = request.FILES['csv_file']
            df = pd.read_csv(file)

            expected_columns = ['fever', 'headache', 'nausea', 'vomiting', 'fatigue',
                                'joint_pain', 'skin_rash', 'cough', 'weight_loss', 'yellow_eyes']
            if not all(col in df.columns for col in expected_columns):
                raise ValueError("CSV must contain the required symptom columns.")

            # Taking only the first row for prediction
            input_data = df[expected_columns].iloc[0].values.tolist()
            prediction_code = model.predict([input_data])[0]
            predicted_disease = label_encoder.inverse_transform([prediction_code])[0]

            # Save to history
            present_symptoms = [symptom for symptom, value in zip(expected_columns, input_data) if int(value) == 1]
            PredictionHistory.objects.create(
                symptoms=", ".join(present_symptoms),
                result=predicted_disease
            )

            return render(request, 'upload_report.html', {'result': predicted_disease})

        except Exception as e:
            return render(request, 'upload_report.html', {'error': f"Error processing file: {str(e)}"})

    return render(request, 'upload_report.html')

from django.shortcuts import get_object_or_404

def delete_history(request, id):
    if request.method == 'POST':
        record = get_object_or_404(PredictionHistory, id=id)
        record.delete()
    return redirect('history')

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect

@csrf_exempt
def delete_all_history(request):
    if request.method == 'POST':
        PredictionHistory.objects.all().delete()
        return redirect('history')

def about_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # Process or save the contact message (e.g., send email or store in DB)
        # Optionally show a success message
    return render(request, 'aboutus.html')

from .models import ContactMessage

def about(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        ContactMessage.objects.create(name=name, email=email, message=message)
        return render(request, 'aboutus.html', {'success': True})

    return render(request, 'aboutus.html')

from django.contrib.auth.decorators import login_required

@login_required
def contact_messages_view(request):
    messages = ContactMessage.objects.order_by('-submitted_at')
    return render(request, 'contact_messages.html', {'messages': messages})
