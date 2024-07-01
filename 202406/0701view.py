from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET
import time
import os

# Simulated long process to generate Excel file
def generate_excel(param1, param2, param3, param4, job_id):
    # Simulating a long process to generate the Excel file
    time.sleep(30)  # Simulate 30 seconds of processing time
    # In real scenario, generate Excel file and save to server
    # For demonstration, create an empty file with the job_id as its name
    file_path = f'/path/to/generated/files/{job_id}.xlsx'
    with open(file_path, 'w') as file:
        file.write("Example content")  # Replace with actual Excel generation code

# Endpoint to initiate file generation and return job_id
@require_GET
def start_file_generation(request):
    param1 = request.GET.get('param1')
    param2 = request.GET.get('param2')
    param3 = request.GET.get('param3')
    param4 = request.GET.get('param4')
    job_id = request.GET.get('job_id')  # Receive job_id from frontend

    # Simulate initiating file generation and return job_id
    generate_excel(param1, param2, param3, param4, job_id)

    return JsonResponse({'job_id': job_id})

# Endpoint to check file generation status and return file for download if ready
@require_GET
def check_file_status(request, job_id):
    # Simulate checking file generation status
    # In real scenario, check if the file exists on the server
    file_path = f'/path/to/generated/files/{job_id}.xlsx'  # Replace with actual file path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="{job_id}.xlsx"'
            return response
    else:
        return JsonResponse({'status': 'pending'})