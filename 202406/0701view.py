from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
import threading
import time
import os

# Function to generate Excel file in a separate thread
def generate_excel_async(param1, param2, param3, param4, job_id):
    # Simulate a long process to generate the Excel file
    time.sleep(300)  # Simulate 300 seconds (5 minutes) of processing time
    # In real scenario, generate Excel file and save to server
    # For demonstration, create an empty file with the job_id as its name
    file_path = f'/path/to/generated/files/{job_id}.xlsx'
    with open(file_path, 'w') as file:
        file.write("Example content")  # Replace with actual Excel generation code

# Endpoint to initiate file generation
@require_GET
def start_file_generation(request):
    param1 = request.GET.get('param1')
    param2 = request.GET.get('param2')
    param3 = request.GET.get('param3')
    param4 = request.GET.get('param4')
    job_id = request.GET.get('job_id')  # Receive job_id from frontend

    # Start file generation in a separate thread to avoid blocking
    thread = threading.Thread(target=generate_excel_async, args=(param1, param2, param3, param4, job_id))
    thread.start()

    return HttpResponse(status=202)  # Return 202 Accepted to indicate the process has started

# Endpoint to check file generation status and return file for download if ready
@require_GET
def check_file_status(request):
    job_id = request.GET.get('job_id')
    attempt = request.GET.get('attempt')
    
    # Simulate checking file generation status
    # In real scenario, check if the file exists on the server
    file_path = f'/path/to/generated/files/{job_id}.xlsx'  # Replace with actual file path
    
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="{job_id}.xlsx"'
            return response
    else:
        return JsonResponse({'status': 'pending', 'attempt': attempt})