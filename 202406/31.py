import os
import threading
import time
from django.http import JsonResponse, HttpResponse
from django.views import View
import pandas as pd
from django.urls import path
from django.shortcuts import render

class TaskManager:
    def __init__(self):
        self.tasks = {}

    def start_task(self, task_id, *args):
        def task_function(*args):
            time.sleep(300)  # Simulate long-running task for 5 minutes
            df = pd.DataFrame({
                'Column1': [args[0], args[1]],
                'Column2': [args[2], args[3]],
            })
            file_path = f'/path/to/excel/{task_id}.xlsx'
            df.to_excel(file_path, index=False, engine='openpyxl')
            self.tasks[task_id]['status'] = 'completed'
            self.tasks[task_id]['file_path'] = file_path

        self.tasks[task_id] = {'status': 'processing', 'file_path': None}
        thread = threading.Thread(target=task_function, args=args)
        thread.start()

    def get_task_status(self, task_id):
        return self.tasks.get(task_id, None)

task_manager = TaskManager()

class StartExcelGenerationView(View):
    def post(self, request, *args, **kwargs):
        param1 = request.POST.get('param1')
        param2 = request.POST.get('param2')
        param3 = request.POST.get('param3')
        param4 = request.POST.get('param4')
        task_id = str(int(time.time()))  # Unique task ID

        task_manager.start_task(task_id, param1, param2, param3, param4)
        return JsonResponse({'task_id': task_id})

class CheckExcelStatusView(View):
    def get(self, request, *args, **kwargs):
        task_id = request.GET.get('task_id')
        task_status = task_manager.get_task_status(task_id)

        if task_status:
            if task_status['status'] == 'completed':
                return JsonResponse({'status': 'success', 'file_path': task_status['file_path']})
            else:
                return JsonResponse({'status': 'processing'}, status=202)
        else:
            return JsonResponse({'status': 'not_found'}, status=404)

class DownloadExcelView(View):
    def get(self, request, *args, **kwargs):
        file_path = request.GET.get('file_path')

        if not os.path.exists(file_path):
            return JsonResponse({'status': 'failure'}, status=404)

        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response

urlpatterns = [
    path('start-excel-generation/', StartExcelGenerationView.as_view(), name='start_excel_generation'),
    path('check-excel-status/', CheckExcelStatusView.as_view(), name='check_excel_status'),
    path('download-excel/', DownloadExcelView.as_view(), name='download_excel'),
]